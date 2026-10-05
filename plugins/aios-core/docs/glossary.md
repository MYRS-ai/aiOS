---
type: doc
created: 2026-10-03T13:21-07:00
updated: 2026-10-04T13:57-07:00
---

# Glossary

Each term below has one meaning across aiOS. Use the term exactly as written here, and don't swap in the words listed under "Don't say." When a new term comes up, add it here before using it in other files.

## Organization

| Term | Meaning | Don't say |
|---|---|---|
| aiOS | The AI operating system: contracts, skills, and plugins that guide AI agents working on the operator's behalf | AI-OS, AI OS, AIOS, the OS repo |
| aiOS root | The folder that holds `.aiOS/`, along with everything inside it. The hooks act only inside an aiOS root. | Tree, project |
| Contract | A folder's `AGENTS.md` file. It says what the folder is for, what agents must follow there, and where to go next. | Index, router, map, README |
| Domain | One of the operator's areas of work. Each has its own workspace. | Area, context |
| Operator | The person aiOS serves, who also manages and maintains it. | User, owner |
| Shared | The shared workspace, `shared/`, which holds what more than one domain uses. It is not a domain. | Common, global |
| Workspace | A top-level folder in the aiOS root for one domain or for shared resources | Area, space |

Use `aiOS` in prose and display names, such as the plugin display name aiOS Core. Plugin and marketplace identifiers use lowercase `aios`, such as `aios-core`, to follow the plugin naming convention. The `.aiOS/` folder keeps the display spelling.

## Files

| Term | Meaning | Don't say |
|---|---|---|
| Convention | A format requirement for files or folders, such as front matter or folder names. Checks enforce conventions. | Rule, policy, standard |
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
