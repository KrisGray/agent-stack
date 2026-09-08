# Spec: [Feature Name]

> **Claim labels are mandatory.** Every statement below carries `[Confirmed]`, `[Target]`, `[Proposed]` or `[Inferred]`. Anything you cannot label goes to Open Questions instead of being asserted. An unlabelled claim in a spec becomes a decision nobody made.

## Objective

[What we're building and why.] Reframe anything vague into testable conditions before planning — "handle records properly" is not an objective, "read and write `<table>` through a repository returning typed models" is.

## Related Specs

- Traces to: `docs/prd.md` → [R1, R3]  ← **required, never empty.** A spec that traces to nothing is out of scope by definition.
- Refines: [path/to/prior-spec.md]
- Supersedes: [path/to/old-spec.md]
- Related: [path/to/adjacent-spec.md]

## Constraints

Things true of the world that this spec must work within, as opposed to choices it makes.

- `[Confirmed]` [Your project's ground truths — external systems, owned-elsewhere contracts, version pins.]
- `[Confirmed]` [...]
- [Anything else this feature is bounded by — schema shape, consumer requirements, ordering against other specs.]

## Out of Scope

Product scope this spec deliberately excludes. Distinct from Boundaries below, which are behavioural rules for the implementing agent. Carry down the relevant PRD non-goals and add anything scoped out during planning.

- [...]

## Tech Stack

`[Confirmed]` [Language, runtime, key libraries with versions, test runner, linters. Only what this spec's tasks touch.]

## Commands

```bash
[install]        # install from clean
[suite]          # full test suite
[fast tests]     # no I/O, for the RED-GREEN loop
[lint / typecheck]
```

## Project Structure

```
[src layout — where the code this spec touches lives]
[tests — mirrored layout, markers if used]
```

## Code Style

[The project's conventions for this surface, with one short canonical example — not a style guide restatement.]

## Testing Strategy

[Runner, markers, what each marker means. The data-layer rule if there is one: integration tests against a real throwaway dependency, never mocks of it — a mock of the thing you map proves nothing about the mapping. Factories over literal fixtures.]

Each task's Verify line **is** the RED test: concrete, runnable, and written before the implementation exists.

## Boundaries

**Always**
- [Carry the project's AGENTS.md Always rules here — only the ones this spec's tasks can trip.]

**Ask first**
- Any new dependency.
- Any change to the public API surface.
- Any CI workflow change.

**Never**
- Modify an existing test rather than add one. If a test must change, stop and report.
- [Carry the project's Never rules here.]

## Success Criteria

Specific and testable. These are what `/review` and `/ship` check the finished feature against.

- [ ] `[Target]` [...]
- [ ] `[Target]` Full suite green.
- [ ] `[Target]` [Lint and typecheck clean.]

## Tasks

Single-session sized, **≤ ~5 files each**, ordered by dependency. One task = one RED→GREEN→REFACTOR→COMMIT cycle; if it needs two failing tests to be meaningful, split it.

Verify must be **concrete and runnable** — it is the RED test the implementing agent writes first, not a description of one. A task whose Verify line cannot be pasted into a shell is not ready for `/task`.

- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: `[one runnable command — the failing test]`
  - Files: [≤5 paths]
  - Depends on: [task numbers, or none]

## Open Questions

Anything unresolved, plus every claim that could not be labelled above. **Must be empty before the spec is approved** — an open question at execution time becomes an assumption made by whoever is typing.
