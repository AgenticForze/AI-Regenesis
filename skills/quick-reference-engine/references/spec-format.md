# Spec Format — Quick-Reference Engine

One use case = one flat dict (call it `uc`), with a `"pattern"` key naming one of the 8 patterns below and a
fixed set of pattern-specific fields. The same `uc` dict drives all three artifacts:

- **Mermaid diagram** — `templates.py`, function name = pattern name (underscored), or via `templates.PATTERNS`
  for the display name.
- **SVG diagram** — `svg_patterns.BUILDERS[uc["pattern"]]`, same positional arguments as the Mermaid function.
- **Build order** — `build_order.build_order_for(uc)`, dispatches on `uc["pattern"]` internally, reads the
  dict directly (not positional args).

The Mermaid and SVG builder functions take **identical positional arguments** for a given pattern — this was
a deliberate design choice (see `svg_patterns.py`'s module docstring) so you can call both without
maintaining two argument lists. `build_order_for` is different: it takes the whole `uc` dict, not positional
args, so its required keys are listed below per pattern too.

## The 8 patterns

### `orchestrator-worker`
Supervisor fans work out to N workers, aggregates their output, optional human gate, then acts.

```python
orchestrator_worker(title, orchestrator, workers, data_sources, actions, human_gate=None)
```
`uc` keys: `title`, `orchestrator` (str), `workers` (list[str]), `data_sources` (list[str]),
`actions` (list[str]), `human_gate` (str or omit).

### `hierarchical`
Top orchestrator → N mid-level managers → each manager's own leaf agents → consolidated action.

```python
hierarchical(title, top, mid_layer, leaves_by_mid, actions)
```
`uc` keys: `title`, `top` (str), `mid_layer` (list[str]), `leaves_by_mid` (list[list[str]], **same length and
order as `mid_layer`** — `leaves_by_mid[i]` is the leaf list for `mid_layer[i]`), `actions` (list[str]).

### `pipeline`
Fixed sequential stages, no fan-out, ending in actions.

```python
pipeline(title, stages, actions)
```
`uc` keys: `title`, `stages` (list[str], in execution order), `actions` (list[str]).

### `blackboard`
Shared read/write store, one controller, N agents that read/write it, then actions.

```python
blackboard(title, controller, agents, store_name, actions)
```
`uc` keys: `title`, `controller` (str), `agents` (list[str]), `store_name` (str), `actions` (list[str]).
**See `lessons-learned.md` #1 before setting `len(actions) != len(agents)`.**

### `debate-critique`
Proposer ↔ critic loop, arbiter makes the final call, then actions.

```python
debate_critique(title, proposer, critic, arbiter, refs, actions)
```
`uc` keys: `title`, `proposer` (str), `critic` (str), `arbiter` (str), `refs` (list[str], data sources feeding
the proposer), `actions` (list[str]).

### `market-based`
Auctioneer + N bidder agents, then actions.

```python
market_based(title, auctioneer, bidders, actions)
```
`uc` keys: `title`, `auctioneer` (str), `bidders` (list[str]), `actions` (list[str]).
**See `lessons-learned.md` #1 before setting `len(actions) != len(bidders)`.**

### `event-swarm`
Event bus + N reactive agents subscribed to it, then actions.

```python
event_swarm(title, bus_name, agents, actions)
```
`uc` keys: `title`, `bus_name` (str), `agents` (list[str]), `actions` (list[str]).
**See `lessons-learned.md` #1 before setting `len(actions) != len(agents)`.**

### `human-escalation`
Chain of auto agents → confidence/risk gate → splits to auto-resolve or human, then actions.

```python
human_escalation(title, auto_agents, escalation_gate, human_role, actions)
```
`uc` keys: `title`, `auto_agents` (list[str], in execution order), `escalation_gate` (str),
`human_role` (str), `actions` (list[str]).

## The `title` parameter — read this before assuming it does something

Every one of the 8 functions takes `title` as its first argument, in both the Mermaid and SVG versions.
**Neither renderer displays it anywhere in the diagram.** See `lessons-learned.md` #2. Pass whatever string
you like (or reuse `uc["title"]`, which is convenient since you already have it), but don't rely on it
showing up in the output — write the title yourself as a markdown `#`/`##` heading above the embedded image.

## `build_order_for(uc)`

```python
from build_order import build_order_for
phases = build_order_for(uc)   # -> list[str], always 4 markdown-formatted phase strings
```

Dispatches on `uc["pattern"]` and reads whichever fields that pattern's private builder needs directly off
`uc` (same field names as above — e.g. `_orchestrator_worker` reads `uc["orchestrator"]`, `uc["workers"]`,
`uc.get("human_gate")`). If you've already built a valid `uc` for the diagram functions, it has everything
`build_order_for` needs too — no separate spec required.

## Registries

- `svg_patterns.BUILDERS` — `{pattern_name: function}`, all 8 SVG builders.
- `templates.PATTERNS` — `{pattern_name: display_name}` (e.g. `"orchestrator-worker"` →
  `"Orchestrator-Worker (Supervisor fan-out/fan-in)"`), for showing a human-readable pattern label in a UI
  or doc header. Does not include the functions themselves — for those, call the same-named function
  directly from `templates.py`.
- `build_order.BUILDERS` — `{pattern_name: private build-order function}`. Don't call these directly; use
  `build_order_for(uc)` instead, it's the public entry point.
