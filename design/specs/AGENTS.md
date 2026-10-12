---
type: AGENTS.md
created: 2026-10-10T13:18-07:00
updated: 2026-10-12T14:04-07:00
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

A spec is `ready` when it has no open questions and every requirement has a test or check. Brief subagents from a ready spec. Start implementation only from a ready spec.

### Close a spec

1. When the work ships, record its settled design in [decisions.md](../decisions.md) and set the status to `done`.
2. Review other active specs for dependencies and open questions that the shipped work resolves.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [agent-context-flow.md](agent-context-flow.md) | Interactive reading map, scenarios, source previews, and context gaps | Building or validating the context visualization |
| [consistency-fixes.md](consistency-fixes.md) | Approved check corrections and documentation reconciliation | Implementing or reviewing the repository audit fixes |
| [core-skills.md](core-skills.md) | Redesign of the core skills and the `SKILL.md` file type | Implementing or reviewing the core skills |
| [plugin-releases.md](plugin-releases.md) | Pre-1.0 release, change history, local refresh, and publication checks | Preparing the plugin update and maintaining release history |
| [setup-example.md](setup-example.md) | Complete fictional aiOS and adaptation guidance inside the setup skill | Implementing or reviewing the setup reference |
| [setup-maintenance.md](setup-maintenance.md) | Shared timestamp initialization, template names, and maintenance prerequisites | Implementing or reviewing setup consistency changes |
| [setup-templates.md](setup-templates.md) | Starter templates grouped separately from the complete example | Moving or validating setup template paths |
| [skill-display-names.md](skill-display-names.md) | Explicit Codex display names for the core skills | Changing or validating skill display metadata |
| [skill-reporting.md](skill-reporting.md) | Outcome, context, and action guidance for shipped skill reports | Revising or validating reporting behavior |
| [type-guidance.md](type-guidance.md) | Type definitions aligned with current packages, maintenance, and reporting | Reviewing the approved documentation refinements |
| [v1-release.md](v1-release.md) | Scope, requirements, and release check for aiOS 1.0 | Preparing the first stable public release |
| [verification-history.md](verification-history.md) | Current verification results separated from historical blocked turns | Changing diagnostic output or troubleshooting guidance |
| [vocabulary.md](vocabulary.md) | Agreed meanings and consistent vocabulary across current product files | Implementing or reviewing the vocabulary changes |
