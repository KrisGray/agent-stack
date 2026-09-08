#!/usr/bin/env bash
# agent-stack persona installer.
#
#   bin/install.sh        copy personas to ~/.pi/agent/agents/ (global)
#   bin/install.sh -l     copy personas to ./.pi/agents/ (this project only)
#
# Prompt templates are NOT copied: pi loads them natively from this package via
#   pi install <repo-path>
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="${HOME}/.pi/agent/agents"
scope="global"
if [ "${1:-}" = "-l" ]; then
  dest="./.pi/agents"
  scope="project-local"
fi

mkdir -p "$dest"
count=0
for f in "$here"/agents/*.md; do
  name="$(basename "$f")"
  if [ -f "$dest/$name" ] && ! cmp -s "$f" "$dest/$name"; then
    echo "OVERWRITE ($scope): $name (existing copy differs — check your customizations)"
  fi
  cp "$f" "$dest/$name"
  count=$((count + 1))
done

echo "Installed $count personas -> $dest ($scope)"
echo "Then load the prompts:  pi install '$here'"
