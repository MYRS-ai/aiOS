---
name: setup
description: Guides an operator through creating or extending an aiOS root with workspaces, contracts, settings, and docs. Use when setting up or initializing aiOS.
---

# Setup

1. Interview the operator about their areas of work, file types, and preferences. Each area becomes a workspace.
2. Propose workspace names with one to four lowercase words separated by hyphens. Reserve `shared` for resources used across domains. Confirm names and purposes before building.
3. Run `python3 <skill>/scripts/setup.py [folder] --workspace NAME="PURPOSE"` with each confirmed workspace. Repeat `--workspace` for each. `<skill>` is this skill's folder; `folder` defaults to the current folder.
4. Review the output and skipped files with the operator. The script adds missing pieces and preserves existing files. It appends the log exclusion to `.gitignore`. Add confirmed preferences and file guidance to the contracts. Update existing root Contents for any added workspaces, following `.aiOS/docs/types/agents-md.md`.
5. Run `python3 <skill>/../check/scripts/check.py` from the aiOS root and resolve problems.
6. Ask the operator to start a new session and finish a turn in each agent harness they use. Run `python3 <skill>/../status/scripts/status.py` there to confirm hooks ran and the docs copy matches. If hooks have not run, report verification as pending.
7. Remind the operator to approve hooks in Codex and update the plugin manually in each agent harness. Read `.aiOS/docs/onboarding.md` for those steps.
