---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-12T10:31-07:00
---

# Front matter

Agents write only `type` in Markdown front matter outside skill folders. The front matter fixer adds `created` and `updated` timestamps.

| File | Fields agents write | Fields the fixer writes |
|---|---|---|
| `SKILL.md` | `name`, `description`, following the Agent Skills format | None |
| Other files inside a skill folder | None required | None |
| All other Markdown files | `type: AGENTS.md` or `type: doc` | `created`, `updated` |

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
