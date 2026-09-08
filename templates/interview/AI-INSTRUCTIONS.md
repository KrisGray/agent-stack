# AI Intake Instructions

How to run project intake and produce a Phase 2 playback.

**Ownership.** This file owns the playback format and the worked examples, and nothing
else. It does not restate the interview rules — those drift the moment they exist in two
places, so read them from source:

| For | Read |
|---|---|
| Questions, budget, one-question-per-message rule, routing procedure | `interview.md` |
| Which packs exist, what composes with what, boundary tests | `interview/PACKS.md` |
| Playback format and examples | this file |

## Before you start

1. Read `interview.md` end to end. It is the contract.
2. Read `AGENTS.md`, the charter, `docs/prd.md` and the repo. Anything they answer is a
   question you do not get to ask.
3. Read `interview/PACKS.md` for the routing vocabulary. Do not route to a pack with no
   file in `interview/`.

Then run the interview as `interview.md` describes. Do not write `docs/prd.md` until the
user explicitly confirms the playback below.

## Playback output format

When intake is complete, write the Phase 2 playback using this exact structure. Do not
change headings or list styles.

- `## Problem` — one paragraph, written from core Q1 and Q6: the outcome that isn't
  currently reachable, and what that costs today.
- `## Users` — who uses or is affected by the work.
- `## In scope` — numbered; these become R1…Rn.
- `## Not in scope` — bulleted; these become the non-goals section.
- `## Assumptions` — table; every deferred answer with what would invalidate it.
- `## Biggest risk` — one line, drawn from core Q4.

Every "you decide" / "skip" answer must appear in the Assumptions table. An answer that
was deferred and then silently omitted reads as a settled decision, which is the failure
this table exists to prevent.

### Template

```md
## Problem
A short paragraph describing the outcome that is not currently possible and the cost of
that limitation.

## Users
- Primary: ...
- Secondary: ...

## In scope
1. R1: ...
2. R2: ...

## Not in scope
- ...

## Assumptions
| Assumption | Invalidation condition |
|-----------|------------------------|
| ...       | ...                    |

## Biggest risk
One line describing the most uncertain or difficult part.
```

Close with one question and stop: *"Is that right? Correct anything before I write the
PRD."*

## Worked examples

### Example 1 — data pipeline that also changes the schema

Routing announcement:

> "Sounds like a data pipeline that also changes the schema — I'll ask about failure
> semantics and record identity, then row counts and backfill."

Packs loaded: `data-pipeline` (three questions from the top) plus `schema-change` (two).
That is the five-question cap; the remaining budget goes to the core and optional banks.

```md
## Problem
Partner CSV exports cannot be ingested into Cloud SQL without duplicate rows or silent
parse failures, and the manual repair work costs several hours a week.

## Users
- Primary: the data engineering team
- Secondary: reporting consumers who depend on the data being fresh

## In scope
1. R1: A scheduled pipeline that ingests the daily export and is safe to re-run.
2. R2: The migrations needed to store the new fields.

## Not in scope
- Real-time ingestion; daily batches only.
- Backfill of history older than the agreed window.

## Assumptions
| Assumption | Invalidation condition |
|-----------|------------------------|
| Partner formats change quarterly, with notice | A format changes without notice |
| Row volumes stay low enough that a brief lock is acceptable | The table grows past the point where an ALTER blocks writes noticeably |

## Biggest risk
Source format changes arriving without notice, since nothing detects them before parsing
breaks.
```

### Example 2 — web app with roles

Routing announcement:

> "Sounds like an authenticated web app — a user logs in, so I'll ask about journeys and
> roles rather than URLs and caching."

Packs loaded: `web-app` (three) plus `auth-permissions` (two). The boundary test in
`PACKS.md` decided `web-app` over `website`; say which test you applied when the call was
close.

```md
## Problem
Project leads cannot see task and deployment status in one place; it is spread across
tickets, chat and CI dashboards, and assembling it by hand delays every status update.

## Users
- Primary: project leads
- Secondary: engineers whose work appears in the view

## In scope
1. R1: A role-aware app showing tasks and deployment status.
2. R2: Authentication and permissions so leads see all projects and engineers see only
   their own.

## Not in scope
- Billing and financial reporting.
- Cross-organisation sharing.

## Assumptions
| Assumption | Invalidation condition |
|-----------|------------------------|
| Single-tenant deployment | A requirement to host external tenants appears |
| Roles are limited to lead and engineer | A third role needs different data visibility |

## Biggest risk
Data isolation between roles, which is harder to retrofit than to build in.
```
