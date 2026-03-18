# summarize-codebase

A Claude Code skill that generates a `CLAUDE.md` knowledge base for any codebase, enabling faster navigation and question-answering in future sessions.

## What it does

When invoked, this skill explores your project — structure, entry points, key files, architectural patterns, shared utilities — and distills everything into a concise `CLAUDE.md` at the project root.

`CLAUDE.md` is automatically loaded by Claude at the start of every session, so future questions get answered faster because Claude already knows where to look.

The generated index also includes a self-updating instruction: if Claude discovers important context during a later session (e.g., after deep exploration to answer a tough question), it will add that knowledge to `CLAUDE.md` so subsequent sessions benefit too.

## Install

```bash
claude install-skill /path/to/CodeBaseSummary/summarize-codebase
```

Or if shared via a git repo:

```bash
claude install-skill https://github.com/your-org/CodeBaseSummary/summarize-codebase
```

## Usage

In any project, just say:

- `/summarize-codebase`
- "summarize this codebase"
- "create a codebase index"
- "generate CLAUDE.md"
- "map this project"

If a `CLAUDE.md` already exists, the skill merges new findings into it without overwriting your manually-written content.
