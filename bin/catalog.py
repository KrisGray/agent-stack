#!/usr/bin/env python3
"""agent-stack model catalog extractor for /hire-pm.

Reads the pi provider configuration (~/.pi/agent/models.json, JSONC) and the
fetched catalog cache (~/.pi/agent/models-store.json, JSONC) and prints a
redacted, merge-enriched catalog as JSON on stdout.

Security contract:
  - apiKey (and any *key*/*secret*/*token*/*credential* field), baseUrl,
    headers and auth material NEVER appear in the output.
  - Parse errors are reported by position only; file content is never echoed.

Output shape:
  {
    "generated":   "<iso8601 utc>",
    "configured":  { "<provider>": [ {id, qualified, name?, reasoning?,
                     contextWindow?, maxTokens?, thinkingLevels, cost?} ] },
    "unconfigured":{ "<provider>": ["<model id>", ...] },   # store-only
    "storeMissing": false
  }

Exit codes: 0 ok, 2 models.json missing, 3 unparseable input.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

EXIT_MISSING = 2
EXIT_PARSE = 3

# Whitelist of model fields that may appear in the output. Everything else —
# apiKey, baseUrl, headers, api, etag, any future auth field — is dropped by
# construction. Never widen this without reviewing what new fields carry.
KEEP_MODEL_FIELDS = ("name", "reasoning", "contextWindow", "maxTokens", "cost")


def agent_dir() -> Path:
    if pi_dir := os.environ.get("PI_CONFIG_DIR"):
        return Path(pi_dir)
    return Path.home() / ".pi" / "agent"


def strip_jsonc(text: str) -> str:
    """Strip // and /* */ comments and trailing commas, string-safely."""
    out = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
        elif c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def elide_trailing_commas(text: str) -> str:
    """Remove commas whose next non-space character closes an object/array.
    String-aware: a comma inside a string value is data and stays."""
    out = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == ",":
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if j < n and text[j] in "}]":
                i += 1  # trailing comma: drop it, keep the whitespace
                continue
        out.append(c)
        i += 1
    return "".join(out)


def parse_error(path: Path, exc: json.JSONDecodeError) -> None:
    # Position only — never echo file content (it may sit next to credentials).
    print(f"catalog: {path.name} is not valid JSONC (line {exc.lineno}, column {exc.colno})", file=sys.stderr)
    sys.exit(EXIT_PARSE)


def thinking_levels(model: dict) -> list[str]:
    """Non-null keys of thinkingLevelMap / reasoningEffortMap (top level or in
    compat), first mapping found wins."""
    sources = [model]
    compat = model.get("compat")
    if isinstance(compat, dict):
        sources.append(compat)
    for src in sources:
        for key in ("thinkingLevelMap", "reasoningEffortMap"):
            mapping = src.get(key)
            if isinstance(mapping, dict):
                return [k for k, v in mapping.items() if v is not None]
    return []


def catalog_model(provider: str, model: dict, store_entry: dict | None) -> dict:
    """Whitelisted projection of one model; credentials cannot pass through."""
    out = {
        "id": model.get("id"),
        "qualified": f"{provider}/{model.get('id')}",
        "thinkingLevels": thinking_levels(model),
    }
    for src in (model, store_entry or {}):
        for field in KEEP_MODEL_FIELDS:
            if field not in out and src.get(field) is not None:
                out[field] = src[field]
    # thinking info may only exist on the store entry
    if not out["thinkingLevels"] and store_entry:
        out["thinkingLevels"] = thinking_levels(store_entry)
    return out


def main() -> None:
    base = agent_dir()
    config_path = base / "models.json"
    store_path = base / "models-store.json"

    if not config_path.exists():
        print(f"catalog: {config_path} not found — no providers configured for this pi install", file=sys.stderr)
        sys.exit(EXIT_MISSING)

    try:
        config = json.loads(elide_trailing_commas(strip_jsonc(config_path.read_text(encoding="utf-8-sig"))))
    except json.JSONDecodeError as exc:
        parse_error(config_path, exc)

    store: dict = {}
    store_missing = not store_path.exists()
    if not store_missing:
        try:
            store = json.loads(elide_trailing_commas(strip_jsonc(store_path.read_text(encoding="utf-8-sig"))))
        except json.JSONDecodeError as exc:
            parse_error(store_path, exc)

    configured: dict[str, list[dict]] = {}
    unconfigured: dict[str, list[str]] = {}

    providers = config.get("providers", {})
    for provider, block in providers.items():
        models = block.get("models", []) if isinstance(block, dict) else []
        store_models = {}
        store_block = store.get(provider)
        if isinstance(store_block, dict) and isinstance(store_block.get("models"), list):
            store_models = {m.get("id"): m for m in store_block["models"] if isinstance(m, dict)}
        configured[provider] = [
            catalog_model(provider, m, store_models.get(m.get("id"))) for m in models if isinstance(m, dict)
        ]

    # unconfigured = models present in the fetched catalog but absent from the
    # user's configuration — not runnable as-is, whether the gap is the whole
    # provider or a single model under a configured provider.
    for provider, block in store.items():
        if not isinstance(block, dict) or not isinstance(block.get("models"), list):
            continue
        configured_ids = set()
        pb = providers.get(provider)
        if isinstance(pb, dict):
            configured_ids = {
                m.get("id") for m in pb.get("models", []) or [] if isinstance(m, dict)
            }
        extras = sorted(
            str(m.get("id"))
            for m in block["models"]
            if isinstance(m, dict) and m.get("id") and m.get("id") not in configured_ids
        )
        if extras:
            unconfigured[provider] = extras

    print(
        json.dumps(
            {
                "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "configured": configured,
                "unconfigured": unconfigured,
                "storeMissing": store_missing,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
