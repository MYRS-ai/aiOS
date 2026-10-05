---
type: AGENTS.md
created: 2026-10-04T11:20-07:00
updated: 2026-10-04T18:50-07:00
---

# aiOS hooks

The hook definitions and Python code that Claude Code and Codex both run.

## Instructions

### Change hook behavior

Read [the hooks guide](../docs/hooks.md) before changing events, file selection, or blocking behavior. Use [the logging guide](../docs/logging.md) to check the recorded result. Changes to `hooks.json` require new Codex approval.

### Keep hook code here

Code in this folder serves the hooks. A script needed by a skill belongs in that skill's folder.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [checks/](checks/AGENTS.md) | Check implementations and defaults | Adding or changing a check |
| [hooks.json](hooks.json) | Hook definitions shared by both agent harnesses | Changing which hook events run |
| [hooks.py](hooks.py) | Docs sync, file selection, checks, and logging | Changing how hooks run |
