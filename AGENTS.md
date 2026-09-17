# Olaniyigeorge Operating System

This repository is my personal operating system and persistent knowledge base.

It contains information about my projects, work, learning, ideas, decisions, meetings, tasks, people, goals, and other useful context.

## Core principle

This repository is the source of truth for persistent context.

When a request depends on my existing context, search the repository before answering.

Do not invent context that is not present in the repository or current conversation.

## Working with context

When answering questions about my:

- projects
- work
- decisions
- goals
- plans
- ideas
- previous work
- preferences
- ongoing tasks

first search for relevant information in the repository.

Use the smallest relevant set of files necessary to answer the question.

Do not read the entire repository unless explicitly asked.

## Memory

When I explicitly ask you to remember something:

1. Determine where it belongs.
2. Search for existing related information.
3. Update the appropriate existing file when possible.
4. Avoid unnecessary duplication.
5. Preserve existing context.
6. If the new information conflicts with existing information, surface the conflict instead of silently overwriting it.

Persistent memory belongs in this repository, not only in the AI's conversation/session memory.

## How I want things done

This section is the canonical instruction set for any agent or model working in this repo.
It sits here so it survives agent/model changes — read it first, always.

### Source of truth
- This repo (olaniyigeorge.os) is the source of truth for persistent context about me, my projects, my decisions, my goals.
- Before answering anything about my work, projects, preferences, or history: search the repo first.
- Do not invent context that isn't in the repo or the current conversation. When uncertain, say so.

### Search before you act
- When a request depends on my existing context, search the repository before acting.
- Use the smallest relevant set of files — do not read the entire repo unless explicitly asked.
- Project context lives in `projects/<project>/context.md` — read it before working on that project.

### Project structure
- Each significant project has a directory under `projects/` with a `context.md` entry point.
- Before making changes to a project, read its `context.md` when one exists.
- Update `context.md` when you learn something persistent about a project — don't duplicate in chat.

### Communication style
- Be concise but preserve important context. Don't pad.
- Lead with the change, answer, or decision — not a preamble.
- Distinguish clearly between: (a) information in the OS, (b) information from this conversation, (c) my inference.
- When uncertain, tell me what is uncertain. Surface conflicts instead of silently resolving them.

### Git protocol
- Do NOT commit or push unless explicitly asked.
- After meaningful changes, summarize what changed — but only commit/push on instruction.
- Commit messages: conventional-commits style (`feat:`, `fix:`, `docs:`, `chore:`, etc.).
- Check `git status` before staging — don't blindly `git add -A` without reviewing.
- Never touch `.env`, OAuth secrets, credential files, or anything secret-bearing unless explicitly instructed.

### Secrets and credentials
- OAuth/client secrets live at `C:\Users\HomePC\Downloads\secrets\` (client_secret_*.json).
- Do NOT read secret-bearing files to find API keys. If a tool can't find its config, say so and ask where it is.
- When setting up auth, prefer device-code flows (gh device code, OAuth device flow) over interactive browser login where possible — they work in headless/agent sessions.
- Store tokens only in the tool's native credential store or the OS keyring — never inline in files or chat.

### LinkedIn rule (hard constraint)
- NEVER scrape LinkedIn directly. Ever.
- Monitor LinkedIn job alerts only via Gmail inbox (email monitoring).
- This is both a preference and an account-safety constraint — violating it risks account blocking.

### Timezone
- Default timezone is WAT (West Africa Time, UTC+1). Lagos, Nigeria.
- Daily 08:00 WAT is the standard scanner/start-of-day time.

### When you don't know
- If something isn't in the repo and isn't in the current conversation, ask rather than guess.
- If you need a tool, config, or credential that isn't set up, say so and ask where it is — don't invent a path.

### Skills in this repo
- Detailed workflow specs live in `skills/` — read the relevant one when you're doing that kind of work.
- These are loaded automatically when in this repo by Hermes Agent (via AGENTS.md → skills/ convention).
- Other agents (Claude Code, Codex, Cursor) should read `AGENTS.md` and then the relevant `skills/<name>/SKILL.md`.

## Projects

Each significant project should have a dedicated directory under `projects/`.

A project's `context.md` should be the primary entry point for understanding that project.

Before making changes to a project, read its `context.md` when one exists.

## File organization

Prefer:

- Markdown for human-readable knowledge
- YAML/frontmatter for structured metadata
- links between related notes
- one canonical location for important information

Avoid creating duplicate notes when an existing note can be updated.

## Safety

Do not:

- delete information unless explicitly instructed
- overwrite large amounts of information unnecessarily
- invent facts about me
- silently resolve conflicting information
- expose sensitive information unnecessarily
- push Git changes unless explicitly asked

## Git

This repository is version controlled.

After meaningful changes, summarize what changed.

Do not commit or push automatically unless explicitly instructed.

## Communication

Be concise but preserve important context.

When uncertain, tell me what is uncertain.

Distinguish between:

- information explicitly stored in the OS
- information from the current conversation
- your own inference