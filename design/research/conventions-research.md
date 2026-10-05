---
type: doc
created: 2026-10-03T14:13-07:00
updated: 2026-10-04T19:11-07:00
---

# Conventions research

Research and tests from 2026-10-03 on storing conventions, loading them into an agent's context window, and checking whether files follow them.

This document compares proposals and records lab results. Read [decisions.md](../decisions.md) for settled design and [hooks.md](../../plugins/aios-core/docs/hooks.md) for the implemented checks.

The proposed approach combines folder instructions, requirements by file type, and automated checks. The lab tested how Claude Code and Codex load instructions and whether hooks catch missed requirements.

## What a convention needs

Skills, instruction files, schemas, and hooks handle different parts of a convention. Evaluate each proposal against three questions.

| Job | Question it answers | Examples |
|---|---|---|
| Storage | Where is the convention defined? | AGENTS.md, a conventions doc, a skill, a schema, the check script |
| Loading | When does the agent read the convention? | At startup, when a file is read, when a skill is picked, at the moment of a write |
| Enforcement | What catches a violation? | Nothing, a review, a hook, a pre-commit check, a test |

Conventions can apply by location or file type.

- Location covers the aiOS root, a domain, a project, or a folder. Nested `AGENTS.md` files support this scope.
- File type covers every file of a kind, regardless of location. The `type` front matter field could identify these files.

## When instructions load

### Claude Code 2.1.286

Startup loading covers the session's start folder and every folder above it. The table distinguishes fresh-session tests from documentation claims.

| Mechanism | Loads | Tested |
|---|---|---|
| AGENTS.md at or above the start folder | At startup | Yes |
| AGENTS.md below the start folder | When the agent reads a file in that folder. Every level in between loads too | Yes |
| `.claude/rules/*.md` without `paths` | At startup | Yes |
| `.claude/rules/*.md` with `paths` globs | When the agent reads a matching file | Yes |
| `sub/.claude/rules/*.md` | When the agent reads a file in `sub/` | Yes |
| Any on-read mechanism, when the agent creates a file without reading first | Never. The docs say Write triggers path rules; the test showed it did not | Yes |
| General-purpose subagents | Same startup and on-read loading as the main session | Yes |
| Explore and Plan subagents | Skip AGENTS.md | Docs only |
| Skills with `paths` | When a matching file is read | Docs only |

Claude Code requires Read before Edit or overwrite, so those operations load rules for existing files. Creating a new file without reading first can miss the rules.

### Codex 0.159.3

Startup loading was tested. Other behavior below comes from documentation unless a test is named.

- It loads `AGENTS.md` from the project root to the start folder. `project_root_markers` identifies the root; its default is `.git`. In `<workspace>/projects/alpha` without a marker, only alpha's `AGENTS.md` loaded. Adding `.ai-os-root` at the root and setting `project_root_markers=[".ai-os-root"]` loaded the full chain.
- In the test configuration, `~/.codex/AGENTS.md` was a symlink to `~/AGENTS.md`, so Codex loaded the operator's instructions.
- It does not automatically load `AGENTS.md` below the start folder. Its system prompt tells the model to look for these files. In tests, it did.
- It has no rules scoped by path patterns. Its `.codex/` folder holds `config.toml`, `hooks.json`, and `rules/` for command permissions. It selects skills in `.agents/skills/` by description.
- Project `.codex/` settings load only for trusted projects. Each hook also needs its own trust (`/hooks`), recorded against the hook's hash.
- Hook matchers filter by tool name only. File writes arrive as `apply_patch` with the patch text in `tool_input.command`.
- Combined AGENTS.md size cap is 32 KiB.

## Options for storing, loading, and enforcing conventions

### Store conventions

| # | Option | Strengths | Weaknesses |
|---|---|---|---|
| H1 | Inline in the folder's AGENTS.md | Loads natively by folder in both tools. No separate file lookup | Adds context on every load. Applies by location only |
| H2 | Separate convention docs, pointed to from AGENTS.md (HumanLayer `agent_docs/`, Pocock `docs/agents/`, Addy `references/`) | Keeps contracts short. One canonical copy | Depends on the agent following the pointer |
| H3 | Hidden per-folder `.rules/` (v1) | Separates conventions from navigation | Hidden and indirect. AGENTS.md now does the folder job natively |
| H4 | `.claude/rules/` with `paths` globs | Applies by path pattern. Tested | Claude only. Hidden folder. Misses new files |
| H5 | Skills (template in `assets/`, checks in `scripts/`) | Portable standard. Carries procedure, template, and scripts together. `paths` in Claude | Chosen by description, so not reliable for conventions that always apply. Adds to the skill list |
| H6 | Type contract: one entry per `type` holding guidance, template, and schema | One place answers "what must a file of this type look like". Check selects the schema by `type` | New structure to design |
| H7 | Machine schema per type (JSON Schema; mdschema or document-schema for sections and token budgets) | Precise. A template can be generated from it | Tooling is young (mdschema, document-schema) |
| H8 | The check script itself (Addy's `skill-lint.js`: exemptions live in the check so they can't be bypassed) | The convention and its enforcement are one thing | Prose must point to it |
| H9 | Decision log or ADRs (MADR has a "Confirmation" field linking a decision to its check) | Records why. Prevents re-arguing | Not delivered to agents by default |
| H10 | One source that generates each tool's files (rulesync, ruler, ai-rulez) | Multi-tool consistency. rulesync simulates scope for tools that lack it | Build step. Generated files must not be hand-edited |
| H11 | Rule packs with `applies_when` (Every) | Rules cited by ID in reviews | Experimental. Plugin-specific |

