---
type: doc
created: 2026-10-04T09:55-07:00
updated: 2026-10-10T15:35-07:00
---

# Features

aiOS guides AI agents working on the operator's behalf through contracts, skills, and plugins.
The core plugin, `aios-core`, provides these features in Claude Code and Codex.

| Feature | What it does | Status |
|---|---|---|
| [Workspaces](#workspaces) | Keeps each domain's files and context in its own folder | Available |
| [Folder contracts](#folder-contracts) | Tells agents what a folder is for, what to follow, and where to look | Available |
| [Skill packages](#skill-packages) | Defines how every skill is built, and helps agents create and maintain skills | Available |
| [Glossary](#glossary) | Gives each aiOS term one meaning | Available |
| [Front matter](#front-matter) | Declares each file's type and records when it changed | Partial |
| [Convention checks](#convention-checks) | Checks changed files before each turn ends | Available |
| [Docs copy](#docs-copy) | Keeps the core plugin docs inside each aiOS root | Available |
| [Status report](#status-report) | Diagnoses aiOS and reports its settings, versions, hook runs, and file problems | Available |
| [Hook log](#hook-log) | Records every hook run and its result | Available |
| [Claude Code and Codex support](#claude-code-and-codex-support) | Runs the same core plugin in both agent harnesses | Available |

## Workspaces

Workspaces are the top-level folders of an aiOS root. Each one keeps a domain's files and context together.
Agents choose the workspace for the domain a request concerns. They ask the operator when the domain is unclear.

- The `aios-core:setup` skill interviews the operator and confirms workspace names before creating them.
- Setup creates `.aiOS/config.yaml`, the docs copy, the root and workspace contracts, workspace glossaries, and `shared/`.
- The `shared/` workspace holds resources that more than one domain uses, such as standards and CLIs. Shared is not a domain.
- Operators name their own domains and workspaces.
- Running setup again adds missing pieces and keeps existing files.
- See [onboarding.md](onboarding.md#2-set-up-a-folder) for the setup steps.

## Folder contracts

A contract is a folder's `AGENTS.md` file. It states the folder's purpose, the instructions that apply there, and links to its contents.
Agents read a folder's contract before working there. They follow its links to the files a task needs and skip the rest.

- The [contract definition](types/agents-md.md) sets the structure and says when a folder needs a contract.
- The `aios-core:manage-agents-md` skill creates, updates, and reviews contracts and keeps the parent contract's links current.
- aiOS uses `AGENTS.md` and never `CLAUDE.md`. In tests, a `CLAUDE.md` file stopped Claude Code from loading `AGENTS.md` files.

## Skill packages

A skill package is a skill's folder: its `SKILL.md` and the scripts, references, and assets it uses. Every aiOS skill follows one structure.
Agents follow that structure when they create or change a skill, so skills stay consistent and easy to use.

- The [skill definition](types/skill-md.md) sets the package structure, front matter, sections, and writing style.
- Skills the operator maintains live in their workspace's `skills/` folder, or in `shared/skills/` when more than one workspace uses them.
- The `aios-core:manage-skills` skill creates, updates, and reviews skill packages.

## Glossary

The aiOS glossary gives each aiOS term one meaning and lists the words not to use in its place.
Agents read it before they create or change aiOS files. They use each term exactly as the glossary defines it.

- The [aiOS glossary](glossary.md) ships with the core plugin and applies to every workspace.
- Each workspace has a workspace glossary at `docs/glossary.md` for the operator's own terms. Setup creates it.
- `shared/docs/glossary.md` holds terms that more than one workspace uses.
- Agents read the aiOS glossary, then the shared glossary, then the current workspace's glossary.
- A workspace glossary adds terms and never redefines aiOS terms.
- [naming.md](naming.md) sets how to write names, such as aiOS and skill names.

## Front matter

Front matter declares each Markdown file's type and records when the file was created and last updated.
Agents write only the `type` field. Hooks fill in the `created` and `updated` timestamps when a turn ends.

- Markdown files outside skill folders use `type: AGENTS.md` or `type: doc`.
- `SKILL.md` files use the `name` and `description` fields of the Agent Skills format.
- Each type has a definition in the [types folder](types/AGENTS.md). Only `AGENTS.md` has one so far.
- Timestamps use the configured time zone, `America/Los_Angeles` by default.
- Operators add types and front matter rules in `.aiOS/config.yaml`.
- See [frontmatter.md](frontmatter.md) for the fields each file needs.

## Convention checks

Convention checks test the files changed in a turn against aiOS conventions, such as front matter and folder names.
When a check fails, the hook blocks the turn and tells the agent what to fix. The agent fixes the problems before the turn ends.

- The `frontmatter` check tests required fields and allowed values.
- The `names` check tests that folder names are lowercase, hyphenated, and one to four words.
- The `docs-copy` check warns when a file in the docs copy changed after the last sync.
- After two blocks in one turn, remaining failures become warnings. The `max_blocks` setting changes the limit.
- Checks run only inside an aiOS root. The plugin searches upward from the session folder for `.aiOS/config.yaml`.
- The `aios-core:status` skill reports problems in every file in the aiOS root, including files changed between sessions.
- See [hooks.md](hooks.md) for the steps each turn and [checks.md](checks.md) for settings.

## Docs copy

The docs copy is the set of core plugin docs in each aiOS root's `.aiOS/docs/` folder. It gives contracts a fixed path to the product docs.
Agents read the docs copy for aiOS terms, conventions, and setup steps. They never edit it.

- The start hook syncs the docs copy from the installed core plugin when a session starts.
- Sync replaces the docs copy when the plugin version or docs change, or when the copy was edited. Edits are lost.
- If the docs copy is newer than the installed plugin, sync keeps it and tells the agent to update the plugin.
- Custom docs belong in a workspace's `docs/` folder.

## Status report

The status report diagnoses aiOS in an aiOS root and shows its full state.
Agents run the `aios-core:status` skill after setup or a plugin update, when hooks seem not to run, or when files changed outside a session.

- It shows the aiOS root and any nested aiOS roots it skips.
- It shows the settings, including each check's mode.
- It shows the plugin and docs copy versions, and any edited docs copy files.
- It shows when hooks last ran in each agent harness, and the latest blocked turn.
- It runs every check on every file.
- The agent leads with a one-line verdict, then explains each problem and its fix.
- See [onboarding.md](onboarding.md#4-verify-the-hooks) for an example.

## Hook log

The hook log records every hook run in `.aiOS/logs/hook-events.jsonl`.
Agents read it to learn why a turn was blocked or whether a hook ran.

- `start` entries record the docs copy sync result.
- `stop` entries record the decision, the problems found, and the fixes made.
- The plugin reads the log to find the files changed in a turn and to count blocks.
- Setup adds `.aiOS/logs/` to `.gitignore`. The plugin never deletes the log.
- See [logging.md](logging.md) for fields and examples.

## Claude Code and Codex support

The core plugin runs in Claude Code and Codex with the same skills, hooks, and conventions.
Agents in either agent harness read the same contracts and pass the same checks.

- The product repo has one marketplace file for each agent harness. Both list `aios-core`.
- Both agent harnesses run the hooks defined in `hooks/hooks.json`.
- Each agent harness installs and updates its own copy of the core plugin. Updates are manual.
- Codex runs plugin hooks only after the operator approves them. It asks again when `hooks/hooks.json` changes.
- See [onboarding.md](onboarding.md) for installation, hook approval, and updates.

## Planned

- Extension plugins. Each will extend aiOS for one area of capability, such as writing and editing or creative media. An extension plugin may use the core plugin but not another extension plugin.
- A routine that keeps contracts current as their folders change. No check verifies yet that a contract matches its folder.
- Session transcripts. Each Claude Code and Codex transcript will be copied into dated folders and converted to one shared format.
