---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-24T10:28-07:00
---

# Front matter

For new Markdown files outside skill folders, agents write only `type`. The front matter fixer adds `created` and `updated` timestamps.
For imported files, follow [Migration timestamps](#migration-timestamps).

| File | Fields agents write | Fields the fixer writes |
|---|---|---|
| `SKILL.md` | `name`, `description`, following the Agent Skills format | None |
| Other files inside a skill folder | None required | None |
| New aiOS documents and contracts | `type: AGENTS.md` or `type: doc` | `created`, `updated` |
| Imported aiOS documents and contracts | `type`, source `created` and `updated`, and `migrated` | Maintains `updated` after later edits |

Allowed types come from the `default` rule's `allowed: type` list in the core plugin's `hooks/checks/checks.yaml`. An operator can override the rules in `.aiOS/config.yaml`. See [checks.md](checks.md) for settings.

The [types folder](types/AGENTS.md) holds the type definitions, including the [`SKILL.md` definition](types/skill-md.md).

## Field syntax

- Required fields belong at the top level. Fields inside `metadata:` do not satisfy these requirements.
- Quoted values and inline comments are supported, so `type: "doc" # Notes` has the value `doc`.
- Skill names and descriptions must be nonempty strings. Numbers, booleans, and nested fields do not qualify.
- Use single-line values. Multiline strings, anchors, and aliases are unsupported and produce syntax diagnostics.

Parsing preserves the original field lines. Timestamp updates preserve existing `created` fields and the document body.

## Timestamps

The stop hook runs the front matter fixer when the turn can end.
Setup uses the same fixer for newly created files, including when no earlier hook session exists.
Both use the configured rules, scope, and time zone. Setup leaves existing files and the docs copy unchanged.

The fields record:

- `created` records when the file was first written and never changes afterward.
- `updated` records its last content change.

The default time zone is `America/Los_Angeles`. Operators can change the front matter check's `zone` setting. Timestamps use ISO 8601 with minutes and the UTC offset, such as `2026-10-03T13:21-07:00`. The default offset changes between -07:00 and -08:00 with daylight saving time.

## Migration timestamps

For imported aiOS documents and contracts, migration preserves source dates and adds `migrated` to record the import time.

1. Capture source timestamps before copying or editing:

    - Use the filesystem creation time for `created` and modification time for `updated`.
    - Do not use Unix `ctime` as creation time; it records metadata changes.
    - If creation time is unavailable, resolve that date before importing.
    - Record the source values in the migration record. Never substitute today's date for missing history.

2. Write the captured `created` and `updated` values in the destination front matter.
3. Set `migrated` to the import time, using the same time zone and timestamp format.
4. Restore the source modification time on the destination after migration edits.
5. Run the fixer explicitly on the imported files and confirm all three fields remain unchanged.
6. Run full file checks; restored modification times can exclude imports from the hook's changed-file selection.

- Keep `migrated` unchanged during later edits. The fixer continues maintaining `updated` normally.
- Preserve separate research dates and source attribution in the document body.
- Exempt skill packages and files governed by another front matter standard.
- Configure matching rules or exclusions for other standards before running aiOS checks or fixers.
- For exempt files and formats without front matter, record the migration time in the migration plan instead.
