---
type: AGENTS.md
---

# aiOS check settings

Settings, the docs copy, and the hook log for this aiOS.

## Instructions

### Change settings

Edit `config.yaml` to enable checks or change their scope and requirements.

### Keep product docs separate

- The start hook replaces outdated or edited `docs/` copies when a session starts. Never edit this copy by hand.
- Change product documentation in the core plugin's source `docs/` folder.
- Keep the operator's custom docs in a workspace's `docs/` folder.

### Read hook results

Use `logs/hook-events.jsonl` to inspect check results.

- Do not edit log entries.
- You can delete `logs/`; the plugin recreates it.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [docs/](docs/AGENTS.md) | Copy of the core plugin docs | Reading product instructions |
| `logs/` | Hook event log, created by the hooks | Investigating a blocked turn or hook run |
| [config.yaml](config.yaml) | Check settings for this aiOS | Changing which checks run or what they require |
