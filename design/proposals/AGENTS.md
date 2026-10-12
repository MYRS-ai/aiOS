---
type: AGENTS.md
created: 2026-10-10T13:18-07:00
updated: 2026-10-11T11:23-07:00
---

# aiOS proposals

Ideas for the aiOS product, from first sketch to a decision to build or decline them. Together they form the backlog.

## Instructions

### Write a proposal

Name the file for its topic, such as `session-transcripts.md`, and title it `# Proposal: <topic>`.

Use these sections in order. Keep each one short; detail belongs in the spec.

| Section | What it holds |
|---|---|
| Status | `proposed`, `promoted` with a link to the spec, or `declined` with the reason |
| Idea | The problem or opportunity, and the change that addresses it |
| Goals | What the change would achieve |
| Sketch | The approach, the options, and their tradeoffs |
| Open questions | What the operator must answer before the proposal becomes a spec |

### Set priority

The operator sets each proposal's priority: `next`, `soon`, or `later`. Ask when a new proposal has none. Record priority only in the Backlog table below.

### Promote a proposal

1. When the operator decides to build a proposal, create a spec in [../specs/](../specs/AGENTS.md).
2. Set the proposal's status to `promoted` with a link to the spec.
3. Move it from the Backlog to Decided.

## Backlog

| Path | What it proposes | Priority |
|---|---|---|
| [session-transcripts.md](session-transcripts.md) | Copies of Claude Code and Codex transcripts, in dated folders and one shared format | Not set |

## Decided

| Path | What it proposed | Outcome |
|---|---|---|
| [core-skills.md](core-skills.md) | Purpose, scenarios, and workflows for the core skills | Promoted to [specs/core-skills.md](../specs/core-skills.md) |
| [setup-example.md](setup-example.md) | A complete example packaged with the setup skill | Promoted to [specs/setup-example.md](../specs/setup-example.md) |
