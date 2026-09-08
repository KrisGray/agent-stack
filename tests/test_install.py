"""Tests for bin/install.sh model-pin rendering.

Run:  uv run --with pytest pytest -q tests/

/hire-pm approves a pin map (.ai/pm/models.json, role -> model/thinking);
the installer renders it into persona frontmatter at copy time:

  { "pm": {"model": "p/m", "thinking": "high"},
    "scout": "p/cheap",        # string shorthand: model only
    ... }
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
INSTALL = REPO / "bin" / "install.sh"

PINS = {
    "pm": {"model": "prov/pm-strong", "thinking": "high"},
    "scout": "prov/scout-cheap",  # shorthand: model only, thinking untouched
    "planner": {"model": "prov/planner-x"},  # persona has NO model: line -> insert
    "nonexistent-role": {"model": "prov/ghost"},  # no such persona -> warn, continue
}


def frontmatter(path: Path) -> dict:
    lines = path.read_text().splitlines()
    assert lines[0] == "---"
    out = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


@pytest.fixture()
def pinfile(tmp_path):
    p = tmp_path / "pins.json"
    p.write_text(json.dumps(PINS))
    return p


def run_install(home, *args, cwd=None):
    env = dict(os.environ, HOME=str(home))
    return subprocess.run(
        ["bash", str(INSTALL), *args], capture_output=True, text=True, env=env, cwd=cwd or str(home)
    )


@pytest.fixture()
def home(tmp_path):
    return tmp_path


def test_pin_map_rewrites_model_and_thinking(home, pinfile):
    r = run_install(home, "-m", str(pinfile))
    assert r.returncode == 0, r.stderr
    dest = home / ".pi" / "agent" / "agents"
    fm = frontmatter(dest / "pm.md")
    assert fm["model"] == "prov/pm-strong"
    assert fm["thinking"] == "high"


def test_shorthand_pin_changes_model_only(home, pinfile):
    r = run_install(home, "-m", str(pinfile))
    assert r.returncode == 0, r.stderr
    source_fm = frontmatter(REPO / "agents" / "scout.md")
    fm = frontmatter(home / ".pi" / "agent" / "agents" / "scout.md")
    assert fm["model"] == "prov/scout-cheap"
    assert fm["thinking"] == source_fm["thinking"]  # untouched


def test_persona_without_model_line_gets_it_inserted(home, pinfile):
    r = run_install(home, "-m", str(pinfile))
    assert r.returncode == 0, r.stderr
    fm = frontmatter(home / ".pi" / "agent" / "agents" / "planner.md")
    assert fm["model"] == "prov/planner-x"


def test_unpinned_persona_is_byte_identical(home, pinfile):
    r = run_install(home, "-m", str(pinfile))
    assert r.returncode == 0, r.stderr
    untouched = home / ".pi" / "agent" / "agents" / "worker.md"
    assert untouched.read_bytes() == (REPO / "agents" / "worker.md").read_bytes()


def test_unknown_role_warns_but_succeeds(home, pinfile):
    r = run_install(home, "-m", str(pinfile))
    assert r.returncode == 0
    assert "nonexistent-role" in r.stderr


def test_pin_only_does_not_copy(home, pinfile):
    r = run_install(home, "-m", str(pinfile))
    assert r.returncode == 0, r.stderr
    dest = home / ".pi" / "agent" / "agents"
    (dest / "worker.md").unlink()
    r2 = run_install(home, "-p", "-m", str(pinfile))
    assert r2.returncode == 0, r2.stderr
    assert not (dest / "worker.md").exists()  # pin-only must not copy
    assert frontmatter(dest / "pm.md")["model"] == "prov/pm-strong"


def test_autodetects_ai_pm_models_json(home):
    cwd = home / "proj"
    (cwd / ".ai" / "pm").mkdir(parents=True)
    (cwd / ".ai" / "pm" / "models.json").write_text(json.dumps({"pm": "prov/auto"}))
    r = run_install(home, cwd=str(cwd))
    assert r.returncode == 0, r.stderr
    assert "models.json" in r.stdout  # said what it did
    assert frontmatter(home / ".pi" / "agent" / "agents" / "pm.md")["model"] == "prov/auto"


def test_pin_only_without_any_pin_file_fails(home):
    r = run_install(home, "-p")
    assert r.returncode != 0
    assert "models.json" in r.stderr
