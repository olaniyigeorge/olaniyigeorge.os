# Koya AI Automations — Program Tracking

## Overview

**What it is:** AI automation developer program. Build AI automation projects over 6 weeks. Graded weekly (15 marks/week) + final assessment (15 marks). Those who pass get placed with companies to take up roles using their skills.

**Current status:** Week 3 of 6.

**Tech stack:** n8n, Claude Code, and others as introduced.

**Cadence:**
- Weekly: receive PRD + docs on what to build
- Daily: attend calls to know what we're building
- Submissions: per week (and/or per project — confirm)

**Placement path:** pass → placed with companies → roles using these skills.

---

## Weekly Structure (Week 1 → Week 6)

Each week needs:

- **Week number & dates** (start → end)
- **PRD / docs received** — what was the spec? link or summary
- **Daily calls** — what was discussed each day? key decisions, clarifications, pivots
- **What was built** — product/feature description, what it does, how it works
- **Submission** — what was turned in, when, format, link
- **Marks / feedback** — score received (15 max per week), comments, gaps
- **Repo / artifacts** — links to code, workflows, screenshots, demos
- **Notes / reflections** — what was hard, what was learned, what to do differently next week

---

## Week 1

**Dates:** (fill in)

**PRD / docs:**
- 

**Daily calls:**
- Day 1:
- Day 2:
- Day 3:
- Day 4:
- Day 5:

**What was built:**
- 

**Submission:**
- 

**Marks / feedback:**
- Score: /15
- Feedback:

**Repo / artifacts:**
- 

**Notes / reflections:**
- 

---

## Week 2

**Dates:** (fill in)

**PRD / docs:**
- 

**Daily calls:**
- Day 1:
- Day 2:
- Day 3:
- Day 4:
- Day 5:

**What was built:**
- 

**Submission:**
- 

**Marks / feedback:**
- Score: /15
- Feedback:

**Repo / artifacts:**
- 

**Notes / reflections:**
- 

---

## Week 3 (current)

**Dates:** Week 3 — Wednesday (started)

**PRD / docs:**
- PRD: [Week 3 PRD: AI Proposal / Document Application](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/PRD.md)
- Reference assets (from PRD repo):
  - [intake-form-fields.md](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/assets/intake-form-fields.md) — 11 intake fields: client_name, client_email, company_name, date_of_call, salesperson_name, client_needs_summary, project_scope, goals_and_objectives, recommended_services, proposed_timeline, estimated_pricing
  - [proposal-template.md](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/assets/proposal-template.md) — 6-section proposal template: Introduction, Proposed Solution (Scope + Recommended Approach), Deliverables, Timeline, Pricing, Next Steps; sign-off "Koya Talent"
  - [client-email-template.md](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/assets/client-email-template.md) — client-facing email: subject "Proposal for {{company_name}}", body with {{proposal_link}} placeholder, sign-off "Koya Talent"

**Project objective (from PRD):**
Build an AI-powered proposal application that takes client/project inputs, uses Claude to generate proposal content, lets a salesperson review and revise, creates a final proposal document, handles internal approval before client delivery, and logs the proposal centrally. Must build a **small web application** + use **Claude API**. Free to choose frontend, backend, database, approval flow, document generation, delivery tools.

**Testing scenarios (7):**
1. Normal Proposal Generation — complete input → clear structured proposal
2. Missing Information — ask for clarification, mark gap, or avoid unsupported assumptions
3. Supporting Material — use it relevantly if provided
4. Section Regeneration — revise/regenerate one section without losing the rest
5. Human Approval — not sent to client before internal approval
6. Final Delivery and Logging — approved proposal exported/sent + record logged
7. Failure Handling — document creation, approval, email delivery, or logging failure must be debuggable

**Deliverables (6):**
1. Application link (working)
2. Generated proposal sample
3. Testing evidence (completed table from project page)
4. Video walkthrough (short Loom)
5. Reflection sheet (answer questions from project page)
6. One-page documentation

**Daily calls:**
- Day 1 (Mon): (fill in from transcription)
- Day 2 (Tue): (fill in from transcription)
- Day 3 (Wed — today): Working on architecture/discovery. (fill in from transcription)
- Day 4 (Thu): (pending)
- Day 5 (Fri): (pending)

**What is being built:**
AI Proposal / Document Application — sales team tool. After discovery calls, salespeople write custom client proposals from notes, old proposals, templates, internal context. The app replaces that slow, quality-variable manual process with an AI-powered workflow that keeps a human in control before anything goes to the client.

**Tech stack (chosen):**
- Backend: FastAPI (Python)
- Frontend: Next.js (web-app/)
- AI: Claude API
- Workflow/orchestration: n8n
- Data: Supabase Postgres (planned)
- Storage: Supabase Storage (planned)
- Auth: Supabase Auth (proposed, pending decision)

