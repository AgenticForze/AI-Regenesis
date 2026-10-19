---
name: architecture-diagrams
description: Draw, edit or extend icon-based enterprise architecture diagrams (trust zones, end-to-end flows, hybrid networking, security gate chains, telemetry pipelines) in the Agentic Ops house style, from a JSON spec rendered to SVG and PNG. Use whenever asked to create, update, re-colour or add a cloud edition of an architecture diagram for the Agentic Ops reference architecture or any diagram "in the same style".
---

# Architecture diagrams

Diagrams are **data, not drawings**. Each diagram is a JSON spec (zones, nodes, edges, legend) rendered by `scripts/render.py` into:

| Output | Use |
| --- | --- |
| `<name>.svg` | Static light-palette SVG for GitHub, docs and Confluence |
| `<name>.themed.svg` | SVG using CSS custom properties, follows light/dark in the explorer and portals |
| `<name>.png` | 2× PNG for slides and Medium (`--png`); `<name>.dark.png` with `--dark` |

Every node is emitted as `<g class="node" data-id=… data-layer=…>` and every edge as `<path class="edge" data-from=… data-to=…>`, which is what makes diagrams clickable in the Architecture Explorer.

## Workflow

1. **Find or start a spec.** Existing diagrams live in the repo at `diagrams/specs/*.json`. To change one, edit its spec, never the SVG. For a new diagram, copy `references/example-spec.json`.
2. **Plan the layout on a grid before writing coordinates** (see Style rules). Decide the columns (zones) left to right in the direction of flow, then rows.
3. **Write nodes, then edges.** Prefer `from`/`to` anchors with a route over raw points.
4. **Render and read the warnings:**
   ```bash
   pip install cairosvg   # once
   python3 scripts/render.py path/to/spec.json -o out --png
   ```
   Fix every warning: overflowing titles, overlapping nodes, edges crossing a node, labels sitting on a node. In the repo, `scripts/build-diagrams.sh` rebuilds everything with `--strict`.
5. **Look at the PNG** before delivering. Check that arrows read left-to-right or top-to-bottom, labels sit on their own line, and nothing important is hidden behind a zone pill.
6. **Deliver** the static SVG and PNG for documents, and the themed SVG for web pages. If a repo is involved, commit the spec together with the outputs.

## Spec format (summary)

```json
{
  "title": "Accessible name of the diagram",
  "width": 1260, "height": 520,
  "zones": [{"x": 10, "y": 20, "w": 230, "h": 470, "title": "Sources", "color": "l0", "sub": "optional note", "style": "dash|solid"}],
  "nodes": [{"id": "otel", "x": 285, "y": 145, "title": "OTel Collector", "sub": "DaemonSet, sidecar", "icon": "trace", "color": "l8", "w": 200, "h": 56}],
  "edges": [
    {"from": "agents.r", "to": "otel.l", "route": "hv", "mid": 255, "label": "spans", "style": "dot", "color": "ink-2"},
    {"from": "otel.b", "to": "sampling.t"},
    {"points": ["k3.r", [1012, 368], [1012, 188]], "arrow": false}
  ],
  "legend": [{"label": "pass", "color": "auto"}, {"label": "deny path", "color": "risk", "style": "dash"}]
}
```

- **Anchors:** `nodeid.l|r|t|b` with an optional pixel offset along that side, e.g. `gateway.r+10`, `fw.t-40`.
- **Routes:** `hv` (horizontal, vertical, horizontal; `mid` = x of the vertical run), `vh` (`mid` = y), `straight`, or `via` waypoints. Use `points` for anything else; points may mix anchors and `[x, y]`.
- **Edge styles:** `solid` request path, `dash` backup or deny path, `dot` telemetry, audit or async feedback. `arrow: false` for trunk segments that join others.
- **Edge colours:** `ink-2` default, `auto` pass/success, `gate` human approval or backup, `risk` deny or security response, `signal`.
- **Labels:** `label` plus optional `at: [x, y]` to place the pill exactly.
- Defaults: node `w` 200, `h` 56.

Full reference: `references/spec-format.md`.

## Style rules

- **Colour = layer.** Use the layer token for every node and zone: `l0` channels/external, `l1` edge, identity, content safety, `l2` orchestration, `l3` gateway and network transit, `l4` model serving, `l5` knowledge, `l6` tools, `l7` data and events, `l8` observability, `l9` security and governance, `l10` MLOps, `risk` restricted enclave and security response, `gate` human approval, `auto` verified/pass. The same component keeps the same colour in every diagram.
- **Icon = kind of thing.** shield (edge security), shieldscan (content screening), lock/key/vault (access and crypto), tunnel (VPN), link (dedicated circuits), router/hub (routing), firewall, agent/supervisor, neural (LLM), chip (accelerator-served SLM), database, search, graph, wrench (tools/executors), policy, approve, trace/log/eye/chart (telemetry). Run `scripts/render.py --icons` for the full list and `--gallery icons.png` for a picture.
- **Grid:** zones are columns roughly 230–250 px wide with 20–30 px gutters; nodes are 200 × 56, placed 15 px inside a zone; vertical rhythm 78–95 px between node tops. Zone pills sit on the zone's top border, so keep 30 px clear above the first node.
- **Text:** titles about 20 characters at width 200, subtitles about 26. Shorten wording rather than widening boxes; move vendor detail into the subtitle.
- **Edges:** orthogonal only. Run trunks in gutters between zones, not across nodes. Put labels on the longest straight segment, away from zone pills.
- **One idea per diagram.** If it needs more than about 45 nodes, split it.
- **No vendor logos or official icon sets.** The icons are original; if a reader needs official cloud icons, say both vendors publish them for architecture diagrams.

## Adding a cloud edition

Copy the Google Cloud spec, keep every coordinate and colour, and change only titles and subtitles to the target cloud's services, so all editions stay visually comparable. Rename zone titles where the concept differs (for example "VPC-SC perimeter" becomes "SCP fenced accounts"). Render with `--strict`.

## Embedding in web pages

Themed SVGs read colours from CSS custom properties. Print the token block with `scripts/render.py --tokens` and include it in the host page or the explorer's shadow root.
