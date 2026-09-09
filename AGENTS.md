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