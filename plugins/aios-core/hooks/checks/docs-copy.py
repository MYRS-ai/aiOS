"""Warn when a file in the docs copy no longer matches what the last sync wrote."""
import hashlib, json, os


def check(files, settings, root):
    docs = os.path.join(root, ".aiOS", "docs")
    try:
        with open(os.path.join(docs, ".sync.json")) as f:
            synced = json.load(f).get("files")
    except (OSError, ValueError):
        return []
    if synced is None:
        return []
    out = []
    for p in files:
        rel = os.path.relpath(p, docs).replace(os.sep, "/")
        if rel.startswith("..") or rel == ".sync.json":
            continue
        with open(p, "rb") as f:
            if synced.get(rel) != hashlib.sha256(f.read()).hexdigest():
                out.append((os.path.relpath(p, root), "This file is a copy of the aios-core docs and is replaced on the next update; "
                                                      "make the change in a workspace's docs/ folder instead."))
    return out
