---
type: AGENTS.md
created: 2026-10-03T16:45-07:00
updated: 2026-10-04T14:09-07:00
---

# Core aiOS plugin

The `aios-core` plugin checks file conventions in Claude Code and Codex. It also holds operator docs, system-level skills, and draft agent roles.

## Instructions

### Keep manifests consistent

When releasing a version, compare both plugin manifests. Their names and versions must match.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [docs/](docs/AGENTS.md) | Operator docs and type definitions | Installing, configuring, or documenting aiOS |
| [drafts/](drafts/AGENTS.md) | Draft skills and agent roles | Designing core skills or agents |
| [hooks/](hooks/AGENTS.md) | Hook definitions, execution, and checks | Changing how conventions are enforced |
| [skills/](skills/AGENTS.md) | Setup, check, status, and contract writing skills | Using or changing core skills |
| [.claude-plugin/plugin.json](.claude-plugin/plugin.json) | Claude Code plugin manifest | Changing plugin metadata or releasing a version |
| [.codex-plugin/plugin.json](.codex-plugin/plugin.json) | Codex plugin manifest | Changing plugin metadata or releasing a version |
