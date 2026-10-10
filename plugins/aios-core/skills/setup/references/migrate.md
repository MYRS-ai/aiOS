# Migrate

Builds a self-contained, fully configured aiOS root from files the operator already has. The sources stay untouched.

1. Ask which folders, files, skills, or projects to bring in, and where they are.
2. Survey each source. Record its folder tree, kinds of files, size, instruction files such as `CLAUDE.md` or `AGENTS.md`, skills, and Git repos.
   For a large source, brief a subagent per source and ask for this summary: the path, what it holds, its size, and its notable files.
3. Interview the operator with [interview.md](interview.md). Also ask which systems, files, and capabilities matter most, and what to leave out.
4. Propose a migration plan, and build nothing until the operator confirms it. The plan shows:
   - the target folder tree
   - one disposition for each source item: copy as is, copy and add front matter, restructure to fit aiOS, or leave out
   - batches in priority order

   Restructure an item when splitting, merging, or rewriting it makes it clearer or easier for agents to use.
5. If no aiOS root exists, build one with steps 2 and 3 of [start-fresh.md](start-fresh.md).
6. Migrate one batch at a time:
   - Copy each source. Never move or delete one.
   - Copy a Git repo with its `.git` folder, so its history comes along.
   - Carry instructions from `CLAUDE.md` and similar files into contracts. Don't copy `CLAUDE.md` files; one can stop Claude Code from loading `AGENTS.md`.
   - Put skills the operator maintains in the workspace that uses them, as `.aiOS/docs/types/skill-md.md` describes. Leave installed skills where the agent harness keeps them.
   - Write or update the contracts for each folder with `aios-core:manage-agents-md`.
   - Run `aios-core:status` and resolve its file problems before starting the next batch.
7. After each batch, report what went where, what was restructured, and what was left out. What happens to the sources is the operator's decision.
8. Return to the setup workflow to verify the aiOS root.
