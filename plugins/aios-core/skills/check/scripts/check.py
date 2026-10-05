"""Check Markdown conventions and edits to the docs copy in the aiOS root.

python3 check.py
"""
import os, sys


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
    config, checks = hooks.load(root)
    files = hooks.files_in_scope(root, config)
    problems = hooks.run_checks(files, checks, root)
    for p in problems:
        print(f"[{p['check']}] {p['path']}: {p['message']}" + (" (warning)" if "mode" in p else ""))
    print(f"Checked {len(files)} files. Problems: {len(problems)}.")


if __name__ == "__main__":
    main()
