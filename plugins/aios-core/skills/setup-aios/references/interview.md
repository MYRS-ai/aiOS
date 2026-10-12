# Interview

Questions that shape the operator's aiOS. Every setup mode uses them.

## How to interview

- Ask about one topic at a time, with two or three questions each.
- Offer an example answer when a question is abstract.
- Skip questions the operator has already answered or the sources show.
- After each topic, summarize what you heard in a few lines and ask the operator to correct it.

## Topics

### 1. Domains

- What areas of work and life should aiOS help with? Examples: a job, a business, family life.
- For each one: what is your role, and what kind of organization or group is it?
- What does good work look like in that area?

### 2. Recurring work

- What work repeats on a schedule, such as a weekly report or a monthly bill run?
- What procedures do you follow often, such as onboarding a client?
- What goals with an end date are you working toward now?

### 3. Files and tools

- What kinds of files do you keep, and where are they today?
- Which apps hold your work, such as a calendar, email, or notes app?
- Which agent harnesses do you use: Claude Code, Codex, or both?

### 4. Terms

- Which words have a specific meaning in each area, such as team names, product names, or abbreviations?
- Which concepts need distinct names to prevent confusion? Give a sentence showing how you use each name.

### 5. Preferences

- How should agents write for you, and what should they never do?
- When should an agent ask before acting?

## Where answers go

| Answer | Where it goes |
|---|---|
| Domains and roles | Workspaces, and each workspace contract's purpose |
| Recurring work | `routines/` for scheduled work, `workflows/` for procedures, `projects/` for goals with an end |
| Background on each area | The workspace's `context/` folder |
| Agreed concepts | The workspace glossary, or `shared/docs/glossary.md` when more than one workspace uses them |
| Preferences | Instructions in the top-level contract, or in a workspace contract when they apply to one domain |
