# Git Protocol Skill

Use when working with git in this repo — when to commit, how to message, when to push.

## Committing

- **Do NOT commit or push unless explicitly asked.** This is the default rule.
- After meaningful changes, summarize what changed — but wait for the go-ahead to commit/push.
- When committing is requested, review `git status` first — don't blindly `git add -A` without looking.
- Stage intentionally: know what's going in.

## Commit messages

Use conventional-commits style:
- `feat:` — new feature or capability
- `fix:` — bug fix
- `docs:` — documentation only
- `chore:` — maintenance, config, tooling
- `refactor:` — code change that neither fixes nor adds
- `test:` — tests
- `scripts:` — scripting/tooling changes

Keep messages concise and descriptive. One line is fine for small changes; add body for larger ones.

## Pushing

- Push only when explicitly asked.
- Push to the current branch's upstream (usually `origin main` or `origin <branch>`).
- After push, verify: `git log --oneline origin/main..HEAD` should be empty (local caught up).

## Safety

- Never push secrets, `.env`, OAuth credentials, or credential stores.
- `.gitignore` already covers common secret patterns — respect it.
- If a file shouldn't be committed, make sure it's in `.gitignore` or explicitly excluded.

## Current branch

This repo is on `main`. Default push target is `origin main`.

## Verifying after push

```bash
git log --oneline origin/main -3   # confirm remote has the commit
git ls-remote origin HEAD           # confirm HEAD matches
```
