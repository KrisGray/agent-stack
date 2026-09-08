# PM Intake Interview

Read at the start of Phase 1. Iterate on this file freely — it is deliberately separate
from the persona so the questions can change without touching the role contract.

This file holds the **core bank** plus the **routing rules**. Domain-specific questions
live in `interview/<kind>.md` packs. A missing pack is not an error — stay generic.

## Rules

- **One question per message.** Never two. Never "and also". Never a question with a
  parenthetical second question inside it. This applies to follow-ups too.
- **Twelve questions maximum.** Budget: ~5 core, ~4 pack, ~3 held back for follow-ups.
  If you need more, the project is too big for one PRD — say so and propose splitting it.
- Open with a one-line map: what you're going to cover and roughly how many questions.
  People answer better when they can see the end.
- **Every question that can have a default gets one, in brackets**, so the user can reply
  "yes" and move on: *"…? [default: sync first]"*. Open-ended questions have no sensible
  default — do not invent bracket filler to satisfy this rule.
- "You decide" / "don't care" / "skip" is a valid answer. Record it as an assumption with
  an invalidation condition. **Never re-ask a deferred question.**
- If an answer is vague, ask **one** follow-up, then move on and log the residual
  uncertainty. Do not interrogate.
- Skip anything already answered by `docs/prd.md`, `AGENTS.md`, the charter, or the repo
  itself. Read first, then ask.
- **Never propose a solution during intake.** You are collecting, not designing. If the
  user hands you a design, log it under fixed decisions and ask what it is *for*.

## Routing

Ask Q1 first, always. Then classify the project from that answer plus whatever the repo
told you, and **say the classification out loud in one line** before continuing:

> *"Sounds like a data pipeline — I'll ask about scheduling and failure semantics."*

Load `interview/<kind>.md` and interleave its questions with the core bank below. The
announcement is not a question and does not count against the budget.

A silent misroute costs four slots and the user never learns why the questions felt
wrong — hence saying it. If the user corrects the classification, drop the pack
immediately and re-route. Correcting a route costs the user nothing and costs you no
question.

If no pack matches, or the pack file does not exist, run the core bank alone and fill the
remaining budget from the optional section.

## Core bank

Ask all five of these unless the repo has already answered one.

### Outcome

1. **What should be possible when this is done that isn't possible now?**
   *(This is also the routing signal. If the answer is a feature list rather than an
   outcome, take your one follow-up here and ask what it would let someone do.)*

### Scope

2. What is delivered first, and why that first? [default: the narrowest end-to-end slice]

3. Name two or three things this explicitly will **not** do.
   *(Push once if the user can't name any — a project with no non-goals grows into a
   platform. If the second attempt also comes back empty, log it as a risk and move on.)*

### Risk

4. What part of this are you least sure about — the bit most likely to turn out harder
   than it looks?

5. Is there anything you've already decided that I should treat as fixed rather than
   re-litigate?
   *(If the user volunteered fixed decisions earlier, log them and skip this.)*

## Optional bank

Pick from these to fill the budget. Ask only what the repo, the charter, and the pack
don't already cover.

6. What are you doing about this today — a workaround, a manual process, nothing?
   [default: nothing]
   - → *if a workaround exists:* what specifically breaks down about it?

7. Who else has to adopt this, or is it just you? [default: just you]
   - → *if others:* have they agreed already, or do they still need persuading?

8. Is there a date this needs to be usable by? [default: none]
   - → *if a date:* is that a demo or a commitment — what happens if it slips?

9. Sync, async, or both? [default: sync first; async is a decision, not a default]

10. What does "done and trusted" mean here — CI gates, coverage, benchmarks, manual
    checks? [default: CI green]

11. What external systems or contracts does this depend on? [default: none]
    *(Whatever the answer, record it as a PRD risk.)*
    - → *if any named:* who can change that without telling you, and would you get notice?
      "No notice" means the freshness habit is the only defence.

12. Anything sensitive — PII, credentials, retention obligations, licensed data?
    [default: no]
    - → *if yes:* is there a retention or deletion obligation, or is it just don't-log?

## Pack format

A pack is a numbered list of three to five questions in the same style as the optional
bank: default in brackets where one makes sense, conditional follow-ups indented beneath
their trigger. Packs assume the core bank has already run — they do not repeat scope,
non-goals, or risk.

Packs encode failure modes someone has actually hit. Do not generate pack questions on
the fly to fill a gap; a generic question asked confidently is worse than one not asked,
because it reads as covered in the playback.

## Close

End with the Phase 2 playback. Structure it as:

- **Problem** — one paragraph. Write this from Q1 and Q6: the outcome that isn't
  currently reachable, and what that costs today.
- **Users** — one line
- **In scope** — numbered, these become R1…Rn
- **Not in scope** — bulleted, these become the non-goals section
- **Assumptions** — table, every deferred answer with what would invalidate it
- **Biggest risk** — one line, drawn from Q4

Then ask one question and stop: *"Is that right? Correct anything before I write the PRD."*

Do not write `docs/prd.md` until you get an explicit yes.