# Setup example

A complete fictional aiOS, packaged with this skill at [assets/example/](../assets/example/AGENTS.md).
Read this guide after the interview, then read the example files relevant to the operator's confirmed needs.

## What the example demonstrates

Alex Rivera leads a mobile product team at Fieldline, runs Rivera Studio, and shares family responsibilities with Sam.
Their two children are Maya and Leo. Alex's parent Elena lives nearby. Every person and organization in the example is fictional.

The records describe October 5–11, 2026, with plans for the following week. They demonstrate a configured aiOS in use.
They do not describe the current operator, provide live information, or authorize actions in their accounts.

| Workspace | Work supported | What to learn |
|---|---|---|
| [Work](../assets/example/work/AGENTS.md) | Alex's job at Fieldline | Team context, project evidence, delivery decisions, and a recurring review |
| [Studio](../assets/example/studio/AGENTS.md) | A business with services and products | Client commitments, separate product records, approval boundaries, and limited capacity |
| [Home](../assets/example/home/AGENTS.md) | Family life and personal goals | Household coordination, constraints, practical projects, and recurring planning |
| [Shared](../assets/example/shared/AGENTS.md) | Resources used across domains | Common writing criteria, shared terms, and cross-domain planning |

These workspace choices are illustrative. A student or caregiver may need a different structure. Shared resources support the domains rather than forming another domain.

## Choose representative files

Start with the example's [top-level contract](../assets/example/AGENTS.md). Then follow one relevant content chain instead of reading every file.

| Need | Read | Look for |
|---|---|---|
| Operator preferences | [Top-level contract](../assets/example/AGENTS.md) and [writing standard](../assets/example/shared/standards/writing.md) | Instructions apply everywhere; standards define quality. |
| A domain's background | [Work context](../assets/example/work/context/AGENTS.md) | Specific responsibilities, people, constraints, and sources |
| A finite goal | [Mobile job-notes project](../assets/example/work/projects/mobile-job-notes/AGENTS.md) | Goal, owner, current evidence, decisions, next steps, and completion criteria |
| Client and product organization | [Studio clients](../assets/example/studio/clients/AGENTS.md) and [products](../assets/example/studio/products/AGENTS.md) | Domain-specific folders with a clear purpose |
| Household planning | [Home routines](../assets/example/home/routines/AGENTS.md) and [workflows](../assets/example/home/workflows/AGENTS.md) | A schedule selects a procedure; the procedure produces a usable plan. |
| Personal goals | [Home goals](../assets/example/home/goals/AGENTS.md) | A goal has evidence of progress and a realistic next action. |
| Shared vocabulary | [Shared glossary](../assets/example/shared/docs/glossary.md) | Concise definitions, with optional distinctions or examples |
| A complete review | [Weekly planning routine](../assets/example/shared/routines/weekly-planning.md) → [workflow](../assets/example/shared/workflows/weekly-review.md) → [journal entry](../assets/example/shared/journal/2026-10-11-weekly-planning.md) | Schedule, procedure, and recorded result remain separate and connected. |

The example's folders exist because they contain useful work. Do not create an empty folder merely to match its tree.

## Map interview answers to files

| Evidence from the operator | Destination | What to preserve |
|---|---|---|
| Domains, roles, and responsibilities | Workspace contracts | Whose work the workspace supports and how to navigate it |
| Preferences that apply everywhere | Top-level contract | Clear instructions an agent can follow |
| Preferences limited to one domain | That workspace's contract | The scope of the instruction |
| People, tools, constraints, and sources | Context files | Confirmed facts, their sources, and unresolved questions |
| Work with an end | Project records | Goal, owner, status, evidence, next action, and completion criteria |
| Recurring responsibilities | Routine files | Cadence, owner, trigger, workflow, and expected output |
| Repeatable procedures | Workflow files | Inputs, ordered actions, decisions, and completion criteria |
| Past events and decisions | Dated journal entries | What happened, what was decided, and what remains open |
| Domain-specific organization | Folders such as clients, products, or goals | The operator's actual needs, rather than a standard folder list |
| Terms used across domains | Shared glossary | One agreed meaning per term |
| Terms used in one domain | Workspace glossary | Domain meanings that do not redefine aiOS concepts |

