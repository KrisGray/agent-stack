# Contributing

## Setup

```bash
git clone https://github.com/KrisGray/pi-agent-stack
cd pi-agent-stack
npm install        # dev toolchain (semantic-release etc.) — consumers never get these
```

Tests need Python via [uv](https://docs.astral.sh/uv/):

```bash
uv run --with pytest pytest -q tests/
```

## Checks before you push

```bash
uv run --with pytest pytest -q tests/        # must pass
npx markdownlint-cli README.md templates/*.md .pi/prompts/*.md docs/*.md
```

The markdownlint config lives in `.markdownlint.json`. `agents/` and
`examples/` are **deliberately excluded** — see provenance below.

## Commits drive releases

Conventional commits are not stylistic here; they *are* the release process
(semantic-release): `feat` → minor, `fix`/`perf` → patch, `BREAKING CHANGE`
→ major, everything else releases nothing. CI runs the suite, then versions,
changelogs, tags and publishes to npm by OIDC trusted publishing. Never bump
versions or edit the changelog by hand.

## Provenance rules — read before touching agents/ or examples/

`THIRD-PARTY-NOTICES.md` maps every derived file at byte precision. This has
a consequence: **do not reformat, rewrap, or "clean up"** files in `agents/`
(eight personas adapted from @chankov/agent-skills v0.4.2 — `planner` is
verbatim upstream) or `examples/nomgen/` (verbatim extraction). Byte
preservation is the documented provenance claim; a tidy diff falsifies it.
If you add genuinely new derived content, add the notices row in the same
commit.

Everything else — the pm kernel, `researcher`/`oracle`/`worker`, the charter
format, the interview pack system, `/spec`, `/task`, `/hire-pm`, the scripts —
is original and normal rules apply.

## What to keep in dialect

The parts of this package form one contract: the pm kernel's Phase 6 review
checks exactly for what `/spec` produces (claim labels, runnable Verify
lines, `traces_to` IDs) and what `templates/spec.md` shapes. Changes to any
one of the three must be checked against the other two. `docs/design.md`
records the rationale — read it before restructuring, and update it after.

## Credit

Derived material is MIT, © 2025 Addy Osmani, via @chankov/agent-skills; this
repo's original material is MIT, © 2025 Kristian Gray.
