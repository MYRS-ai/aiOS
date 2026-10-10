---
type: AGENTS.md
created: 2026-10-03T13:21-07:00
updated: 2026-10-10T13:18-07:00
---

# aiOS design records

Design records for the aiOS product: research, proposals, specs, and settled decisions. They guide product development and do not ship in any plugin.

## Instructions

### Move work from idea to decision

1. Research records tests and findings that inform a design.
2. A proposal describes an idea. Proposals form the backlog, and the operator sets their priority.
3. When the operator decides to build a proposal, promote it to a spec. A spec gives a subagent enough detail to implement and test the work.
4. When the spec's work ships, record its settled design in [decisions.md](decisions.md).

Read `decisions.md` before relying on a proposal or spec. Only `decisions.md` records settled design.

### Keep operator instructions out

Put instructions for operators and their agents in the [core plugin docs](../plugins/aios-core/docs/AGENTS.md).

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [proposals/](proposals/AGENTS.md) | Ideas for the product, which form the backlog | Suggesting, reviewing, or prioritizing an idea |
| [research/](research/AGENTS.md) | Tests and findings behind proposals and specs | Examining evidence for a design |
| [specs/](specs/AGENTS.md) | Decided work, detailed for implementation and testing | Implementing, testing, or planning decided work |
| [decisions.md](decisions.md) | Settled product decisions | Checking what the product has decided |
