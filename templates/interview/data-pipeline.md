# Pack: data pipeline

Compose with: `schema-change` if the pipeline creates or alters the tables it writes to.

Fetching, parsing, and landing external data in a database. Assumes the core bank has
run. Ordered by cost-of-missing; drop from the bottom.

1. If a run fails halfway through, what should happen — resume, restart clean, or leave
   the partial data? [default: safe to re-run from the start, no duplicates]
   *(This is the idempotency question. The default is the expensive one to retrofit, so
   confirm it rather than assuming it.)*

2. How does the source tell you its format changed? [default: it doesn't — you find out
   when parsing breaks]
   *(Record as a PRD risk whatever the answer, under core Q11's rule.)*
   - → *if there is notice:* how much, and through what channel?

3. What identifies a record as one you've already seen? [default: the source provides a
   stable id]
   - → *if no stable id:* what combination of fields is unique enough to dedupe on, and
     is it stable if the source re-issues a record?

4. What triggers a run — a schedule, an event, or you? [default: scheduled]
   - → *if scheduled:* what happens if a run overruns into the next one?

5. Is there history to load once, separately from the ongoing runs? [default: no backfill
   — start from now]
   - → *if yes:* roughly how much, and does it go through the same path as a normal run?

## Notes for the PRD

- Q1 and Q3 together define what "a successful run" means. If either is vague, the
  pipeline has no testable success condition — say so in the playback rather than
  writing R1 as "ingests the data".
- Rate limits, pagination and auth on the source belong in the PRD dependency section via
  core Q11. Don't spend a pack question on them unless the user raises one.
- Q5 answers involving volume are a scope finding: a backfill is frequently a second
  deliverable rather than part of the first slice.
