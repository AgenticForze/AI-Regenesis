# Spec Format Reference

Full field-by-field reference for the spec dict consumed by `build_deep8_diagram()`,
`auto_blueprint_rows()`, and `auto_agent_stack()` in `scripts/deep8_engine.py`.

## Top-level shape

```python
spec = {
    "l1": [...],          # required, 2-4 items
    "l2": [...],           # required, usually exactly 3 items
    "l3_orch": {...} | None,   # optional
    "l3_workers": [...],   # required, 1-5 items
    "l4": [...],           # required, 2-3 items
    "gate": {...} | None,  # optional but recommended — see "Omitting the gate" below
    "l5": [...],           # required, 2-5 items
    "l6": [...],           # required, 2-3 items
    "l7": [...],           # required, 2-3 items
    "l8": [...],           # required, 2-3 items
}
```

Memory (Working / Episodic / Semantic / Policy) is generated automatically between `l3_workers` and `l4` —
never specify it in the spec.

## Item dict fields

Every item in `l1`, `l2`, `l3_workers`, `l4`, `l5`, `l6`, `l7`, `l8`, plus `l3_orch` and `gate` (which are
single dicts, not lists), share this base shape:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique string within this spec (e.g. `"w1"`, `"gw"`). Used to wire edges internally — you never write edges by hand. |
| `title` | yes | The card's bold title text. Wraps automatically up to 3 lines. |
| `sub` | yes | The card's smaller subtitle text. Convention: `"L{n} · {short category}"` (e.g. `"L3 · Specialist"`), or a more specific tag like `"Short-Term · current session"` for memory-adjacent items. |
| `external` | no, `l1` only | `True` renders the card with a dashed border (third-party/external data source). Default `False` (internal system of record). |
| `prod` | no | A specific production technology string (e.g. `"Neo4j graph database"`). If omitted, a generic per-layer default is used in the auto-generated blueprint table and agent stack. |
| `learn` | no | A specific learning-stack technology string. If omitted, a generic per-layer default is used. |
| `purpose` | no | A full sentence describing this item's purpose, used in the agent stack table's "Purpose" column. If omitted, a templated sentence is generated from the title (see `LAYER_PURPOSE_TEMPLATE` in `deep8_engine.py`) — always readable, but genuinely bespoke text is better for the items that matter most to the reader (typically `l4` governance items and any `l5` item with a `gate_branch`). |
| `io` | no | A specific "X → Y" inputs/outputs string. If omitted, a generic per-layer default is used. |
| `color` | no | Override the card's color key (see `COLORS` in `svg_engine.py`: `data`, `orch`, `agent`, `action`, `obs`, `channel`, `leadership`, `memory`). Layers have sensible defaults; you mainly need this for `l5` human/hold branch items (see below). |
| `gate_branch` | no, `l5` only | `"auto"` \| `"human"` \| `"hold"` \| omit. Marks this item as a target of the conditional gate's three branches. See "The gate and its branches" below. |

## The gate and its branches

If `spec["gate"]` is set, exactly one `l5` item should have `gate_branch="auto"`, one `gate_branch="human"`,
and one `gate_branch="hold"`. The engine draws three labeled edges from the gate to these three items:
`"high confidence"` → auto, `"medium confidence"` → human, `"low confidence"` → hold (dashed).

**Ordering matters.** Put the `human` item at one end of the `l5` row and the `hold` item at the other end,
with the `auto` item and any plain tool-registry items in between. If `human` and `hold` end up in adjacent
columns, their condition labels will overlap (their edge midpoints land too close together — see
`references/lessons-learned.md`). The convention used across all 22 validated use cases:

```python
"l5": [
    _l5_human("human", "..."),      # position 1 (leftmost)
    _l5_plain("a1", "..."),          # tool-registry chain starts
    _l5_auto("a2", "..."),           # the "auto" gate target, usually mid-chain
    _l5_plain("a3", "..."),
    _l5_hold("hold", "..."),         # position 5 (rightmost)
],
```

Conventional colors: `human` items use `"leadership"` (rose), `hold` items use `"obs"` (lavender), everything
else in `l5` defaults to `"action"` (amber).

### Omitting the gate

If a use case genuinely has no conditional branch point (rare — most agentic decisions have *some* confidence
threshold), set `spec["gate"] = None`. In that case every `l4` item gets a direct edge to whichever `l5` item
has `gate_branch` set (there should be exactly one). This path exists but wasn't exercised in the validated
22-use-case batch — test it visually before relying on it for a real deliverable.

## Omitting the orchestrator (`l3_orch: None`)

Use `None` when the underlying execution pattern is a strict pipeline with no central coordinator (e.g. a
sequential mediation/ETL pipeline, or a rigid regulatory process like number portability where the sequence
itself, not a supervisor, is the control structure). When `l3_orch` is `None`:

- `l3_workers` all sit in one row, directly below L2, with no separate orchestrator row above them.
- L2's edges connect directly into the first `l3_workers` item instead of into an orchestrator node.
- Everything else (memory hookups, L4 fan-in, the gate, L5 onward) works identically.

This was used for 5 of the 20 validated BSS/OSS use cases (mediation, number portability, migration,
collections, and any other strict-pipeline-shaped use case) — it's a well-exercised path, not an edge case.

## `build_order_params` for `generic_build_order()`

Not part of the spec dict itself, but the standard companion. Seven positional arguments:

```python
generic_build_order(
    domain_word,      # e.g. "order fulfillment" — used in Phase 1's "Fake {domain_word} data..." sentence
    entry_name,        # the first l3_workers item's title — Phase 1's single-path proof-of-concept agent
    orch_name,          # l3_orch's title, or None if l3_orch is None
    n_extra_workers,    # len(l3_workers) - 1 — how many more agents Phase 2 brings online
    gate_name,          # spec["gate"]["title"]
    l5_auto_name,       # the l5 item with gate_branch="auto"
    human_name,         # the l5 item with gate_branch="human", or None if there isn't one
)
```

## Auto-generated content — what you get for free vs. what needs authoring

`auto_blueprint_rows(spec)` and `auto_agent_stack(spec)` derive their content directly from the spec with no
extra input required. This means:

- **Titles, subtitles, and any explicit `purpose`/`io`/`learn`/`prod` overrides** are always bespoke —
  exactly what you wrote in the spec.
- **Everything else** (default `purpose` sentences, default `io` text, default `learn`/`prod` tooling) is
  **derived at the layer level**, not the item level — every `l4` item without an explicit override gets the
  *same* generic "Plain Python rule functions" / "Open Policy Agent (OPA)" stack text, for instance. This is
  an intentional scale trade-off (see `references/lessons-learned.md`), acceptable for batch production of
  many use cases, but worth explicitly overriding for a small number of items that most need bespoke detail —
  typically the `l4` governance items (since they're what most differentiates one use case's actual rules from
  another's) and any `l5` item with a `gate_branch`.
