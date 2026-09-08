# PM reference

Read on demand, not at session start. `pm.md` says when.

## Schema inventory checklist (Phase 0)

Ask `scout` for exactly this. Nothing more — an open-ended request comes back as a wall of DDL.

- Table count per schema
- **Tables with no primary key** — these cannot be mapped normally and each one is a decision
- Cross-schema foreign keys, listed
- CHECK constraints — reflection loses these, so each becomes a Pydantic validator task
- Native enums vs text-with-a-constraint
- Generated columns, and whether each is VIRTUAL or STORED
- Views and materialised views
- Triggers — invisible to reflection; anything writing rows behind our back is a correctness risk
- Column types needing custom handling: arrays, `jsonb`, ranges, `tstzrange`
- Primary key strategy: identity, sequence, natural key, UUID
- Partitioned or inherited tables
- Naming inconsistencies between the three schemas

Write the result to `docs/schema-inventory.md`. Pair with `docs/schema-stats.md` if `scripts/introspect.py` has run: row counts and cardinality decide lazy vs eager defaults and which text columns become `Literal` types. If the local copy is schema-only or synthetic, say so at the top and take those decisions from the user instead.

## PRD template (Phase 3)

```markdown
# <Project> — PRD
Status: draft | approved | superseded
Last updated: <date>

## Problem
<2–4 sentences. Whose pain, and what it costs them today.>

## Users
<Who. Be specific enough that a requirement can be rejected as "not for them".>

## Requirements
R1. <Testable statement. If you can't imagine the failing test, rewrite it.>
R2. ...

## Non-goals
<Explicit. This section is load-bearing — it is how scope creep gets refused later.>

## Data model (sketch)
<Entities and relationships only. Detail belongs in the schema spec.>

## Constraints
<Runtime, deployment target, compliance, performance budgets, hard deadlines.>

## Assumptions
| # | Assumption | Why | Invalidated if |
|---|---|---|---|
| A1 | ... | User deferred Q4 | ... |

## Open questions
<Anything still unresolved. Empty by Phase 4.>

## Changelog
| Date | Change | Reason |
```

## Task template (Phase 5)

```markdown
### T3 — <Title>
Traces to: R2, R5
Depends on: T1, T2
Parallel with: T4
Risk: low | medium | high — <one line>

#### T3.1 — <Subtask>
Acceptance:
  Given <state>
  When <action>
  Then <observable outcome>
Test type: unit | integration (ephemeral DB) | e2e
Fixtures: <what the test needs to exist>
Docs: <docstrings on X; ADR required? y/n>
Done when: new test failed for the right reason, then passed; full suite green; docs in same commit.
```

Every subtask carries acceptance criteria concrete enough to write the RED test from **before** any code exists. A subtask without them is not ready to hand over, and you do not hand it over.
