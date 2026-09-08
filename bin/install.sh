#!/usr/bin/env bash
# agent-stack persona installer.
#
#   bin/install.sh [-l] [-p] [-m FILE]
#
#     (no flags)  copy personas to ~/.pi/agent/agents/   (global)
#     -l          copy personas to ./.pi/agents/         (this project only)
#     -p          pin-only: rewrite model pins in the destination, no copy
#     -m FILE     model pin map, {"role": {"model": "…", "thinking": "…"} | "…"}
#                 default: ./.ai/pm/models.json when it exists
#
# Prompt templates are NOT copied: pi loads them natively from this package via
#   pi install <repo-path>
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="${HOME}/.pi/agent/agents"
scope="global"
pin_file=""
pin_only=0

while getopts ":lpm:" opt; do
  case "$opt" in
    l) dest="./.pi/agents"; scope="project-local" ;;
    p) pin_only=1 ;;
    m) pin_file="$OPTARG" ;;
    *) echo "usage: bin/install.sh [-l] [-p] [-m FILE]" >&2; exit 64 ;;
  esac
done

# Auto-detect the /hire-pm pin map in the project root.
if [ -z "$pin_file" ] && [ -f ./.ai/pm/models.json ]; then
  pin_file="./.ai/pm/models.json"
  echo "Using pin map: $pin_file"
fi

if [ "$pin_only" -eq 1 ]; then
  if [ -z "$pin_file" ]; then
    echo "pin-only (-p) needs a pin map: pass -m FILE or create ./.ai/pm/models.json" >&2
    exit 1
  fi
else
  mkdir -p "$dest"
fi

count=0
if [ "$pin_only" -eq 0 ]; then
  for f in "$here"/agents/*.md; do
    name="$(basename "$f")"
    if [ -f "$dest/$name" ] && ! cmp -s "$f" "$dest/$name"; then
      echo "OVERWRITE ($scope): $name (existing copy differs — check your customizations)"
    fi
    cp "$f" "$dest/$name"
    count=$((count + 1))
  done
  echo "Installed $count personas -> $dest ($scope)"
fi

if [ -n "$pin_file" ]; then
  [ -f "$pin_file" ] || { echo "pin map not found: $pin_file" >&2; exit 1; }
  # Also install the catalog extractor next to the personas so /hire-pm can
  # run it from a stable path.
  if [ "$pin_only" -eq 0 ]; then
    mkdir -p "$(dirname "$dest")/bin"
    cp "$here/bin/catalog.py" "$(dirname "$dest")/bin/agent-stack-catalog.py"
    echo "Installed catalog extractor -> $(dirname "$dest")/bin/agent-stack-catalog.py"
  fi
  python3 - "$pin_file" "$dest" <<'PY'
import json, re, sys
from pathlib import Path

pin_file, dest = Path(sys.argv[1]), Path(sys.argv[2])
pins = json.loads(pin_file.read_text())

def fmt(persona, pin):
    if isinstance(pin, str):
        return {"model": pin}
    if isinstance(pin, dict) and pin.get("model"):
        return {"model": pin["model"], **({"thinking": pin["thinking"]} if pin.get("thinking") else {})}
    print(f"  SKIP {persona}: pin has no model", file=sys.stderr)
    return None

def apply(path, changes):
    text = path.read_text()
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        print(f"  SKIP {path.name}: no frontmatter", file=sys.stderr)
        return False
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        print(f"  SKIP {path.name}: unterminated frontmatter", file=sys.stderr)
        return False
    for key, value in changes.items():
        pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
        block = "".join(lines[1:end])
        if pattern.search(block):
            lines[1:end] = pattern.sub(f"{key}: {value}", "".join(lines[1:end])).splitlines(keepends=True)
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        else:
            lines.insert(1, f"{key}: {value}\n")
            end += 1
    path.write_text("".join(lines))
    return True

applied = 0
for persona, pin in pins.items():
    changes = fmt(persona, pin)
    if changes is None:
        continue
    target = dest / f"{persona}.md"
    if not target.exists():
        print(f"  WARN {persona}: no persona at {target} (unknown role or not installed)", file=sys.stderr)
        continue
    if apply(target, changes):
        shown = ", ".join(f"{k}={v}" for k, v in changes.items())
        print(f"  pinned {persona}: {shown}")
        applied += 1
print(f"Pins applied: {applied}/{len(pins)} -> {dest}")
PY
fi

if [ "$pin_only" -eq 0 ]; then
  echo "Then load the prompts:  pi install '$here'"
fi
