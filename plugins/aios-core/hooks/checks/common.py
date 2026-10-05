"""Helpers shared by hooks.py and the checks."""
import fnmatch, os


def load_yaml(path):
    """Read aiOS configuration YAML: nested settings, scalar values, and inline lists."""
    root = {}
    stack = [(-1, root)]
    for raw in open(path):
        line = _without_comment(raw).rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        while indent <= stack[-1][0]:
            stack.pop()
        if value.strip():
            stack[-1][1][key] = _scalar(value.strip())
        else:
            stack[-1][1][key] = {}
            stack.append((indent, stack[-1][1][key]))
    return root


def _without_comment(line):
    quote, escaped = None, False
    for i, char in enumerate(line):
        if escaped:
            escaped = False
        elif quote == '"' and char == "\\":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in "\"'" and (i == 0 or line[i - 1] in " \t[:,"):
            quote = char
        elif char == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def _scalar(value):
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(v.strip()) for v in value[1:-1].split(",") if v.strip()]
    if value[:1] in "\"'" and value[-1:] == value[:1]:
        return value[1:-1]
    if value in ("true", "false"):
        return value == "true"
    return int(value) if value.lstrip("-").isdigit() else value


def front_matter(path):
    """Return front matter lines, or None when no front matter block exists."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except UnicodeError as error:
        raise OSError(str(error)) from error
    end = text.find("\n---", 3)
    return text[4:end].split("\n") if text.startswith("---\n") and end != -1 else None


def field(lines, key):
    """Return a front matter field's value, including one nested under metadata:."""
    for line in lines:
        name, sep, value = line.strip().partition(":")
        if sep and name == key:
            return value.strip()
    return None


def skill_package(path, root):
    """Return the nearest folder containing path and a SKILL.md, or None."""
    folder = os.path.dirname(os.path.abspath(path))
    while folder.startswith(root) and folder != os.path.dirname(root):
        if os.path.isfile(os.path.join(folder, "SKILL.md")):
            return folder
        folder = os.path.dirname(folder)
    return None


def matches(rel, patterns):
    """True if rel matches any pattern. A leading **/ also matches zero folders."""
    return any(fnmatch.fnmatch(rel, g) or (g.startswith("**/") and fnmatch.fnmatch(rel, g[3:])) for g in patterns)
