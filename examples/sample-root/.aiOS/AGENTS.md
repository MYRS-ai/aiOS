---
type: AGENTS.md
created: 2026-10-04T14:12-07:00
updated: 2026-10-04T14:12-07:00
---

# aiOS check settings

Settings, the docs copy, and the hook log for this aiOS root.

## Instructions

### Change settings

Edit `config.yaml` to enable checks or change their scope and requirements.

### Keep product docs separate

The core plugin replaces `docs/` on updates. Put custom docs in a workspace's `docs/` folder instead.

### Read hook results

Use `logs/hook-events.jsonl` to inspect check results. Do not edit log entries. You can delete `logs/`; the plugin recreates it.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [docs/](docs/AGENTS.md) | Copy of the core plugin docs | Reading product instructions |
| `logs/` | Hook event log, created by the hooks | Investigating a blocked turn or hook run |
| [config.yaml](config.yaml) | Check settings for this aiOS root | Changing which checks run or what they require |
