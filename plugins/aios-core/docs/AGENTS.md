---
type: AGENTS.md
created: 2026-10-03T13:21-07:00
updated: 2026-10-04T14:09-07:00
---

# aiOS operator docs

These docs explain aiOS terms, file conventions, checks, and setup. They ship inside the core plugin for installed operators.

## Instructions

### Keep docs usable after installation

Keep one doc per topic. Link to existing docs instead of repeating their content.
Use plugin-relative paths for scripts and `.aiOS/` for instance settings and logs.
Keep Markdown links within `docs/` so they work in both the plugin and the synced copy.
An installed plugin cannot reach the product repo's design records.
Describe current behavior and mark planned behavior clearly.

## Contents

### Folders

| Path | What it holds | Read when |
|---|---|---|
| [media/](media/AGENTS.md) | Documentation screenshots | Adding or finding a screenshot |
| [types/](types/AGENTS.md) | Front matter type definitions | Creating or editing a file of that type |

### Files

| Path | What it holds | Read when |
|---|---|---|
| [checks.md](checks.md) | Check settings and implementation requirements | Configuring, adding, or changing a check |
| [features.md](features.md) | Capabilities and their status | Reviewing what aiOS can do |
| [frontmatter.md](frontmatter.md) | Required Markdown fields | Creating a Markdown file |
| [glossary.md](glossary.md) | Shared terms and meanings | Naming something or checking a term |
| [hooks.md](hooks.md) | Hook behavior | Changing or debugging a hook |
| [logging.md](logging.md) | Hook event log format and use | Investigating a blocked turn or hook run |
| [onboarding.md](onboarding.md) | Installation, setup, approval, and updates | Setting up a folder or computer |