**Working repo:** [github.com/olaniyigeorge/ai-proposal-workflow](https://github.com/olaniyigeorge/ai-proposal-workflow)

**Repo structure:**
```
ai-proposal-workflow/
├── backend/
│   └── main.py            ← Architecture & Design Doc (discovery phase, no code written)
├── docs/
│   ├── architecture.md    ← empty
│   ├── decisions.md       ← empty
│   └── system-flow.md     ← empty (contains Next.js default README — placeholder)
├── web-app/               ← Next.js scaffold (create-next-app), no custom code yet
│   ├── app/               ← pages/layout (default)
│   ├── public/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── README.md          ← default Next.js README
│   └── ...
├── .gitignore
└── README.md              ← empty
```

**What's done so far (as of Wednesday, Week 3):**
- Backend `main.py` contains a full **Architecture & Design Document** (discovery phase only — explicitly "no code written"):
  - 19 unresolved architectural questions (identity/tenancy, n8n boundary, document generation format, regeneration semantics, approval/delivery, data/compliance)
  - Comprehensive risk & edge-case analysis across intake, generation, review/approval, delivery/logging layers
  - Proposed system context/data flow diagram (Google Form → Sheets → n8n → FastAPI → Supabase → Next.js UI → Claude → Storage → Delivery)
  - Backend layering proposal (API / services / domain / adapters / background jobs)
  - Frontend layering proposal (routes / feature components / API client / server-side auth)
  - Domain entities: Proposal, ProposalSection, IntakeSubmission, GenerationEvent, ApprovalDecision, DocumentArtifact, DeliveryRecord, ActivityLogEntry, User, Client, (conditional) Organization
  - Full proposal state machine: DRAFT → GENERATING → IN_REVIEW → PENDING_APPROVAL → APPROVED → DOCUMENT_READY → DELIVERED → CLOSED (with REJECTED and *_FAILED substates)
  - Section-level regeneration strategy (7-point approach: proposal context object, tone profile, sibling summaries, canonical facts layer, regeneration instructions, version+diff tracking, optional consistency pass)
  - Auth & authorization model (Supabase Auth proposed, role-based, defense in depth + RLS, segregation of duties pending decision)
  - Failure handling for every integration boundary (n8n webhook idempotency, Claude retry/backoff, document gen failure state, delivery tracking, optimistic concurrency, audit log integrity)
  - 10-phase implementation plan (Phase 0 Foundations → Phase 9 Hardening)
  - Consolidated blocking decisions table (6 items: tenancy, n8n auth, doc format, regeneration instructions, self-approval, delivery mechanism)

**Marks / feedback:**
- Score: /15
- Feedback: (not yet graded — Week 3 in progress)

**Repo / artifacts:**
- [ai-proposal-workflow repo](https://github.com/olaniyigeorge/ai-proposal-workflow) — architecture doc in backend/main.py; Next.js scaffold in web-app/; docs/ mostly empty
- PRD reference repo: [aat-c3-week-3-proposal-app](https://github.com/quadri40/aat-c3-week-3-proposal-app) (PRD + 3 reference assets)

**Notes / reflections:**
- Current phase: discovery/architecture only. No code written yet.
- Key blocking decisions to resolve before Phase 2 (from architecture doc): tenancy (single vs multi), n8n webhook auth method, final document format, whether regeneration takes user instructions, self-approval allowed or not, delivery mechanism.
- `docs/` folder is empty — decisions.md and system-flow.md should be populated as the build progresses.
- `web-app/` is still a default Next.js scaffold — no proposal UI built yet.

---

## Week 4

**Dates:** (fill in — ahead)

**PRD / docs:**
- (pending)

**Daily calls:**
- (pending)

**What will be built:**
- (pending)

**Submission:**
- (pending)

**Marks / feedback:**
- Score: /15
- Feedback:

**Repo / artifacts:**
- 

**Notes / reflections:**
- 

---

## Week 5

**Dates:** (fill in — ahead)

**PRD / docs:**
- (pending)

**Daily calls:**
- (pending)

**What will be built:**
- (pending)

**Submission:**
- (pending)

**Marks / feedback:**
- Score: /15
- Feedback:

**Repo / artifacts:**
- 

**Notes / reflections:**
- 

---

## Week 6

**Dates:** (fill in — ahead)

**PRD / docs:**
- (pending)

**Daily calls:**
- (pending)

**Final project / assessment:**
- 

**Submission:**
- (pending)

**Marks / feedback:**
- Score: /15
- Feedback:

**Repo / artifacts:**
- 

**Notes / reflections:**
- 

---

## Program Summary

**Total marks so far:** ___ / 45 (Weeks 1–3 × 15)

**Projected final:** ___ / 90 (all 6 weeks + final)

**Placement status:** (not yet — pending pass)

**Overall notes:**
- 

---

## Artifacts Index

A running list of everything produced across the program — repos, workflows, demos, docs, screenshots, submissions.

| Week | What | Type | Link / path | Notes |
|------|------|------|-------------|-------|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 | PRD + reference assets | Spec | [PRD](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/PRD.md), [intake fields](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/assets/intake-form-fields.md), [proposal template](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/assets/proposal-template.md), [client email template](https://github.com/quadri40/aat-c3-week-3-proposal-app/blob/main/assets/client-email-template.md) | Week 3 assignment: AI Proposal / Document Application |
| 3 | Architecture & Design Doc | Doc | [backend/main.py](https://github.com/olaniyigeorge/ai-proposal-workflow/blob/main/backend/main.py) in [ai-proposal-workflow](https://github.com/olaniyigeorge/ai-proposal-workflow) | Discovery-phase architecture; no code written yet. Covers Q1–Q19, risks, state machine, regeneration strategy, auth model, failure handling, 10-phase plan. |
| 3 | Next.js scaffold | Code (scaffold) | [web-app/](https://github.com/olaniyigeorge/ai-proposal-workflow/tree/main/web-app) in [ai-proposal-workflow](https://github.com/olaniyigeorge/ai-proposal-workflow) | Default create-next-app scaffold; no custom proposal UI yet |
| 3 | AI-proposal-workflow repo | Repo | [github.com/olaniyigeorge/ai-proposal-workflow](https://github.com/olaniyigeorge/ai-proposal-workflow) | Main working repo for Week 3 project |

---

## How to update this

After each meeting or transcription:
1. Pull out: PRD content, what was said on calls, what was built, submission status, marks/feedback.
2. Fill in the relevant week's section.
3. Add any new artifact to the Artifacts Index.
4. If something shifts (new week, new direction), update ahead accordingly.
