---
type: doc
created: 2026-10-03T20:14-07:00
updated: 2026-10-04T18:50-07:00
---

# AGENTS.md

An `AGENTS.md` file is a folder's contract. It tells an agent three things:

- what it describes and what purpose it serves
- which instructions apply there
- where to find what they need

People read contracts too, so write them in plain sentences.

## When a folder needs a contract

A folder should have an `AGENTS.md` if it has its own purpose or instructions. It should also have one when agents need help finding files or folders. Skip it when:

- the folder is a skill or is inside one; `SKILL.md` provides the instructions
- the folder follows an agent harness's or Git's structure, such as `.claude-plugin/` or `.git/`
- the parent's contract already covers the folder

## Structure

Use this outline as a starting point:

```markdown
---
type: AGENTS.md
---

# Descriptive title

Purpose

## Instructions   (optional)

## Skills         (optional)

## Contents
```

Put purpose before instructions, followed by navigation. Adapt headings and tables to the contract's role. Leave out optional sections when they would be empty.

## Sections

### Title

Use a short title that names what the contract describes. It does not have to match the folder name. For example, use `# Shared workspace` for `shared/` and `# AI operating system` for the top-level contract.

### Purpose

Explain the purpose in one to three sentences. Lead with the subject itself, such as "Dated records of events, notes, and decisions." Don't open with "This folder holds" or "This folder is reserved for"; the reader already knows the contract describes a folder. A system contract describes what the system does. A domain contract describes whose work it supports. A documentation folder's contract describes its contents. Put directions to agents under Instructions.

### Instructions

State what agents must follow when working in the folder. Include operator preferences that apply to future work.

- Keep each instruction short, but include everything needed to follow it.
- Give each topic its own `###` heading.
- Explain how to check the work, such as which script to run or standard to meet.

### Skills

List the skills commonly used in this folder.

| Column | What to write |
|---|---|
| Skill | The skill's name, such as `aios-core:audit-agents-md` |
| Use when | The task or situation that calls for it |

### Contents

Help the agent find what the task needs. List relevant files and folders, or domains and shared resources for the top-level contract.

Use the columns below when listing files. Adapt the labels when the table serves a different purpose.

| Column | What to write |
|---|---|
| Path | A link to the file, or to the folder's own `AGENTS.md` |
| What it holds | What's inside, in a few words |
| Read when | The task or situation that calls for reading it |

Organize the table as follows:

- List folders first, then files. Sort each group alphabetically.
- Give every file and folder its own row.
- If the table has more than about ten rows, split it into groups under `###` headings, such as Folders and Files.

## Writing a contract

- Describe what exists now.
- Choose language that fits the subject.
- Use the terms in the [glossary](../glossary.md), not synonyms.
- Don't repeat content from a parent contract. The agent has already read it.
- Link to other files and skills instead of repeating their content.
- Keep the file under about 50 lines. If it exceeds 100 lines, tell the operator.

## Keeping a contract current

Update the contract in the same turn when:

- You add, rename, move, or remove a file or folder it lists or should list.
- The folder's purpose changes.
- A new instruction applies to everyone working in the folder.
- The operator states a preference that applies to future work in the folder.

When you add or remove a folder with its own contract, update the parent contract's Contents section too.

A contract may conflict with another contract or with the folder's contents. If the correct fix is unclear, ask the operator.
