# PM Intake Interview

Read at the start of Phase 1. Iterate on this file freely — it is deliberately separate from the persona so the questions can change without touching the role contract. Charters seed domain-specific banks; this is the generic default.

## Rules

- **One question per message.** Never two. Never "and also". Never a question with a parenthetical second question inside it.
- **Twelve questions maximum.** If you need more, the project is too big for one PRD — say so and propose splitting it.
- Open with a one-line map: what you're going to cover and roughly how many questions. People answer better when they can see the end.
- Every question gets a **default in brackets** so the user can reply "yes" and move on: *"…? [default: sync first]"*
- "You decide" / "don't care" / "skip" is a valid answer. Record it as an assumption with an invalidation condition. Never re-ask a deferred question.
- If an answer is vague, ask **one** follow-up, then move on and log the residual uncertainty. Do not interrogate.
- Skip anything already answered by `docs/prd.md`, `AGENTS.md`, the charter, or the repo itself. Read first, then ask.
- Never propose a solution during intake. You are collecting, not designing.

## Question bank

Pick the ~10 that matter for this project. Not all of them apply.

### Problem
1. What do users do today instead? What specifically hurts about it?
2. Who has to adopt this — just you, or does someone else have to be persuaded?

### Scope
3. What is delivered first, and why that first? [default: the narrowest end-to-end slice]
4. Name two or three things this explicitly will **not** do. *(Push once if the user can't name any — a project with no non-goals grows into a platform.)*
5. Is there a date this needs to be usable by? [default: none]

### Interfaces and operations
*Ask only what the repo and charter don't already answer.*

6. Sync, async, or both? [default: sync first; async is a decision, not a default]
7. What does "done and trusted" mean here — CI gates, coverage, benchmarks, manual checks? [default: CI green]

### Data and dependencies
*Skip this section entirely if the charter declares no external ground truth.*

8. What external systems or contracts does this depend on, and who changes them without asking you? [default: none] *(Whatever the answer, record it as a PRD risk. "No notice" means the freshness habit is the only defence.)*
9. Anything sensitive — PII, credentials, retention obligations, licensed data? [default: no]

### Risk
10. What part of this are you least sure about — the bit most likely to turn out harder than it looks?
11. Is there anything you've already decided that I should treat as fixed rather than re-litigate?

## Close

End with the Phase 2 playback. Structure it as:

- **Problem** — one paragraph
- **Users** — one line
- **In scope** — numbered, these become R1…Rn
- **Not in scope** — bulleted, these become the non-goals section
- **Assumptions** — table, every deferred answer with what would invalidate it
- **Biggest risk** — one line, drawn from Q10

Then ask one question and stop: *"Is that right? Correct anything before I write the PRD."*

Do not write `docs/prd.md` until you get an explicit yes.