## Adapt the example

1. Compare the interview with the relevant workspace. Identify which files have an actual counterpart in the operator's work.
2. Propose the smallest useful structure. Explain any domain-specific folder and obtain the confirmation required by the setup mode.
3. Use the setup script to create missing settings, contracts, and glossaries from the starter templates.
4. Adapt selected example structures using the operator's facts. Write their context, instructions, and work records in their own words.
5. Identify missing information explicitly. Do not invent people, projects, past reviews, deadlines, approvals, or completed work.
6. Connect contracts and content. A routine should name its workflow, and a project should link its evidence and next action.
7. Review the result with the checks below, then return to the setup mode's verification step.

Starter templates live in `assets/templates/`; the complete example lives in `assets/example/`.
Templates create the initial files; the example demonstrates useful content and connections.
The setup script does not copy the example. There is no step that clones every fictional file into the operator's aiOS.

Each contract template describes its generated destination:

| Template | Destination |
|---|---|
| [Top-level contract](../assets/templates/top-level-contract.md) | `AGENTS.md` |
| [Settings contract](../assets/templates/settings-contract.md) | `.aiOS/AGENTS.md` |
| [Workspace contract](../assets/templates/workspace-contract.md) | `<workspace>/AGENTS.md` |
| [Shared contract](../assets/templates/shared-contract.md) | `shared/AGENTS.md` |

For migration, preserve the meaning and history of source material. For extension, follow the existing operator's choices instead of replacing them.
Use `aios-core:manage-agents-md` for contracts and `aios-core:manage-skills` only when a skill needs creating or changing.

## Review the adapted result

- **Facts:** Every person, organization, date, and claimed result comes from the operator or an identified source.
- **Vocabulary:** Names match the aiOS, shared, and workspace glossaries. New meanings follow the vocabulary agreement process.
- **Structure:** Every created folder has useful content and accurate navigation. No example workspace is mandatory.
- **Connections:** Project status agrees with its evidence. Each routine identifies its workflow and expected output.
- **Capacity:** Planned work fits the operator's commitments. Conflicts remain visible until the operator resolves them.
- **Access:** Tools and accounts are described accurately. A routine file does not create an automation or connect an account.
- **Writing:** Paragraphs, headings, tables, and lists make the purpose and next action easy to find.
- **Example content:** No fictional names, example dates, placeholder markers, or setup guidance remain in the operator's files.

Run `aios-core:verify-aios` and resolve file problems. Ask the operator to confirm any unresolved facts before relying on them.

## Maintain and validate the example

Keep one copy inside this skill. The example's contracts describe the fictional operator's files; maintenance instructions belong here.
Its `.aiOS/docs/` and `.aiOS/logs/` are generated and excluded from the source. Do not create them inside the packaged asset.

Validate a temporary copy outside any skill package:

1. Copy `assets/example/` to an empty temporary folder. Exclude generated docs, logs, and interpreter caches.
2. Run `python3 <skill>/scripts/setup.py <temporary-folder>` to generate the docs copy using the plugin's current source.
3. From the temporary folder, run `python3 <plugin>/skills/verify-aios/scripts/status.py` and resolve every file problem.
4. Check all relative Markdown links, including links into the generated docs copy.
5. Review context, project status, routines, workflows, and journals together for conflicting names, dates, and decisions.
6. Remove the temporary copy after verification.

Here, `<skill>` is the installed setup skill folder and `<plugin>` is the core plugin folder.
The product test suite performs the standalone checks and verifies that the reference also works from a plugin-only installation.

The temporary copy matters because files inside skill packages are normally exempt from document front matter checks.
Checking the product repository alone does not validate the example as an operator's aiOS.
