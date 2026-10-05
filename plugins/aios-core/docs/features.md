---
type: doc
created: 2026-10-04T09:55-07:00
updated: 2026-10-04T19:11-07:00
---

# Features

aiOS uses contracts, skills, and plugins to guide agents working for an operator.
The core plugin currently provides guided setup, docs sync, checks, timestamps, and hook logs in Claude Code and Codex.

| Feature | What it does | Status |
|---|---|---|
| [Domains and shared](#domains-and-shared) | Separates files for different areas of work | Guided setup implemented |
| [Folder contracts](#folder-contracts) | Gives agents folder instructions and links to relevant files | Definition and write-contract skill available |
| [Glossary](glossary.md) | Gives each term one meaning | Available; grows as terms arise |
| [Decision log](#decision-log) | Records settled product design | Available in the product repo |
| [Typed files](frontmatter.md) | Identifies file types and records changes | Checks and timestamps work; type definitions incomplete |
| [Convention checks](hooks.md) | Checks changed Markdown files at the end of each turn | Implemented |
| [Docs copy](hooks.md) | Syncs core plugin docs at session start and warns about edits | Implemented |
| [Status](onboarding.md#4-verify-the-hooks) | Reports docs version and hook history | Implemented |
| [Hook log](logging.md) | Records hook runs, problems, and fixes | Implemented |
| [The same marketplace in both agent harnesses](#the-same-marketplace-in-both-agent-harnesses) | Installs the core plugin in Claude Code and Codex | Core plugin installable; extension plugins remain drafts |

## Domains and shared

Each domain is one of the operator's areas of work. Its workspace keeps its files and context together.
Agents choose a domain by whose work the request concerns. They ask when that is unclear.
The `shared/` workspace holds resources that more than one domain uses, such as standards and CLIs.
Operators choose their own domains and workspace names. Shared is not a domain.

The setup skill interviews the operator and creates workspace contracts, settings, and a copy of the core plugin docs.

## Folder contracts

A folder's `AGENTS.md` is its contract. It states the purpose, instructions, and links to relevant files and folders.
Agents follow those links to find what a task needs without reading unrelated files.
The [contract definition](types/agents-md.md) describes the structure and when a folder needs a contract.

aiOS uses `AGENTS.md` for instructions. Tests found that `CLAUDE.md` files could prevent Claude Code from loading `AGENTS.md`.
Those tests describe the tested version; they do not establish behavior for every release.
The write-contract skill guides contract updates and parent navigation.
No check yet verifies that a contract matches its folder.

## Decision log

The product repo's `design/decisions.md` records settled product design. Other design docs hold proposals and research.
Design records are for product development and do not ship inside the core plugin.

## Typed files and checks

Markdown files outside skill folders start with `type: AGENTS.md` or `type: doc`.
Only `AGENTS.md` has a type definition so far. Operators can extend front matter rules in `.aiOS/config.yaml`.
Hooks fill in timestamps using the configured time zone; agents never write them.

The `frontmatter` check checks required fields and allowed values.
The `names` check checks lowercase folder names with one to four words separated by hyphens.
A failed blocking check stops the turn and tells the agent what to fix.
After the configured block limit, remaining failures become warnings. The default limit is two blocks per turn.

Checks run only where the plugin finds `.aiOS/config.yaml` above or at the session folder.
The [onboarding guide](onboarding.md) explains setup and Codex hook approval.

## Hook log

The core plugin records each hook run in `.aiOS/logs/hook-events.jsonl`.
Entries identify the agent harness, session, event, and time. End-of-turn entries record the decision, problems, and fixes.
The plugin uses the log to select changed files and count blocks within a turn.
Setup adds the log folder to `.gitignore`. See [logging.md](logging.md) for fields and retention.

## The same marketplace in both agent harnesses

The product repo has separate marketplace files for Claude Code and Codex. Both list `aios-core`.
Each agent harness installs its own copy of the same core plugin.

Extension plugins remain drafts without manifests. Each will extend aiOS for one capability, such as writing or creative media.
An extension plugin may use the core plugin but should not depend on another extension plugin.

## Planned

- A routine that keeps contracts current as their folders change.
- Logging beyond hook runs.
