---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-04T14:09-07:00
---

# Decisions

This file records settled product decisions. Proposals remain in the other design docs.

## Folders and instructions

- Folder names are lowercase, hyphenated, and one to four words.
- Each folder's `AGENTS.md` is its contract. Add another canonical file only when no existing convention meets the need.
- Use `AGENTS.md` for instruction files. Do not add `CLAUDE.md` anywhere in the repo.
- Keep the glossary in the core plugin's `docs/glossary.md`. Use each term only as it defines it.

## Agents and plugins

- The main agent coordinates work, delegates to subagents, and briefs them.
- The skills and agent roles in `plugins/aios-core/drafts/` remain drafts. Extension plugin folders are placeholders.
- The core plugin ships setup, status, check, and write-contract skills in `plugins/aios-core/skills/`.
- The core plugin lives at `plugins/aios-core/`. It holds system-level skills and hooks.
- Extension plugins come later. Each extends aiOS for one area of capability, such as writing and editing or creative media.
- An extension plugin may use the core plugin but should not depend on another extension plugin.
- Define extension plugin boundaries around shared goals, workflows, and components that work together.

## Front matter

- The standard fields are `type`, `created`, and `updated`.
- `created` and `updated` include the time in Pacific time.
- `status` is not a universal field. It may return for some file types.
- `AGENTS.md` has its own type, `type: AGENTS.md`, and needs its own type definition or template.
- Each type has a definition in the core plugin's `docs/types/` folder, one file per type.

## Enforcement

- The aios-core plugin provides hooks in one `hooks.json` for Claude Code and Codex.
- Hook code lives in the plugin's `hooks/` folder and serves only the hooks. A script a skill needs lives inside that skill.
- Hooks check changed files at the end of each turn. Failures block the turn with a reason; passes fill in timestamps.
- An aiOS root's `.aiOS/config.yaml` enables enforcement and holds `enabled`, `include`, `exclude`, and settings for individual checks.
- The plugin searches upward from the session folder for that file. Without it, the plugin does nothing. Nested aiOS roots use their own config and are excluded from parent checks.

## Setup and product docs

- The setup skill confirms workspaces with the operator before creating contracts and settings.
- Setup preserves existing files and adds missing pieces. It appends the log exclusion to `.gitignore` when needed.
- The start hook syncs core plugin docs into `.aiOS/docs/` before logging, even when checks are off.
- Sync records the plugin version and source hash. Newer versions or changed content at the same version replace the copy.
- An older plugin keeps the newer copy and tells the agent to update that agent harness's plugin.
- The docs-copy check warns about edits to the copy. Custom docs belong in a workspace's `docs/` folder.
- The product README omits front matter for GitHub rendering and is excluded from this repo's checks.
