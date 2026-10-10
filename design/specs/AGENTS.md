---
type: AGENTS.md
created: 2026-10-10T13:18-07:00
updated: 2026-10-10T15:25-07:00
---

# aiOS specs

Decided product work, detailed enough for a subagent to implement and test it without further design.

## Instructions

### Write a spec

Name the file for its topic and title it `# Spec: <topic>`. Link the proposal it came from, if any.
Use these sections in order:

| Section | What it holds |
|---|---|
| Status | `draft`, `ready`, `in progress`, or `done`, and what remains |
| Goal | The outcome and why it matters |
| Scope | What the work includes and excludes |
| Requirements | Numbered statements, each one testable |
| Design | The files, behavior, and interfaces to change |
| Test plan | The tests to add or run, with commands |
| Tasks | Ordered steps. Each is one bounded action a subagent can finish and verify. |
| Done when | The checks that prove the work is complete |
| Open questions | Questions that block the work |

### Start from a ready spec

A spec is `ready` when it has no open questions and every requirement has a test or check.
Brief subagents from a ready spec. Start implementation only from a ready spec.

### Close a spec

When the work ships, record its settled design in [decisions.md](../decisions.md) and set the status to `done`.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [core-skills.md](core-skills.md) | Redesign of the core skills and the `SKILL.md` file type | Implementing or reviewing the core skills |
| [v1-release.md](v1-release.md) | Scope, requirements, and release check for aiOS 1.0 | Preparing the first stable public release |
