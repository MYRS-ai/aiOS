"""Helpers shared by hooks.py and the checks."""
import fnmatch, json, os, re


def load_yaml(path):
    """Read the supported YAML forms, rejecting syntax we cannot interpret."""
    with open(path, encoding="utf-8") as stream:
        return parse_yaml(stream.read().splitlines())


def parse_yaml(lines):
    """Read nested mappings, scalar values, and inline or block scalar lists."""
    entries = []
    for number, raw in enumerate(lines, 1):
        line = _without_comment(raw).rstrip()
        if not line.strip():
            continue
        if "\t" in line[:len(line) - len(line.lstrip())]:
            raise ValueError(f"line {number}: use spaces for YAML indentation")
        entries.append((len(line) - len(line.lstrip()), line.strip(), number))

    def fail(number, message):
        raise ValueError(f"line {number}: {message}")

    def scalar(value, number):
        try:
            return _scalar(value)
        except ValueError as error:
            fail(number, str(error))

    def block(index, indent):
        sequence = entries[index][1].startswith("-") and (entries[index][1] == "-" or entries[index][1].startswith("- "))
        result = [] if sequence else {}
        while index < len(entries) and entries[index][0] >= indent:
            depth, text, number = entries[index]
            if depth != indent:
                fail(number, "unexpected indentation")
            if sequence:
                if not text.startswith("- "):
                    fail(number, "use a nonempty scalar after each list dash")
                value = scalar(text[2:].strip(), number)
                if isinstance(value, (dict, list)):
                    fail(number, "block lists support scalar values only")
                result.append(value)
                index += 1
                continue
            key, sep, value = text.partition(":")
            if not sep or not key or key != key.strip() or any(c in key for c in "[]{}\"'") or key.startswith("- "):
                fail(number, "expected an unquoted setting name followed by ':'")
            if key in result:
                fail(number, f"duplicate setting '{key}'")
            index += 1
            if value.strip():
                result[key] = scalar(value.strip(), number)
            elif index < len(entries) and entries[index][0] > indent:
                result[key], index = block(index, entries[index][0])
            else:
                # Empty settings sections, such as checks:, mean an empty mapping.
                result[key] = {}
        return result, index

    if not entries:
        return {}
    if entries[0][0]:
        fail(entries[0][2], "top-level settings must not be indented")
    result, _ = block(0, 0)
    if not isinstance(result, dict):
        fail(entries[0][2], "expected a mapping of settings")
    return result


def _without_comment(line):
    quote, escaped = None, False
    for i, char in enumerate(line):
        if escaped:
            escaped = False
        elif quote == '"' and char == "\\":
            escaped = True
        elif quote:
            if quote == "'" and char == "'" and line[i + 1:i + 2] == "'":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "\"'" and (i == 0 or line[i - 1] in " \t[:,"):
            quote = char
        elif char == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def _scalar(value):
    if value.startswith("["):
        if not value.endswith("]"):
            raise ValueError("close the inline list with ']'")
        items, start, quote, escaped = [], 1, None, False
        for i, char in enumerate(value[1:-1], 1):
            if escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif quote:
                if quote == "'" and char == "'" and value[i + 1:i + 2] == "'":
                    escaped = True
                elif char == quote:
                    quote = None
            elif char in "\"'" and (i == start or value[i - 1].isspace()):
                quote = char
            elif char == ",":
                items.append(value[start:i].strip())
                start = i + 1
        items.append(value[start:-1].strip())
        if quote or any(not item for item in items[:-1]):
            raise ValueError("use a comma-separated list of scalar values")
        result = [_scalar(item) for item in items if item]
        if any(isinstance(item, (list, dict)) for item in result):
            raise ValueError("inline lists support scalar values only")
        return result
    if value.startswith('"'):
        try:
            return json.loads(value)
        except ValueError as error:
            raise ValueError("use a double-quoted string with JSON-compatible escapes") from error
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise ValueError("close single-quoted strings; escape an apostrophe as two apostrophes")
        return value[1:-1].replace("''", "'")
    if value == "{}":
        return {}
    if not value or value[0] in "{}&*!|>@`" or ": " in value:
        raise ValueError("unsupported YAML value; use a single-line scalar, a list, or an indented mapping")
    if value in ("true", "false"):
        return value == "true"
    if value in ("null", "~"):
        return None
    if re.fullmatch(r"[-+]?[0-9]+", value):
        return int(value)
    if re.fullmatch(r"[-+]?[0-9]+\.[0-9]+", value):
        return float(value)
    return value


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
    """Return the decoded value of a top-level front matter field."""
    return parse_yaml(lines or []).get(key)


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
