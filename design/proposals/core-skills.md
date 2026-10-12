---
type: doc
created: 2026-10-10T13:35-07:00
updated: 2026-10-12T10:47-07:00
---

# Proposal: core skills

This proposal records the earlier skill names. Current names are `aios-core:setup-aios` and `aios-core:verify-aios`; see [the rename spec](../specs/setup-maintenance.md).

## Status

Promoted to the [core skills spec](../specs/core-skills.md).

## Idea

The four core skills started as placeholders. Each runs a script or follows a short list, but none defines its purpose, its scenarios, or a complete workflow.

| Skill | Problem today |
|---|---|
| `aios-core:setup` | Builds and extends an aiOS root, but has no workflow for bringing in existing files. Step 4 holds five separate instructions. It calls other skills' scripts by path, such as `<skill>/../check/scripts/check.py`. |
| `aios-core:status` | Runs a script and shows the output. It doesn't interpret results or say what to fix. |
| `aios-core:check` | Runs a script and shows the output. It says to fix problems only when asked, while setup says to resolve them. Hooks already check changed files, so it mostly repeats their work. |
| `aios-core:manage-agents-md` | Four steps with no guidance on inspecting a folder or deciding whether it needs a contract. It can't review a folder tree for outdated contracts. |

The descriptions also mix implementation details with triggers. For example, the check description says "excluding nested aiOS roots" but not when to run a full check.

## Goals

- Each skill has one clear purpose and named scenarios. A skill exists only when it does work no other skill, hook, or script does.
- Each skill runs a complete workflow, from reading the current state to reporting results.
- All core skills share one structure and one writing style.
- Skills call other skills by name, never by script path.

## Sketch

### Three skills, not four

Keep `aios-core:setup`, `aios-core:status`, and `aios-core:manage-agents-md`. Retire `aios-core:check`.

- The stop hook already checks every file changed during a session, including files edited in another tool between turns.
- The status report includes the result of every check on every file. That covers files changed between sessions, such as edits made before a session starts.
- That leaves `aios-core:check` with no work of its own.

Each remaining skill does work no hook or script does on its own.

### Operator scenarios

| Scenario | Skills, in order |
|---|---|
| Set up aiOS from an interview alone | `aios-core:setup`, then `aios-core:status` in a new session |
| Bring existing files, context, skills, or projects into aiOS | `aios-core:setup`, then `aios-core:status` in a new session |
| Add a domain to an existing aiOS root | `aios-core:setup` |
| Add, move, or remove folders | `aios-core:manage-agents-md` |
| Record a preference the operator wants kept | `aios-core:manage-agents-md` |
| Confirm aiOS works after a plugin update | `aios-core:status` |
| Find out why hooks seem silent or a turn was blocked | `aios-core:status` |
| Find problems in files edited between sessions, such as after a Git pull | `aios-core:status` |
| Apply changed check settings to existing files | `aios-core:status` |
| Review the full state of aiOS before committing or sharing | `aios-core:status` |

### `aios-core:setup`

Builds an operator's aiOS root, or adds to an existing one. It has three modes:

| Mode | Starting point | Result |
|---|---|---|
| Start fresh | An empty folder. The interview is the only source of context. | A new aiOS root, written from the [setup example](setup-example.md) |
| Migrate | Files, context, skills, or projects the operator already has | Those sources surveyed, prioritized, and brought into a new or existing aiOS root |
| Extend | An existing aiOS root | New workspaces, and an updated root contract |

`SKILL.md` finds the mode, then sends the agent to one reference file per mode. The agent reads only the workflow it needs.
An existing `.aiOS/config.yaml` means extend. Otherwise, the agent asks whether the operator has existing files to bring in.

#### Start fresh

1. Interview the operator about their domains, recurring work, kinds of files, preferences, and the agent harnesses they use. A reference file holds the questions.
2. Propose the structure as a folder tree with each workspace's purpose. Build nothing until the operator confirms.
3. Run the setup script to create settings, the docs copy, contracts, and glossaries.
4. Write each file's content from the setup example, following its callouts. Add the terms the operator used to the workspace glossaries.
5. Run `aios-core:status` and resolve every file problem it reports.
6. Report what was created. List the next steps: start a new session in each agent harness, approve hooks in Codex, and run `aios-core:status` there.

