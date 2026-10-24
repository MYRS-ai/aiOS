---
type: doc
created: 2026-10-03T13:21-07:00
updated: 2026-10-24T10:01-07:00
---

# Glossary

Agreed aiOS concepts, grouped by topic. Terms are alphabetical within each group; each term has one definition.

Use the section index to browse, or search this file for a term.

Ordinary domain meanings, quotations, identifiers, and external product names keep their wording.

## Find a term

| Section | Covers |
|---|---|
| [Organization](#organization) | The system, people, workspaces, and glossaries |
| [Files](#files) | File formats, quality criteria, and readiness |
| [Agents and sessions](#agents-and-sessions) | Who does the work and where interactions happen |
| [Skills and tools](#skills-and-tools) | Capabilities and the resources they use |
| [Plugins](#plugins) | Packaging and distribution |
| [Work](#work) | Context, projects, and recurring work |
| [Enforcement](#enforcement) | Checks, hooks, and their records |

For guidance, see [Using the glossary](#using-the-glossary) and [Maintaining vocabulary](#maintaining-vocabulary). [Retired wording](#retired-wording) explains previous names.

## Organization

| Term | Meaning | Notes |
|---|---|---|
| **aiOS** | The AI operating system. Its contracts, skills, and plugins guide AI agents working on the operator's behalf. | Say "your aiOS" for the operator's configured system and work. For locations, name the folder containing `.aiOS/config.yaml`. Example: "Set up aiOS in this folder." |
| **aiOS glossary** | The agreed definitions of aiOS concepts, maintained with the core plugin and used across workspaces. | A workspace glossary adds terms for the operator's domains. |
| **Contract** | A folder's `AGENTS.md`. It states the folder's purpose, instructions, and where agents should go next. | A README introduces a product or folder. A contract directs agents working there. |
| **Domain** | One of the operator's areas of work. | A workspace is the folder supporting a domain or shared resources. Example domains: teaching and personal life. |
| **Operator** | The person aiOS serves, who also manages and maintains it. | Use for the person's relationship with aiOS. A product's users and a file's owner retain those meanings. |
| **Shared** | The workspace for resources used across domains. | Shared is a workspace, not a domain. Example: writing criteria used across domains. |
| **Workspace** | A top-level folder for one domain or shared resources in the operator's aiOS. | A domain is an area of work. Example: Teaching is a domain. `teaching/` is its workspace. |
| **Workspace glossary** | The agreed terms used in a workspace, recorded in its `docs/glossary.md`. | The aiOS glossary defines system concepts. The shared glossary holds terms used across workspaces. |

## Files

| Term | Meaning | Notes |
|---|---|---|
| **Convention** | A format requirement for files or folders, such as required front matter or folder names. | A standard defines quality criteria. Checks test some conventions. Example: lowercase, hyphenated folder names. |
| **Docs copy** | The core plugin docs copied into `.aiOS/docs/` so agents can read them from a predictable location. | Plugin docs are the source; workspace docs hold the operator's documentation. See [sync behavior](hooks.md) and [plugin updates](onboarding.md). |
| **Draft** | Work that is not ready for its intended use and still needs development or validation. | A placeholder reserves space for missing content. Example: unfinished skill instructions are a draft; an empty skill folder is a placeholder. |
| **Front matter** | Structured fields between `---` lines at the start of a Markdown file. | Headings belong to the document body; metadata is a broader category. See [field requirements](frontmatter.md). |
| **Placeholder** | A file or folder that identifies intended content without providing it yet. | A draft contains work under development. Example: a standards folder with only a contract describing future standards. |
| **Standard** | Quality criteria used to judge work. | A convention specifies file or folder format. A file records the criteria; the criteria are the standard. Example: require concrete verbs. |
| **Type** | A classification of files with a shared purpose and requirements. | The `type` field records a classification; filenames identify others, such as `SKILL.md`. See [built-in definitions](types/AGENTS.md) and [custom type settings](frontmatter.md). |

## Agents and sessions

| Term | Meaning | Notes |
|---|---|---|
| **Agent** | The AI acting on instructions and using tools to do work within an agent harness. | A model supplies capabilities; the agent uses them during work. |
| **Agent harness** | Software that runs an agent and provides its instructions, tools, skills, plugins, and hooks. | The agent surface is where a person interacts. aiOS supports Claude Code and Codex. |
| **Agent role** | A file defining a kind of subagent, including when to use it and the instructions it follows. | The role describes how a subagent should work; the subagent performs the delegated task. |
| **Agent surface** | The interface through which a person interacts with an agent. | One harness can support several surfaces, such as a desktop app and a CLI. |
| **Main agent** | The agent the operator talks to. It coordinates work and briefs subagents. | The parent agent delegated a particular task. A subagent can also be a parent agent. |
| **Session** | One conversation with an agent, from start to finish. | Each request and the agent's full response is a turn within the session. |
| **Subagent** | An agent another agent starts for a delegated task. | Delegation can have several levels. The delegating agent need not be the main agent. |
| **Turn** | One request from the operator and the agent's full response to it. | A session can contain many turns. Tool calls and delegated work can occur within a turn. |

## Skills and tools

| Term | Meaning | Notes |
|---|---|---|
| **CLI** | A command-line interface. | Example: the Codex CLI lets the operator interact with an agent from a terminal. |
| **Reference** | Supporting material a skill consults when it needs more detail. | A template supplies a starting form; a reference supplies information. |
| **Script** | A program run to carry out a task. | A tool is an action that may run a script. Skills can run setup scripts; hooks can run checking scripts. |
| **Skill** | Instructions teaching an agent one capability, written in `SKILL.md` using the Agent Skills format. | The skill package contains these instructions and their supporting files. |
| **Skill package** | A skill's folder, containing its `SKILL.md` and any scripts, references, or assets it uses. | See [package structure and placement](types/skill-md.md). |
| **Template** | A reusable starting form copied to create a new file. | A placeholder marks missing content; a template provides structure for producing content. |
| **Tool** | An action an agent harness exposes to an agent, such as reading a file or running a command. | A tool can invoke a script, which is a program. |

## Plugins

| Term | Meaning | Notes |
|---|---|---|
| **Core plugin** | `aios-core`, the plugin providing the foundation of aiOS through system-level skills, hooks, and docs. |  |
| **Extension plugin** | An aiOS plugin that adds capabilities in an area such as writing, creative media, or product design. | Groups capabilities. A domain identifies an area of the operator's work. |
| **Marketplace** | A catalog an agent harness uses to find and install plugins. |  |
| **Plugin** | An installable package that adds capabilities to an agent harness. | Can contain skills, agent roles, or hooks. It does not need all three. |

## Work

| Term | Meaning | Notes |
|---|---|---|
| **Context** | Information relevant to work, including instructions, background material, and results. | Qualify as domain or session context when needed. A context window limits how much information a model can use at once. |
| **Journal** | Dated records of events, notes, and decisions. | The hook log records automated hook activity. |
| **Project** | Work with a defined goal and an end. | A domain continues across projects. A workspace stores the domain's work. |
| **Routine** | Work that repeats on a schedule. | A workflow describes the steps; a routine determines when work repeats. Example: a weekly review can follow a review workflow. |
| **Workflow** | A sequence of steps for reaching an outcome. | A skill teaches a capability and may describe its workflow. Example: read a draft, compare it with criteria, and report changes needed. |

## Enforcement

| Term | Meaning | Notes |
|---|---|---|
| **Block** | A hook response that prevents a turn from ending and gives the agent problems to address. | A check reports problems; its mode and the block limit determine blocking. See [hook behavior](hooks.md). |
| **Check** | A test of files or system state against defined requirements. | Hooks check changed files; `aios-core:verify-aios` checks all files in scope. Example: `frontmatter` reports missing required fields. |
| **Hook** | A command an agent harness runs at a defined point, such as session start or turn end. | Can invoke checks or perform other work, such as syncing docs. |
| **Log** | The record of hook runs in `.aiOS/logs/hook-events.jsonl`. | Use for aiOS hook activity. Other systems have their own logs. See [recorded fields](logging.md). |
| **Rule** | In front matter settings, a named entry defining the requirements for matching files. | A convention states the format requirement; a rule configures its application. Other uses retain their domain meanings. |
| **Timestamps** | The `created` and `updated` fields recording when a file was created and last changed; `migrated` records its import into aiOS. | See [timestamp handling](frontmatter.md#timestamps) and [migration timestamps](frontmatter.md#migration-timestamps). |

## Retired wording

| Previous wording | Current usage |
|---|---|
| aiOS root | Use `aiOS` for the system. For paths or settings, describe the folder containing `.aiOS/config.yaml` directly. |

Existing identifiers and paths containing `root` keep their names. See [check scope](checks.md) for nested configurations.

## Using the glossary

Read glossaries in this order:

1. The aiOS glossary, copied to `.aiOS/docs/glossary.md`.
2. The shared glossary at `shared/docs/glossary.md`.
3. The current workspace's `docs/glossary.md`.

Workspace glossaries add domain terms without changing aiOS meanings. State the context when an ordinary word has another domain meaning.

Put terms used across workspaces in the shared glossary. Put terms used in one workspace in that workspace's glossary.

Related guidance lives in these places:

- [Naming conventions](naming.md) cover spelling and identifiers.
- Contracts describe where files belong.
- Operator docs explain behavior.

## Maintaining vocabulary

For a new concept, changed meaning, or replacement name:

1. Describe the meaning, its boundary with related concepts, and representative sentences.
2. Agree on the meaning and name with the operator. Keep unresolved proposals in discussion or the relevant design record.
3. Add the agreed entry to the source glossary that covers it.
4. Update current instructions, docs, templates, examples, and messages that use the concept.
5. Search for the previous wording and review each match in context. Check related concepts for conflicting definitions.

### Table structure

Use the same columns in aiOS and workspace glossaries:

- **Term:** the agreed name. Alphabetize rows within each group.
- **Meaning:** the definition. Keep one authoritative row for each term.
- **Notes:** a concise distinction, usage example, or link when useful. Leave this cell empty when the meaning is enough.

### Keeping the glossary easy to scan

- Start a small glossary with one table. Add topic headings and a linked section index when it covers several groups.
- Keep each group focused. Split a broad group into smaller groups when its terms become difficult to find.
- Keep definitions here and link to topic docs for longer explanations. Avoid turning table cells into instructions or essays.
- Keep one file while its groups remain easy to browse. If groups later need separate files, keep this file as their index.
- Define each term in one place, including after any file split. Link to that definition instead of copying it.

### Scope and source

- Record an alternative only when it causes a specific confusion. An ordinary synonym is not automatically a retired term.
- Keep storage rules in contracts, spelling in naming conventions, and operating policy in the relevant operator doc.
- Preserve historical records, code identifiers, and external terminology when propagating a vocabulary change.

Change aiOS definitions in the core plugin's source docs. Agents never edit `.aiOS/docs/glossary.md` directly. After the local plugin is updated, the start hook refreshes the docs copy.

Workspace glossaries follow the same agreement process and are edited in their own folders.
