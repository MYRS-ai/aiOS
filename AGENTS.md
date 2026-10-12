---
type: AGENTS.md
created: 2026-10-04T13:19-07:00
updated: 2026-10-12T14:28-07:00
---

# aiOS product

The aiOS product: plugins, operator docs, design records, and tests, developed for any operator. The setup skill includes a complete fictional example.

## Instructions

### Keep the product generic

- The product should be generalizable to any operator, their workspaces, or their organizations.
- Keep instance settings and customizations outside product files.

### Follow the documentation conventions

- Use the [glossary](plugins/aios-core/docs/glossary.md), the [naming conventions](plugins/aios-core/docs/naming.md), and the [contract definition](plugins/aios-core/docs/types/agents-md.md).
- Follow the [document structure guidance](plugins/aios-core/docs/types/doc.md#structure) for paragraphs, lists, and headings.
- Keep relative Markdown links valid.

### Keep contracts and skills current

- Use `aios-core:manage-agents-md` when a folder's purpose, instructions, or contents change.
- Use `aios-core:manage-skills` when creating, changing, or reviewing a skill.

### Agree on vocabulary

Before introducing or changing a concept, follow [Maintaining vocabulary](plugins/aios-core/docs/glossary.md#maintaining-vocabulary).

### Maintain release history

- Update [changelog.md](changelog.md) for substantial batches of related changes. Summarize outcomes and upgrade actions under `Unreleased`.
- Create a new version for a substantial batch. Move its entries into a dated section and match both core plugin manifests.
- Run the required tests and refresh the context visualization before committing the release.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [.aiOS/](.aiOS/AGENTS.md) | Checks scoped to this product repo | Changing how this repo checks itself |
| [design/](design/AGENTS.md) | Research, proposals, specs, and product decisions | Developing the product design |
| [plugins/](plugins/AGENTS.md) | Core plugin and draft extension plugins | Changing shipped behavior or operator docs |
| [tests/](tests/AGENTS.md) | Automated setup and hook tests | Verifying changes to the core plugin |
| [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) | Codex marketplace | Changing the Codex plugin catalog |
| [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) | Claude Code marketplace | Changing the Claude Code plugin catalog |
| [.gitignore](.gitignore) | Paths excluded from Git | Changing which files Git tracks |
| [changelog.md](changelog.md) | Release history and upgrade actions | Recording changes or preparing an update |
| [LICENSE](LICENSE) | MIT License | Checking how aiOS may be used |
| [README.md](README.md) | Product overview, installation, setup, and updates | Evaluating or installing aiOS |
