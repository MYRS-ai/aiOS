"""aiOS hooks. Claude Code and Codex call this file through hooks.json.

python3 hooks.py start|stop, with the hook event JSON on stdin.
"""
import hashlib, importlib.util, json, os, re, shutil, sys, tempfile
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CHECKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checks")
PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CHECKS)
from common import load_yaml, matches


def now():
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


def plugin_version():
    with open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")) as f:
        return json.load(f)["version"]


def docs_hash(folder):
    """Hash sorted relative paths and bytes, with lengths to separate entries."""
    paths = []
    for base, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in (".DS_Store", "__pycache__")]
        paths += [os.path.relpath(os.path.join(base, f), folder)
                  for f in files if f not in (".DS_Store", "__pycache__")]
    digest = hashlib.sha256()
    for path in sorted(paths):
        with open(os.path.join(folder, path), "rb") as f:
            for value in (path.replace(os.sep, "/").encode("utf-8"), f.read()):
                digest.update(len(value).to_bytes(8, "big"))
                digest.update(value)
    return digest.hexdigest()


def file_hashes(folder):
    """Map each file's relative path to the sha256 of its bytes."""
    out = {}
    for base, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in (".DS_Store", "__pycache__")]
        for name in files:
            if name in (".DS_Store", "__pycache__"):
                continue
            path = os.path.join(base, name)
            with open(path, "rb") as f:
                out[os.path.relpath(path, folder).replace(os.sep, "/")] = hashlib.sha256(f.read()).hexdigest()
    out.pop(".sync.json", None)
    return out


def version_parts(version):
    """Compare the leading number of each dotted part, ignoring suffixes."""
    return tuple(int(re.match(r"[0-9]*", part).group() or "0") for part in version.split("."))


