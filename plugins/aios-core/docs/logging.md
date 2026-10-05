---
type: doc
created: 2026-10-03T16:45-07:00
updated: 2026-10-04T14:09-07:00
---

# Hook logs

The aios-core hooks write one log per aiOS root at `.aiOS/logs/hook-events.jsonl`. Each line is a JSON object.

## Events and outcomes

| Event | When it is logged |
|---|---|
| `start` | A session starts |
| `stop` | A turn ends and the hook runs |

A `stop` entry records one of three decisions:

- `block`: checks failed and the agent must continue working.
- `allow`: the turn can end. Any listed problems remain unresolved.
- `skip`: checks did not run. Either no earlier entry exists for this session, so checking starts next turn, or `enabled` is `false`. The `reason` field says which.

## Fields

| Field | Present on | Meaning |
|---|---|---|
| `time` | All entries | Local time with UTC offset, to the millisecond |
| `harness` | All entries | The agent harness that ran the hook: `claude-code` or `codex` |
| `session` | All entries | Session ID used to separate concurrent sessions |
| `event` | All entries | `start` or `stop` |
| `cwd` | `start` | Folder where the session started |
| `docs` | `start` | Sync result with `action` and installed plugin `version`; errors also include `message` |
| `decision` | `stop` | `block`, `allow`, or `skip` |
| `reason` | `skip` | Why the hook skipped checks |
| `checked` | `block`, `allow` | Number of files checked |
| `problems` | `block`, `allow` | Failures, each with `check`, `path`, and `message`; warning-only checks add `"mode": "warn"` |
| `fixed` | `block`, `allow` | Changes made by fixers, each with `check` and `path` |

The `docs.action` values are `copied`, `replaced`, `unchanged`, `kept-newer`, and `error`.
If the plugin version cannot be read, an error uses `version: "unknown"`.
The hook records `start` after sync, including when checks are off.

Example of a start entry's sync result:

```json
{"docs": {"action": "copied", "version": "0.9.0"}}
```

Example of a blocked turn:

```json
{"time": "2026-10-03T17:27:46.585-07:00", "harness": "claude-code", "session": "q1", "event": "stop", "decision": "block", "checked": 2, "problems": [{"check": "frontmatter", "path": "y.md", "message": "type 'memo' is not allowed (type is one of: AGENTS.md, doc). Rule: default"}], "fixed": []}
```

## How the log tracks turns

The plugin reads entries for the current session. Its last entry other than `block` marks the turn's start. The plugin checks only files changed after that entry.

Later `block` entries count toward `max_blocks`. The count resets each turn.

## Retention

Logs are not deleted automatically. You can delete `.aiOS/logs/`; the plugin recreates it. Setup adds `.aiOS/logs/` to the folder's `.gitignore`.