### Load conventions

| # | Option | Reaches new-file creation? | Codex |
|---|---|---|---|
| D1 | Startup: AGENTS.md chain, unscoped `.claude/rules` | Yes, if the instruction is at or above the start folder | Yes, once a root marker exists |
| D2 | On read, by folder: nested AGENTS.md | No | Model must choose to look |
| D3 | On read, by glob: `.claude/rules` or skill `paths` | No | No |
| D4 | By description: skills | Sometimes | Yes |
| D5 | Manual: `/skill`, `$skill` | If invoked | Yes |
| D6 | Brief: the main agent writes instructions into the subagent prompt | If the main agent remembers | Yes |
| D7 | At the write, via hook (block with a reason, or add context) | Yes | Yes, hooks exist |
| D8 | Via the check's error message, at the moment of a violation | Yes, after the fact | Through hooks or pre-commit |
| D9 | SessionStart hook that injects text | Yes | Yes |

### Enforce conventions

| # | Option | Catches |
|---|---|---|
| E1 | None (advisory) | Nothing |
| E2 | Review: a reviewer agent, a critique skill, or the operator | Instructions requiring judgment, when run |
| E3 | Correct by construction: a `new` script or template the agent must use (plop, copier; Templater for Obsidian) | File format at creation |
| E4 | Write-time hook: PreToolUse blocks, or PostToolUse validates and reports | Agent writes in Claude Code and Codex |
| E5 | Stop hook: the turn can't end until checks pass | Everything the agent touched that turn |
| E6 | Pre-commit running the same check script | Every edit, including Obsidian, Codex, and manual. Needs git |
| E7 | Periodic check of the whole aiOS root | Accumulated convention failures |
| E8 | Permission deny rules on paths | Writes to protected files |
| E9 | Clean-session tests: marker tests for delivery, scenario tests graded by the check; `claude plugin eval` once things are plugins | Whether agents receive and follow instructions |

## Proposed design

### Choose where each convention belongs

Use a routing table to choose where a convention is stored and how it reaches the agent. The proposed capture skill would use the same table.

| Convention | Store in | Load through | Check with |
|---|---|---|---|
| Needs no judgment, such as format, names, or timestamps | Check script | Error message after a violation | Hook and pre-commit |
| Applies everywhere and needs judgment | One line in root `AGENTS.md` | Startup instructions | Review |
| Applies to one folder or project | That folder's `AGENTS.md` | Nested folder instructions | Review, plus a script for mechanical checks |
| Applies to a file type anywhere | Requirements for that `type` | Write hook and a pointer from root | Check script selected by `type` |
| Describes a procedure | Skill | Description or explicit invocation | The skill's checks |
| Explains a decision | `decisions.md` | Read when conventions change | No automated check proposed |

### Define requirements by file type

Each `type` would have one definition with guidance, a template, and a schema. This document calls that definition a "type contract". For example, `type: AGENTS.md` could specify required sections and a size limit.

The check would apply the matching schema alongside the base fields, `type`, `created`, and `updated`. Nested `AGENTS.md` files would add folder requirements without repeating their parents.

### Automate mechanical checks

One check script would support hooks, pre-commit, and checks of the whole aiOS root. Agents would not type timestamps.

