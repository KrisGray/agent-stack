# Charter — <project>

The project-specific bindings for the pm kernel. The kernel (`agents/pm.md` in agent-stack) defines the role; this file binds it to `<project>`. Where they conflict, the kernel wins. This charter may bind tighter, never weaker.

Every section below is optional — delete what does not apply. An absent section means the thing it governs is not part of this project.

## Project

One paragraph. What this is, what kind of thing it is (library / application / service / migration effort), and the single most important consequence of that for planning.

## Ground truth

The external thing this project maps or depends on that changes without asking you. If there is none, delete this section — the pm skips Phase 0 step 3 and the drift recovery branch.

| Binding | Value |
| --- | --- |
| Artefact | `<file>` — what holds the ground truth locally |
| Refresh | `<command>` — how it is refreshed |
| Staleness bound | when it is too old to trust |
| Drift signal | what goes red / non-empty when ground truth moved |
| Ownership | who changes it, and what notice you get |

## Artefact map additions

Files beyond the kernel's generic map that the pm treats as authoritative or maintains.

| File | Holds | Written by |
| --- | --- | --- |

## Hard boundary additions

Stricter than the kernel. Never weaker.

- 

## Phase 0 inventory

If ground truth needs summarising into an inventory, name the role that does it and where the checklist lives. The pm never reads raw ground truth itself.

- Role: `<agent>`
- Checklist: `.ai/pm/reference.md` (or wherever)
- Output: `docs/<inventory>.md`

## F0 — fixed foundation task

The first task, fixed and unskippable: the proof that a clean checkout works end to end. Typically: install from clean, throwaway environment, one trivial vertical slice, the project's central quality gate green in CI. If you cannot state one, the project is not ready to be planned.

## Delegation additions

Domain rows for the delegation map. Generic rows (researcher, oracle, plan-reviewer, worker, ship gate) are already in the kernel.

| Need | Role |
| --- | --- |

## Anti-rationalization additions

Domain-specific traps. The kernel's rows always apply; these add.

| Thought | Reality |
|---|---|

## Interview and reference

- `.ai/pm/interview.md` — the question bank (charter-seeded; agent-stack `templates/interview.md` is the generic default)
- `.ai/pm/reference.md` — phase detail and templates (agent-stack `templates/pm-reference.md` is the generic default)

## Model policy

Which model each persona runs, and the constraints the assignment must satisfy. The pm verifies pins against this at session start and reports drift.

Constraints worth encoding:

- Ship-gate reviewers (`code-reviewer`, `test-engineer`, `security-auditor`) must not share the worker's model — a reviewer sharing the author's blind spots finds the author's bugs.
- `plan-reviewer` and `oracle` review the pm's output; they must differ from `pm`'s model.
- Recon roles (`scout`, `researcher`) run cheap and fast; reasoning roles run strong.

| Role | Model | Thinking | Why |
| --- | --- | --- | --- |
| pm | | | |
| scout | | | |
| researcher | | | |
| worker | | | |
| code-reviewer | | | |
| test-engineer | | | |
| security-auditor | | | |
| plan-reviewer | | | |
| oracle | | | |

Model IDs are provider-qualified (`provider/model-id`) exactly as they appear in persona frontmatter. `/hire-pm` reads the available catalog from `~/.pi/agent/models.json` (JSONC — strip comments before parsing) and never copies `apiKey` fields anywhere.

## Domain review rules

Where the ship-gate reviewers find this project's blocking rules. Usually the project's `AGENTS.md` — kept there, not here, so reviewers read them from the project rather than from a frozen copy.
