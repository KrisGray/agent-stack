# PM reference

Read on demand, not at session start. The persona says when. Charters extend this with domain-specific checklists (see `examples/nomgen/reference.md` for a worked one); this is the generic default.

## Phase 0 scaffolding checklist (generic)

- `.ai/templates/spec.md` exists and carries the six core areas plus Constraints and Out of Scope
- Ship-gate personas (`code-reviewer`, `test-engineer`, `security-auditor`) are installed
- Ground truth (if any) present and within the charter's staleness bound
- Inventory (if any) delegated per the charter

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
<Entities and relationships only. Detail belongs in the feature spec.>

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
Test type: unit | integration | e2e
Fixtures: <what the test needs to exist>
Docs: <docstrings on X; ADR required? y/n>
Done when: new test failed for the right reason, then passed; full suite green; docs in same commit.
```

Every subtask carries acceptance criteria concrete enough to write the RED test from **before** any code exists. A subtask without them is not ready to hand over, and you do not hand it over.
