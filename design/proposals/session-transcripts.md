---
type: doc
created: 2026-10-10T13:18-07:00
updated: 2026-10-10T13:18-07:00
---

# Proposal: session transcripts

## Status

Proposed. Nothing is built.

## Idea

The core plugin copies each Claude Code and Codex session transcript into the aiOS root. It files the copies in dated folders and converts both into one shared format.
Agents and the operator can then find a session by date and read sessions from either agent harness with one parser.

### What each agent harness stores

Checked on 2026-10-10.

| Agent harness | Location | Format |
|---|---|---|
| Claude Code | `~/.claude/projects/<folder slug>/<session ID>.jsonl` | One JSON object per line with `type`, `sessionId`, `timestamp`, and `cwd`. Conversation entries add `message`. Subagent entries set `isSidechain`. |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-<start time>-<session ID>.jsonl` | One JSON object per line with `timestamp`, `type`, and `payload`. Types include `session_meta`, `turn_context`, `response_item`, and `event_msg`. |

Neither format is verified as stable. Plan for both to change.
Sizes vary widely. One Claude Code transcript reached 14 MB. Codex stored 884 MB of sessions in ten days across all projects.

## Goals

- Keep a copy of every session that runs in an aiOS root, independent of each agent harness's own storage.
- File copies by date so a session can be found by when it happened.
- Read Claude Code and Codex sessions with one format.

## Sketch

### Capture

- The stop hook copies the current session's transcript at the end of each turn. A session that ends without a clean exit still has a current copy.
- The hook appends only the lines added since the last copy, so large transcripts stay fast to capture.
- The hook finds the transcript from the `transcript_path` field in its input.
- Capture runs only inside an aiOS root, like checks. A setting in `.aiOS/config.yaml` turns it on or off.

### Layout

```
.aiOS/logs/
├── hook-events.jsonl
└── sessions/
    └── 2026-10-10/
        ├── claude-code-<session ID>.jsonl
        ├── codex-<session ID>.jsonl
        └── raw/
            ├── claude-code-<session ID>.jsonl
            └── codex-<session ID>.jsonl
```

- The folder date is the session's start date in the configured time zone. A session that continues on later days stays in its start folder.
- `raw/` holds exact copies. The converted files sit beside it.

### Shared format

Each line of a converted file is one JSON object.

| Field | Meaning |
|---|---|
| `time` | Local time with UTC offset, as in the hook log |
| `harness` | `claude-code` or `codex` |
| `session` | Session ID |
| `turn` | Turn number within the session |
| `agent` | `main`, or the subagent's ID |
| `role` | `operator`, `agent`, or `tool` |
| `kind` | `message`, `tool-call`, or `tool-result` |
| `text` | Message text or tool output |
| `tool` | Tool name, for tool calls and results |
| `input` | Tool input, for tool calls |

- The converter reads only raw copies. When an agent harness changes its format, update the converter and regenerate the converted files.
- Fields that only one agent harness records stay in the raw copy.

### Privacy and retention

- Transcripts hold everything in a session, including pasted secrets and personal details.
- Setup already excludes `.aiOS/logs/` from Git, so transcripts stay on the operator's computer.
- Nothing deletes transcripts automatically, as with the hook log.

### Glossary changes

- Add "Transcript": the record of one session, as the agent harness wrote it or converted to the shared format.
- Widen "Log" to cover everything the hooks write in `.aiOS/logs/`, or keep it for hook runs only.

## Open questions

- Does Codex's hook input include `transcript_path`? If not, the hook finds the rollout file by session ID.
- Should subagent sessions get their own files or stay inside the main session's file?
- Should an operator be able to exclude a workspace, such as one with sensitive work?
- Does any transcript content need redaction before it is copied?
- Should the converter also record reasoning summaries, where an agent harness provides them?
