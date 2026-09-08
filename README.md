# pi-agent-stack

[![npm version](https://img.shields.io/npm/v/pi-agent-stack.svg)](https://www.npmjs.com/package/pi-agent-stack)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A chartered project-manager agent plus the specialist team it delegates to, packaged for [pi](https://github.com/earendil-works/pi-coding-agent).

## The stack

```text
 ┌────────────────────────────────────────────────────────────────┐
 │  global contract      ~/.pi/agent/AGENTS.md — the TDD spine   │
 │      (shipped as templates/AGENTS.md; seeded by /hire-pm)     │
 ├────────────────────────────────────────────────────────────────┤
 │  pm kernel            agents/pm.md — phases 0–6, gates,       │
 │                       recovery, anti-rationalization          │
 │                       (identical in every project)            │
 ├────────────────────────────────────────────────────────────────┤
 │  charter              .ai/pm/charter.md — ground truth, F0,   │
 │                       domain rows, model policy               │
 │                       (binds tighter, never weaker)           │
 ├────────────────────────────────────────────────────────────────┤
 │  pipeline             /spec → /task → /review → /ship         │
 │                       (pi-subagents runtime + pipeline pkg)   │
 └────────────────────────────────────────────────────────────────┘
   precedence: contract > kernel > charter > conversation
```

The **pm kernel** (`agents/pm.md`) is the role contract — identical in every project. The **charter** (`.ai/pm/charter.md`, per project) binds it to a project: ground truth and how it is refreshed, the fixed foundation task F0, domain delegation rows, hard boundaries, and the model policy. Where they conflict, the kernel wins; the charter may bind tighter, never weaker.

Generality in the process, specificity in the charter. `examples/nomgen/` is the worked extraction from the project this stack was born in.

## The team

| Persona | Job | Invoked by |
| --- | --- | --- |
| `pm` | Owns *what* gets built and in what order. Interviews, PRD, feature graph, gates. Never writes code. | you, via `/pm` |
| `researcher` | Evidence-backed external facts, version-pinned, citations required | pm |
| `scout` | Fast read-only recon of codebase and artefacts | pm (as ground-truth role when the charter says so) |
| `oracle` | Adversarial second opinion on expensive-to-reverse decisions | pm |
| `plan-reviewer` | Critiques the pm's own PRD and feature graphs | pm |
| `worker` | One spec task, strict TDD cycle, stops before committing | pm proposes, you run |
| `code-reviewer` | Ship gate: correctness | `/review`, `/ship` |
| `test-engineer` | Ship gate: tests and coverage | `/review`, `/ship` |
| `security-auditor` | Ship gate: security | `/review`, `/ship` |
| `builder`, `planner`, `documenter` | Execution-side utilities | you, ad hoc |

The pm sits **above** a `/spec → /task → /review → /ship` pipeline and never runs those commands itself — it decides what runs, reads the results, and gates. The pipeline is split across packages, deliberately:

- **`/spec` and `/task` ship with pi-agent-stack** — they are the kernel's contract surface. `/spec` writes specs in planning mode from `.ai/templates/spec.md` (claim labels, runnable Verify lines, `traces_to` requirement IDs — exactly what the kernel's Phase 6 review checks); `/task` runs one task through a strict TDD cycle and stops before committing. If you also run [@chankov/agent-skills](https://github.com/chankov/agent-skills) or [agent-fleet](https://github.com/chankov/agent-fleet), this package's `/spec` shadows their generic one — that is the intent.
- **`/build`, `/test`, `/review`, `/ship`** come from the pipeline package — the kernel treats them as pluggable and only emits their command lines.
- The **global TDD contract** (`~/.pi/agent/AGENTS.md`) the kernel assumes is shipped as an installable default: `templates/AGENTS.md`. `/hire-pm` checks for it and offers to seed it.

## Install

One command. The package carries its companions as npm dependencies — pi
installs them and loads their resources through the package manifest:

```bash
pi install npm:pi-agent-stack
# or from git:
pi install git:github.com/KrisGray/pi-agent-stack
```

What arrives with it:

- `pi-subagents` — the team runtime: the `subagent` tool, persona loading, review fan-out (core pi has none of this)
- `@chankov/agent-skills` 0.4.2 — the execution pipeline: `/build`, `/test`, `/review`, `/ship`, `/code-simplify` and its skills
- `pi-ask-user` — structured interview questions for `/hire-pm`
- `pi-prompt-template-model` — deterministic pre-steps (the `/hire-pm` catalog feed)

Then the personas (pi packages don't ship agents natively — copy step):

```bash
PKG=~/.pi/agent/npm/node_modules/pi-agent-stack   # global install
# (project install: ./.pi/npm/node_modules/pi-agent-stack; a git checkout of this repo works the same)
bash $PKG/bin/install.sh      # → ~/.pi/agent/agents/   (global)
bash $PKG/bin/install.sh -l   # → ./.pi/agents/         (this project only)
```

> **Already running any of these standalone?** Remove them (`pi remove npm:pi-subagents`, `pi remove npm:@chankov/agent-skills@0.4.2`, `pi remove npm:pi-prompt-template-model`, `pi remove npm:pi-ask-user`) — this package now carries them, and dual installs register duplicate resources.

## Quick start

Your first hour in a project:

1. **Install** (above), then in the project root run `/hire-pm`.
2. **The interview.** You confirm-or-correct proposals — never author from a blank page: the project *archetype* (PostgreSQL schema-mapping library, Python data pipeline…), ground truth and its refresh, the fixed foundation task F0, domain boundaries, and a model slate drawn from *your* configured catalog. Nothing is written until you approve the full playback.
3. **`/hire-pm` writes** `.ai/pm/` — the charter, the seeded interview system, the model pin map — and installs the personas with your approved pins.
4. **`/pm` opens the working relationship.** It reads the contract, charter and task state, restates its constraints in five lines or fewer, and states which phase it is entering. If work is in flight, it *resumes* — it never re-interviews.
5. **The loop.** The pm announces the next feature and emits `/spec "<feature>"`; you run it in a fresh session; the pm reviews what came back (runnable Verify lines, labelled claims, requirement traces); it emits `/task` lines; workers implement in strict TDD and stop before committing; `/review` + `/ship` gate the merge behind three isolated reviewers. The pm decides and gates; you execute.

Re-running `/hire-pm` on a chartered project is an **audit**: it verifies installed pins against the catalog and the charter's policy, flags drift, and re-pins with your approval.

The pm refuses to run unchartered — a project without bindings gets generic mush, which is worse than no pm.

## Model policy

Which model each persona runs is a charter section, not a frozen frontmatter accident. The frontmatter `model:` line is the only mechanism pi reads, so the *policy* lives in reviewable files — the charter's table (the why) and `.ai/pm/models.json` (the pin map) — and `bin/install.sh -m` renders them into frontmatter. The pm verifies installed pins against the charter at session start and reports drift. Constraints encoded in the template: ship-gate reviewers never share the worker's model; plan-reviewer and oracle differ from pm's; recon runs cheap, reasoning runs strong. The shipped pins are bootstrap defaults matching the author's catalog — `/hire-pm` audits them against *yours* and proposes a slate from what you can actually run.

## Security

The model catalog lives in `~/.pi/agent/models.json` next to live API keys, and this package treats that file accordingly:

- The **only** sanctioned reader is `bin/catalog.py` — a *whitelisted* field projection: `apiKey`, `baseUrl`, `headers` and any future auth-shaped field cannot appear in its output by construction. Leak checks are part of the test suite (`tests/test_catalog.py`).
- Parse errors report position only — never file content.
- `/hire-pm` consumes only the redacted catalog output, never the file; credentials cannot appear in charters, prompts, or the pin map because nothing carries them.
- Nothing in the package makes network calls on its own; no telemetry. The catalog extractor reads two local files and prints.

## Working with the pm

| It does | It never does |
| --- | --- |
| Interviews you; writes the PRD and feature graph | Writes or patches code — "just a small fix" included |
| Emits the exact command line for you to run | Runs `/spec`, `/task`, `/review`, `/ship` itself |
| Reviews every spec: runnable Verify lines, claim labels, requirement traces | Marks a task done — you commit; `/ship` closes |
| Delegates recon and second opinions; gates behind three reviewers | Accepts secrets in prose, prompts or URLs |
| Stops at every gate: what completed, what's next, what could go wrong | Re-interviews a project mid-flight — it resumes instead |

## The interview

Project intake is a **pack system**: a core bank of five questions plus archetype packs (`orm-model`, `data-pipeline`, `web-app`, `cli-tool`, …), routed from the first answer, at most two packs composing, five pack questions max. `AI-INSTRUCTIONS.md` owns the intake procedure and playback format; `PACKS.md` owns the boundary tests that separate close archetypes (does a user log in? does the model choose what to call next?). `/hire-pm` seeds the charter with a route *hint* — intake verifies it, never assumes it.

## Layout

```text
agents/            personas: pm kernel + 8 specialists + researcher/oracle/worker
.pi/prompts/       pi prompt templates (shipped natively by the package)
bin/               installer (personas + pins) and the catalog extractor
templates/         charter; interview system (core bank, PACKS index, AI intake instructions, archetype packs); pm-reference; spec template; global AGENTS.md contract
examples/nomgen/   worked charter/interview/reference extraction
docs/design.md     kernel/charter rationale, coverage map, /hire-pm design
```

## Troubleshooting

- **`/pm` refuses to run** — no `.ai/pm/charter.md`. By design. Run `/hire-pm`, or copy `templates/charter.md` there and fill it in.
- **Prompt conflict notices at startup** — pi's precedence is project > user > package. This package's `/spec` intentionally shadows the generic pipeline one. If you see duplicates of `build`/`test`/`review`/`ship`, you have a standalone companion package installed — remove it (see Install).
- **Personas don't appear in `subagent list`** — the runtime isn't loaded. `pi install npm:pi-agent-stack` provides `pi-subagents`; then run the persona copy step.
- **Pins reference models you can't run** — the shipped defaults match the author's catalog. Run `/hire-pm` (audit mode) to propose a slate from yours.
- **`CATALOG_SCRIPT_MISSING`** — the persona copy step hasn't run from an installed package (≥ 1.0.1). See Install.

## Status

- [x] Kernel/charter split, nomgen extraction, team personas, `/pm` launcher
- [x] `/hire-pm` interview compiler (catalog extractor + pin rendering, tested)
- [x] Pack-based intake interview (core bank, PACKS index, AI intake instructions, 15 archetype packs)
- [x] Package publication (npm + GitHub — listed on the [pi.dev gallery](https://pi.dev/packages/pi-agent-stack))
- [x] Installable generic global contract (`templates/AGENTS.md`, seeded by `/hire-pm`)

## Releasing

Automated by [semantic-release](https://semantic-release.gitbook.io): push
conventional commits to `main` and CI does the rest — `feat` bumps minor,
`fix`/`perf` bump patch, breaking changes bump major, and
`docs`/`chore`/`refactor` release nothing. On a release it runs the test
suite, bumps `package.json`, prepends `CHANGELOG.md`, commits the release
back to `main`, tags, opens the GitHub release, and publishes to npm with
provenance.

Publishing auth is OIDC trusted publishing — no npm tokens exist, ever.
Bootstrap once by hand (the trusted-publisher config needs the package to
exist): `npm login` locally, `npm publish` from the repo (public access is
set via `publishConfig`), then on npmjs.com → pi-agent-stack
→ Settings → Trusted Publisher → GitHub Actions
(`KrisGray` / `pi-agent-stack` / `release.yml`). From then on, every release
publishes by OIDC: GitHub proves the workflow's identity to npm, provenance
is automatic, and there is no credential anywhere to leak. (Requires
npm ≥ 11.5 in CI; the workflow pins latest.)

## Provenance

Eight specialist personas are adapted from [@chankov/agent-skills](https://github.com/chankov/agent-skills) v0.4.2 (MIT), which is itself a fork of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (MIT) — imported from the live installed copies, with `model:`/`thinking:` pins added (`planner` verbatim). Upstream has since moved to [agent-fleet](https://github.com/chankov/agent-fleet). The pm kernel, charter format, researcher/oracle/worker personas, the interview pack system, and the scripts are original to this repo. License notices for derived material: [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md); this repo's license: MIT, see [LICENSE](LICENSE).

Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md).
