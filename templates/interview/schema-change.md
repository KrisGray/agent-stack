# Pack: schema change

Compose with: any pack whose project alters the shape of a database that already holds
data.

**Usually the second pack, rarely the first** — it describes a change to a database, not
a kind of project. That is a note about position, not a restriction; see the composition
rules in `interview.md`.

Relational migration — adding, altering, or dropping columns, tables, constraints, or
indexes on a database that already holds data someone cares about.

Assumes the core bank has run. Ask in order and drop from the bottom if the budget is
tight; the ordering is by cost-of-missing, not by interest. Read `migrations/` first and
skip anything already settled there.

1. Roughly how many rows are in the tables you're changing?
   [default: small enough that a brief lock doesn't matter]
   - → *if large enough to matter:* how much write-blocking is acceptable, and is there a
     window where it costs less?

2. During the deploy, does the old application code have to keep working against the new
   schema? [default: yes — deploys aren't atomic, so assume both shapes are live at once]
   - → *if no:* what makes the app and the migration land together?

3. Do existing rows need values under the new shape, or are any of them invalid under the
   new rules? [default: no — new columns are nullable or defaulted]
   - → *if yes:* does the application need to behave correctly while the backfill is
     still in flight?

4. Is rollback a requirement, or is forward-only acceptable once the app has written data
   in the new shape? [default: forward-only after first write]

5. Who else reads these tables directly — replicas, reporting, ETL, another service?
   [default: this application only]
   *(Core Q11 asks what this depends on. This is the inverse: what depends on this.)*
   - → *if any:* do they touch the columns you're changing, and who tells them?

## Notes for the PRD

- Q1 and Q2 together decide whether this is one migration or a sequence of them. If the
  answers point at a sequence, that is a **scope finding** — report it in the playback as
  a change to what gets delivered first. Do not propose the sequence itself; that's
  design, and intake doesn't do design.
- A forward-only answer to Q4 is a stated constraint, not an assumption. It changes what
  "done and trusted" means, so it belongs in the PRD body rather than the assumptions
  table.
- Any Q5 consumer outside this repo is a PRD risk under the same rule as core Q11 —
  record it whatever the answer.
