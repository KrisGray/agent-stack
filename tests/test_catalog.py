"""Tests for bin/catalog.py — the credential-safe model catalog extractor.

Run:  uv run --with pytest pytest -q tests/

The script reads ~/.pi/agent/models.json (JSONC, contains apiKey fields) and
~/.pi/agent/models-store.json (fetched catalog cache) and emits a redacted,
merge-enriched catalog to stdout. The security property under test is the
most important one: credential values must never appear in the output.
"""

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "bin" / "catalog.py"

CONFIG_JSONC = textwrap.dedent(
    """\
    // pi provider configuration — comments are stripped before parsing
    {
      "providers": {
        /* block comment too */
        "zai": {
          "apiKey": "sk-SECRET-CONFIG-KEY",
          "baseUrl": "https://example.test/v4",
          "models": [
            { "id": "glm-5.3", "reasoning": true, "contextWindow": 1048576, "maxTokens": 4096, },
            { "id": "glm-4.7", "contextWindow": 204800, }
          ]
        },
        "deepinfra": {
          "apiKey": "sk-SECRET-CONFIG-KEY-2",
          "models": [
            {
              "id": "deepseek-ai/DeepSeek-V4-Pro",
              "reasoning": true,
              "contextWindow": 1048576,
              "compat": { "reasoningEffortMap": { "minimal": "high", "low": null } }
            }
          ]
        }
      }
    }
    """
)

STORE_JSONC = textwrap.dedent(
    """\
    {
      "zai": {
        "models": [
          {
            "id": "glm-5.3",
            "name": "GLM-5.3",
            "reasoning": true,
            "contextWindow": 1048576,
            "cost": { "input": 0.6, "output": 2.2, "cacheRead": 0.11 },
            "thinkingLevelMap": { "minimal": "low", "xhigh": null }
          },
          { "id": "glm-5.3-air", "name": "GLM-5.3 Air" }
        ],
        "checkedAt": "2026-09-08T00:00:00Z",
        "etag": "store-etag-value"
      },
      "google": {
        "models": [ { "id": "gemini-pro", "name": "Gemini Pro", "cost": { "input": 1 } } ]
      }
    }
    """
)


@pytest.fixture()
def home(tmp_path):
    """A fake HOME containing a pi agent dir with fixture catalog files."""
    agent = tmp_path / ".pi" / "agent"
    agent.mkdir(parents=True)
    (agent / "models.json").write_text(CONFIG_JSONC)
    (agent / "models-store.json").write_text(STORE_JSONC)
    return tmp_path


def run_catalog(home, *args):
    env = dict(os.environ, HOME=str(home), PI_CONFIG_DIR="")
    return subprocess.run(
        [sys.executable, str(CATALOG), *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_script_exists():
    assert CATALOG.exists(), "bin/catalog.py must exist"


def test_parses_jsonc_and_emits_valid_json(home):
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert "configured" in data and "unconfigured" in data


def test_credentials_never_appear_in_output(home):
    r = run_catalog(home)
    blob = r.stdout + r.stderr
    for secret in ("sk-SECRET-CONFIG-KEY", "sk-SECRET-CONFIG-KEY-2"):
        assert secret not in blob
    assert "apiKey" not in r.stdout


def test_configured_models_get_provider_qualified_ids(home):
    r = run_catalog(home)
    data = json.loads(r.stdout)
    zai = {m["id"]: m for m in data["configured"]["zai"]}
    assert zai["glm-5.3"]["qualified"] == "zai/glm-5.3"
    deepinfra = data["configured"]["deepinfra"]
    assert deepinfra[0]["qualified"] == "deepinfra/deepseek-ai/DeepSeek-V4-Pro"


def test_store_metadata_enriches_configured_models(home):
    r = run_catalog(home)
    data = json.loads(r.stdout)
    glm = {m["id"]: m for m in data["configured"]["zai"]}["glm-5.3"]
    assert glm["name"] == "GLM-5.3"
    assert glm["cost"] == {"input": 0.6, "output": 2.2, "cacheRead": 0.11}


def test_thinking_levels_are_non_null_keys_only(home):
    r = run_catalog(home)
    data = json.loads(r.stdout)
    glm = {m["id"]: m for m in data["configured"]["zai"]}["glm-5.3"]
    assert glm["thinkingLevels"] == ["minimal"]  # "xhigh": null dropped
    deep = data["configured"]["deepinfra"][0]
    assert deep["thinkingLevels"] == ["minimal"]  # from reasoningEffortMap


def test_store_only_providers_reported_as_unconfigured(home):
    r = run_catalog(home)
    data = json.loads(r.stdout)
    assert "google" in data["unconfigured"]
    # a store-only model under a configured provider is equally unrunnable
    assert data["unconfigured"]["zai"] == ["glm-5.3-air"]


def test_missing_store_degrades_gracefully(home):
    (home / ".pi" / "agent" / "models-store.json").unlink()
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data.get("storeMissing") is True
    assert data["unconfigured"] == {}


def test_missing_models_json_is_exit_2(home):
    (home / ".pi" / "agent" / "models.json").unlink()
    r = run_catalog(home)
    assert r.returncode == 2
    assert "models.json" in r.stderr


def test_parse_error_does_not_leak_file_content(home):
    (home / ".pi" / "agent" / "models.json").write_text(
        '{ "providers": { "x": { "apiKey": "sk-SECRET-CONFIG-KEY",,, } } }'
    )
    r = run_catalog(home)
    assert r.returncode != 0
    assert "sk-SECRET-CONFIG-KEY" not in r.stderr


# --- review findings: string-safety, BOM, empty arrays, multiline comments ---


def test_multiline_block_comment_is_stripped(home):
    p = home / ".pi" / "agent" / "models.json"
    p.write_text(
        '{\n  /* a comment\n     spanning\n     lines */\n'
        '  "providers": { "zai": { "apiKey": "s", "models": [{"id": "m"}] } }\n}\n'
    )
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count('"id"') == 1


def test_trailing_comma_inside_string_value_is_preserved(home):
    """The comma elision must be string-aware: ',}' inside a value is data."""
    p = home / ".pi" / "agent" / "models.json"
    p.write_text('{"providers": {"zai": {"models": [{"id": "m", "name": "a,}b"}]}}}')
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["configured"]["zai"][0]["name"] == "a,}b"


def test_escaped_quotes_inside_strings_survive(home):
    p = home / ".pi" / "agent" / "models.json"
    p.write_text(
        r'{"providers": {"zai": {"models": [{"id": "m", "name": "say \"hi\""}]}}}'
    )
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["configured"]["zai"][0]["name"] == 'say "hi"'


def test_bom_is_tolerated(home):
    p = home / ".pi" / "agent" / "models.json"
    p.write_bytes(
        b"\xef\xbb\xbf" + b'{"providers": {"zai": {"models": [{"id": "m"}]}}}'
    )
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    assert "zai" in json.loads(r.stdout)["configured"]


def test_empty_models_array_yields_empty_provider(home):
    p = home / ".pi" / "agent" / "models.json"
    p.write_text('{"providers": {"zai": {"apiKey": "s", "models": []}}}')
    r = run_catalog(home)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["configured"]["zai"] == []
