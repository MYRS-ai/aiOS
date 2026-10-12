---
name: verify-aios
description: Verifies aiOS settings, plugin and docs copy versions, hook activity, and files, then explains problems and their fixes. Use after setup, plugin updates, configuration changes, or edits outside a session; when hooks fail or block a turn; or before committing.
---

# Verify aiOS

Verifies the operator's aiOS, diagnoses problems, and explains what to fix.

## When to use

- After setup, in a new session in each agent harness, to confirm the hooks run
- After a plugin update
- When hooks seem not to run, or a turn was blocked
- After files change outside a session, such as edits in another app or a Git pull
- After a change to `.aiOS/config.yaml`, to see how existing files meet the new settings
- Before committing, to check all files in scope

To create aiOS, bring existing files into it, or add a workspace, use `aios-core:setup-aios`.

## Workflow

1. From the operator's current folder, run:

   ```bash
   python3 <skill>/scripts/status.py
   ```

   `<skill>` is this skill's folder.

   - If the folder is not set up, offer `aios-core:setup-aios` and stop.
   - A configuration error exits with a nonzero status. Explain the error and correct settings within the authorized scope before retrying. File checks have not run in that case.

   Add `--last-block` only when investigating a blocked turn or when the operator requests history. Compare historical failures with current checks; excluded files remain unverified.

2. Compare each section of the output with the expected state below. Note every difference.
3. For each difference, find the cause and the fix.
4. Fix file problems in files the current task changed. Ask before fixing other files.
5. Run the script again to confirm the fixes.

| Section | Expected state | When it differs |
|---|---|---|
| Settings | `Checks: on` | Checks are off in `.aiOS/config.yaml`. Confirm with the operator that this is intended. |
| Versions | The docs copy matches the installed plugin | Start a new session so the start hook syncs the docs copy. If the copy is newer, update the plugin in this agent harness, as `.aiOS/docs/onboarding.md` describes. |
| Versions | `Edited docs copy files: none` | The next sync replaces these edits. Move any change worth keeping into a workspace's `docs/` folder first. |
| Hooks | A recent run in each agent harness the operator uses | In Codex, approve the hooks, as `.aiOS/docs/onboarding.md` describes. Otherwise, confirm the plugin is installed at user scope in that agent harness. "never ran here" is expected for an agent harness the operator doesn't use. |
| Files | `Problems: 0` | Each line names the check, the file, and the fix. Lines marked `(warning)` come from checks in `warn` mode. |

The hooks fill in timestamps when the turn ends, so don't write them.

## Report

1. Lead with the verification result and its scope. If checks could not run, say what prevented them.
2. Explain findings by impact, with supporting evidence, known causes, and fixes.
3. State any decision or action still needed and how to confirm resolution.

Limit conclusions to checks that ran and hook activity confirmed in the operator's agent harnesses.
Keep routine reports focused on current findings. Omit historical failures unless they explain the problem being investigated.
Keep clean results brief. Include script output only when requested or needed to support a finding.
