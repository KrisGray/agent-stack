# Changelog

Semver. The gallery renders this from the npm tarball.

## 0.2.0

The contract surface — agent-stack becomes self-coherent end to end.

- `/spec` and `/task` prompt templates ship with the package: planning-mode
  specs from `.ai/templates/spec.md` (claim labels, runnable Verify lines,
  `traces_to` requirement IDs) and the single-task TDD cycle that stops
  before committing — the exact dialect the pm kernel's Phase 6 review
  checks for. Shadows the generic agent-skills `/spec` when both are
  installed (intended; pi precedence: project > user > package).
- `templates/spec.md`: the generic spec-template default; `/hire-pm` seeds
  it into `.ai/templates/spec.md` at hire time.
- `templates/AGENTS.md`: the installable global TDD contract (RED/GREEN/
  REFACTOR autopilot loop, spec-driven planning, anti-rationalization
  table) the kernel assumes; `/hire-pm` checks `~/.pi/agent/AGENTS.md` and
  offers to seed it.
- Provenance verified: the rolled-in prompts are original (no version of
  the agent-skills chain ships their like); THIRD-PARTY-NOTICES unchanged.
- `/build`, `/test`, `/review`, `/ship` deliberately stay in the pipeline
  package (@chankov/agent-skills / agent-fleet).

## 0.1.0

First public release.

- Kernel/charter split: `agents/pm.md` (the role contract — phases 0–6, gates,
  recovery, anti-rationalization) + per-project `.ai/pm/charter.md` bindings
  (ground truth, F0, delegation rows, model policy). Worked example:
  `examples/nomgen/`.
- Team personas: pm + eight specialists (adapted from @chankov/agent-skills
  v0.4.2 — see THIRD-PARTY-NOTICES.md) + original researcher, oracle, worker.
- `/pm` launcher; `/hire-pm` interview compiler with archetype binding,
  credential-safe model-catalog extractor (`bin/catalog.py`), audit + slate,
  and model-pin rendering at install (`bin/install.sh -m` / `-p`).
- Pack-based intake interview: core bank, PACKS index with boundary tests,
  AI intake instructions with playback format, 15 archetype packs.
- Test suite: `uv run --with pytest pytest -q tests/` (32 tests).
