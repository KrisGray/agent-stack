# PM Intake Interview

Read at the start of Phase 0. Iterate on this file freely — it is deliberately separate from `pm.md` so the questions can change without touching the role contract.

## Precondition

**Do not start this interview without the schema inventory from Phase 0.** The DDL answers the data questions better than the user can, and asking someone to describe a database you already have the definition of is how you lose their patience in the first five minutes.

## Rules

- **One question per message.** Never two. Never "and also". Never a question with a parenthetical second question inside it.
- **Twelve questions maximum.** If you need more, the project is too big for one PRD — say so and propose splitting it.
- Open with a one-line map: what you're going to cover and roughly how many questions. People answer better when they can see the end.
- Every question gets a **default in brackets** so the user can reply "yes" and move on: *"…? [default: Postgres on Cloud SQL]"*
- "You decide" / "don't care" / "skip" is a valid answer. Record it as an assumption with an invalidation condition. Never re-ask a deferred question.
- If an answer is vague, ask **one** follow-up, then move on and log the residual uncertainty. Do not interrogate.
- Skip anything already answered by `docs/prd.md`, `AGENTS.md`, or the repo itself. Read first, then ask.
- Never propose a solution during intake. You are collecting, not designing.

## Question bank

Pick the ~10 that matter for this project. Not all of them apply.

### Change notification — ask first
*Ownership is settled: nomgen is owned elsewhere and this library maps it. What is not settled is how we learn when it moves.*

1. Who changes nomgen, how would you find out, and how much notice do you get? [default: no notice; the dump diff is the only signal]

*Whatever the answer, record it as a PRD risk. If the answer is "no notice", the introspect-before-work habit is the only defence and belongs in the PRD as a stated operating assumption.*

### Problem
2. What do consumers do today instead — raw SQL, psycopg by hand, an older ORM? What specifically hurts about it?
3. Which codebases will import this? Yours, or does someone else have to be persuaded to adopt it?

### Scope
4. All three schemas at once, or one first? Which, and why that one? [default: one schema end-to-end before the second is started]
5. Read-only or read-write, per schema — `archive` in particular? [default: read-write for `curation` and `app`, read-only for `archive`]
6. Name two or three things this explicitly will **not** do. *(Likely candidates: query builder, migrations, caching, async. Push once if the user can't name any — a library with no non-goals grows into a framework.)*
7. Is there a date this needs to be usable by? [default: none]

### Data
*Most of this section is answered by the schema inventory. Ask only what the DDL cannot tell you.*

8. ~~Table counts, cross-schema FKs, missing primary keys, enums, views~~ — **read from the inventory, do not ask.**
9. The inventory found `<n>` tables. Are all of them in scope, or is there a subset that actually matters? *(A hundred-table schema where twelve tables carry the work is a completely different plan.)*
10. *(Only if the inventory flagged oddities.)* Present them as a short list and ask which are deliberate versus historical accidents to be worked around. One list, one question.
11. Anything sensitive — PII, embargoed records, retention obligations? [default: no PII]
12. Is the dump current? When did nomgen last change, and is a change expected during this project? [default: stable]

### Interface
13. Sync, async, or both? [default: sync only; async is an ADR, not a default]
14. Do consumers need transactions spanning multiple repositories? [default: yes — caller owns the session]

### Operations
15. Local docker compose against a PG18 image for tests? [default: yes]
16. Any performance number that's actually a requirement rather than a nice-to-have? [default: none]

*This project has no cloud target. Do not ask about hosting, deployment or scaling beyond Q16 — if the user raises it unprompted, log it as a possible future scope change and move on.*

### Risk
17. What part of this are you least sure about — the bit most likely to turn out harder than it looks?
18. Is there anything you've already decided that I should treat as fixed rather than re-litigate?

## Close

End with the Phase 1 playback. Structure it as:

- **Problem** — one paragraph
- **Users** — one line
- **In scope** — numbered, these become R1…Rn
- **Not in scope** — bulleted, these become the non-goals section
- **Assumptions** — table, every deferred answer with what would invalidate it
- **Biggest risk** — one line, drawn from Q17

Then ask one question and stop: *"Is that right? Correct anything before I write the PRD."*

Do not write `docs/prd.md` until you get an explicit yes.
