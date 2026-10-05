---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-04T13:57-07:00
---

# Front matter

Agents write only `type` in Markdown front matter outside skill folders. Hooks add `created` and `updated` timestamps.

| File | Fields agents write | Fields hooks write |
|---|---|---|
| `SKILL.md` | `name`, `description`, following the Agent Skills format | None |
| Other files inside a skill folder | None required | None |
| All other Markdown files | `type: AGENTS.md` or `type: doc` | `created`, `updated` |

Allowed types come from the `default` rule's `allowed: type` list in the core plugin's `hooks/checks/checks.yaml`.
An operator can override the rules in `.aiOS/config.yaml`. See [checks.md](checks.md) for settings.
The [types folder](types/AGENTS.md) holds the available type definitions.

`created` records when the file was first written and never changes afterward.
`updated` records its last content change. The hook fills in timestamps when the turn can end.

The default time zone is `America/Los_Angeles`. Operators can change the front matter check's `zone` setting.
Timestamps use ISO 8601 with minutes and the UTC offset, such as `2026-10-03T13:21-07:00`.
The default offset changes between -07:00 and -08:00 with daylight saving time.
