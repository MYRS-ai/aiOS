---
name: manage-agents-md
description: Creates, updates, and reviews AGENTS.md contracts, including navigation and skill references. Use when folders or instructions change, a skill is added, renamed, moved, or retired, its invocation conditions change, the operator states a preference to keep, or contracts need review.
---

# Manage AGENTS.md contracts

Keeps each folder's contract true to the folder, so agents find the right instructions and files.

## When to use

- A folder is added, moved, renamed, or removed.
- File changes affect a folder's instructions or navigation.
- A folder's purpose or instructions change.
- A skill is added, renamed, moved, or retired, or its invocation conditions change.
- The operator states a preference that should apply to future work in a folder.
- The operator wants a folder tree checked for outdated contracts.

For related work:

- To add a workspace, use `aios-core:setup-aios`.
- To create or change a skill, use `aios-core:manage-skills`.
- Contracts inside complete examples describe the example's folders.

## Workflow

Before you begin:

- Read the [contract definition](../../docs/types/agents-md.md) first. It defines the contract structure and when a folder needs one.
- Read applicable ancestor contracts before editing, including ancestors outside a nested Git checkout.
- Follow [Maintaining vocabulary](../../docs/glossary.md#maintaining-vocabulary) before introducing or changing concepts in a contract.

Follow [Create a contract](#create-a-contract), [Update a contract](#update-a-contract), or [Review contracts](#review-contracts).

### Create a contract

1. List the folder's contents. Identify applicable instructions and useful navigation for its tasks.
2. Decide whether the folder needs a contract, using the definition's criteria.
3. If a contract is needed:

   1. Write the contract: title, purpose, instructions, skills, and contents.
   2. Add the folder to the parent contract's Contents.
   3. Confirm that every link in both contracts resolves and [check skill references](#skill-reference-checks).

### Update a contract

1. Compare the contract with the folder, checking that:

   - Every listed path exists.
   - Applicable instructions and relevant resources are discoverable through the listed paths.
   - The purpose and instructions still hold.
   - Skill names, paths, and invocation conditions pass [Skill reference checks](#skill-reference-checks).

2. Correct each difference. Record operator preferences alongside the instructions they relate to.
3. If the folder was added, moved, renamed, or removed, update the parent contract's Contents.
4. Confirm that every link resolves.

### Review contracts

1. Find every `AGENTS.md` in the folder tree the operator names. Skip subfolders that have their own `.aiOS/config.yaml`.
2. Compare each contract with its folder, as [Update a contract](#update-a-contract) step 1 describes. Also note folders that need a contract but have none.
3. Propose a fix for each difference. Apply the fixes the operator confirms.

## Skill reference checks

These checks apply to all three workflows.

1. Inspect skill instructions, Skills entries, and navigation in the contract and its applicable ancestors.
2. Compare names, paths, and invocation conditions with each maintained skill's `SKILL.md`. Report a missing package or unknown replacement.
3. Check whether inherited instructions already cover the folder's use. Identify missing or incorrect entries without duplicating inherited guidance.
4. Keep contract corrections in this workflow. Use `aios-core:manage-skills` only for needed package changes within the task's scope. During reviews, record differences before applying approved fixes.

The stop hook checks every changed contract when the turn ends.

## Report

1. Lead with what the contracts now support or the most important review finding and its effect.
2. Explain significant instruction, navigation, or skill-reference changes, with useful links.
3. State unresolved conflicts or decisions and the next action needed.
4. If no changes are needed, state what you checked and why.
