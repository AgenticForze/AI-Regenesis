#!/usr/bin/env bash
# Rebuild every diagram from diagrams/specs/*.json into svg/, png/ and themed/.
# Requires: python3, cairosvg (pip install cairosvg)
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
python3 skills/architecture-diagrams/scripts/render.py diagrams/specs/*.json -o "$tmp" --png --strict
mkdir -p diagrams/svg diagrams/png diagrams/themed
for f in "$tmp"/*.themed.svg; do mv "$f" "diagrams/themed/$(basename "${f%.themed.svg}").svg"; done
mv "$tmp"/*.svg diagrams/svg/
mv "$tmp"/*.png diagrams/png/
rm -rf "$tmp"
echo "Diagrams rebuilt."
