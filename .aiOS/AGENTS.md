---
type: AGENTS.md
created: 2026-10-04T13:57-07:00
updated: 2026-10-11T10:37-07:00
---

# Product repo check settings

Check settings for this product repo, using the core plugin defaults.

## Instructions

### Keep checks local

- Keep this configuration generic. It scopes checks to this repo and its contents.
- Exclude `README.md` because it omits front matter for GitHub rendering.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| `docs/` | Copy of the core plugin docs, created at session start | Reading product instructions as an installed operator sees them |
| `logs/` | Hook event log, created by the hooks | Investigating a blocked turn or hook run |
| [config.yaml](config.yaml) | Check scope for the product repo | Changing how this repo checks itself |
