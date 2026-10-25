"""Check hyphenated folder names, preserving approved terms and ignoring hidden folders."""
import os, re

WORD = re.compile(r"[a-z0-9]+")
BUILTIN_TERMS = frozenset({"aiOS"})


def valid_name(name, settings):
    """Require one to four lowercase or approved words, separated by hyphens."""
    allowed_terms = BUILTIN_TERMS | set(settings.get("allowed_terms", []))
    words = name.split("-")
    return (1 <= len(words) <= 4 and
            all(word in allowed_terms or WORD.fullmatch(word) for word in words))


def check(files, settings, root):
    folders = {os.path.relpath(os.path.dirname(p), root) for p in files}
    out = set()
    for folder in folders:
        parts = folder.split(os.sep)
        for i, part in enumerate(parts):
            if part in (".", "") or part.startswith("."):
                continue
            if not valid_name(part, settings):
                out.add((os.sep.join(parts[: i + 1]),
                         "folder name must be lowercase, hyphenated, one to four words; "
                         "approved terms may keep their exact capitalization"))
    return sorted(out)
