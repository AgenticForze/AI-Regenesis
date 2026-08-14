---
name: deep8-architecture-engine
description: Generates the "Deep 8-Layer Regenerative Architecture" view for an AI/agentic use case — a labeled, color-coded flow diagram (SVG) mapping the use case through the 8-layer Decision Engineering Meta-Architecture (L1 Foundational Data & Infrastructure through L8 Feedback & Reinforcement Loops), plus a matching reference blueprint table, an agent-level stack table (Learning vs. Production tooling), and a phased build order — all from one compact spec per use case, no bespoke diagram code needed. Use whenever asked to create, add, extend, or batch-produce a "Deep 8-Layer" view, an "8-layer architecture diagram", a "decision engineering" diagram/blueprint, an "L1-L8" layer diagram, a "regenerative architecture" diagram, or a manuscript-style layer blueprint table with Learning/Production Stack columns — including "do the Finance domain next" once this pattern is established for a project.
---

# Deep 8-Layer Architecture Engine

Turns one compact Python spec per use case into four artifacts, all from the same source of truth:

1. **A labeled flow diagram** (SVG) — 8 rows (L1→L8) of pastel rounded cards, left-margin layer labels
   connected to a vertical spine, conditional-branch edges with condition labels, internal/external data
   store distinction (dashed border = external), and a regenerative feedback loop closing back into memory.
2. **A blueprint table** (SVG) — the manuscript's own two-column reference-model format: layer badge/title/
   description on the left, this use case's specific solution + tools on the right.
3. **An agent-level stack table** (plain Python tuples, render as markdown/HTML) — one row per agent:
   Layer, Agent Name, Purpose, Inputs/Outputs, Learning Stack, Production Stack.
4. **A phased build order** (list of strings) — six phases teaching the 8-layer model incrementally instead
   of building all layers at once.

This was built and validated across 22 real use cases (2 hand-crafted pilots + 20 spec-driven BSS/OSS use
cases, batch-produced from this same engine) before being packaged as a skill — the design decisions below
are lessons learned from that process, not theoretical.

## When to use this vs. building bespoke

Use the generic spec-driven approach (`deep8_engine.py`) for anything beyond one or two use cases — it's what
makes batches of 10-20+ tractable. Only hand-write a bespoke `Diagram()`-building function (see
`references/bespoke-pattern.md`) for a single flagship/pilot example where you want full manual control over
every edge and it's worth the extra time.

## Quick start

```python
import sys; sys.path.insert(0, "scripts")
from deep8_engine import build_deep8_diagram, auto_blueprint_rows, auto_agent_stack, generic_build_order
from blueprint_table import blueprint_table

spec = { ... }  # see "The spec format" below

diagram_svg   = build_deep8_diagram(spec)
blueprint_svg = blueprint_table(auto_blueprint_rows(spec))
agent_stack   = auto_agent_stack(spec)          # list of (layer, name, purpose, io, learn, prod) tuples
build_order   = generic_build_order(            # list of 6 phase strings
    "domain word", "entry agent name", "orchestrator name or None",
    n_extra_workers, "gate name", "auto-path action name", "human role or None"
)
```

