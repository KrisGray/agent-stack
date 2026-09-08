# Changelog

Versions, commits and this file are managed by semantic-release: `feat` → minor, `fix`/`perf` → patch, breaking → minor while pre-1.0.

## 0.3.0

One-command install — the package now distributes its companions.

- npm dependencies, pinned and loaded through the pi manifest:
  `pi-subagents` 0.66.0 (team runtime), `@chankov/agent-skills` 0.4.2
  (pipeline: /build /test /review /ship /code-simplify + skills — spec/plan
  excluded, agent-stack's own supersede them), `pi-ask-user` 0.15.0,
  `pi-prompt-template-model` 0.12.2 (the /hire-pm catalog pre-step).
- Plain dependencies, not bundled: bundling pi-subagents' transitive tree
  would ship a 22 MB tarball; npm fetches at install time and the agent-stack
  tarball stays ~59 kB.
- Install docs rewritten: `pi install npm:pi-agent-stack` is the whole setup,
  plus the persona copy-step; migration note for existing standalone
  installs of the same packages.
- THIRD-PARTY-NOTICES gains a distributed-dependencies section (all MIT,
  authored and licensed by their maintainers).

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
