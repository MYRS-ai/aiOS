"""aiOS hooks. Claude Code and Codex call this file through hooks.json.

python3 hooks.py start|stop, with the hook event JSON on stdin.
"""
import hashlib, importlib.util, json, os, re, shutil, sys, tempfile
from datetime import datetime

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


def load(root):
    """Return the aiOS root's config and each check's settings: defaults with the config's overrides."""
    config = load_yaml(os.path.join(root, ".aiOS", "config.yaml"))
    checks = load_yaml(os.path.join(CHECKS, "checks.yaml"))
    for name, override in config.get("checks", {}).items():
        checks.setdefault(name, {}).update(override)
    return config, checks


def files_in_scope(root, config, since=0):
    """Changed Markdown and docs copy files, without crossing into nested aiOS roots."""
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
    config, checks = load(root)
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

    if event == "start":
        docs = sync_docs(root)
        log(cwd=data.get("cwd"), docs=docs)
        context = []
        if docs["action"] == "kept-newer":
            context.append("This agent harness has an outdated aios-core plugin and should be updated.")
        if not config.get("enabled", True):
            context.append("Checks are off for this aiOS root (.aiOS/config.yaml).")
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
    if not history:
        log(decision="skip", reason="no earlier entry for this session; checking starts next turn")
        return
    turn_start = datetime.fromisoformat(history[-1]["time"]).timestamp() + 0.001

    files = files_in_scope(root, config, turn_start)
    problems = run_checks(files, checks, root)
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