#### Migrate

Migration builds a self-contained, fully configured aiOS root from what the operator already has. The sources stay untouched.

1. Survey the sources the operator names. Record the folder tree, kinds of files, sizes, instruction files such as `CLAUDE.md`, skills, Git repos, and anything other tools depend on. Use subagents for large sources.
2. Ask which systems, files, and capabilities matter most. Ask what to leave behind and what must stay where it is.
3. Propose a migration plan with the target folder tree. Give each source item one disposition:
   - Copy as is.
   - Copy and add front matter.
   - Restructure it to fit aiOS: split, merge, or rewrite it where that improves it.
   - Leave it out.
4. Build nothing until the operator confirms the plan. If no aiOS root exists, create one with the start fresh steps.
5. Migrate in priority order, one batch at a time. Copy sources; never move or delete them. Skills the operator maintains go into their workspace. Installed skills stay where the agent harness keeps them. Run `aios-core:status` after each batch and resolve its file problems.
6. Carry instructions from `CLAUDE.md` and similar files into contracts. Don't copy `CLAUDE.md` files, since one can stop Claude Code from loading `AGENTS.md`.
7. Report what went where and what was left out. What happens to the sources is the operator's decision.

#### Extend

1. Interview the operator about the new domain.
2. Propose the workspace name and purpose. Build nothing until the operator confirms.
3. Run the setup script to add the workspace and its glossary.
4. Write the workspace's content from the setup example. Add the workspace to the root contract's Contents.
5. Run `aios-core:status` and resolve every file problem it reports.

### `aios-core:status`

Diagnoses aiOS in this aiOS root and reports its full state: settings, versions, hook activity, and file problems.

1. Run the status script. It reports:
   - the aiOS root, and any nested aiOS roots it skips
   - settings: whether checks are on, each check's mode, `include` and `exclude` patterns, `max_blocks`, and the time zone
   - the installed plugin version, the docs copy version, and any edited docs copy files
   - when hooks last ran in each agent harness, and the latest blocked turn with its problems
   - the result of every check on every file
2. Compare each item with the expected state. For each difference, explain the cause and the fix, such as an outdated plugin or Codex hooks that were never approved.
3. Fix file problems in files the current task changed. Ask before fixing anything else.
4. Report a one-line verdict first, such as "Working in Claude Code. Codex hooks have not run here." Follow it with the details by section, then the fixes.

### `aios-core:manage-agents-md`

Keeps each folder's contract true to the folder.

1. Read the contract definition in `.aiOS/docs/types/agents-md.md`.
2. List the folder's files and subfolders. Read enough of each to describe it.
3. Decide whether the folder needs a contract, using the definition's criteria.
4. Write or update the purpose, instructions, skills, and contents.
5. Update the parent contract's Contents.
6. Confirm that every link resolves. The stop hook checks the changed contracts when the turn ends.
7. Report what changed and why.

A review mode would run the same steps across a folder tree and report contracts that no longer match their folders.

### Shared skill structure

Every core `SKILL.md` uses these parts in order:

| Part | What it holds |
|---|---|
| Front matter | `name`, and a `description` that says what the skill does, then "Use when" with its scenarios |
| Title and purpose | The skill's name and one or two sentences on what it achieves |
| When to use | The scenarios, and which skill to use instead for similar requests |
| Workflow | Numbered steps. Each is one action and says how to confirm it worked. |
| Report | What to tell the operator, in order |
| References | Files in `references/` to read for detail, and when to read them |

### Writing style

- Address the agent with direct instructions.
- Use glossary terms and plugin-prefixed skill names.
- Keep implementation details out of descriptions.
- Keep each skill's `SKILL.md` short. Move detail into `references/`.

## Open questions

- Does contract review belong in `aios-core:manage-agents-md`, or in a separate skill?
- Should the checks also cover broken links and folders without contracts?
- Should a skill run plugin updates in both agent harnesses?
- Should the shared skill structure become a shipped doc for operators who write their own skills?
