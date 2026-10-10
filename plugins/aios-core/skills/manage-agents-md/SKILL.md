---
name: manage-agents-md
description: Creates, updates, and reviews AGENTS.md contracts so each one matches its folder, and keeps the parent contract's links current. Use when a folder is added, moved, renamed, or removed, when its purpose or instructions change, when the operator states a preference to keep, or to find outdated contracts.
---

# Manage AGENTS.md contracts

Keeps each folder's contract true to the folder, so agents find the right instructions and files.

## When to use

- A folder is added, moved, renamed, or removed.
- Files are added to or removed from a folder whose contract lists them.
- A folder's purpose or instructions change.
- The operator states a preference that should apply to future work in a folder.
- The operator wants a folder tree checked for outdated contracts.

To add a workspace, use `aios-core:setup`. To create or change a skill, use `aios-core:manage-skills`. Skill folders don't get contracts.

## Workflow

Read `.aiOS/docs/types/agents-md.md` in the aiOS root first. It defines the contract structure and when a folder needs one. Then follow the mode that fits.

### Create

1. List the folder's files and subfolders. Read enough of each to describe it in a few words.
2. Decide whether the folder needs a contract, using the definition's criteria. If it doesn't, confirm that the parent contract covers it, and stop.
3. Write the contract: title, purpose, instructions, skills, and contents.
4. Add the folder to the parent contract's Contents.
5. Confirm that every link in both contracts resolves.

### Update

1. Compare the contract with the folder. Every listed path exists, every file and subfolder is listed, and the purpose and instructions still hold.
2. Correct each difference. Record an operator preference as an instruction under its own heading.
3. If the folder was added, moved, renamed, or removed, update the parent contract's Contents.
4. Confirm that every link resolves.

### Review

1. Find every `AGENTS.md` in the folder tree the operator names. Skip nested aiOS roots.
2. Compare each contract with its folder, as Update step 1 describes. Also note folders that need a contract but have none. Change nothing yet.
3. Propose a fix for each difference. Apply the fixes the operator confirms.

The stop hook checks every changed contract when the turn ends.

## Report

1. Each contract created or changed, and what changed in it.
2. Anything left unresolved, such as two contracts that conflict, with the question the operator needs to answer.

For a review, report the differences and proposed fixes before changing anything.
