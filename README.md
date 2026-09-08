# agent-stack

A chartered project-manager agent plus the specialist team it delegates to, packaged for [pi](https://github.com/earendil-works/pi-coding-agent).

The core idea is a **kernel / charter split**:

- The **pm kernel** (`agents/pm.md`) is the role contract — phase machine (0–6), hard boundaries, gates, recovery branches, anti-rationalization table. Identical in every project.
- The **charter** (`.ai/pm/charter.md`, per project) binds the kernel to a project: ground truth and how it is refreshed, the fixed foundation task F0, domain delegation rows, hard boundary and anti-rationalization additions, and the model policy. The charter may bind tighter, never weaker; where they conflict, the kernel wins.

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

- **`/spec` and `/task` ship with agent-stack** — they are the kernel's contract surface. `/spec` writes specs in planning mode from `.ai/templates/spec.md` (claim labels, runnable Verify lines, `traces_to` requirement IDs — exactly what the kernel's Phase 6 review checks); `/task` runs one task through a strict TDD cycle and stops before committing. If you also run [@chankov/agent-skills](https://github.com/chankov/agent-skills) or [agent-fleet](https://github.com/chankov/agent-fleet), agent-stack's `/spec` shadows their generic one — that is the intent.
- **`/build`, `/test`, `/review`, `/ship`** come from the pipeline package — the kernel treats them as pluggable and only emits their command lines.
- The **global TDD contract** (`~/.pi/agent/AGENTS.md`) the kernel assumes is shipped as an installable default: `templates/AGENTS.md`. `/hire-pm` checks for it and offers to seed it.

## Install

One command. The package carries its companions as npm dependencies — pi
installs them and loads their resources through agent-stack's manifest:

```bash
pi install npm:pi-agent-stack
# or from git:
pi install git:github.com/KrisGray/agent-stack
```

What arrives with it:

- `pi-subagents` — the team runtime: the `subagent` tool, persona loading, review fan-out (core pi has none of this)
- `@chankov/agent-skills` 0.4.2 — the execution pipeline: `/build`, `/test`, `/review`, `/ship`, `/code-simplify` and its skills (`/spec` and `/task` are agent-stack's own and shadow the generic ones — intended)
- `pi-ask-user` — structured interview questions for `/hire-pm`
- `pi-prompt-template-model` — deterministic pre-steps (the `/hire-pm` catalog feed)

Then the personas (pi packages don't ship agents natively — copy step):

```bash
PKG=~/.pi/agent/npm/node_modules/pi-agent-stack   # global install
# (project install: ./.pi/npm/node_modules/pi-agent-stack; a git checkout of this repo works the same)
bash $PKG/bin/install.sh      # → ~/.pi/agent/agents/   (global)
bash $PKG/bin/install.sh -l   # → ./.pi/agents/         (this project only)
```

> **Already running any of these standalone?** Remove them (`pi remove npm:pi-subagents`, `pi remove npm:@chankov/agent-skills@0.4.2`, `pi remove npm:pi-prompt-template-model`, `pi remove npm:pi-ask-user`) — agent-stack now carries them, and dual installs register duplicate resources.

Then in any project:

```bash
/hire-pm            # the interview: compiles the charter, seeds the
                    # interview system (core bank + archetype packs + intake
                    # instructions + route hint), writes the model pin map —
                    # then installs the personas with the approved pins
# or by hand (PKG as above, or a checkout):
mkdir -p .ai/pm
cp $PKG/templates/charter.md .ai/pm/charter.md   # and fill it in
/pm
```

`/hire-pm` on a project that already has a charter runs as an **audit**: it
verifies installed model pins against the catalog and the charter's policy,
flags drift, and re-pins with `bin/install.sh -p -m .ai/pm/models.json`.

The pm refuses to run unchartered — a project without bindings gets generic mush, which is worse than no pm.

## Model policy

Which model each persona runs is a charter section, not a frozen frontmatter accident. The pm verifies installed pins against the charter at session start and reports drift. Constraints encoded in the template: ship-gate reviewers never share the worker's model; plan-reviewer and oracle differ from pm's; recon runs cheap, reasoning runs strong. `/hire-pm` reads the catalog through a whitelisted projection (credentials stripped by construction), audits existing pins, and suggests per-role assignments from what you can actually run. Credentials never leave the catalog files.

## Layout

```text
agents/            personas: pm kernel + 8 specialists + researcher/oracle/worker
.pi/prompts/       pi prompt templates (shipped natively by the package)
bin/install.sh     persona installer (global or project-local)
templates/         charter; interview system (core bank, PACKS index, AI intake instructions, archetype packs); pm-reference; spec template; global AGENTS.md contract
examples/nomgen/   worked charter/interview/reference extraction
docs/design.md     kernel/charter rationale, coverage map, /hire-pm design
```

## Status

- [x] Kernel/charter split, nomgen extraction, team personas, `/pm` launcher
- [x] `/hire-pm` interview compiler (catalog extractor + pin rendering, tested)
- [x] Pack-based intake interview (core bank, PACKS index, AI intake instructions, 15 archetype packs)
- [x] Package publication (npm + GitHub — listed on the [pi.dev gallery](https://pi.dev/packages))
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
set via `publishConfig`; interactive 2FA; provenance not available outside
CI — fine for the seed release), then on npmjs.com → pi-agent-stack
→ Settings → Trusted Publisher → GitHub Actions
(`KrisGray` / `agent-stack` / `release.yml`). From then on, every release
publishes by OIDC: GitHub proves the workflow's identity to npm, provenance
is automatic, and there is no credential anywhere to leak. (Requires
npm ≥ 11.5 in CI; the workflow pins latest. The package name `agent-stack`
must remain unscoped for the registry match.)

## Provenance

Eight specialist personas are adapted from [@chankov/agent-skills](https://github.com/chankov/agent-skills) v0.4.2 (MIT), which is itself a fork of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (MIT) — imported from the live installed copies, with `model:`/`thinking:` pins added (`planner` verbatim). Upstream has since moved to [agent-fleet](https://github.com/chankov/agent-fleet). The pm kernel, charter format, researcher/oracle/worker personas, the interview pack system, and the scripts are original to this repo. License notices for derived material: [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md); this repo's license: MIT, see [LICENSE](LICENSE).