def sync_docs(root):
    """Stage a complete docs copy, then swap it in with rollback on failure."""
    version, stage, backup = "unknown", None, None
    target = os.path.join(root, ".aiOS", "docs")
    try:
        version = plugin_version()
        source = os.path.join(PLUGIN, "docs")
        if not os.path.isdir(source):
            raise FileNotFoundError(source)
        recorded = {}
        marker = os.path.join(target, ".sync.json")
        if os.path.isfile(marker):
            with open(marker) as f:
                recorded = json.load(f)
        current = version_parts(version)
        previous = version_parts(recorded.get("version", "0"))
        if recorded and current < previous:
            return {"action": "kept-newer", "version": version}
        fingerprint = docs_hash(source)
        intact = recorded.get("files") == file_hashes(target)
        if recorded and current == previous and fingerprint == recorded.get("hash") and intact:
            return {"action": "unchanged", "version": version}
        exists = os.path.exists(target)
        stage = tempfile.mkdtemp(prefix=".docs-", dir=os.path.dirname(target))
        shutil.copytree(source, stage, dirs_exist_ok=True, copy_function=shutil.copy,
                        ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
        files = file_hashes(stage)
        with open(os.path.join(stage, ".sync.json"), "w") as f:
            json.dump({"version": version, "hash": fingerprint, "files": files}, f)
        if exists:
            backup = tempfile.mkdtemp(prefix=".docs-old-", dir=os.path.dirname(target))
            os.rmdir(backup)
            os.replace(target, backup)
        try:
            os.replace(stage, target)
        except Exception as error:
            if backup:
                try:
                    os.replace(backup, target)
                except Exception as rollback:
                    saved, backup = backup, None
                    raise OSError(f"{error}; rollback failed: {rollback}; backup retained at {saved}") from rollback
                backup = None
            raise
        return {"action": "replaced" if exists else "copied", "version": version}
    except Exception as error:
        return {"action": "error", "version": version, "message": str(error)}
    finally:
        if stage:
            shutil.rmtree(stage, ignore_errors=True)
        # Keep the backup if rollback itself failed.
        if backup and os.path.exists(target):
            shutil.rmtree(backup, ignore_errors=True)


def find_root(path):
    """Return the nearest folder at or above path that holds .aiOS/config.yaml."""
    path = os.path.abspath(path)
    while True:
        if os.path.isfile(os.path.join(path, ".aiOS", "config.yaml")):
            return path
        if os.path.dirname(path) == path:
            return None
        path = os.path.dirname(path)


class ConfigurationError(ValueError):
    """Invalid settings, with a safe block limit for reporting the failure."""

    def __init__(self, message, max_blocks=2):
        super().__init__(message)
        self.max_blocks = max_blocks


def validate(config, checks):
    """Reject settings that could silently change scope or disable a check."""
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def mapping(value, label):
        require(isinstance(value, dict), f"{label} must be a mapping")

    def strings(value, label):
        require(isinstance(value, list) and all(isinstance(v, str) and v for v in value),
                f"{label} must be a list of nonempty strings")

    def keys(value, allowed, label):
        unknown = set(value) - set(allowed)
        require(not unknown, f"{label} has unknown settings: {', '.join(sorted(unknown))}")

    mapping(config, "configuration")
    keys(config, ("enabled", "include", "exclude", "max_blocks", "checks"), "configuration")
    require(type(config.get("enabled", True)) is bool, "enabled must be true or false")
    limit = config.get("max_blocks", 2)
    require(type(limit) is int and limit >= 0, "max_blocks must be a nonnegative integer")
    for key in ("include", "exclude"):
        strings(config.get(key, ["**"] if key == "include" else []), key)
    mapping(config.get("checks", {}), "checks")
    for name, settings in checks.items():
        require(bool(re.fullmatch(r"[a-z][a-z0-9-]*", name)) and
                os.path.isfile(os.path.join(CHECKS, name + ".py")) and
                not os.path.islink(os.path.join(CHECKS, name + ".py")),
                f"checks.{name}: unknown or unavailable check")
        try:
            implementation = module(name)
        except Exception as error:
            raise ValueError(f"checks.{name}: could not load check: {error}") from error
        require(any(callable(getattr(implementation, method, None)) for method in ("check", "fix")),
                f"checks.{name}: no callable check or fix function")
        label = "checks." + name
        mapping(settings, label)
        require(settings.get("mode", "block") in ("block", "warn", "off"),
                f"{label}.mode must be block, warn, or off")
        strings(settings.get("exclude", []), label + ".exclude")
        if name != "frontmatter":
            if name in ("names", "docs-copy"):
                keys(settings, ("mode", "exclude"), label)
            # Other check implementations may define their own settings.
            continue
        keys(settings, ("mode", "exclude", "zone", "rules"), label)
        require(isinstance(settings.get("zone"), str), f"{label}.zone must be a time zone name")
        try:
            ZoneInfo(settings["zone"])
        except (ValueError, ZoneInfoNotFoundError):
            raise ValueError(f"{label}.zone is not a known time zone: {settings['zone']}")
        mapping(settings.get("rules"), label + ".rules")
        for rule_name, rule in settings["rules"].items():
            rule_label = label + ".rules." + rule_name
            mapping(rule, rule_label)
            keys(rule, ("match", "required", "allowed", "timestamps", "format"), rule_label)
            match = rule.get("match", ["**"])
            if not isinstance(match, str):
                strings(match, rule_label + ".match")
            else:
                require(bool(match), f"{rule_label}.match must not be empty")
            strings(rule.get("required", []), rule_label + ".required")
            strings(rule.get("timestamps", []), rule_label + ".timestamps")
            require(set(rule.get("timestamps", [])) <= {"created", "updated"},
                    f"{rule_label}.timestamps accepts only created and updated")
            require(rule.get("format", "agent-skills") == "agent-skills",
                    f"{rule_label}.format must be agent-skills")
            mapping(rule.get("allowed", {}), rule_label + ".allowed")
            for field, values in rule.get("allowed", {}).items():
                strings(values, rule_label + ".allowed." + field)


def load(root):
    """Return the folder's config and each check's settings: defaults with the config's overrides."""
    config = {}
    try:
        config = load_yaml(os.path.join(root, ".aiOS", "config.yaml"))
        checks = load_yaml(os.path.join(CHECKS, "checks.yaml"))
        overrides = config.get("checks", {})
        if not isinstance(overrides, dict):
            raise ValueError("checks must be a mapping")
        for name, override in overrides.items():
            if not isinstance(override, dict):
                raise ValueError(f"checks.{name} must be a mapping")
            checks.setdefault(name, {}).update(override)
        validate(config, checks)
        return config, checks
    except (OSError, UnicodeError, ValueError) as error:
        limit = config.get("max_blocks", 2)
        raise ConfigurationError(str(error), limit if type(limit) is int and limit >= 0 else 2) from error


def files_in_scope(root, config, since=0):
    """Changed Markdown and docs copy files, skipping subfolders with their own .aiOS/config.yaml."""
    include, exclude = config.get("include", ["**"]), config.get("exclude", [])
    found = []
    for base, dirs, files in os.walk(root):
        in_docs = os.path.relpath(base, root) == ".aiOS/docs" or os.path.relpath(base, root).startswith(".aiOS/docs/")
        dirs[:] = sorted(d for d in dirs
                         if (in_docs or not d.startswith(".") or (base == root and d == ".aiOS"))
                         and d not in (".DS_Store", "__pycache__")
                         and not os.path.islink(os.path.join(base, d))
                         and not os.path.isfile(os.path.join(base, d, ".aiOS", "config.yaml")))
        for name in sorted(files):
            path = os.path.join(base, name)
            if name in (".DS_Store", "__pycache__") or os.path.islink(path):
                continue
            rel = os.path.relpath(path, root)
            if name.endswith(".md") or rel.startswith(".aiOS/docs/"):
                found.append(path)
    return [p for p in found
            if os.path.getmtime(p) > since
            and matches(os.path.relpath(p, root), include)
            and not matches(os.path.relpath(p, root), exclude)]


def for_check(files, settings, root):
    """Exclude files matching this check's exclude patterns."""
    return [p for p in files if not matches(os.path.relpath(p, root), settings.get("exclude", []))]


def module(name):
    """Load only a bare check name backed by a file directly in checks/."""
    if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        return None
    path = os.path.join(CHECKS, f"{name}.py")
    if not os.path.isfile(path) or os.path.islink(path):
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_checks(files, checks, root):
    """Return problem records: {check, path, message}, plus mode for warn-only checks."""
    problems = []
    for name, settings in checks.items():
        mod, mode = module(name), settings.get("mode", "block")
        if mod and mode != "off" and hasattr(mod, "check"):
            for file in for_check(files, settings, root):
                try:
                    results = list(mod.check([file], settings, root))
                except Exception as error:
                    results = [(os.path.relpath(file, root), f"could not read: {error}")]
                for path, message in results:
                    problem = {"check": name, "path": path, "message": message, **({"mode": "warn"} if mode == "warn" else {})}
                    if problem not in problems:
                        problems.append(problem)
    return problems


def describe(problems):
    return "\n- ".join(f"[{p['check']}] {p['path']}: {p['message']}" for p in problems)


def run_fixers(files, checks, root, problems):
    fixed = []
    for name, settings in checks.items():
        mod = module(name)
        if mod and settings.get("mode", "block") != "off" and hasattr(mod, "fix"):
            for file in for_check(files, settings, root):
                try:
                    fixed += [{"check": name, "path": path} for path in mod.fix([file], settings, root)]
                except Exception as error:
                    problem = {"check": name, "path": os.path.relpath(file, root), "message": f"could not read: {error}"}
                    if settings.get("mode", "block") == "warn":
                        problem["mode"] = "warn"
                    if problem not in problems:
                        problems.append(problem)
    return fixed


def read_events(path):
    """Yield log entries, skipping damaged or incomplete JSON lines."""
    if os.path.exists(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if isinstance(entry, dict):
                    yield entry


def hook(event):
    data = json.load(sys.stdin)
    root = find_root(data.get("cwd") or os.getcwd())
    if not root:
        return
    log_file = os.path.join(root, ".aiOS", "logs", "hook-events.jsonl")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    session = data.get("session_id")
    harness = "codex" if os.environ.get("PLUGIN_ROOT") else "claude-code"

    def log(**entry):
        with open(log_file, "ab+") as f:
            if f.tell():
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b"\n":
                    f.write(b"\n")
            f.write((json.dumps({"time": now(), "harness": harness, "session": session, "event": event, **entry}) + "\n").encode("utf-8"))

    def reply(obj):
        print(json.dumps(obj))

    configuration_problem = None
    try:
        config, checks = load(root)
    except ConfigurationError as error:
        config, checks = {"max_blocks": error.max_blocks}, {}
        configuration_problem = {"check": "configuration", "path": ".aiOS/config.yaml", "message": str(error)}

    if event == "start":
        docs = sync_docs(root)
        log(cwd=data.get("cwd"), docs=docs,
            **({"problems": [configuration_problem]} if configuration_problem else {}))
        context = []
        if configuration_problem:
            context.append("aiOS configuration is invalid. Fix .aiOS/config.yaml: " + configuration_problem["message"])
        if docs["action"] == "kept-newer":
            context.append("This agent harness has an outdated aios-core plugin and should be updated.")
        if not config.get("enabled", True):
            context.append("Checks are off in .aiOS/config.yaml for this folder.")
        if context:
            reply({"hookSpecificOutput": {"hookEventName": "SessionStart",
                   "additionalContext": " ".join(context)}})
        return
    if not config.get("enabled", True):
        log(decision="skip", reason="checks are off")
        return

    # The turn began at this session's last entry that is not a block.
    history = [e for e in read_events(log_file) if e.get("session") == session]
    blocks = 0
    while history and history[-1].get("decision") == "block":
        history.pop()
        blocks += 1
    if not history and not configuration_problem:
        log(decision="skip", reason="no earlier entry for this session; checking starts next turn")
        return
    turn_start = datetime.fromisoformat(history[-1]["time"]).timestamp() + 0.001 if history else 0

    files = [] if configuration_problem else files_in_scope(root, config, turn_start)
    problems = [configuration_problem] if configuration_problem else run_checks(files, checks, root)
    blocking = [p for p in problems if "mode" not in p]
    if blocking and blocks < config.get("max_blocks", 2):
        log(decision="block", checked=len(files), problems=problems, fixed=[])
        return reply({"decision": "block", "reason": "aiOS check failed. Fix these, then finish:\n- " + describe(blocking)})
    fixed = run_fixers(files, checks, root, problems)
    log(decision="allow", checked=len(files), problems=problems, fixed=fixed)
    if problems:
        reply({"systemMessage": "aiOS check left these unresolved:\n- " + describe(problems)})


if __name__ == "__main__":
    hook(sys.argv[1])
