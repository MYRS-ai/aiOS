---
type: AGENTS.md
created: 2026-10-03T13:21-07:00
updated: 2026-10-11T14:17-07:00
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

### Agree on vocabulary before propagation

1. For a new concept, changed meaning, or replacement name, record its meaning, related concepts, and representative sentences in the design record.
2. After the operator agrees, update the glossary and current uses together, following [Maintaining vocabulary](../plugins/aios-core/docs/glossary.md#maintaining-vocabulary).

### Keep operator instructions out

Put instructions for operators and their agents in the [core plugin docs](../plugins/aios-core/docs/AGENTS.md).

### Maintain the context visualization

The context visualization shows intended reading paths, not observed agent activity.
After source changes, review its scenario definitions and evidence, then run:

```bash
python3 design/agent-context-flow.py
python3 design/agent-context-flow.py --check
```

Run these commands from the product repository. Rebuilding requires Python-Markdown; the saved HTML and freshness check work without it.
Keep the visualization offline and preserve the distinction between reading instructions, references, and program access.

## Contents

| Path | What it holds | Read when |
|---|---|---|
| [proposals/](proposals/AGENTS.md) | Ideas for the product, which form the backlog | Suggesting, reviewing, or prioritizing an idea |
| [research/](research/AGENTS.md) | Tests and findings behind proposals and specs | Examining evidence for a design |
| [specs/](specs/AGENTS.md) | Decided work, detailed for implementation and testing | Implementing, testing, or planning decided work |
| [decisions.md](decisions.md) | Settled product decisions | Checking what the product has decided |
| [agent-context-flow.html](agent-context-flow.html) | Interactive context map, scenario traces, and rendered file previews | Inspecting reading conditions and possible gaps |
| [agent-context-flow.json](agent-context-flow.json) | Reviewed scenario definitions, semantic connections, and findings with source evidence | Revising the context model after instructions change |
| [agent-context-flow.py](agent-context-flow.py) | Builds the standalone visualization and checks source freshness | Regenerating the visualization or changing source extraction |
| [agent-context-flow.template.html](agent-context-flow.template.html) | Offline interface used by the generator | Changing the visualization's layout or interactions |
