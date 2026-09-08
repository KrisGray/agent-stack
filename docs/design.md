# agent-stack design

Why this package is shaped the way it is.

## The kernel / charter split

The original pm persona (`nomgen-orm/.pi/agents/pm.md`) was simultaneously two things:

1. A **role contract** — phases, gates, recovery branches, anti-rationalization — that is identical for any project run under strict TDD with the `/spec → /task → /review → /ship` pipeline.
2. A **project charter** — nomgen's ground truth, drift test, F0, delegation rows, interview bank — that is meaningless outside that repo.

Packaging it required separating them. `agents/pm.md` in this package is the kernel: the role contract, identical everywhere, referencing `.ai/pm/charter.md` for every project-specific binding. The charter is a small per-project file that may bind tighter but never weaker; where they conflict, the kernel wins.

The design constraint that matters: **generality in the process, specificity in the charter.** A generalized pm that emits vague charters is worse than no pm. The current pm's value is lines like "F0 is fixed: PG18 container, drift test green in CI" — concrete, checkable, unskippable. Whatever produces charters (today: hand-written from `templates/charter.md`; later: `/hire-pm`) must compile specificity, not average it away.

### Precedence

```
global AGENTS.md contract  >  pm kernel  >  project charter  >  conversation
```

The kernel is a layer on top of the global TDD contract (where they conflict, the contract wins). The charter binds the kernel to a project. Decisions live in files, never in conversation.

### Coverage map — the nomgen extraction

Every nomgen-specific element of the original monolithic `pm.md`, and where it now lives (`examples/nomgen/charter.md` unless noted):

| Original element | New home |
| --- | --- |
| pgpass / password-free URL boundary | Charter → Hard boundary additions |
| `db/nomgen_schema.sql` + `scripts/introspect.py` artefact rows | Charter → Artefact map additions |
| `docs/schema-inventory.md` / `schema-stats.md` rows | Charter → Artefact map additions |
| Phase 0 steps 3–4 (dump freshness, scout inventory) | Kernel generalized: ground truth + inventory per charter |
| F0 fixed content (PG18 container, trivial model, drift test) | Charter → F0 |
| Recovery: "the drift test goes red" | Kernel generalized: "ground truth moved", signal named by charter |
| Delegation rows: SQLAlchemy/Pydantic/PG18 facts → researcher; nomgen shape → scout | Charter → Delegation additions |
| Anti-rationalization: "user described the schema", "it's localhost" | Charter → Anti-rationalization additions |
| Interview bank (Postgres/ORM questions) | `examples/nomgen/interview.md` (copied verbatim) |
| Schema inventory checklist | `examples/nomgen/reference.md` (copied verbatim) |
| PRD + task templates | `templates/pm-reference.md` (generic default; identical wording) |

The generic halves of `reference.md` (PRD template, task template) moved to the package default. The nomgen halves stayed with the nomgen example.

## The personas

Eight specialist personas were imported from the live `~/.pi/agent/agents/` copies (which carry local customizations; they differ from the upstream `@chankov/agent-skills` v0.4.2 files). Three referenced roles existed nowhere on disk despite appearing in the pm's delegation map, and are authored here:

- **researcher** — evidence-backed external facts, version-pinned, citations required. Tools include `web_search` / `fetch_content`; verify at install that subagents can be granted them.
- **oracle** — adversarial second opinion on expensive-to-reverse decisions, with a decision-memo output.
- **worker** — the `/task` discipline as a subagent persona: one task, RED-GREEN-REFACTOR, stops before committing.

Pi packages ship prompts, skills, extensions and themes natively — **not** personas. `bin/install.sh` copies `agents/*.md` into pi's agent directories, the same pattern `@chankov/agent-skills` uses.

## Model policy

Model pins live in persona frontmatter (the only mechanism pi reads), but the *policy* — which role runs what, and why — lives in the charter. The pm verifies pins against the charter at session start and reports drift. This makes the policy reviewable per project and diffable in git, instead of frozen in eleven frontmatters nobody compares.

Hard constraints encoded in the template:

- Ship-gate reviewers must not share the worker's model.
- `plan-reviewer` and `oracle` must differ from `pm`'s model.
- Recon runs cheap; reasoning runs strong.

## `/hire-pm` (interview compiler)

Built (`.pi/prompts/hire-pm.md`). A prompt template that runs in the main session and *hires* the pm for a project: an interview that produces the charter, the seeded interview system, the reference file, the model pin map, and the installed, pinned personas. Re-running it against an existing charter enters **migration mode**: audit and amend, not re-interview.

### Implementation notes

