# Pack: ORM model

Compose with: `schema-change` when Q1 comes back as anything other than mapping-only.

Object-relational mapping work — adding or changing models, relationships, sessions, or
the migration layer that generates from them.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. Does this change the database shape, or only the mapping onto an existing one?
   [default: mapping only]
   - → *if the shape changes:* load `schema-change` and take its top two.

2. Which is the source of truth — the models, or the database? [default: models, with
   migrations generated from them]
   *(A reflected or legacy database inverts most of the assumptions below. Worth one
   follow-up if the answer is unclear rather than discovering it mid-build.)*

3. Who owns the transaction boundary on the code paths this touches — where does the
   commit happen? [default: unchanged from the existing convention]

4. Are new relationships involved, and what should happen to related rows when a parent
   is deleted? [default: no new relationships]
   - → *if any:* is the cascade enforced by the database, the ORM, or neither?

5. Does anything query these tables outside the ORM — raw SQL, reporting, another
   service? [default: no, everything goes through the models]
   *(Skip if composing: `schema-change` Q5 covers the same ground more broadly.)*

## Notes for the PRD

- A "database is the source of truth" answer to Q2 means generated migrations cannot be
  trusted blind. Record it as a constraint on Q10's definition of done, not as trivia.
- Q4 answers where the cascade is enforced by neither side are a data-integrity risk even
  if nothing is currently broken. Log it.
