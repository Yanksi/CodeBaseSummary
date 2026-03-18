---
name: summarize-codebase
description: >
  Generate or update a CLAUDE.md knowledge base that indexes a codebase for fast navigation.
  Use this skill whenever the user asks to summarize, index, or map a codebase, generate a CLAUDE.md,
  create a project overview, or says things like "help me understand this project structure",
  "make a codebase index", "document the architecture", or "/summarize-codebase".
  Also trigger when the user says their CLAUDE.md is outdated or wants to refresh it.
  Do NOT trigger for general documentation requests (READMEs, API docs, JSDoc) — this skill
  is specifically about creating a navigational index for Claude's own future use.
---

# Summarize Codebase

You are generating a **CLAUDE.md** file that serves as a navigational index for this codebase.
The goal is simple: when a future Claude session gets a question about this project, CLAUDE.md
should tell it exactly where to look — so it doesn't have to explore the entire repo.

Think of it like a table of contents + map, not documentation. Every line should help Claude
find code faster.

## Step 1: Explore the codebase

Do a thorough but efficient sweep. Use Glob and Grep in parallel to gather intel quickly.

**Start with structure:**
- `Glob("**/*", ...)` scoped to key directories to understand the folder layout
- Look at the root for config files (package.json, Cargo.toml, pyproject.toml, go.mod, etc.)
  — these reveal the tech stack, entry points, and scripts
- Identify the primary language(s) and framework(s)

**Then go deeper:**
- Read entry points (main files, index files, app bootstrapping)
- Identify routing, API definitions, or CLI command registrations
- Find shared utilities, types, constants, and config that other files import
- Look for architectural patterns: dependency injection, event systems, plugin architectures,
  middleware chains, etc.
- Check for monorepo structure (workspaces, packages/, apps/)

**Find the hidden gems** — files that are important but not obvious:
- Shared type definitions or interfaces
- Helper/utility modules that many files import
- Middleware, hooks, or decorators that modify behavior silently
- Database schema files, migration directories
- Environment config, feature flags
- Test fixtures or factories that reveal data shapes

Use `Grep` to find highly-imported files:
```
Grep("from.*import|require\\(|import .* from", type="<lang>", output_mode="content")
```
Files that appear as import targets frequently are likely important shared code.

## Step 2: Check for existing CLAUDE.md

Before writing, check if a CLAUDE.md already exists at the project root.

**If it exists:**
- Read it carefully
- Preserve any user-written content (instructions, preferences, conventions)
- Merge your new findings into the existing structure
- Add new sections for anything not already covered
- Update outdated information
- Do NOT delete or rewrite sections the user clearly wrote manually

**If it doesn't exist:**
- Create a fresh one using the template below

## Step 3: Generate the CLAUDE.md

Use this structure. Be concise — each entry is a signpost, not an essay.
Adjust sections based on what's actually in the codebase (skip sections that don't apply,
add sections that are needed).

```markdown
# [Project Name]

## Project Overview
[1-3 sentences: what this project does, who it's for]

**Tech Stack:** [languages, frameworks, key libraries]
**Package Manager:** [npm/yarn/pip/cargo/etc.]

## Directory Structure
[Purpose of each major folder — one line each]

src/           — Main application source
src/api/       — REST API route handlers
src/models/    — Database models and schemas
src/utils/     — Shared helper functions
tests/         — Test suites (mirrors src/ structure)
scripts/       — Build and deployment scripts
config/        — Environment and app configuration

## Key Files & Entry Points
[The files you'd read first to understand the system]

- `src/index.ts` — Application bootstrap, server startup
- `src/api/router.ts` — All API routes registered here
- `src/db/schema.ts` — Database schema definitions
- `package.json` — Scripts: `dev`, `build`, `test`, `lint`

## Architecture & Patterns
[How the code is organized and why — data flow, key abstractions]

- Request flow: router → middleware → handler → service → repository → database
- Dependency injection via `src/container.ts`
- Event-driven notifications through `src/events/`

## Important Utilities & Shared Code
[Files that are easy to miss but widely used]

- `src/utils/errors.ts` — Custom error classes used across all handlers
- `src/types/index.ts` — Shared TypeScript interfaces
- `src/middleware/auth.ts` — Authentication middleware applied to all protected routes
- `src/constants.ts` — App-wide constants and magic strings

## Development
[How to get the project running]

- Install: `npm install`
- Dev server: `npm run dev`
- Tests: `npm test`
- Build: `npm run build`

---

> **Self-updating index:** If you spend significant effort exploring this codebase to answer
> a question and discover important context not captured above (key files, patterns, gotchas,
> or relationships between components), update this file with what you learned. Future sessions
> will thank you. Keep entries concise — file path + one-line description is ideal.
```

**CRITICAL:** The self-updating footer (the blockquote starting with "Self-updating index") must
be included **verbatim** in every generated CLAUDE.md. This is the mechanism that enables future
sessions to accumulate knowledge over time — without it, the index becomes static and loses its
primary advantage over plain documentation. Do not paraphrase, shorten, or replace it with a
different message.

## Guidelines

- **Be specific with paths.** Write `src/api/middleware/rateLimit.ts`, not "the rate limiting module."
- **One line per entry.** If you need more than one sentence to describe a file, it's too much.
- **Include line numbers for key definitions** when they'd save future Claude from searching:
  e.g., `src/config.ts:42` — default configuration object.
- **Order by importance**, not alphabetically. Put the files someone would read first at the top.
- **Note non-obvious relationships.** If `src/hooks/useAuth.ts` depends on a context provider
  in `src/providers/AuthProvider.tsx`, say so — that connection isn't obvious from file names.
- **Skip generated files.** Don't index `node_modules/`, `dist/`, `.next/`, `__pycache__/`, etc.
- **Mention gotchas.** If there's a config file that looks unimportant but breaks everything
  when missing, call it out.

## After generating

Tell the user what you created and highlight the most interesting findings — things they might
not have expected, or files that turned out to be more central than their names suggest.
If you noticed potential issues during exploration (circular dependencies, dead code, missing
tests for critical paths), mention them briefly as observations.
