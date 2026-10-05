"""Folder names are lowercase, hyphenated, one to four words. Hidden folders, such as .aiOS, are exempt."""
import os, re

PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+){0,3}$")


def check(files, settings, root):
    folders = {os.path.relpath(os.path.dirname(p), root) for p in files}
    out = set()
    for folder in folders:
        parts = folder.split(os.sep)
        for i, part in enumerate(parts):
            if part not in (".", "") and not part.startswith(".") and not PATTERN.match(part):
                out.add((os.sep.join(parts[: i + 1]), "folder name must be lowercase, hyphenated, one to four words"))
    return sorted(out)
