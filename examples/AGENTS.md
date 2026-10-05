---
type: AGENTS.md
created: 2026-10-04T14:18-07:00
updated: 2026-10-04T18:50-07:00
---

# aiOS examples

A small aiOS root for a fictional operator. The automated tests copy it into temporary folders.

## Instructions

### Keep the example small

Use fictional content without real people or organizations. Keep each workspace understandable in two minutes.

### Restore generated files

Run `python3 plugins/aios-core/skills/setup/scripts/setup.py examples/sample-root` from the product repo before checking sample links.
Setup restores the ignored `.aiOS/docs/` and `.aiOS/logs/` folders without overwriting existing files.
Keep both generated folders out of commits.

### Verify the sample

From `sample-root/`, run `python3 ../../plugins/aios-core/skills/check/scripts/check.py` and resolve every problem.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [sample-root/](sample-root/AGENTS.md) | Three domains and shared resources | Exploring a configured aiOS root |
