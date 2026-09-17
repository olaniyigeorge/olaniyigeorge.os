# Project Context Protocol

Use when working on any project tracked in this OS — read context.md first.

## Rule

Before making changes to a project, read its `context.md` when one exists.

## Structure

Each project lives under `projects/<project-name>/` with:
- `context.md` — primary entry point. Read this first.
- Additional docs as the project demands (weekly notes, meeting notes, decisions, etc.).

## What context.md contains

A good `context.md` has:
- **Overview** — what the project is, current status, tech stack.
- **Cadence** — how often work happens, what triggers it.
- **Current focus** — what's being worked on right now.
- **What's automated / built so far** — status of completed work.
- **What's next / in progress** — open items.
- **Tools & stack** — what's being used.
- **How to update** — how to record new information.

## Before you start work on a project

1. Read `projects/<project>/context.md`.
2. Search the repo for related files (code, notes, decisions).
3. If context.md is stale or missing key info, ask before assuming.
4. After work, update context.md with what changed — don't leave the canonical file behind.

## Updating context.md

- Prefer updating the existing file over creating duplicates.
- Preserve existing structure unless there's a reason to change it.
- If new info conflicts with existing info, surface the conflict — don't silently overwrite.
- Keep it concise — it's an index, not a dump.

## Project index

`projects/index.md` is the entry point listing all active projects and where to find them. Check it when you're not sure which project you're working on.

## Current active projects

- **Koya AI Automations** — `projects/koya-ai-automations/` — AI automation developer program, Week 3 of 6.
- **Coopwise** — `projects/coopwise/` — side project, tokenizing co-op contribution receipts.
- **Winnov8** — `projects/winnov8/` — current employment, Backend Developer.
- **Workflow Automation** — `projects/workflow-automation/` — ongoing personal initiative.
- **Job Search** — `projects/job-search/` — parallel to Koya.
