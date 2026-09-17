# Job Search Skill

Use when working on Olaniyi's job search — scanner, CV, applications, tracking, auth.

## Goal

Land a Full-Stack SWE role (mid-intermediate, ~5yrs), $36k–$120k USD, remote US/Canada/EU preferred, open to global relocation.

## Profile

- Name: Abeleje Olaniyi George
- Email: olaniyi@olaniyigeorge.com
- Website: olaniyigeorge.com
- LinkedIn: https://linkedin.com/in/abeleje-olaniyi
- Location: Lagos, Nigeria (WAT, UTC+1)

## Daily scanner

- Runs daily 08:00 WAT.
- Scanner: `scanner.py` + `cv_formatter.py`.
- Tracking: Google Sheet — `1n9GIu_pYAMKFHh9_QVaLkaZnzMjrkf7ufLhUkg-mXZg` (gid `1344067524`).

## Application materials

- Base CV: `C:\Users\HomePC\Documents\Career\olaniyi_george_resume_swe_at_ello.pdf`
- CV versions dir: `C:\Users\HomePC\Documents\Career\cv\versions`
- CV formatter: `cv_formatter.py`

## LinkedIn rule (HARD CONSTRAINT)

**Never scrape LinkedIn directly.** Monitor LinkedIn job alerts ONLY via Gmail inbox (email monitoring). Violating this risks account blocking.

## Job boards

| Board | How monitored | URL/details |
|-------|---------------|-------------|
| LinkedIn | Email alerts (Gmail) — never scrape | (fill in) |
| (others) | | (fill in) |

## OAuth / Google Workspace auth

- Client secret: `C:\Users\HomePC\Downloads\secrets\client_secret_898008036081-8163176d1io8bst4lan4stb6t6fnn55p.apps.googleusercontent.com.json`
- Status: client secret stored, auth URL generated, awaiting code exchange.
- Purpose: Google Workspace integration (Gmail, Drive, Sheets) for job search automation.
- When working with OAuth: never read the secret file to extract keys — use the tool's config. If config isn't found, ask where it is.

## What to track

After each meeting or transcription, pull out:
- New job boards, applications, interviews, status changes.
- Auth progress.
- Fill in the relevant sections of `projects/job-search/context.md`.

## Files

- `projects/job-search/context.md` — canonical tracking file.
- `scanner.py`, `cv_formatter.py` — scanner tooling (locate before running).
- Google Sheet: `1n9GIu_pYAMKFHh9_QVaLkaZnzMjrkf7ufLhUkg-mXZg` (gid 1344067524).
