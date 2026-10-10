---
name: status
description: Reports the full state of aiOS in this aiOS root, including settings, plugin and docs copy versions, hook activity in each agent harness, and problems in any file. Use after setup or a plugin update, when hooks seem not to run or a turn was blocked, after files change outside a session, or before committing.
---

# Status

Diagnoses aiOS in the current aiOS root and explains what to fix.

## When to use

- After setup, in a new session in each agent harness, to confirm the hooks run
- After a plugin update
- When hooks seem not to run, or a turn was blocked
- After files change outside a session, such as edits in another app or a Git pull
- After a change to `.aiOS/config.yaml`, to see how existing files meet the new settings
- Before committing or sharing the aiOS root

To find contracts that no longer match their folders, use `aios-core:manage-agents-md` instead.

## Workflow

1. From the operator's current folder, run `python3 <skill>/scripts/status.py`, where `<skill>` is this skill's folder. If it reports that the folder is not set up, offer `aios-core:setup` and stop.
2. Compare each section of the output with the expected state below. Note every difference.
3. For each difference, find the cause and the fix.
4. Fix file problems in files the current task changed. Ask before fixing other files. Run the script again to confirm the fixes.

| Section | Expected state | When it differs |
|---|---|---|
| Settings | `Checks: on` | Checks are off in `.aiOS/config.yaml`. Confirm with the operator that this is intended. |
| Versions | The docs copy matches the installed plugin | Start a new session so the start hook syncs the docs copy. If the copy is newer, update the plugin in this agent harness, as `.aiOS/docs/onboarding.md` describes. |
| Versions | `Edited docs copy files: none` | The next sync replaces these edits. Move any change worth keeping into a workspace's `docs/` folder first. |
| Hooks | A recent run in each agent harness the operator uses | In Codex, approve the hooks, as `.aiOS/docs/onboarding.md` describes. Otherwise, confirm the plugin is installed at user scope in that agent harness. "never ran here" is expected for an agent harness the operator doesn't use. |
| Hooks | `Latest blocked turn: none`, or problems since fixed | Explain the listed problems. The Files section shows whether they remain. |
| Files | `Problems: 0` | Each line names the check, the file, and the fix. Lines marked `(warning)` come from checks in `warn` mode. |

The hooks fill in timestamps when the turn ends, so don't write them.

## Report

1. A one-line verdict, such as "Working in Claude Code. Codex hooks have not run here."
2. Each difference, with its cause and fix, the most serious first.
3. What you fixed, and what needs the operator's decision.
4. The script's output, so the operator sees the full configuration.
