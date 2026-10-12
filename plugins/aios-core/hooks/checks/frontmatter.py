"""Check front matter using the first matching rule.

match: skill (a SKILL.md), skill-resource (any other file in a skill folder),
or a list of path patterns.
required: fields the agent must write; missing fields fail the check.
allowed: permitted values for each field, such as type: [AGENTS.md, doc].
timestamps: fields the hook fills in at the end of the turn (created, updated).
format: agent-skills adds the Agent Skills rules for name and description.
"""
import os, re
from datetime import datetime
from zoneinfo import ZoneInfo
from common import field, front_matter, matches, parse_yaml, skill_package

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def rule_for(path, settings, root):
    rel, package = os.path.relpath(path, root), skill_package(path, root)
    is_skill_md = os.path.basename(path) == "SKILL.md"
    for name, rule in settings["rules"].items():
        m = rule.get("match", ["**"])
        if m == "skill":
            hit = bool(package) and is_skill_md
        elif m == "skill-resource":
            hit = bool(package) and not is_skill_md
        else:
            hit = matches(rel, m if isinstance(m, list) else [m])
        if hit:
            return name, rule
    return None, {}


def agent_skills_problems(path, values, root):
    out = []
    name, folder = values.get("name"), os.path.basename(skill_package(path, root) or "")
    if not isinstance(name, str) or not name.strip():
        out.append("name must be a nonempty top-level string")
    elif name != folder:
        out.append(f"name '{name}' must match its folder '{folder}'")
    elif not NAME.match(name) or len(name) > 64:
        out.append("name must be lowercase letters, numbers, and hyphens, at most 64 characters")
    description = values.get("description")
    if not isinstance(description, str) or not description.strip():
        out.append("description must be a nonempty top-level string")
    elif len(description) > 1024:
        out.append("description must be at most 1024 characters")
    return out


def check(files, settings, root):
    out = []
    for p in files:
        if not p.endswith(".md"):
            continue
        rule_name, rule = rule_for(p, settings, root)
        if not any(rule.get(key) for key in ("required", "allowed", "format")):
            continue
        lines = front_matter(p)
        rel, allowed = os.path.relpath(p, root), rule.get("allowed", {})
        try:
            values = parse_yaml(lines or [])
        except ValueError as error:
            out.append((rel, f"invalid front matter: {error}. Rule: {rule_name}"))
            continue
        hint = lambda k: f" ({k} is one of: {', '.join(allowed[k])})" if k in allowed else ""
        missing = [k for k in rule.get("required", []) if k not in values or values[k] in (None, "", {}, [])]
        if missing:
            out.append((rel, f"missing front matter: {', '.join(missing)}{''.join(hint(k) for k in missing)}. Rule: {rule_name}"))
            continue
        for k, choices in allowed.items():
            value = values.get(k)
            if value is not None and value not in choices:
                out.append((rel, f"{k} '{value}' is not allowed{hint(k)}. Rule: {rule_name}"))
        if rule.get("format") == "agent-skills":
            out += [(rel, f"{m}. Rule: {rule_name}") for m in agent_skills_problems(p, values, root)]
    return out


def _find(lines, key):
    return next((i for i, l in enumerate(lines) if l.partition(":")[0] == key), None)


def _changed_since(p, value):
    """True if the file was modified after the minute recorded in value."""
    try:
        recorded = datetime.fromisoformat(value).timestamp()
    except (TypeError, ValueError):
        return True
    return os.path.getmtime(p) // 60 * 60 > recorded


def fix(files, settings, root):
    now = datetime.now(ZoneInfo(settings["zone"])).isoformat(timespec="minutes")
    done = []
    for p in files:
        # The docs copy keeps the timestamps it was synced with.
        if not p.endswith(".md") or os.path.relpath(p, root).startswith(".aiOS/docs/"):
            continue
        timestamps = rule_for(p, settings, root)[1].get("timestamps", [])
        lines = front_matter(p)
        if not timestamps or lines is None:
            continue
        try:
            parse_yaml(lines)
        except ValueError:
            # A syntax diagnostic comes from check(); never rewrite an invalid block.
            continue
        c, u = _find(lines, "created"), _find(lines, "updated")
        add_created = "created" in timestamps and c is None
        set_updated = "updated" in timestamps and (u is None or _changed_since(p, field(lines, "updated")))
        if not (add_created or set_updated):
            continue
        t = _find(lines, "type")
        anchor = t if t is not None else len(lines) - 1
        indent = lines[anchor][: len(lines[anchor]) - len(lines[anchor].lstrip())] if t is not None else ""
        if add_created:
            lines.insert(anchor + 1, f"{indent}created: {now}")
        if set_updated:
            u = _find(lines, "updated")
            if u is None:
                lines.insert((_find(lines, "created") or anchor) + 1, f"{indent}updated: {now}")
            else:
                lines[u] = f"{indent}updated: {now}"
        with open(p, encoding="utf-8") as f:
            text = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write("---\n" + "\n".join(lines) + text[text.find("\n---", 3):])
        done.append(os.path.relpath(p, root))
    return done
