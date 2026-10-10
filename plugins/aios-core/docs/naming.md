---
type: doc
created: 2026-10-10T13:18-07:00
updated: 2026-10-10T14:54-07:00
---

# Naming conventions

How to write names in aiOS files: the product name, skills, plugins, folders, and files.
The [glossary](glossary.md) defines what terms mean. This doc covers how to write names.

## aiOS

- Write `aiOS` in prose and display names, such as aiOS Core.
- Write `aios` in lowercase in plugin and marketplace identifiers, such as `aios-core`. Plugin identifiers must be lowercase and hyphenated.
- The `.aiOS/` folder keeps the display spelling.

## Skills

- Refer to a plugin skill as `plugin:skill`, such as `aios-core:setup`. Claude Code and Codex both list plugin skills this way.
- Refer to a skill outside a plugin by its name alone.
- Use the bare skill name only where a format requires it, such as the `name` field in `SKILL.md` or a path like `skills/setup/`.
- Write `/aios-core:setup` only when showing a command to type in Claude Code.
- Name skills with lowercase, hyphenated words, such as `manage-agents-md`. The name matches the skill's folder.

## Plugins

- Name aiOS plugins `aios-` followed by one word for their area of capability, such as `aios-core` or `aios-write`.

## Folders

- Name folders with one to four lowercase words separated by hyphens. The `names` check enforces this.
- Hidden folders, such as `.aiOS/`, are exempt. See [checks.md](checks.md#the-names-check).

## Files

- Name files with lowercase, hyphenated words, such as `hook-events.jsonl`. No check enforces this.
- Keep the exact names that agent harnesses and Git expect, such as `AGENTS.md`, `SKILL.md`, and `README.md`.
