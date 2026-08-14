# The Bespoke Pattern (for flagship/pilot examples only)

The generic spec-driven engine (`deep8_engine.py`) is the right tool for anything beyond one or two use
cases. But the first two examples ever built with this system (a customer retention use case and a network
fault RCA use case) were hand-coded directly against `svg_engine.py`'s `Diagram` class, with full manual
control over every node and edge. That approach is still worth knowing, for a single showcase example where
the extra time is worth it — or when a use case's structure genuinely doesn't fit the generic engine's
assumptions (e.g. more than one gate, or a fan-in from multiple L3 rows).

## When to reach for this instead of the generic engine

- A single flagship/reference example meant to demonstrate the full model in maximum depth, where every edge
  is worth individually deciding.
- A use case whose structure the generic engine's spec format genuinely can't express (check
  `references/spec-format.md` first — most apparent exceptions turn out to be expressible with `l3_orch: None`
  or a `gate: None` before you need to go bespoke).
- You're prototyping a new layout idea before deciding whether to generalize it into the engine itself.

## The pattern

```python
from svg_engine import Diagram

def my_flagship_diagram():
    d = Diagram()

    # L1
    ext1 = d.node("ext1", "External Feed Name", "External Data Store", "data", external=True)
    int1 = d.node("int1", "Internal DB Name", "Internal Data Store", "data")
    d.add_row([ext1, int1], label=("L1", "Foundational Data & Infrastructure", None))

    # L2
    gw = d.node("gw", "AI Gateway", "L2 · The Brain", "orch")
    llm = d.node("llm", "LLM Reasoning Core (Claude)", "L2 · The Brain", "agent")
    d.add_row([gw, llm], label=("L2", "Agent Intelligence & Models", None))

    # ... continue through L3-L8, calling d.add_row() once per row,
    # with a label=("L#", "Title", "Subtitle-or-None") only on the first row of each layer

    # Edges — full manual control
    d.edge("ext1", "gw")
    d.edge("gw", "llm")
    d.edge("gate", "action_item", label="high confidence")
    d.edge("gate", "hold_item", dashed=True, label="low confidence")
    # ... etc

    return d.render()
```

Key API points (see `svg_engine.py` for the full implementation):

- `d.node(id, title, subtitle, color_key, external=False)` creates a node. Color keys: `data`, `orch`,
  `agent`, `action`, `obs`, `channel`, `leadership`, `memory`.
- `d.add_row(nodes, label=None)` — `label` is a `(badge, title, subtitle_or_None)` tuple. Only the *first* row
  of a given layer should carry the label (e.g. the L3 orchestrator row gets the label; the L3 workers row and
  memory row right below it don't — they read as visually part of the same layer without repeating the label
  box).
- `d.edge(from_id, to_id, dashed=False, bidir=False, label=None)` — draws an elbow connector. Same-row edges
  route side-to-side automatically; cross-row edges route with a rounded elbow. See
  `references/lessons-learned.md` items 3-5 for what *not* to do with labels on these.

## What you still get automatically

Even in the bespoke pattern, the left-margin layer labels, the vertical red spine, and the "SYSTEM
ORCHESTRATION & KNOWLEDGE FLOW" rotated axis label are all handled by `Diagram.render()` itself, driven off
whatever `label=` tuples you passed to `add_row()` — you don't need to draw any of that by hand.

## What you lose vs. the generic engine

Going bespoke means `auto_blueprint_rows()` and `auto_agent_stack()` won't work — those functions read a
`spec` dict's structure, not a `Diagram` object. For a bespoke flagship example, hand-author the blueprint
table rows (pass them to `blueprint_table()` in `scripts/blueprint_table.py` directly) and the agent stack
table (just a plain list of `(layer, name, purpose, io, learn, prod)` tuples) alongside the diagram code.
This is exactly what was done for the two original pilot examples — expect it to take meaningfully longer
per use case than the spec-driven path.
