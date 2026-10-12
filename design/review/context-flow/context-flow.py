#!/usr/bin/env python3
"""Build the offline context map from repository files and reviewed reading rules.

Run: python3 design/review/context-flow/context-flow.py
Check snapshot freshness: python3 design/review/context-flow/context-flow.py --check
Rendering requires Python-Markdown (python3 -m pip install Markdown).
The freshness check uses only the Python standard library. Nothing is installed by this script.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import html
from html.parser import HTMLParser
import json
import mimetypes
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit


FOLDER = Path(__file__).resolve().parent
REPO = FOLDER.parents[2]
OUTPUT = FOLDER / "context-flow.html"
TEMPLATE = FOLDER / "context-flow.template.html"
MODEL = FOLDER / "context-flow.json"
CORE = "plugins/aios-core/"
EXAMPLE = CORE + "skills/setup-aios/assets/example/"
DOCS = CORE + "docs/"
SKILLS = CORE + "skills/"
LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
ALLOWED = {"p", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "strong", "em", "del", "s", "code", "pre", "blockquote", "table", "thead", "tbody", "tr", "th", "td", "a", "img", "details", "summary", "span", "div", "sup", "sub"}


def inventory():
    """Read source files, never ignored docs copies, logs, temporary folders, or private parents."""
    found = {}
    for p in sorted(REPO.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(REPO).as_posix()
        parts = p.relative_to(REPO).parts
        if any(part in (".git", "__pycache__", ".DS_Store") or part.startswith((".aios-tests-", ".aios-example-")) for part in parts):
            continue
        if ".aiOS" in parts and any(x in parts[parts.index(".aiOS") + 1:] for x in ("docs", "logs")):
            continue
        if p == OUTPUT or p.suffix not in (".md", ".py", ".json", ".yaml", ".html", ".png", ".jpg", ".jpeg", ".webp") and p.name not in (".gitignore", "LICENSE"):
            continue
        found[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return found


def prose_lines(text):
    fence = None
    front = text.startswith("---\n")
    for number, line in enumerate(text.splitlines(), 1):
        if front:
            if number > 1 and line == "---":
                front = False
            continue
        mark = re.match(r"^\s*(`{3,}|~{3,})", line)
        if mark:
            token = mark.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


def plain(text):
    text = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*`_]+", "", text).strip()


def heading(text, fallback):
    match = re.search(r"^# (.+)$", text, re.M)
    return plain(match.group(1)) if match else fallback


def summary(text, path):
    if path.endswith(".py"):
        match = re.match(r'(?:#![^\n]*\n)?(?:"""|\x27\x27\x27)(.*?)(?:"""|\x27\x27\x27)', text, re.S)
        if match:
            return match.group(1).strip().split("\n\n")[0].replace("\n", " ")
        return "Python source used by the repository. Running it returns its output; it does not automatically load its source into the agent's context."
    if path.endswith((".yaml", ".json")) or Path(path).name == ".gitignore":
        return "Configuration or file-selection data. Its incoming connections distinguish program access from an agent reading the contents."
    if path.endswith("SKILL.md"):
        match = re.search(r"^description: (.+)$", text, re.M)
        if match:
            return match.group(1).strip("\"'")
    paragraphs, paragraph = [], []
    for _, line in prose_lines(text):
        if not line.strip() or line.startswith("#"):
            if paragraph:
                paragraphs.append(" ".join(paragraph)); paragraph = []
        elif not re.match(r"^\s*(?:\||[-*>]|\d+\.)", line):
            paragraph.append(line.strip())
        if len(paragraphs) >= 2:
            break
    if paragraph and len(paragraphs) < 2:
        paragraphs.append(" ".join(paragraph))
    result = plain(" ".join(paragraphs))
    if not result:
        result = "Source file used by the repository. Inspect its contents and incoming conditions to see where it participates."
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", result)
    result = " ".join(sentences[:3])
    return result if len(result) <= 480 else result[:477].rsplit(" ", 1)[0] + "…"


class Model:
    def __init__(self, hashes):
        self.hashes = hashes
        self.nodes = {}
        self.edges = []
        self.edge_keys = set()
        self.missing = []
        self.review = json.loads(MODEL.read_text())

    def node_id(self, path, scope="product"):
        if path.startswith(EXAMPLE):
            return "operator:" + path[len(EXAMPLE):]
        operator_path = scope == "operator" and not path.startswith("plugins/")
        if operator_path and path in self.hashes and EXAMPLE + path not in self.hashes:
            operator_path = False
        return ("operator:" if operator_path else "product:") + path

    def add_node(self, source_path, path=None, scope="product", generated=False):
        path = path or source_path
        ident = self.node_id(path, scope)
        if ident in self.nodes:
            return ident
        source = REPO / source_path
        is_image = source.suffix in (".png", ".jpg", ".jpeg", ".webp")
        text = "" if is_image else source.read_text(encoding="utf-8")
        if source_path.startswith(EXAMPLE):
            scope = "operator"; path = source_path[len(EXAMPLE):]
        name = Path(path).name
        kind = "image" if is_image else "template" if "/assets/" in source_path and not source_path.startswith(EXAMPLE) else "contract" if name == "AGENTS.md" else "skill" if name == "SKILL.md" else "script" if source.suffix == ".py" else "settings" if source.suffix in (".json", ".yaml") or name == ".gitignore" else "reference" if "/references/" in path else "design" if path.startswith("design/") else "doc"
        scopes = [scope]
        if source_path.startswith(EXAMPLE) or source_path.startswith(SKILLS) or source_path.startswith(CORE + "hooks/") or source_path.startswith(DOCS) and not generated:
            scopes = ["operator", "product"]
        self.nodes[ident] = {"id": ident, "scope": scope, "scopes": scopes, "path": path, "sourcePath": source_path,
            "title": heading(text, name), "summary": summary(text, source_path), "kind": kind,
            "words": len(re.findall(r"\b[\w'-]+\b", text)), "lines": len(text.splitlines()), "bytes": len(text.encode()),
            "sha": self.hashes[source_path], "text": text, "html": "", "generated": generated}
        if generated:
            generated_summary = "Generated docs path, shown using its plugin source. " + self.nodes[ident]["summary"]
            self.nodes[ident]["summary"] = " ".join(re.split(r"(?<=[.!?])\s+(?=[A-Z])", generated_summary)[:3])
        if is_image:
            self.nodes[ident]["summary"] = "Documentation screenshot of hook configuration or approval. Open the preview to inspect the recorded interface."
            self.nodes[ident]["bytes"] = source.stat().st_size
        return ident

    def resolve(self, node, destination):
        link = urlsplit(html.unescape(destination.strip().strip("<>")))
        if link.scheme or link.netloc:
            return None, unquote(link.fragment), link.geturl()
        template_targets = {"top-level-contract.md": "AGENTS.md", "settings-contract.md": ".aiOS/AGENTS.md", "workspace-contract.md": "work/AGENTS.md", "shared-contract.md": "shared/AGENTS.md", "glossary.md": "work/docs/glossary.md"}
        if node["sourcePath"].startswith(SKILLS + "setup-aios/assets/templates/") and node["kind"] == "template" and Path(node["path"]).name in template_targets:
            context = self.nodes.get("operator:" + template_targets[Path(node["path"]).name])
            if context:
                return self.resolve(context, destination)
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(node["path"]), unquote(link.path))) if link.path else node["path"]
        scope = node["scope"]
        ident = self.node_id(rel, scope)
        if ident in self.nodes:
            return ident, unquote(link.fragment), None
        if rel.startswith(".aiOS/docs/"):
            origin = DOCS + rel[len(".aiOS/docs/"):]
            if origin in self.hashes:
                return self.add_node(origin, rel, scope, True), unquote(link.fragment), None
        physical = (EXAMPLE + rel) if scope == "operator" and not node["generated"] else rel
        if physical in self.hashes:
            return self.node_id(physical), unquote(link.fragment), None
        # Virtual docs have physical relative targets within the core docs folder.
        if node["generated"]:
            physical = posixpath.normpath(posixpath.join(posixpath.dirname(node["sourcePath"]), unquote(link.path)))
            if physical in self.hashes and Path(physical).suffix == ".md":
                return self.add_node(physical, rel, scope, True), unquote(link.fragment), None
        return None, unquote(link.fragment), None

    def evidence(self, path, text="", line=None, scope="product"):
        ident = self.node_id(path, scope)
        if ident not in self.nodes:
            raise ValueError("Evidence file is absent: " + path)
        lines = self.nodes[ident]["text"].splitlines()
        if text:
            content = self.nodes[ident]["text"]
            position = content.find(text)
            if position < 0:
                raise ValueError("Evidence text changed: " + path + ": " + text)
            line = content[:position].count("\n") + 1
        if not line or not 1 <= line <= len(lines):
            raise ValueError("Invalid evidence line: " + path)
        return {"node": ident, "line": line, "text": text or lines[line - 1].strip()}

    def edge(self, source, target, kind, label, evidence=None, inferred=False):
        if source == target:
            return None
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("Unknown edge endpoint: " + source + " -> " + target)
        key = (source, target, kind, label)
        if key in self.edge_keys:
            return next(e["id"] for e in self.edges if (e["source"], e["target"], e["kind"], e["label"]) == key)
        self.edge_keys.add(key)
        ident = "edge-" + hashlib.sha256("|".join(key).encode()).hexdigest()[:12]
        self.edges.append({"id": ident, "source": source, "target": target, "kind": kind, "label": label, "evidence": evidence, "inferred": inferred})
        return ident

    def scan_links(self):
        # Ordinary links remain references unless an instruction or contract table supplies a condition.
        seen = set()
        while set(self.nodes) - seen:
            ident = next(iter(sorted(set(self.nodes) - seen))); seen.add(ident)
            node = self.nodes[ident]
            if not node["sourcePath"].endswith(".md"):
                continue
            section = ""
            for number, line in prose_lines(node["text"]):
                if line.startswith("#"):
                    section = line.lstrip("# ")
                for match in LINK.finditer(line):
                    destination = match.group(2)
                    # A previous sentence's imperative does not govern this link.
                    sentence_break = r"(?<=[.!?])\s+(?=[A-Z])"
                    statement = re.split(sentence_break, line[:match.start()])[-1] + re.split(sentence_break, line[match.start():])[0]
                    target, anchor, external = self.resolve(node, destination)
                    if not target or target not in self.nodes:
                        if not external and not destination.endswith(OUTPUT.name):
                            self.missing.append({"node": ident, "line": number, "destination": destination})
                        continue
                    kind = "reference"; label = "Reference: " + section
                    if node["kind"] == "template":
                        label = "Output-template link, resolved against the representative operator example"
                    elif node["kind"] == "contract" and line.startswith("|"):
                        cells = [plain(c.strip()) for c in line.strip("|").split("|")]
                        kind = "conditional"; label = cells[-1] if len(cells) >= 3 else "When this folder or file is relevant"
                    elif re.match(r"^\s*(?:[-*]\s+|\d+\.\s+)?(?:Read\b|Follow\b|Use\b|Start with\b|(?:Before|After)\b.*?\b(?:read|follow|use)\b)", statement):
                        kind = "conditional" if re.search(r"\b(before|when|if|relevant|choose)\b", statement, re.I) else "required"
                        label = plain(statement.lstrip("- 0123456789."))
                    if len(label) > 260:
                        label = label[:257].rsplit(" ", 1)[0] + "…"
                    self.edge(ident, target, kind, label, {"node": ident, "line": number, "text": line.strip()})

    def semantic_edges(self):
        for item in self.review.get("edges", []):
            scope = item.get("scope", "product")
            source = self.node_id(item["source"], scope)
            target = self.node_id(item["target"], scope)
            ev = self.evidence(item.get("evidencePath", item["source"]), item["evidenceText"], scope=scope)
            self.edge(source, target, item["kind"], item["label"], ev, item.get("inferred", False))

    def scenarios(self):
        scenarios = []
        for raw in self.review["scenarios"]:
            item = {k: v for k, v in raw.items() if k != "steps"}; item["steps"] = []
            for step in raw["steps"]:
                node = self.node_id(step["path"], step.get("scope", raw["scope"]))
                if node not in self.nodes:
                    raise ValueError("Scenario file is absent: " + step["path"])
                ev = self.evidence(step["sourcePath"], step.get("sourceText", ""), step.get("sourceLine"), raw["scope"]) if step.get("sourcePath") else None
                candidates = [e for e in self.edges if e["target"] == node and ev and e["source"] == ev["node"]
                              and e.get("evidence") and e["evidence"]["line"] == ev["line"]]
                via = candidates[0]["id"] if candidates else None
                # A scenario is a reviewed sequence, not an invented chain of file-to-file instructions.
                item["steps"].append({"node": node, "mode": step.get("mode", "read"), "reason": step["reason"],
                    "phase": step.get("phase", "Task context"), "readingKind": step.get("readingKind", step.get("mode", "read")), "evidence": ev, "via": via,
                    "recommended": step.get("recommended", False)})
            scenarios.append(item)
        return scenarios

    def findings(self):
        findings = []
        for raw in self.review["findings"]:
            item = {k: v for k, v in raw.items() if k not in ("evidence", "nodes")}
            item["evidence"] = [self.evidence(e["path"], e.get("text", ""), e.get("line"), raw.get("scope", "product")) for e in raw["evidence"]]
            item["nodes"] = list(dict.fromkeys([self.node_id(p, raw.get("scope", "product")) for p in raw.get("nodes", [])] + [e["node"] for e in item["evidence"]]))
            if any(n not in self.nodes for n in item["nodes"]):
                raise ValueError("Finding file is absent: " + raw["id"])
            findings.append(item)
        return findings


class SafePreview(HTMLParser):
    """Keep document formatting, rewrite local navigation, and never execute source HTML."""
    def __init__(self, model, node):
        super().__init__(convert_charrefs=True)
        self.model, self.node, self.out = model, node, []
        self.blocked = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style", "iframe", "object"):
            self.blocked += 1; return
        if self.blocked or tag not in ALLOWED:
            return
        safe = {}
        if attrs.get("id"):
            safe["id"] = attrs["id"]
        if tag in ("ol", "li") and attrs.get("start", attrs.get("value", "")).isdigit():
            safe["start" if tag == "ol" else "value"] = attrs.get("start", attrs.get("value"))
        if tag == "a":
            target, anchor, external = self.model.resolve(self.node, attrs.get("href", ""))
            if target and target in self.model.nodes:
                safe.update({"href": "#", "data-file": target, "data-anchor": anchor})
            elif external and urlsplit(external).scheme in ("https", "http"):
                safe.update({"href": external, "target": "_blank", "rel": "noopener noreferrer"})
            elif not external and posixpath.normpath(posixpath.join(posixpath.dirname(self.node["sourcePath"]), unquote(urlsplit(attrs.get("href", "")).path))) == OUTPUT.relative_to(REPO).as_posix():
                # The current viewer is not embedded recursively as another source node.
                safe.update({"href": "#", "data-close": "file-dialog"})
            else:
                safe.update({"href": "#", "data-unavailable": attrs.get("href", "")})
        if tag == "img":
            original = attrs.get("src", "")
            physical = (REPO / self.node["sourcePath"]).parent / unquote(urlsplit(original).path)
            try:
                physical = physical.resolve(); physical.relative_to(REPO)
                mime = mimetypes.guess_type(str(physical))[0]
                if physical.is_file() and mime in ("image/png", "image/jpeg", "image/webp"):
                    safe["src"] = "data:" + mime + ";base64," + base64.b64encode(physical.read_bytes()).decode()
            except (OSError, ValueError):
                pass
            safe["alt"] = attrs.get("alt", "Image not embedded")
        self.out.append("<" + tag + "".join(" " + k + '="' + html.escape(str(v), quote=True) + '"' for k, v in safe.items()) + ">")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe", "object"):
            self.blocked = max(0, self.blocked - 1); return
        if not self.blocked and tag in ALLOWED and tag not in ("img", "hr", "br"):
            self.out.append("</" + tag + ">")

    def handle_data(self, data):
        if not self.blocked:
            self.out.append(html.escape(data))


def render(model):
    try:
        import markdown
    except ImportError:
        raise SystemExit("Rebuilding requires Python-Markdown. Install it with: python3 -m pip install Markdown\nThe existing HTML and --check remain usable without it.")
    for node in list(model.nodes.values()):
        text = node["text"]
        if node["kind"] == "image":
            source = REPO / node["sourcePath"]
            mime = mimetypes.guess_type(str(source))[0]
            node["html"] = '<p><img alt="' + html.escape(node["title"], quote=True) + '" src="data:' + mime + ';base64,' + base64.b64encode(source.read_bytes()).decode() + '"></p>'
        elif node["sourcePath"].endswith(".md"):
            front = re.match(r"^---\n.*?\n---\n", text, re.S)
            body = text[front.end():] if front else text
            rendered = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists", "toc"])
            preview = SafePreview(model, node); preview.feed(rendered); preview.close()
            node["html"] = "".join(preview.out)
        else:
            node["html"] = "<pre><code>" + html.escape(text) + "</code></pre>"


def build(hashes):
    model = Model(hashes)
    for path in hashes:
        model.add_node(path)
    # Virtual docs model a synchronized copy, never the actual installed state.
    for path in hashes:
        if path.startswith(DOCS) and path.endswith(".md"):
            model.add_node(path, ".aiOS/docs/" + path[len(DOCS):], "operator", True)
            model.add_node(path, ".aiOS/docs/" + path[len(DOCS):], "product", True)
    model.scan_links()
    model.semantic_edges()
    scenarios = model.scenarios(); findings = model.findings()
    render(model)
    finding_ids = {f["id"] for f in findings}
    for scenario in scenarios:
        assert set(scenario.get("findings", [])) <= finding_ids, scenario["id"]
    digest = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    meta = dict(model.review.get("meta", {}))
    meta.update({"title": "Agent context flow", "builtAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sourceHash": digest, "sourceCount": len(hashes), "sourceFiles": hashes,
        "rebuild": "python3 design/review/context-flow/context-flow.py", "check": "python3 design/review/context-flow/context-flow.py --check",
        "linkGaps": model.missing})
    return {"meta": meta, "scopes": model.review["scopes"], "nodes": list(model.nodes.values()),
        "edges": model.edges, "scenarios": scenarios, "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that all source hashes still match the saved HTML.")
    args = parser.parse_args()
    hashes = inventory()
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit("Missing HTML. Run python3 design/review/context-flow/context-flow.py")
        found = re.search(r'<script[^>]*id=[\"\']context-data[\"\'][^>]*>(.*?)</script>', OUTPUT.read_text(), re.S)
        if not found:
            raise SystemExit("HTML has no context-data snapshot.")
        saved = json.loads(found.group(1))["meta"]["sourceFiles"]
        changed = sorted(p for p in set(saved) | set(hashes) if saved.get(p) != hashes.get(p))
        if changed:
            print("Snapshot is stale. Rebuild after reviewing reading rules and scenario evidence.")
            print("\n".join(changed)); return 1
        print("Snapshot is current: " + str(len(hashes)) + " source files match."); return 0
    data = build(hashes)
    template = TEMPLATE.read_text()
    if template.count("__CONTEXT_DATA__") != 1:
        raise SystemExit("Template must contain exactly one __CONTEXT_DATA__ placeholder.")
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    OUTPUT.write_text(template.replace("__CONTEXT_DATA__", encoded), encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(REPO)}: {len(data['nodes'])} files, {len(data['edges'])} links, {len(data['scenarios'])} scenarios, {len(data['findings'])} findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
