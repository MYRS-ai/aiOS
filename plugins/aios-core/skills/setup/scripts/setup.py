"""Build missing pieces of an aiOS root without overwriting existing files.

python3 setup.py [folder] --workspace NAME="PURPOSE" (repeatable)
"""
import argparse, os, re, sys
from datetime import datetime

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


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


def build_config(hooks):
    """Return the config template followed by the check defaults, nested under checks:."""
    lines = open(os.path.join(hooks.CHECKS, "checks.yaml")).read().split("\n")
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        lines.pop(0)
    body = "\n".join(f"  {l}" if l.strip() else "" for l in lines)
    return open(os.path.join(ASSETS, "config.yaml")).read() + body.rstrip() + "\n"


def workspace(value):
    name, sep, purpose = value.partition("=")
    if not sep or not purpose.strip() or "\n" in purpose or "\r" in purpose:
        raise argparse.ArgumentTypeError('Use NAME="PURPOSE" with a nonempty, single-line purpose.')
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+){0,3}", name) or name == "shared":
        raise argparse.ArgumentTypeError("Workspace names need one to four lowercase, hyphenated words; shared is reserved.")
    return name, purpose.strip()


def write_missing(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "x") as f:
            f.write(text)
        print(f"Created {path}")
        return True
    except FileExistsError:
        print(f"Skipped existing file: {path}")
        return False


def template(filename, **values):
    text = open(os.path.join(ASSETS, filename)).read()
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    return text


def main(target, workspaces):
    hooks = import_hooks()
    dest = os.path.join(target, ".aiOS")
    os.makedirs(os.path.join(dest, "logs"), exist_ok=True)
    write_missing(os.path.join(dest, "config.yaml"), build_config(hooks))
    stamp = datetime.now().astimezone().isoformat(timespec="minutes")
    write_missing(os.path.join(dest, "AGENTS.md"), template("AGENTS.md", now=stamp))
    docs = os.path.join(dest, "docs")
    if os.path.exists(docs):
        print(f"Skipped existing folder: {docs}; the start hook manages updates.")
    else:
        result = hooks.sync_docs(target)
        print(f"Docs: {result['action']} (plugin {result['version']})")
        if result["action"] == "error":
            sys.exit(result["message"])
    rows = []
    for name, purpose in sorted(workspaces.items()):
        safe = purpose.replace("|", "&#124;")
        rows.append(f"| [{name}/]({name}/AGENTS.md) | {safe} | Working in this domain |")
        write_missing(os.path.join(target, name, "AGENTS.md"),
                      template("workspace.md", title=name.replace("-", " ").capitalize(), purpose=purpose))
    write_missing(os.path.join(target, "shared", "AGENTS.md"), template("shared.md"))
    rows.append("| [shared/](shared/AGENTS.md) | Resources used by more than one domain | Working across domains |")
    rows.sort()
    root_created = write_missing(os.path.join(target, "AGENTS.md"), template("root.md", workspaces="\n".join(rows)))
    ignore = os.path.join(target, ".gitignore")
    text = open(ignore).read() if os.path.exists(ignore) else ""
    if ".aiOS/logs/" not in text.splitlines():
        with open(ignore, "a") as f:
            f.write(("\n" if text and not text.endswith("\n") else "") + ".aiOS/logs/\n")
        print(f"Added .aiOS/logs/ to {ignore}")
    else:
        print(f"Skipped existing entry in {ignore}: .aiOS/logs/")
    if not root_created and workspaces:
        print("The root AGENTS.md already existed. Add any new workspaces to its Contents table.")
    print("Codex users: run /hooks in Codex once and approve the aios-core hooks.")
    print("Plugin updates are manual in each agent harness. Run the check and status skills to verify setup.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", nargs="?", default=os.getcwd())
    parser.add_argument("--workspace", action="append", type=workspace, default=[])
    args = parser.parse_args()
    if len(dict(args.workspace)) != len(args.workspace):
        parser.error("Give each workspace name only once.")
    main(os.path.abspath(args.folder), dict(args.workspace))