- A deterministic pre-step runs `bin/catalog.py` (installed as `~/.pi/agent/bin/agent-stack-catalog.py`) before the LLM turn, so the catalog enters the session *already redacted*. The script projects the two catalog files through a **field whitelist** — `apiKey`, `baseUrl`, `headers` cannot pass through by construction, and parse errors report position only. Tested in `tests/test_catalog.py`, including the leak checks.
- The approved policy lands in `.ai/pm/models.json` (`role → {model, thinking?}`), the machine-readable pin map. `bin/install.sh -m` renders it into persona frontmatter at copy time (`-p` re-pins without copying); the charter carries the human-readable table with the *why*. Tested in `tests/test_install.py`.
- **Archetype binding**: the interview's first question fixes the project archetype — the class of project the pm is an expert for (PostgreSQL schema-mapping library, Python data pipeline, …). The charter records it; the kernel instructs the pm to adopt its vocabulary, failure modes and review focus. Generality stays in the process, expertise in the archetype.
- **The interview pack system** (`templates/interview.md` + `templates/interview/`): the core bank owns questions, budget and routing; `PACKS.md` owns the pack table and boundary tests; `AI-INSTRUCTIONS.md` owns the intake procedure and playback format. The archetype packs encode failure modes someone has actually hit. `/hire-pm` copies the trio **verbatim** and seeds only a routing hint in the charter (at most two packs, chosen per the composition rules) — the pack files are never edited or extended ad hoc at hire time, because a generic question asked confidently reads as covered in the playback. The pm's Phase 1 reads `AI-INSTRUCTIONS.md` before the first question and routes from core Q1, verifying or correcting the hint.
- `.ai/pm/agent-stack-path` caches the checkout location so repeat hires and audits don't re-ask.

### Interview flow

1. **Project shape** (multiple choice where possible — pi's ask-user extension gives structured options with a freeform fallback): library / application / service / migration. Greenfield or existing. What is the source of truth — a database, an API contract, upstream docs, the user? This answer decides whether the charter gets a ground-truth section, whether Phase 0 gets an inventory step, and what "drift" means for this project.
2. **Process**: which ship-gate personas, PRD formality, spec template baseline.
3. **Domain**: what is blocking in review for this stack — proposed by the session from earlier answers, confirmed by the user. The user proposes nothing here; they confirm or correct.
4. **F0**: the session proposes the fixed foundation task from the project shape; the user approves. Users do not know what F0 should be; asking them open-endedly produces mush.
5. **Playback**: the charter is read back in full. Explicit approval or it does not get written.

### Model selection

The user's requirement: `/hire-pm` reads the models actually available to this pi install and suggests better ones when existing pins are substandard.

- **Catalog source**: `~/.pi/agent/models.json` (the user's configured providers and models; JSONC — strip comments before parsing) and `~/.pi/agent/models-store.json` (the fetched catalog cache). Parse provider-qualified IDs, `reasoning`, `contextWindow`, `maxTokens`, thinking-level maps. Never display or copy `apiKey` fields anywhere — model IDs flow into charters; credentials never leave that file.
- **Role requirements** drive the assignment: interview/review roles need strong reasoning and long context; recon needs speed and cost; the ship gate needs strength *and* diversity (the constraints above).
- **Audit mode** when migrating a project that already has pins: flag (a) models absent from the catalog, (b) deprecated entries, (c) diversity-rule violations, (d) role mismatches — a flash model pinned to code-reviewer is a finding. Every flag cites catalog evidence or is labelled `[Inferred]`.
- **Suggestion**: per role, recommended + two alternatives from *their* catalog, as multiple choice. Never suggest models the user cannot run.
- **Verification**: contested picks can be delegated to `researcher` for evidence-backed confirmation (current docs, benchmark standing, deprecation notices) rather than trusting session memory of model quality — the same discipline the stack applies to library facts.
- **Render**: the approved policy is written to the charter and rendered into each persona's frontmatter at install.

## Dependency: the global contract (v0.2: shipped)

The kernel assumes a global `~/.pi/agent/AGENTS.md` TDD contract above it ("You are a layer on top of the global TDD contract"). Consumers without one lose the RED/GREEN/REFACTOR spine the whole stack leans on. **v0.2 ships the spine** as `templates/AGENTS.md`, and closes the wider coherence gap in the same move: `/spec` and `/task` now ship in `.pi/prompts/`, so the kernel's contract surface (planning-mode specs from `.ai/templates/spec.md`, claim labels, runnable Verify lines, `traces_to` IDs, the stop-before-commit task discipline) comes from the same package as the kernel that reviews it. Previously the shipped-world `/spec` was the generic skill-delegating one, and the kernel's Phase 6 checklist mismatched what it produced.

Provenance was verified before rolling in: the user's `/spec` and `/task` are original implementations of their own AGENTS.md contract — no version of `@chankov/agent-skills` (0.1.0 → 1.0.8) shipped a task prompt, and every shipped spec prompt is the unrelated generic one; upstream addyosmani/agent-skills ships neither. THIRD-PARTY-NOTICES therefore still covers the eight persona files only. `/build`, `/test`, `/review`, `/ship` and the skills deliberately stay in the pipeline package — the kernel emits their command lines and reads results; owning them would collapse the layering and create a living fork of work upstream has already moved to agent-fleet.

## Migration path for nomgen-orm

1. Copy `examples/nomgen/charter.md` → `nomgen-orm/.ai/pm/charter.md`
2. Replace `nomgen-orm/.pi/agents/pm.md` with this package's kernel (or remove it and rely on the global install)
3. Verify: `/pm` session start restates constraints including the charter's bindings; nothing else changes
