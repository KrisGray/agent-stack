---
description: Plan a feature as a spec (planning mode, no code). Defaults to a single spec file.
argument-hint: "<feature description> [--design] [--prd]"
---

You are in PLANNING mode. In this mode you write specs; you do NOT implement.
(Planning and execution are different mindsets — an agent that plans thinks through
edge cases, an agent that executes rushes to ship. Never do both in one pass.)

Task: read `.ai/templates/spec.md` and produce a spec for the feature described at
the end of this message. Save it to `.ai/specs/<kebab-case-feature-name>.md`.

## Default behavior — stay light

Produce a SINGLE spec file. Do NOT create a PRD or a design doc unless I include a
flag below, or the work clearly meets an escalation trigger.

Flags I may add after the feature description:
--design also produce `.ai/design/<name>.md` from `.ai/templates/design.md` FIRST,
then derive the spec(s) from it.
--prd also produce `.ai/prd/<name>.md` from `.ai/templates/prd.md` FIRST.

Escalation triggers (use judgement — if one clearly applies but I didn't flag it,
ASK me before escalating; do not silently generate extra documents):

- a non-trivial relational schema, or a migration with data-loss risk
- three or more integration points, or new GCP infrastructure
- work that will obviously span multiple sessions or spawn multiple specs

## Rules for the spec you produce

1. Every Task MUST have a concrete, runnable **Verify** line — it is the failing
   test the implementing agent writes first. No task without one.
2. [CRITICAL INTERVIEW GATE] If the feature description is vague, or if there are
   more than 2 critical unknowns (e.g., storage, edge cases, error behavior),
   DO NOT generate the spec file yet. Instead, print an "Interview Checklist"
   to the terminal and STOP for my input. Only write the file once these are cleared.
3. Make decisions explicit. Where you would otherwise guess (storage, expiry,
   error behavior, libraries), either choose and record it under Constraints, or
   list it under Open Questions and STOP for my input.
4. Keep scope tight: fewer, well-bounded tasks beat many vague ones. Put everything
   you are NOT building under "Out of scope."
5. Match detail to complexity. A small feature gets a short spec.
6. Output is the spec file only. Do NOT write implementation code in this mode.

After saving, show me the spec and pause for review — I will correct assumptions
before any code is written.

---

Feature to spec:
$ARGUMENTS
