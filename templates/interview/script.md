# Pack: script

Compose with: `cli-tool` when it is reused or distributed, `batch-worker` when
something other than a person starts it, `data-pipeline` when it moves data on a
schedule. See the boundary tests in `PACKS.md` — this pack is the one most often
routed to by mistake.

A standalone script or small tool. Short pack — four questions, and often fewer are
needed. Assumes the core bank has run.

The failure mode this pack exists to catch: scripts become infrastructure without anyone
deciding that they should. Q1 and Q2 are there to make that decision explicit rather than
retrospective.

1. Is this run once, or does it become something that runs again? [default: once]

2. Who runs it, and from where — your machine, a server, a scheduler? [default: you, on
   your machine, by hand]
   *(If Q1 said "once" and Q2 names a scheduler or another person, those answers
   contradict each other. Take your one follow-up here — it is the highest-value
   follow-up in this pack.)*

3. Does it change anything that can't be undone — writes, deletes, sends, spends?
   [default: read-only]
   - → *if yes:* does it need to be rehearsed against real data before it runs for real?

4. If it stops halfway, is it safe to just run it again? [default: yes]

## Notes for the PRD

- A script that is genuinely run once, by one person, read-only, does not need a PRD.
  Say so and offer to skip straight to building it. Recognising that is a better outcome
  than a well-formed document nobody needed.
- Anything that answers "repeatedly" to Q1 or names a scheduler in Q2 should be routed to
  a fuller pack instead. Use the boundary tests in `PACKS.md`: another person runs it →
  `cli-tool`; a scheduler or queue starts it → `batch-worker`; it moves data on a
  schedule → `data-pipeline`. Re-routing costs no question.
- A Q3 answer that is not read-only makes Q4 a requirement rather than a preference.
