# Changelog

## 1.0.0 (2026-09-08)

### Features

* **agents:** import specialist personas, author researcher, oracle and worker ([5b13980](https://github.com/KrisGray/agent-stack/commit/5b1398053a8b7bdb2af93303b0d9c591f778dc93))
* **hire-pm:** credential-safe model catalog extractor ([a535d3b](https://github.com/KrisGray/agent-stack/commit/a535d3b029e49bc45675908947a84e3d619f2ebd))
* **install:** render model pin map into persona frontmatter ([ca4a800](https://github.com/KrisGray/agent-stack/commit/ca4a800abe90781f9c0b853de85053a87761e45a))
* **install:** v0.3 one-command install — companions as pinned dependencies ([1222e86](https://github.com/KrisGray/agent-stack/commit/1222e8614f0b6f6d0df338bc71c618508bff84a6))
* **interview:** pack-based intake system, wired into /hire-pm ([969c70b](https://github.com/KrisGray/agent-stack/commit/969c70b7d8c1a0d9f62cab3b691374ab9211be2b))
* **pm:** split pm into a general kernel and a per-project charter ([695e5d3](https://github.com/KrisGray/agent-stack/commit/695e5d3a302a70d9ca2080cf8ac0ea146183f0d4))
* **prompts:** /hire-pm interview compiler with archetype binding ([af7e593](https://github.com/KrisGray/agent-stack/commit/af7e593429f97922407d6f2d6a1b52cd1ece6695))
* **prompts:** ship /pm launcher with charter enforcement ([2a0ebe9](https://github.com/KrisGray/agent-stack/commit/2a0ebe94e919b1c58c705206f43425be5ada5be2))
* **prompts:** v0.2 contract surface — /spec, /task, spec template, global TDD spine ([753a4b3](https://github.com/KrisGray/agent-stack/commit/753a4b3fc737e066147faa3dcb1033959693347b))

### Bug Fixes

* **ci:** also install the git plugin transiently ([78a886a](https://github.com/KrisGray/agent-stack/commit/78a886aafd0259969f09ef383bd561272ec311bc))
* **ci:** fetch full history for release tags; install the conventionalcommits preset ([db68c68](https://github.com/KrisGray/agent-stack/commit/db68c68114dfd0bc86c3f081476c65db277041fb))
* **ci:** green skip while the package is absent from npm (bootstrap gate) ([5dd66eb](https://github.com/KrisGray/agent-stack/commit/5dd66eb1b3c86918a9d8c107836a2cccf3d0532c))
* **ci:** install the changelog plugin transiently — semantic-release does not bundle it ([58c36fe](https://github.com/KrisGray/agent-stack/commit/58c36fe42df2f8d15e411b0e065f3c9ba409640a))
* **ci:** install the conventionalcommits preset the analyzers require ([f9e277e](https://github.com/KrisGray/agent-stack/commit/f9e277e97be45adda4d3b6891bf570f0f92bcc48))
* **ci:** npm ci before semantic-release — plugins live in the local tree ([e79e18d](https://github.com/KrisGray/agent-stack/commit/e79e18d432c5b498e5d087b2377a767239fcc27b))
* **ci:** preset v8 pairs with the generator's writer v8; fetch tags so v0.3.0 is seen ([5fe4026](https://github.com/KrisGray/agent-stack/commit/5fe4026606968928b090e3013a881bcbcd6586e3))
* **ci:** release toolchain as devDependencies — consistent local tree ([ce5d342](https://github.com/KrisGray/agent-stack/commit/ce5d342d20287ddc30e4aafe7e39f8f6b353c252))
* **ci:** secrets are not allowed in workflow-level env — gate moves to job level ([355b9be](https://github.com/KrisGray/agent-stack/commit/355b9bec26a52ad7ae598ac1444ce82ee44f088f))
* **license:** drop post-warranty pointer line for license detection ([6fa7855](https://github.com/KrisGray/agent-stack/commit/6fa7855fc41fa9179f313a84ea161af7c16bc526))
* **license:** restore canonical MIT text, attribution moves to notices ([53625db](https://github.com/KrisGray/agent-stack/commit/53625dbc6147fb2eb02c3453f6330ebb3e7df2b6))
* **publish:** rename to pi-agent-stack — registry name conflict and pi convention ([7668f01](https://github.com/KrisGray/agent-stack/commit/7668f019eec0cfb3ac0e972b83dae29cfb5fa0ef))
* **review:** harden pin rendering, JSONC elision, and install CWD ([e65f455](https://github.com/KrisGray/agent-stack/commit/e65f455981c6420d2a6c5d0b4693376534083f2d))

Versions, commits and this file are managed by semantic-release: `feat` → minor, `fix`/`perf` → patch, breaking → major.

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
