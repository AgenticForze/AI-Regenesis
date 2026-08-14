# Engine / Content Split — Convention

**Status:** formalized from the pattern already proven in `deep8-architecture-engine` (Deep 8-Layer system).
This document makes that convention explicit so every future skill extraction (Quick-Reference, Retrospective
Generator, Proposal Generator) follows the same shape instead of re-deriving it.

## The rule

- **Engine** = takes a spec (plain dict/list of primitives), produces an artifact (SVG string, list of
  strings, table rows). Zero domain knowledge. Every parameter is a name, list, or string passed in by the
  caller — nothing about telecom, finance, or BSS/OSS is hard-coded inside it.
- **Content** = pure data (dicts/lists of strings). Zero rendering logic. No SVG-building, no string
  templating beyond simple f-string interpolation of its own fields.

If a file (or a function inside a file) does both, it's not finished being split yet.

## Audit: current repo, file by file

| File | Role | Notes |
|---|---|---|
| `templates.py` | **Engine** (Mermaid) | 8 pattern builders (`orchestrator_worker`, `hierarchical`, `pipeline`, `blackboard`, `debate_critique`, `market_based`, `event_swarm`, `human_escalation`) plus two small private helpers (`_san`, `_obs_block`, `_obs_wiring`). Every function takes only names/lists as params. Clean. |
| `svg_patterns.py` | **Mixed — engine + embedded content** | The same 8 pattern builders as `templates.py` (SVG instead of Mermaid) are clean engine. But `e2e_platform()`, `decision_engineering_meta_architecture()`, and `rca_deep8_architecture()` are hand-authored, hard-coded one-off diagrams living in the same file — their node labels, edges, and layer text are baked into the function body, not passed in. `blueprint_table()` is a generic renderer (takes `rows` as a parameter) and belongs on the engine side, but the `RCA_BLUEPRINT_ROWS` data it's usually called with sits in the same file as the renderer. `BUILDERS` (the pattern-name → function dispatch dict) is engine plumbing. |
| `build_order.py` | **Engine** | `_orchestrator_worker`, `_hierarchical`, etc. take a use-case dict (`uc`) and interpolate *that use case's own* field values into fixed phase templates. No hard-coded domain content — clean, matches the docstring's claim exactly. |
| `telecom_data.py` / `bssoss_data.py` / `finance_data.py` | **Content** | Lists of dicts: id, slug, title, pattern name, problem statement, orchestrator/workers/data_sources/actions, agents_table, tech_table. Zero rendering logic. Clean. |
| `deep8_engine.py`, `deep8_data.py` (+ per-domain `*_deep8_data.py`) | **Already split** — this is the reference pair. `deep8_engine.py` is pure engine (already extracted into the `deep8-architecture-engine` skill); the `*_deep8_data.py` files are pure content. This is the shape every future split should match. |
| `build.py` | **Glue, not engine or content** | Site-build orchestration: reads content files, calls the right engine function per pattern, writes output to `docs/`. Repo-specific — doesn't get extracted into a skill. |

## What this means for Phase 3b (Quick-Reference Engine skill)

- `templates.py` and the **8-pattern-builder portion** of `svg_patterns.py` extract cleanly as-is — same
  process as the deep8 extraction: copy into `skills/quick-reference-engine/scripts/`, no rewrite needed.
- `build_order.py` extracts cleanly as-is.
- **Before packaging**, split `svg_patterns.py` itself: move `e2e_platform()`, `decision_engineering_meta_architecture()`,
  `rca_deep8_architecture()`, and `RCA_BLUEPRINT_ROWS` out of the engine file (they're one-off flagship content,
  not reusable pattern logic — they don't belong in a general-purpose skill that other people's use cases will
  call). `blueprint_table()` itself stays (generic renderer); only the RCA-specific data that feeds it moves out.
- The three domain data files (`telecom_data.py`, `bssoss_data.py`, `finance_data.py`) are the Phase 3d
  "vertical packs" — they don't go into the Quick-Reference Engine skill itself, since the whole point of the
  engine/content split is that the engine ships without any one domain's content baked in.

## Regression check — deep8-architecture-engine, re-tested

Isolation test re-run before writing this doc, as a check that the reference pattern is still sound:

1. Copied `skills/deep8-architecture-engine/scripts/` to a scratch folder with **no other repo path on
   `sys.path`**.
2. Ran `example_spec.py` standalone — produced `example_diagram.svg`, `example_blueprint.svg`,
   `example_agent_stack.txt`, `example_build_order.txt` with no import errors.
3. Validated both generated SVGs with `cairosvg.svg2png()` — both parsed and rendered without exceptions.

**Result: pass.** The existing skill is still cleanly standalone — safe to use as the template for the next
extraction.

## One-sentence test (for future files)

Before writing a new function, ask: *if I deleted every domain-specific string, list, and file from this
repo, would this function still compile and run?* If yes, it's engine. If no, it's content — split it out.
