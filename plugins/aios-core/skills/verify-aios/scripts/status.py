"""Report aiOS settings, versions, hook runs, and check results for files in scope.

python3 status.py [--last-block]
"""
import argparse, json, os, sys


def import_hooks():
    """Import the plugin's hooks/hooks.py, found by searching upward from this script."""
    path = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(path, "hooks", "hooks.py")):
        if os.path.dirname(path) == path:
            sys.exit("Cannot find the aios-core plugin's hooks/hooks.py.")
        path = os.path.dirname(path)
    sys.path.insert(0, os.path.join(path, "hooks"))
    import hooks
    return hooks


def listing(value):
    """Join a setting that holds a list or a single pattern, or return none."""
    items = value if isinstance(value, list) else [value] if value not in (None, "") else []
    return ", ".join(str(item) for item in items) or "none"


def problem_line(p):
    return f"[{p.get('check')}] {p.get('path')}: {p.get('message')}" + (" (warning)" if "mode" in p else "")


def nested_roots(root):
    """Relative paths of subfolders holding their own .aiOS/config.yaml, without descending into them."""
    found = []
    for base, dirs, _ in os.walk(root):
        keep = []
        for d in sorted(dirs):
            path = os.path.join(base, d)
            if d.startswith(".") or d == "__pycache__" or os.path.islink(path):
                continue
            if os.path.isfile(os.path.join(path, ".aiOS", "config.yaml")):
                found.append(os.path.relpath(path, root).replace(os.sep, "/"))
            else:
                keep.append(d)
        dirs[:] = keep
    return found


def settings(config, checks):
    print("Settings")
    print(f"  Checks: {'on' if config.get('enabled', True) else 'off'}")
    print(f"  Include: {listing(config.get('include', ['**']))}")
    print(f"  Exclude: {listing(config.get('exclude', []))}")
    print(f"  Max blocks per turn: {config.get('max_blocks', 2)}")
    print(f"  Time zone: {checks.get('frontmatter', {}).get('zone', 'America/Los_Angeles')}")
    modes = ", ".join(f"{name} {values.get('mode', 'block')}" for name, values in checks.items())
    print(f"  Check modes: {modes or 'none'}")


def versions(hooks, root):
    print("Versions")
    version = hooks.plugin_version()
    print(f"  Installed plugin: {version}")
    docs = os.path.join(root, ".aiOS", "docs")
    try:
        with open(os.path.join(docs, ".sync.json")) as f:
            marker = json.load(f)
        same = marker["version"] == version
        content = marker["hash"] == hooks.docs_hash(os.path.join(hooks.PLUGIN, "docs"))
        print(f"  Docs copy: {marker['version']}; "
              + ("matches the installed plugin" if same and content else "differs from the installed plugin"))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"  Docs copy: missing or unreadable ({error})")
        print("  Edited docs copy files: unknown, because the docs copy is missing or unreadable")
        return
    recorded = marker.get("files")
    if not isinstance(recorded, dict):
        print("  Edited docs copy files: unknown, because .sync.json records no file hashes")
        return
    try:
        current = hooks.file_hashes(docs)
    except OSError as error:
        print(f"  Edited docs copy files: unknown ({error})")
        return
    edited = [f".aiOS/docs/{path}" for path in sorted(current) if recorded.get(path) != current[path]]
    edited += [f".aiOS/docs/{path} (deleted)" for path in sorted(recorded) if path not in current]
    print(f"  Edited docs copy files: {', '.join(edited) or 'none'}")


def hook_runs(hooks, root, last_block=False):
    print("Hooks")
    last, blocked = {}, None
    for entry in hooks.read_events(os.path.join(root, ".aiOS", "logs", "hook-events.jsonl")):
        if "harness" in entry and "time" in entry:
            last[entry["harness"]] = entry["time"]
            if entry.get("decision") == "block":
                blocked = entry
    for harness in ("claude-code", "codex"):
        print(f"  {harness}: last ran {last[harness]}" if harness in last else f"  {harness}: never ran here")
    if not last_block:
        return
    print()
    print("Historical block")
    if not blocked:
        print("  Latest blocked turn: none")
        return
    print("  Recorded hook result; does not establish current status.")
    problems = [p for p in blocked.get("problems") or [] if isinstance(p, dict)]
    count = len(problems)
    print(f"  Latest blocked turn: {blocked['time']} in {blocked['harness']}: "
          f"{count} problem{'' if count == 1 else 's'}")
    for p in problems:
        print("    " + problem_line(p))


def file_results(hooks, root, config, checks):
    print("Files")
    files = hooks.files_in_scope(root, config)
    problems = hooks.run_checks(files, checks, root)
    for p in problems:
        print("  " + problem_line(p))
    print(f"  Checked {len(files)} files. Problems: {len(problems)}.")


def main():
    parser = argparse.ArgumentParser(description="Verify aiOS settings, hook activity, and files in scope.")
    parser.add_argument("--last-block", action="store_true",
                        help="include the latest recorded block as historical context")
    args = parser.parse_args()
    hooks = import_hooks()
    root = hooks.find_root(os.getcwd())
    if not root:
        print("Not set up here. Run the aios-core:setup-aios skill first.")
        return
    print(f"Folder: {root}")
    try:
        config, checks = hooks.load(root)
    except hooks.ConfigurationError as error:
        print("Configuration")
        print(f"  [configuration] .aiOS/config.yaml: {error}")
        print("  File checks did not run. Correct the configuration and run aios-core:verify-aios again.")
        return 1
    print(f"Folders with separate settings skipped: {', '.join(nested_roots(root)) or 'none'}")
    print()
    settings(config, checks)
    print()
    versions(hooks, root)
    print()
    hook_runs(hooks, root, args.last_block)
    print()
    file_results(hooks, root, config, checks)


if __name__ == "__main__":
    sys.exit(main())
