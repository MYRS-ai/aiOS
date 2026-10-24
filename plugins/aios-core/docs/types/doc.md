---
type: doc
created: 2026-10-11T09:34-07:00
updated: 2026-10-24T10:01-07:00
---

# Doc

A `doc` records information an agent or operator needs, such as context, research, decisions, or instructions for using aiOS. Use `doc` for general Markdown content outside skill packages. Folder contracts use `AGENTS.md` instead.

## Front matter

For new docs, agents write only the type. Setup and hooks add timestamps through the fixer described in [frontmatter.md](../frontmatter.md).
For imported docs, follow [Migration timestamps](../frontmatter.md#migration-timestamps) to preserve source dates and record `migrated`.

```markdown
---
type: doc
---
```

## Structure

Start with a descriptive title and state the document's purpose or main point. Organize the rest around its subject and audience. Follow any structure required by the folder's contract, such as proposal or spec sections.

- Use paragraphs for connected explanations. Give each paragraph one main idea and separate paragraphs with a blank line.
- Use bullets for parallel points that readers can consider independently. Keep their grammatical structure consistent.
- Use numbered steps for actions that must happen in order. Give each step one bounded action.
- Use headings to group distinct topics and show their hierarchy. Keep short explanations together under one heading.
- Use tables to compare items with the same attributes, such as settings and their effects.
- Use emphasis sparingly for labels or distinctions readers need to find. Keep technical names and paths exact.

Single line breaks usually render as spaces in Markdown. Use paragraph breaks and list syntax to express the intended structure.

## Writing and upkeep

- Use the [aiOS glossary](../glossary.md) and applicable workspace glossaries.
- Keep one topic per document. Link to existing detail instead of repeating it.
- Distinguish current instructions, proposals, and historical findings.
- Review the rendered structure as well as the source text.
- Include sources and verification dates when the information can change.
- Update related instructions and links when the document's purpose or content changes.
