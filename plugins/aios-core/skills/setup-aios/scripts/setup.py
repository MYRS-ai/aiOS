"""Build missing parts of the operator's aiOS without overwriting existing files.

python3 setup.py [folder] --workspace NAME="PURPOSE" (repeatable)
"""
import argparse, os, sys

TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "templates")


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
    return open(os.path.join(TEMPLATES, "config.yaml")).read() + body.rstrip() + "\n"


def workspace(value):
    name, sep, purpose = value.partition("=")
    if not sep or not purpose.strip() or "\n" in purpose or "\r" in purpose:
        raise argparse.ArgumentTypeError('Use NAME="PURPOSE" with a nonempty, single-line purpose.')
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
    text = open(os.path.join(TEMPLATES, filename)).read()
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    return text


def main(target, workspaces):
    hooks = import_hooks()
    from common import parse_yaml
    dest = os.path.join(target, ".aiOS")
    config_text = build_config(hooks)
    try:
        if os.path.isfile(os.path.join(dest, "config.yaml")):
            config, checks = hooks.load(target)
        else:
            config = parse_yaml(config_text.splitlines())
            checks = config["checks"]
            hooks.validate(config, checks)
    except ValueError as error:
        sys.exit(f"Invalid .aiOS/config.yaml: {error}")
    names = hooks.module("names")
    for name in workspaces:
        if name == "shared" or not names.valid_name(name, checks["names"]):
            sys.exit(f"Invalid workspace name {name!r}: use one to four lowercase or approved "
                     "words separated by hyphens; shared is reserved.")
    created = []

    def write_markdown(path, text):
        if write_missing(path, text):
            created.append(path)
            return True
        return False

    os.makedirs(os.path.join(dest, "logs"), exist_ok=True)
    write_missing(os.path.join(dest, "config.yaml"), config_text)
    write_markdown(os.path.join(dest, "AGENTS.md"), template("settings-contract.md"))
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
        words = name.split("-")
        title = " ".join([words[0].capitalize() if words[0].islower() else words[0]] + words[1:])
        write_markdown(os.path.join(target, name, "AGENTS.md"), template("workspace-contract.md", title=title, purpose=purpose))
        write_markdown(os.path.join(target, name, "docs", "glossary.md"),
                       template("glossary.md", title=title, scope="terms used in this workspace"))
    write_markdown(os.path.join(target, "shared", "AGENTS.md"), template("shared-contract.md"))
    write_markdown(os.path.join(target, "shared", "docs", "glossary.md"),
                   template("glossary.md", title="Shared", scope="terms that more than one workspace uses"))
    rows.append("| [shared/](shared/AGENTS.md) | Resources used by more than one domain | Working across domains |")
    rows.sort()
    root_created = write_markdown(os.path.join(target, "AGENTS.md"), template("top-level-contract.md", workspaces="\n".join(rows)))
    ignore = os.path.join(target, ".gitignore")
    text = open(ignore).read() if os.path.exists(ignore) else ""
    if ".aiOS/logs/" not in text.splitlines():
        with open(ignore, "a") as f:
            f.write(("\n" if text and not text.endswith("\n") else "") + ".aiOS/logs/\n")
        print(f"Added .aiOS/logs/ to {ignore}")
    else:
        print(f"Skipped existing entry in {ignore}: .aiOS/logs/")
    if created and config.get("enabled", True):
        eligible = set(hooks.files_in_scope(target, config))
        problems = []
        fixed = hooks.run_fixers([p for p in created if p in eligible],
                                 {"frontmatter": checks["frontmatter"]}, target, problems)
        if problems:
            sys.exit("Could not initialize timestamps:\n- " + hooks.describe(problems))
        if fixed:
            print(f"Initialized timestamps in {len(fixed)} new Markdown files.")
    if not root_created and workspaces:
        print("The top-level AGENTS.md already existed. Add any new workspaces to its Contents table.")
    print("Codex users: run /hooks in Codex once and approve the aios-core hooks.")
    print("Plugin updates are manual in each agent harness. Run the aios-core:verify-aios skill to verify setup.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", nargs="?", default=os.getcwd())
    parser.add_argument("--workspace", action="append", type=workspace, default=[])
    args = parser.parse_args()
    if len(dict(args.workspace)) != len(args.workspace):
        parser.error("Give each workspace name only once.")
    main(os.path.abspath(args.folder), dict(args.workspace))
