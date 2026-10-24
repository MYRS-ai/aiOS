# Migrate

Builds a configured aiOS from files the operator already has. The sources stay untouched.

## Plan

1. Identify the source locations and intended destination with the operator.
2. Survey both locations:

    - Record their folder structures, file kinds, sizes, instructions, skills, configuration, and dependencies.
    - Distinguish missing content, identical content, conflicts, and partially completed migrations.
    - Identify standalone repositories, linked worktrees, submodules, and symbolic links.
    - Check which destination instructions and conventions apply.

    For large sources, delegate surveys to subagents using these same checks.

3. Interview the operator with [interview.md](interview.md) to establish priorities and exclusions.
4. Draft `plan.md` in a [dedicated migration project](#migration-project), using the [migration-plan template](../assets/templates/migration-plan.md).

    - Read the [example guide](example.md) and relevant files before proposing the destination structure.
    - Maintain one source-to-destination map across batches, with actions: copy, transform, reuse, defer, or omit.
    - Record deferred dependencies without assuming their future destinations. Link detailed file mappings from this map.
    - Group files receiving the same treatment; list exceptions separately.
    - Order batches by priority and record conflict resolutions.
    - Record source and destination state for comparison when resuming, such as file hashes or snapshot references.
    - Record how to recover existing destination content before changing it.

    Transform content only when adapting its format or structure makes it fit aiOS or easier to use.

5. Ask whether the operator wants a pilot to validate the strategy before committing to the full migration.

    - If accepted, agree on a sample, a representative task, and success criteria.
    - Record the pilot as the first batch, with a review before the remaining batches.

6. Confirm the plan with the operator before creating or changing migration content.

## Migration project

Create or reuse a dedicated project under the relevant workspace's `projects/`, such as `projects/aios-migration/`.
Follow the destination's project conventions and keep migrated content in its intended destinations.

| Path | Purpose |
|---|---|
| `AGENTS.md` | Project instructions and navigation |
| `plan.md` | Scope, migration map, decisions, progress, and remaining dependencies |
| `batches/<batch-name>/` | File mappings, copy records, inventories, prepared content, and verification evidence |

- Keep migration working files in this project, rather than the workspace's general `docs/` folder.
- Use `aios-core:manage-agents-md` to create the project contract and update its parent navigation.
- Link batch files from the plan so another session can resume the work.

## Migrate a batch

Repeat these steps for each batch, including when resuming interrupted work.

1. Reconcile the plan with the current sources and destination.

    - Check for changes since planning or the last completed work.
    - Confirm previously verified work still matches; existing output alone does not establish completion.
    - Resolve changed or unrecorded destination content as a conflict and update the plan before writing.

2. Configure aiOS if the destination lacks it, using steps 2 and 3 of [start-fresh.md](start-fresh.md).
3. Copy or adapt the batch's content according to the plan. For regular files, follow [Import files](import-files.md).

    - Never move or delete sources.
    - Capture source timestamps before copying, following [Migration timestamps](../../../docs/frontmatter.md#migration-timestamps).
    - Preserve source dates and add `migrated` to eligible documents; leave skill packages and other front matter standards unchanged.
    - Restore source modification times after migration edits so the fixer preserves the imported `updated` values.
    - Choose a copy method suited to each repository's structure; preserve required history, local changes, and working files.
    - Keep destination Git metadata independent of the source before running commands that can modify it.
    - Recreate symbolic links deliberately and record retained external dependencies.
    - Carry instructions from `CLAUDE.md` and `AGENTS.md` into contracts, preserving their scope.
    - Replace `CLAUDE.md` with `AGENTS.md` in the destination. Claude Code v2.1.277+ supports [loading `AGENTS.md` directly](https://code.claude.com/docs/en/memory#agentsmd); no `CLAUDE.md` routing file with `@AGENTS.md` is needed.
    - Place operator-maintained skills using the [skill definition](../../../docs/types/skill-md.md#where-skills-live).
    - Leave installed skills where the agent harness keeps them.
    - Update folder contracts with `aios-core:manage-agents-md`.
    - Record progress in the plan as work completes.

4. Complete [Review references](#review-references), including references in previously migrated content.
5. Run [Verify a batch](#verify-a-batch) before marking items verified.

    - Record the results and unresolved gaps.
    - Update the recorded source and destination state for the next comparison.

6. Report the batch's destinations, changes, omissions, and remaining work.

    For a pilot:

    - Review the representative task's result with the operator before continuing to the remaining batches.
    - Update the plan with any agreed adjustments.

## Review references

1. Search the batch and destination content for incoming and outgoing references. Include applicable ancestor contracts and related repositories within the agreed scope.

    - Search old paths, project names, relative paths, and known aliases in links, prose, scripts, and configuration.
    - Review matches in context; search results are candidates, not instructions to replace every match.

2. Classify each reference against the migration map:

    | Reference | Treatment |
    |---|---|
    | Navigation or operational path to migrated content | Update to the verified destination; recalculate relative paths from the referring file |
    | Dependency not yet migrated | Keep its working path and record when to revisit it |
    | Historical citation or migration record | Preserve the original path as evidence |
    | Ambiguous target or conflicting copies | Resolve before replacing; record unresolved items |

3. Apply reviewed changes only in destination content. Preserve sources and use `aios-core:manage-agents-md` for contract edits.
4. Confirm each changed reference reaches the intended resource, including any heading anchor. Existing paths can still point to obsolete copies.
5. Repeat the search. Account for retained old paths, record verification, and carry unresolved dependencies into the next batch.

## Verify a batch

- Compare unchanged copies with their sources.
- Confirm imported timestamps match the captured metadata and survive the fixer; record migration times for exempt files separately.
- Review transformed content for preserved meaning, instructions, and relevant history.
- Confirm reference review covered incoming links, outgoing links, and retained dependencies. Record search scope and any verification limits.
- Confirm destination Git operations do not depend on source metadata.
- For an agreed pilot, run the representative task against its success criteria.
- Run `aios-core:verify-aios` for the affected scopes and resolve file problems before the next batch.

## Finish

1. Review the [adaptation checks](example.md#review-the-adapted-result), then return to the setup workflow for final verification.
2. Reconcile the work record before declaring completion.

    - Every required item must be migrated or reused and verified.
    - Account for deferred and omitted items separately.
    - Leave the sources untouched; their eventual disposition is the operator's decision.
