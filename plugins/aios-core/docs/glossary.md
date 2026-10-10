---
type: doc
created: 2026-10-03T13:21-07:00
updated: 2026-10-10T15:35-07:00
---

# Glossary

This is the aiOS glossary. Each term below has one meaning in every workspace.
Use each term exactly as written here. Don't use the words listed under "Don't say."
See [naming.md](naming.md) for how to write names, such as aiOS and skill names.

## Workspace glossaries

Workspace glossaries hold the operator's own terms.

- `shared/docs/glossary.md` holds terms that more than one workspace uses.
- Each workspace's `docs/glossary.md` holds terms for that workspace.
- Read the glossaries in this order: aiOS, shared, then the current workspace.
- A workspace glossary adds terms. It never redefines a term in the aiOS glossary. Choose a different term instead.
- Add a new term to the workspace glossary where it applies. Only core plugin updates change the aiOS glossary.

## Organization

| Term | Meaning | Don't say |
|---|---|---|
| aiOS | The AI operating system: contracts, skills, and plugins that guide AI agents working on the operator's behalf | AI-OS, AI OS, AIOS, the OS repo |
| aiOS glossary | The core plugin's `docs/glossary.md`, which defines aiOS terms for every workspace. Agents read the copy at `.aiOS/docs/glossary.md`. | Global glossary, product glossary |
| aiOS root | The folder that holds `.aiOS/`, along with everything inside it. The hooks act only inside an aiOS root. | Tree, project |
| Contract | A folder's `AGENTS.md` file. It says what the folder is for, what agents must follow there, and where to go next. | Index, router, map, README |
| Domain | One of the operator's areas of work. Each has its own workspace. | Area, context |
| Operator | The person aiOS serves, who also manages and maintains it. | User, owner |
| Shared | The shared workspace, `shared/`, which holds what more than one domain uses. It is not a domain. | Common, global |
| Workspace | A top-level folder in the aiOS root for one domain or for shared resources | Area, space |
| Workspace glossary | A workspace's `docs/glossary.md`, which adds terms for that workspace. The shared workspace's glossary holds terms that more than one workspace uses. | Local glossary, domain glossary |

## Files

| Term | Meaning | Don't say |
|---|---|---|
| Convention | A format requirement for files or folders, such as front matter or folder names. Checks enforce conventions. | Rule, policy, standard |
| Docs copy | The copy of the core plugin docs in an aiOS root's `.aiOS/docs/`. The start hook replaces it when the plugin changes, so agents never edit it. | Synced docs, docs mirror |
| Draft | Work that hasn't been validated. Files in a `drafts/` folder are drafts, and neither agent harness loads them. | Prototype, WIP |
| Front matter | The fields between `---` lines at the top of a Markdown file. Write it as two words. `frontmatter` is only the name of the check and its files. | Frontmatter, header, metadata |
| Placeholder | A file that names its intended content but doesn't have it yet | Stub, skeleton |
| Standard | A file of quality criteria that skills apply, such as `shared/standards/writing.md` | Convention, guideline, rule |
| Type | The `type` field in front matter, which names what kind of file it is. Each type has a definition in the core plugin's `docs/types/` folder. | Kind, category, doc type |

## Agents, skills, and plugins

| Term | Meaning | Don't say |
|---|---|---|
| Agent | The AI doing the work in a session inside an agent harness, such as Claude in Claude Code | Model, assistant, bot |
| Agent harness | The software that runs an agent and loads its instructions, tools, skills, plugins, and hooks: Claude Code and Codex are currently supported in aiOS | App, client, platform |
| Agent role | A file that defines a kind of subagent: when to use it, its instructions, and optionally its persona, model, reasoning effort, and tools | Agent definition, agent file, persona |
| Agent surface | Where a person interacts with an agent, such as a CLI, a desktop app, an IDE or browser extension, or a chat app like Slack. One agent harness can run behind many agent surfaces. | Surface, product, client, interface |
| CLI | A command-line program that more than one skill uses, kept in `shared/clis/` | Tool, utility, script |
| Core plugin | `aios-core`, the plugin with the foundation of aiOS: system-level skills and hooks | Base plugin |
| Extension plugin | A plugin that extends aiOS for one area of capability, such as writing and editing, creative media, or product design. It may use the core plugin but not another extension plugin. | Domain plugin, add-on |
| Main agent | The agent the operator talks to. It coordinates the work and briefs subagents. | Orchestrator, parent agent |
| Marketplace | The catalog that Claude Code and Codex use to install aiOS plugins | Registry, store |
| Plugin | A package of skills, agent roles, and hooks that Claude Code and Codex install | Add-on, package |
| Reference | A file a skill reads for detail when it needs it, kept in the skill's `references/` folder | Doc, resource |
| Script | A program a skill runs, kept in the skill's `scripts/` folder | Tool, helper, command |
| Session | One conversation with an agent, from start to finish | Chat, thread |
| Skill | A folder with a `SKILL.md` that teaches an agent one capability, in the Agent Skills format. It can hold its own scripts, references, and assets. | Command, prompt, ability |
| Skill package | A skill's folder: its `SKILL.md` and the scripts, references, and assets it uses. [types/skill-md.md](types/skill-md.md) defines it. | Skill bundle, skill directory |
| Subagent | An agent the main agent starts for one delegated task | Worker, child agent |
| Template | A file copied to start a new one, kept in a skill's `assets/` folder | Boilerplate, scaffold |
| Tool | An action an agent harness gives its agent, such as Read, Write, or Bash | Command, function |
| Turn | One request from the operator and the agent's full response to it | Exchange, step |

## Work

| Term | Meaning | Don't say |
|---|---|---|
| Context | Background information about a domain, kept in its `context/` folder. For the information an agent holds during a session, say "context window." | Background, knowledge base |
| Journal | Dated records of events, notes, and decisions | Log, diary |
| Project | Work with a defined goal and an end | Initiative, effort |
| Routine | Work that repeats on a schedule. Each routine runs a workflow. | Recurring task, job, cron |
| Workflow | A procedure that reaches a goal using skills, context, and subagents | Process, playbook, pipeline |

## Enforcement

| Term | Meaning | Don't say |
|---|---|---|
| Block | What the hook does when a check fails: it stops the turn from ending and gives the agent the problems to fix. Checks fail; the hook blocks the turn. | Reject |
| Check | A test the hooks run on files changed during a turn, such as `frontmatter` or `names` | Validator, lint, rule |
| Hook | A command an agent harness runs when a session starts or a turn ends. The core plugin's hooks run `hooks/hooks.py`. | Trigger, runner |
| Log | The record of hook runs in `.aiOS/logs/hook-events.jsonl` | Journal, history |
| Rule | A named entry in the `frontmatter` check's settings that sets what a matching file needs. Use "rule" only in this sense. | Policy, convention |
| Timestamps | The `created` and `updated` fields in front matter. The hooks fill them in, so agents never write them. | Stamps, dates |
