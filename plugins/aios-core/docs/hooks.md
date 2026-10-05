---
type: doc
created: 2026-10-03T17:23-07:00
updated: 2026-10-04T14:09-07:00
---

# Hooks

The core plugin's hooks check file conventions and fill in timestamps at the end of each turn. Claude Code and Codex share the hook definitions in `hooks/hooks.json` inside the installed core plugin. Both hooks run `hooks/hooks.py`, which does the work described below.

## Enable checks for a folder

Install the plugin at user scope, then use the setup skill in the folder to check. Setup creates `.aiOS/config.yaml`. The plugin searches upward from the session folder for that file and exits if none exists.

Codex also requires hook approval. See [onboarding.md](onboarding.md) for installation and approval steps.

## What happens each turn

At session start, `hooks.py` syncs the plugin's `docs/` into `.aiOS/docs/`, then writes the `start` log entry.
Sync runs even when checks are off. Copied files precede the turn and are not treated as edits.

The `.aiOS/docs/.sync.json` file records the plugin version and a SHA-256 hash.
The hash covers sorted relative paths and file bytes, ignoring `.DS_Store` and `__pycache__`.
Versions are compared numerically, so `0.10.0` is newer than `0.9.0`.

| Copy state | Action |
|---|---|
| Missing | Copy the plugin docs |
| Older version | Replace the copy |
| Same version, different source hash | Replace the copy |
| Same version and source hash | Leave the copy unchanged |
| Newer version | Keep the copy and tell the agent to update this agent harness's plugin |

Sync builds a complete temporary sibling folder before replacing the copy.
If replacement fails, it restores the previous folder. Sync errors are logged and do not prevent session start.
See [logging.md](logging.md) for the `docs` field.

At the end of a turn, `hooks.py`:

1. Finds changed Markdown files and files in `.aiOS/docs/`, subject to configured include and exclude patterns.
   It skips hidden folders outside the root's `.aiOS/` and the docs copy.
   It also skips subfolders holding their own `.aiOS/config.yaml`.
2. Runs checks in the order listed in `hooks/checks/checks.yaml`.
3. Blocks the turn if a check in `block` mode fails and the block limit has not been reached.
4. Runs fixers when the turn can end. The `frontmatter` fixer fills in `created` and `updated` where required.
5. Logs the result in `.aiOS/logs/hook-events.jsonl`.

A blocked agent receives the failures and continues working. After `max_blocks` blocks in one turn (default 2), unresolved failures become warnings and the turn ends.

## Available checks

| Check | What it checks | Default mode |
|---|---|---|
| `frontmatter` | Required fields, allowed values, and Agent Skills format; uses the first matching rule | `block` |
| `names` | Folder names are lowercase, hyphenated, and one to four words | `block` |
| `docs-copy` | Edits to `.aiOS/docs/` since the last sync | `warn` |

File names are not checked. For front matter requirements by file type, see [frontmatter.md](frontmatter.md).

## Configure checks

Edit `.aiOS/config.yaml` in the aiOS root being checked. Setup copies the plugin defaults into it. Omitted check settings use defaults from `hooks/checks/checks.yaml`.

| Setting | Purpose |
|---|---|
| `enabled` | `false` turns checks off and tells the agent at session start |
| `include`, `exclude` | Path patterns relative to the aiOS root |
| `max_blocks` | Maximum blocks per turn before failures become warnings |
| `checks.<name>` | Settings for one check, such as `mode`, `exclude`, or front matter rules |

Each check supports `mode: block`, `mode: warn`, or `mode: off`. An `exclude` under one check applies only to that check. For example, `exclude: ["**/media/**"]` skips media folders for that check.

See [the checks guide](checks.md) for all options and rule examples.

## Limits and troubleshooting

- Subagents run no hooks of their own. The main agent checks their changed files when its turn ends.
- Concurrent sessions check every file changed during their own turn, including another session's edits. Either session can block on those files.
- A missing or crashed hook script allows the turn to end.
- Codex asks for approval again when `hooks.json` changes.
- Logs record hook runs and explain blocked turns. See [logging.md](logging.md).

## Add a check

Follow the steps in [the checks guide](checks.md#add-or-change-a-check). Adding a check leaves `hooks.json` unchanged, so Codex does not require new approval.
