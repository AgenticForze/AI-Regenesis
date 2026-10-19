#!/usr/bin/env bash
# Rebuild the Agentic Ops outputs and copy the published pages into the AI-Regenesis site.
#
# The site is served by GitHub Pages from main /docs, so the published copy lives in
#   docs/agentic-ops/            landing page, Google Cloud and AWS editions, diagram PNGs
#   docs/agentic-ops/explorer/   the Architecture Explorer (component + data.json)
# and appears at https://agenticforze.github.io/AI-Regenesis/agentic-ops/
#
# Run from anywhere:  agentic-ops/scripts/publish-site.sh
# Requires: python3, plus  pip install markdown pyyaml cairosvg
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="../docs/agentic-ops"

python3 tools/build_catalog.py
./scripts/build-diagrams.sh
python3 explorer/build.py

rm -rf "$OUT"
mkdir -p "$OUT/diagrams" "$OUT/explorer"
cp site/index.html site/gcp.html site/aws.html "$OUT/"
cp diagrams/png/*.png "$OUT/diagrams/"
cp explorer/dist/index.html explorer/dist/agentic-ops-explorer.js explorer/dist/data.json "$OUT/explorer/"
echo "Published to docs/agentic-ops/ — commit and push to update the live site."
