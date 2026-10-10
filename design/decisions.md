---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-10T15:35-07:00
---

# Decisions

This file records settled product decisions. Proposals remain in the other design docs.

## Folders and instructions

- Folder names are lowercase, hyphenated, and one to four words.
- Each folder's `AGENTS.md` is its contract. Add another canonical file only when no existing convention meets the need.
- Use `AGENTS.md` for instruction files. Do not add `CLAUDE.md` anywhere in the repo.

## Terms and names

- The aiOS glossary lives in the core plugin's `docs/glossary.md` and applies to every workspace. Only core plugin updates change it.
- Each workspace has a workspace glossary at `docs/glossary.md`. `shared/docs/glossary.md` holds terms that more than one workspace uses.
- Agents read glossaries in this order: aiOS, shared, then the current workspace. A workspace glossary adds terms and never redefines aiOS terms.
- Agents read the aiOS glossary and naming conventions before they create or change contracts, glossaries, skills, plugins, or `.aiOS/` settings. They read the shared and workspace glossaries before working in a workspace.
- Naming conventions live in the core plugin's `docs/naming.md`.
- Refer to a plugin skill as `plugin:skill`, such as `aios-core:setup`.

## Agents and plugins

- The main agent coordinates work, delegates to subagents, and briefs them.
- The skills and agent roles in `plugins/aios-core/drafts/` remain drafts. Extension plugin folders are placeholders.
- The core plugin ships four skills in `plugins/aios-core/skills/`: setup, status, manage-agents-md, and manage-skills.
- A skill exists only when it does work that no other skill, hook, or script does. The check skill was retired because the stop hook checks changed files and the status report checks every file.
- `docs/types/skill-md.md` defines the skill package. Skills an operator maintains live in their workspace's `skills/` folder, or in `shared/skills/`.
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
- Setup creates a placeholder glossary in each workspace, including `shared/`.
- Setup preserves existing files and adds missing pieces. It appends the log exclusion to `.gitignore` when needed.
- The start hook syncs core plugin docs into `.aiOS/docs/` before logging, even when checks are off.
- Sync records the plugin version and source hash. Newer versions or changed content at the same version replace the copy.
- An older plugin keeps the newer copy and tells the agent to update that agent harness's plugin.
- The docs-copy check warns about edits to the copy. Custom docs belong in a workspace's `docs/` folder.
- The product README omits front matter for GitHub rendering and is excluded from this repo's checks.

## Design records

- `design/` holds research, proposals, specs, and `decisions.md`. It does not ship in any plugin.
- Proposals form the backlog. The operator sets their priority and decides which become specs.
- A spec gives a subagent enough detail to implement and test the work. Implementation starts only from a ready spec.
- When a spec's work ships, its settled design moves into `decisions.md`.
- Open topics get no placeholder file.
