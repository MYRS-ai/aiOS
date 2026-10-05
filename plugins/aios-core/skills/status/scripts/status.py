"""Show whether aiOS checks are on here and when each agent harness's hooks last ran.

python3 status.py
"""
import json, os, sys


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


def main():
    hooks = import_hooks()
    root = hooks.find_root(os.getcwd())
    if not root:
        print("Not set up here. Run the setup skill first.")
        return
    config, _ = hooks.load(root)
    print(f"aiOS root: {root}")
    print(f"Checks: {'on' if config.get('enabled', True) else 'off'}")
    version = hooks.plugin_version()
    print(f"Installed plugin: {version}")
    marker = os.path.join(root, ".aiOS", "docs", ".sync.json")
    try:
        with open(marker) as f:
            docs = json.load(f)
        same = docs["version"] == version
        content = docs["hash"] == hooks.docs_hash(os.path.join(hooks.PLUGIN, "docs"))
        print(f"Docs copy: {docs['version']}; "
              + ("matches installed plugin" if same and content else "differs from installed plugin"))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Docs copy: missing or unreadable ({error})")
    last = {}
    log_file = os.path.join(root, ".aiOS", "logs", "hook-events.jsonl")
    for entry in hooks.read_events(log_file):
        if "harness" in entry and "time" in entry:
            last[entry["harness"]] = entry["time"]
    for harness in ("claude-code", "codex"):
        print(f"{harness} hooks: last ran {last[harness]}" if harness in last else f"{harness} hooks: never ran here")


if __name__ == "__main__":
    main()
