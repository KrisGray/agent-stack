---
description: Implement ONE task from a spec in a strict TDD cycle (execution mode).
argument-hint: "<spec-path> <task-id>"
---
You are in EXECUTION mode for a SINGLE task. This is a different mode from planning:
do not redesign the spec, do not expand scope, do not start the next task.

Spec file: $1
Task to implement: $2
(If only one argument was given, treat the whole of it as the spec path and ask me
which task id to implement.)

1. RED — write the failing test first.
   Take the task's **Verify** line and turn it into a real test in the real test file.
   Run it. Confirm it FAILS, and that it fails for the right reason (behavior missing,
   not a typo or import error). Do not proceed on a test that passes immediately.
   For DB-touching work: write an integration test against the ephemeral test database
   and include the migration; the test must fail before the DDL exists.

2. GREEN — minimal implementation.
   Write the least code that makes the failing test pass. Then run the FULL suite, not
   just the new test. Do not advance while anything is red.

3. REFACTOR — clean up while staying green. Re-run the suite after.

4. STOP and report: what files changed, the final test output, and the conventional
   commit message you propose (`<type>(<scope>): <summary> (Task <id>)`). Do NOT
   begin the next task — I review and commit, then start a fresh session for it.

If implementing this task reveals a flaw in the spec, STOP and tell me. We fix the
spec — the living source of truth — rather than papering over it in code.
