---
type: AGENTS.md
created: 2026-10-03T13:21-07:00
updated: 2026-10-11T10:37-07:00
---

# aiOS operator docs

These docs explain aiOS terms, file conventions, checks, and setup. They ship inside the core plugin for installed operators.

## Instructions

### Keep docs usable after installation

- Keep one doc per topic. Link to existing docs instead of repeating their content.
- Use plugin-relative paths for scripts and `.aiOS/` for settings and logs.
- Keep Markdown links within `docs/` so they work in both the plugin and the docs copy.
- An installed plugin cannot reach the product repo's design records.
- Describe current behavior and mark planned behavior clearly.
- Follow the [document structure guidance](types/doc.md#structure) for readable paragraphs, lists, and headings.

### Change documentation at its source

Make product documentation changes in the core plugin's source repository. After the local plugin is updated, the start hook refreshes `.aiOS/docs/` from it. Never edit the generated copy by hand.

## Contents

### Folders

| Path | What it holds | Read when |
|---|---|---|
| [media/](media/AGENTS.md) | Documentation screenshots | Adding or finding a screenshot |
| [types/](types/AGENTS.md) | File type definitions, such as `AGENTS.md` and `SKILL.md` | Creating or editing a file of that type |

### Files

| Path | What it holds | Read when |
|---|---|---|
| [checks.md](checks.md) | Check settings and implementation requirements | Configuring, adding, or changing a check |
| [features.md](features.md) | Capabilities and their status | Reviewing what aiOS can do |
| [frontmatter.md](frontmatter.md) | Required Markdown fields | Creating a Markdown file |
| [glossary.md](glossary.md) | Agreed aiOS meanings and vocabulary upkeep | Using, introducing, or changing a concept |
| [hooks.md](hooks.md) | Hook behavior | Changing or debugging a hook |
| [logging.md](logging.md) | Hook event log format and use | Investigating a blocked turn or hook run |
| [naming.md](naming.md) | How to write the product name, skills, plugins, folders, and files | Naming something or referring to a skill |
| [onboarding.md](onboarding.md) | Installation, setup, approval, and updates | Setting up a folder or computer |
