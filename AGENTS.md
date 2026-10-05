---
type: AGENTS.md
created: 2026-10-04T13:19-07:00
updated: 2026-10-04T19:11-07:00
---

# aiOS product

The aiOS product: plugins, operator docs, design records, examples, and tests, developed for any operator.

## Instructions

### Keep the product generic

Nothing in this repo may name an operator, their workspaces, or their organizations, except author and owner fields in plugin manifests and the copyright notice in `LICENSE`.
Keep instance settings and customizations outside product files.

### Follow the documentation conventions

Use the [glossary](plugins/aios-core/docs/glossary.md) and the [contract definition](plugins/aios-core/docs/types/agents-md.md).
Except for `README.md`, start Markdown files outside skill folders with only `type: AGENTS.md` or `type: doc` in front matter.
Hooks add timestamps. Use plain sentences and no em dashes.
Update contracts when their contents change. Keep relative Markdown links valid.

### Verify changes

Read [decisions.md](design/decisions.md) before relying on a design proposal.
Run `python3 plugins/aios-core/skills/check/scripts/check.py` from this repo and resolve every problem.
Run `python3 -m unittest discover -s tests -v`, then again with `/usr/bin/python3`, macOS's built-in Python 3.9, the oldest version aiOS supports.
Check relative Markdown links and scan for operator details before reporting completion.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [.aiOS/](.aiOS/AGENTS.md) | Checks scoped to this product repo | Changing how this repo checks itself |
| [design/](design/AGENTS.md) | Product decisions, research, and plans | Developing the product design |
| [examples/](examples/AGENTS.md) | A fictional operator's sample aiOS root | Learning the folder structure or preparing test data |
| [plugins/](plugins/AGENTS.md) | Core plugin and draft extension plugins | Changing shipped behavior or operator docs |
| [tests/](tests/AGENTS.md) | Automated setup and hook tests | Verifying changes to the core plugin |
| [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) | Codex marketplace | Changing the Codex plugin catalog |
| [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) | Claude Code marketplace | Changing the Claude Code plugin catalog |
| [LICENSE](LICENSE) | PolyForm Noncommercial License 1.0.0 | Checking how aiOS may be used |
| [README.md](README.md) | Product overview, installation, setup, and updates | Evaluating or installing aiOS |