The Stop hook prototype checks files changed during a turn, blocks on failures, and fills in timestamps on a pass. It catches shell writes that hooks on Write or Edit miss. See [the lab results](#lab-results).

HumanLayer's guidance is "Never send an LLM to do a linter's job".

### Test whether instructions reach the agent

Rerun fresh-session marker tests when folder instructions change. Scenario tests should cover instructions the model cannot infer, following Every's guidance, and use the check to grade results.

Keep startup instructions short. IFScale and ManyIFEval found that instruction-following degrades as instruction count grows. An ETH study found AGENTS.md files rarely improve task success and add over 20% cost unless they contain non-inferable requirements.

## Example of the proposed workflow

Suppose an agent starts in `<aiOS root>/` and is asked to add a note in `<workspace>/context/`. This example includes proposed pre-commit checks and scenario tests.

1. Load `~/AGENTS.md` and `<aiOS root>/AGENTS.md`. The root describes front matter requirements, where types are defined, and the end-of-turn check.
2. Follow the root pointer and read `<workspace>/AGENTS.md` and `<workspace>/context/AGENTS.md`. Create `<workspace>/context/budget.md` with any tool, including Bash.
3. Check changed files with the Stop hook. Failures block the turn with a reason for the agent to fix. A pass fills in `created` and `updated`.
4. Run the same script at pre-commit to catch edits made in Obsidian, Codex, or by hand.
5. Run the "add a context note" scenario in a fresh session whenever conventions change.

## Implementation strategies

| | A. Portable minimum | B. Layered | C. Skill-centric | D. Generated single source |
|---|---|---|---|---|
| Storage | AGENTS.md cascade, type docs pointed to from root, check script | A plus type contracts with templates and schemas | Each type contract is a skill (template in `assets/`, checks in `scripts/`) | One source folder generates AGENTS.md sections, `.claude/rules`, and Codex files |
| Loading | Startup and pointers | Plus write-time hooks | Skill descriptions, `paths` in Claude, hooks that say "use skill X" | Whatever each tool supports |
| Enforcement | Pre-commit | Hook, pre-commit, fresh-session tests | Skill scripts, hook, pre-commit | Per tool |
| Covers new files | No | Yes | Partly | Depends |
| Codex support in proposal | Equal | Hooks need porting | Good | Good |
| Cost | Low | Medium | Medium to high | High |
| Shareable as plugins | Weak | Medium | Strong | Strong |

The research recommends strategy B, built in steps:

1. Build the check script and timestamp hook; timestamp requirements are already settled.
2. Define type contracts, starting with `type: AGENTS.md`.
3. Load the needed instructions when an agent creates a file.
4. Add tests.

A skill could later package a type contract, allowing a move toward strategy C.

## Open design questions

1. Decide whether both tools must load the same parent instructions. Codex needs a root marker, configured through `project_root_markers` in `~/.codex/config.toml` or created by `git init`.
2. Decide Git repository boundaries. Pre-commit requires repositories; one repository per domain remains an option.
3. Choose how to check manual and Obsidian edits, which do not run agent hooks. Options include pre-commit and Obsidian Linter's timestamp rule. The latter uses local time, which is Pacific on the test machine.
4. Choose a term that distinguishes aiOS conventions from `.claude/rules` and Codex's `.rules` command-permission files.
5. Decide whether file types need line or token limits, such as a cap on the root `AGENTS.md`. A type contract and check script could enforce them.
6. Decide whether to use `.claude/rules` with `paths` under strategy B. It loads type rules on read with little setup, but misses new files and works only in Claude Code.

## Lab results

The lab at `<lab folder>/` copies the domain folder structure. Each instruction file contains a unique marker word. Every run used a fresh headless session. Paths and operator details are generalized.

### Nested Claude Code rules

- One root `.claude/rules/` covers the whole aiOS root. Globs cascade: reading `<workspace>/context/note.md` loaded both the `<workspace>/**` and the `<workspace>/context/**` rules.
- Reading any AGENTS.md loaded the `**/AGENTS.md` rule. Type-scoped rules work.
- A subfolder's own `.claude/rules/` also works. It loaded on read, or at startup when the session started in that folder. All matching rules stack. None overrides another.
- A session started in `<workspace>/projects/alpha` loaded every ancestor AGENTS.md and the root's unscoped rule at startup. It did not load path-scoped root rules until a read.

### Following a file-creation request

The prompt was "Create <workspace>/context/budget-N.md with a one-line note". The root instruction required front matter with `type`. The folder instruction required ending with `Owner: the operator`.

| Tool | Runs | Read the contracts first | Followed both instructions | How it read | How it wrote |
|---|---|---|---|---|---|
| Claude | 3 | 3 | 3 | Bash `cat`, so automatic loading never fired | Bash heredoc in 2 of 3 runs, Write in 1 |
| Codex | 3 | 3 | 3 | Shell `cat` | `apply_patch` |

Both tools followed the root `AGENTS.md` pointer without a reminder. These few runs do not establish reliability in larger tasks. A hook watching only Write and Edit would have missed 2 of 3 Claude writes.

### End-of-turn check prototype

A SessionStart hook records the start time. A Stop hook checks every `.md` file changed since that time. Failure returns `{"decision": "block", "reason": ...}` so the agent can fix the problem. Success fills in `created` and `updated` in Pacific time. Allowed `type` values appeared only in the script.

| Run | First `type` written | Blocked | Fixed by | Final |
|---|---|---|---|---|
| Claude 1 | `meeting-note` | Yes | Bash `sed` | `context`, stamped |
| Claude 2 | `context` | No | n/a | Stamped |
| Codex 3 | `note` | Yes | `apply_patch` | `context`, stamped |
| Codex 4 | `context` | No | n/a | Stamped |

- Same script and output format in both tools. Codex needed the project trusted and the hook trusted. The test used `-c` and `--dangerously-bypass-hook-trust` for one run each.
- Some runs passed by copying a neighbor. Runs 2 and 4 picked a valid type, likely from the file the previous run had left beside them.
- A check enforces form, not meaning. A kickoff note in a project folder passed as `context`, which is valid but arguably wrong. Error messages should say what each type is for.

### Where hook settings load

The test placed hook settings at the root, then started sessions there and in `<workspace>/projects/alpha`.

| Tool | Started at root | Started in a subfolder |
|---|---|---|
| Claude, project `.claude/settings.json` at root | Fires | Does not fire, with or without git |
| Codex, project `.codex/hooks.json` at root | Fires | Fires only with a root marker (`project_root_markers`) |

Claude project hooks come only from the start folder. To cover every start folder, register the hook at user level (`~/.claude/settings.json`) or through a plugin enabled at user scope. The script then exits at once for paths outside the aiOS root.

### Shared plugin test

The prototype included both manifests, a runner, one file per check, and `checks.toml`. Its shared `hooks/hooks.json` used `${CLAUDE_PLUGIN_ROOT}`, which Codex also sets for compatibility.

Claude loaded the plugin with `--plugin-dir`. Codex installed it from a local marketplace into a separate test home folder. The prototype used `.ai-os-root` to enable checks; the implemented plugin uses `.aiOS/config.yaml`.

| Start folder | Claude | Codex |
|---|---|---|
| aiOS root | Fired. Blocked `type: note`, agent fixed it, stamped | Same |
| `<workspace>/projects/alpha` | Fired. Blocked once, fixed, stamped | Fired with no root marker. Blocked twice (no front matter, then `type: note`), fixed, stamped |
| A folder with no `.ai-os-root` | Fired, runner exited, file untouched | Same |

- One `hooks.json` serves both tools. Neither needs hook config in any project folder.
- Plugin hooks fire from any start folder in both tools. This fixes the Claude problem with project hooks.
- The `.ai-os-root` marker works as the on switch for each aiOS root.
- The Codex subfolder run never saw the root AGENTS.md, because there was no root marker, so it skipped front matter entirely. The hook caught it anyway.
- Every run guessed `type: note` first, because the allowed types were written only in the check. Listing them where agents read would save one blocked round per run.
- Codex copies an installed plugin into its cache. Edits to the source need a reinstall or upgrade.
- Claude reads a plugin from a marketplace added as a local folder directly from that folder, per the docs. Edits apply at the next session or after `/reload-plugins`. People installing from a hosted marketplace get a cached copy.
- Claude reads project `.claude/settings.json` only from the folder where the session starts, per the docs. "To use a file committed at the repository root, start Claude Code there." Project-scope plugin installs are limited the same way. That is why the plugin is installed at user scope and gated by a marker.
- Untested in this lab: a Claude marketplace install (only `--plugin-dir` was tested), and Codex's one-time hook approval through `/hooks` (tests used `--dangerously-bypass-hook-trust`). Both were later confirmed during development: marketplace installs in Claude Code and Codex, and hook approval in the Codex app.

## Sources

- [Claude Code memory, rules, imports, instruction-file setting](https://code.claude.com/docs/en/memory)
- [Skills front matter (`paths`, `disable-model-invocation`)](https://code.claude.com/docs/en/skills)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Best practices ("Would removing this cause Claude to make mistakes?")](https://code.claude.com/docs/en/best-practices)
- [Plugin evals](https://code.claude.com/docs/en/plugin-evals)
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Codex AGENTS.md, skills, hooks, rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [AGENTS.md specification](https://agents.md) and [open proposals](https://github.com/agentsmd/agents.md/issues)
- [Cursor rules](https://cursor.com/docs/context/rules)
- [Copilot instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- [Kiro steering](https://kiro.dev/docs/steering/)
- [rulesync](https://rulesync.dyoshikawa.com/reference/file-formats)
- [ruler](https://github.com/intellectronica/ruler)
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [Every compound-engineering packs](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/guides/packs.md)
- [HumanLayer, Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [IFScale](https://arxiv.org/abs/2507.11538)
- [Evaluating AGENTS.md (ETH)](https://arxiv.org/abs/2602.11988)
- [mdschema](https://github.com/jackchuka/mdschema)
- [document-schema](https://document-schema.org/)
- [ls-lint](https://ls-lint.org)
- [MADR](https://adr.github.io/madr/)
