---
type: AGENTS.md
created: 2026-10-03T18:07-07:00
updated: 2026-10-04T18:50-07:00
---

# File convention checks

The checks for front matter, folder names, and edits to the docs copy, with their default settings and shared Python functions.

## Instructions

### Configure a check

Read [the settings guide](../../docs/checks.md#how-settings-work) before changing defaults or front matter rules. Keep `checks.yaml` and the setup template consistent when their settings change.

### Implement a check

Follow [the check interface and validation steps](../../docs/checks.md#add-or-change-a-check).

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [checks.yaml](checks.yaml) | Default settings, in check order | Changing defaults or adding a check |
| [common.py](common.py) | Shared functions for YAML, front matter, and paths | Changing how checks read settings or match files |
| [docs-copy.py](docs-copy.py) | Warning for edits to the docs copy | Protecting copied product docs |
| [frontmatter.py](frontmatter.py) | Front matter check, which also fills in timestamps | Changing required fields, rules, or timestamps |
| [names.py](names.py) | Folder name check | Changing folder naming conventions |