Then write `diagram_svg` and `blueprint_svg` to `.svg` files, embed them via `<img src="diagram.svg"/>` in a
markdown doc (don't inline raw SVG into markdown — always write sibling files and reference them), and render
`agent_stack` as a 6-column table.

**Always validate every generated SVG before presenting it** — render to PNG with `cairosvg` (`pip install
cairosvg --break-system-packages`) and either view it yourself or at minimum confirm it parses without
exceptions. This caught real bugs during development (see `references/lessons-learned.md`) that would not
have been visible from the Python code alone.

## The spec format

One dict per use case. Every field maps directly to a diagram row or a governed edge — see
`references/spec-format.md` for the full field-by-field reference and `scripts/example_spec.py` for a
complete worked example. The shape, briefly:

```python
spec = {
    "l1": [ {"id","title","sub","external": bool}, ... ],       # 2-4 data stores
    "l2": [ {"id","title","sub","prod": optional}, ... ],        # usually 3: AI Gateway, LLM core, knowledge graph
    "l3_orch": {"id","title","sub"} or None,                     # single orchestrator, own row (None for strict pipelines)
    "l3_workers": [ {"id","title","sub"}, ... ],                 # 1-4 specialist agents
    "l4": [ {"id","title","sub"}, ... ],                         # 2-3 governance/policy engines
    "gate": {"id","title","sub"} or None,                        # the conditional confidence/risk gate
    "l5": [ {"id","title","sub","color","gate_branch"}, ... ],   # action items; gate_branch = "auto"|"human"|"hold"|None
    "l6": [ {"id","title","sub"}, ... ],                         # 2-3 observability/nervous-system items
    "l7": [ {"id","title","sub"}, ... ],                         # 2-3 leadership-dashboard items
    "l8": [ {"id","title","sub"}, ... ],                         # 2-3 self-healing/feedback items
}
```

Memory (Working/Episodic/Semantic/Policy) is generated automatically — you never specify it. Node `id`s only
need to be unique within one spec (each spec builds its own isolated `Diagram()` instance).

## Design conventions — preserve these

These aren't arbitrary — each one exists because an earlier version broke without it. Full details and the
actual before/after screenshots that drove each decision are in `references/lessons-learned.md`; the summary:

- **Keep `l3_orch` separate from `l3_workers`.** Putting the orchestrator in the same row as its workers
  creates a same-row multi-column edge that visually passes through intermediate cards. Always give the
  orchestrator (if present) its own row above the workers.
- **Order `l5` items so the gate's branch targets aren't adjacent columns.** If "human" and "hold" sit next
  to each other, their condition labels collide. Spread the three `gate_branch` targets across the row (e.g.
  human at position 1, auto in the middle, hold at the end) — see `scripts/deep8_engine.py`'s L5 ordering
  comment for the exact pattern that works.
- **Don't add a label to a same-row edge that skips a column.** If you need `human → auto_action` as an
  explicit edge and there's an item between them, drop the label or drop the edge entirely — a labeled
  same-row edge that has to route behind an intervening card will render its label invisibly behind that
  card. `generic_build_order` and the L5 chain-building logic in `deep8_engine.py` already avoid this; don't
  reintroduce it by hand-adding edges outside the spec's declarative shape.
- **Don't label the L8→memory closing-loop edges.** They span 6+ rows by design (that's the "regenerative
  loop" this whole model is named for). A label on a jump that long lands inside an unrelated row. Leave
  these edges unlabeled — the loop is still visually traceable, just not labeled.
- **External vs. internal data stores matter — set `"external": True` deliberately**, don't default
  everything to internal. A use case with zero external stores is a signal worth double-checking against the
  real system, not just a simpler spec.
- **Fix content bugs (like a hardcoded domain name or a placeholder-only purpose column) at the generator
  level, not per-generated-file.** When producing content programmatically for many use cases, if you
  hand-patch one output file instead of fixing the function that produced it, every other output has the
  same bug and you won't remember to check.

## Building the four artifacts into a project

If you're adding this to an existing multi-use-case catalog (the scenario this skill was built for):

1. Write one spec + a short intro/problem/diagram-note text block per use case (see
   `references/spec-format.md` for the markdown-doc field shape).
2. Run every spec through `build_deep8_diagram` / `auto_blueprint_rows` / `auto_agent_stack` /
   `generic_build_order` in a batch script — don't hand-call these one at a time in conversation.
3. Validate every output SVG with `cairosvg` before writing anything to a shipped file or presenting it.
4. Spot-check 2-3 structurally different specs visually (different pattern shapes — e.g. one with `l3_orch`,
   one without, one with a `market-based`-style flavor) — don't assume the whole batch is fine because the
   first one rendered.
5. Write each use case's diagram/blueprint as sibling `.svg` files next to its markdown doc, referenced via
   `<img src="...">`, not inlined as raw SVG text in the markdown.

## Reference files

- `references/spec-format.md` — full field-by-field spec reference, with the exact dict shape for every layer
  and what each optional field does (`external`, `prod`, `purpose`, `io`, `learn`, `gate_branch`, `color`).
- `references/lessons-learned.md` — the specific bugs hit during development (double-escaped ampersands,
  overlapping condition labels, edges rendering invisibly behind cards, a hardcoded domain string, a
  purpose-column that just repeated the layer tag) and the fix for each — read this before extending the
  engine, not just before using it.
- `references/bespoke-pattern.md` — how to hand-write a one-off `Diagram()`-building function instead of using
  the generic spec, for a single flagship example where full manual control is worth the time.
- `scripts/svg_engine.py` — the underlying card/layout/connector renderer (`Diagram` class, `COLORS`,
  layer-label/spine rendering). You generally don't need to touch this directly.
- `scripts/deep8_engine.py` — the generic spec → diagram/blueprint-rows/agent-stack/build-order engine.
- `scripts/blueprint_table.py` — standalone blueprint-table SVG renderer, takes a list of 8 row dicts.
- `scripts/example_spec.py` — one complete, runnable, worked example (run it directly to produce sample
  output files and confirm your environment is set up correctly before writing new specs).
