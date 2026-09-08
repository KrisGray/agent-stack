# Charter — nomgen-orm

The project-specific bindings for the pm kernel. The kernel (`agents/pm.md` in agent-stack) defines the role; this file binds it to nomgen-orm. Where they conflict, the kernel wins. This charter may bind tighter, never weaker.

Extracted verbatim from the original monolithic `.pi/agents/pm.md` — see `docs/design.md` for the coverage map.

## Project

Archetype: PostgreSQL schema-mapping library (Python).

A Python ORM / data-access library over the **nomgen** PostgreSQL 18 database (`curation`, `app`, `archive` schemas). A library, not an application: the public API is a contract, session lifecycle belongs to the caller, and the nomgen schema is owned elsewhere — this library maps it and never authors a migration against it.

## Ground truth

| Binding | Value |
| --- | --- |
| Artefact | `db/nomgen_schema.sql` — checked-in pg_dump, refreshed deliberately, reviewed as a diff |
| Refresh | `uv run python scripts/introspect.py` (pg_dump **18+**, credentials via `~/.pgpass` and never on a command line) |
| Staleness bound | Run `introspect.py` at the start of any working session; stop if the dump diff is non-empty |
| Drift signal | The drift test — models vs committed dump (CI, every push); committed dump vs live nomgen (introspect diff, human-only) |
| Ownership | nomgen is owned elsewhere. "This feature needs a schema change" is a **hard stop**, not a task |

## Artefact map additions

| File | Holds | Written by |
| --- | --- | --- |
| `db/nomgen_schema.sql` | The schema, as ground truth | `scripts/introspect.py` |
| `docs/schema-inventory.md` | What the DDL contains | `scout`, via you |
| `docs/schema-stats.md` | What DDL cannot express | `scripts/introspect.py` |

## Hard boundary additions

- You **never** accept a password-bearing connection string. The password lives in `~/.pgpass` at mode 0600 and nowhere else; the URL you may see is `postgresql://kris@localhost:5432/nomgen` and never carries more.

## Phase 0 inventory

- Role: `scout`
- Checklist: `.ai/pm/reference.md` (schema inventory checklist)
- Output: `docs/schema-inventory.md`
- `scout` may run ad-hoc read-only SQL (`SELECT` / `EXPLAIN`, nothing else, ever) against localhost for follow-ups the inventory doesn't answer. The pm does not connect — not for safety, but because reading raw schema output costs the context the plan needs.

## F0 — fixed foundation task

Clean-checkout install, throwaway PG18 container loading the nomgen DDL, one trivial model, drift test green in CI. Never skipped, reordered or merged.

## Delegation additions

| Need | Role |
| --- | --- |
| External facts about SQLAlchemy, Pydantic or PG18 behaviour | `researcher` |
| nomgen's actual shape; read-only SQL against localhost | `scout` |

## Anti-rationalization additions

| Thought | Reality |
|---|---|
| "The user described the schema, that's enough." | It is not. Descriptions omit exactly what breaks ORM mapping — missing primary keys, triggers, CHECK constraints. |
| "It's localhost, I'll query it myself." | Safety was never the reason. Raw output eats the context you need for the plan. Delegate to `scout`. |

## Interview and reference

- `.ai/pm/interview.md` — the nomgen question bank (Postgres/ORM-specific)
- `.ai/pm/reference.md` — schema inventory checklist + PRD/task templates

## Model policy

Constraints: ship-gate reviewers must not share the worker's model; `plan-reviewer` and `oracle` must differ from `pm`'s.

| Role | Model | Thinking | Why |
| --- | --- | --- | --- |
| pm | deepinfra/deepseek-ai/DeepSeek-V4-Pro-0813 | high | Interview quality, spec review, long horizon |
| scout | zai/glm-5.3-flash | low | Fast cheap recon |
| researcher | zai/glm-5.3-flash | low | Fast evidence gathering |
| worker | zai/glm-5.3 | high | Agentic implementation |
| builder | zai/glm-5.3 | high | Agentic implementation (execution-side) |
| planner | *(package default)* | — | Not invoked by pm |
| code-reviewer | deepinfra/deepseek-ai/DeepSeek-V4-Pro-0813 | high | Ship gate — differs from worker |
| test-engineer | deepinfra/Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo | — | Ship gate — differs from worker |
| security-auditor | deepinfra/ByteDance/Seed-2.0-code | — | Ship gate — differs from worker |
| plan-reviewer | deepinfra/MiniMaxAI/MiniMax-M3 | high | Second opinion — differs from pm |
| oracle | deepinfra/MiniMaxAI/MiniMax-M3 | high | Second opinion — differs from pm |
| documenter | zai/glm-5.3-flash | low | Docs drafting (execution-side) |

## Domain review rules

The nomgen-specific blocking rules for the ship gate live in the project's `AGENTS.md` (Review checklist section). Reviewers read them from the project, not from here.
