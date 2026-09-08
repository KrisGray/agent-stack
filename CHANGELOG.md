# Changelog

Semver. The gallery renders this from the npm tarball.

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
