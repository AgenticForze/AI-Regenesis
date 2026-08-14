---
name: quick-reference-engine
description: Generates the "Quick Reference" multi-agent architecture view for an AI/agentic use case — a labeled flow diagram in both Mermaid text and rendered SVG card form, plus a four-phase build order — for any of 8 named multi-agent patterns (Orchestrator-Worker, Hierarchical, Sequential Pipeline, Blackboard/Shared-Memory, Debate-Critique-Arbiter, Market-Based/Auction, Event-Driven Reactive Swarm, Human-in-the-Loop Escalation Chain), all from one compact spec per use case, no bespoke diagram code needed. Use whenever asked to create, add, extend, or batch-produce a "Quick Reference" diagram, an architecture diagram for one of the named patterns above, a Mermaid flowchart for a multi-agent system, or a build order for one of these 8 patterns — including "do the Finance domain next" once established for a project. Distinct from deep8-architecture-engine (the 8-layer L1-L8 regenerative-architecture view) — use this one for a named multi-agent *pattern*, not the layered decision-engineering model.
---

# Quick-Reference Engine

Turns one compact Python dict per use case into three artifacts, all from the same source of truth, for
whichever of 8 named multi-agent patterns fits the use case:

1. **A Mermaid flowchart** (text) — subgraph-per-layer flowchart source, ready to embed in markdown or render
   with any Mermaid-compatible viewer.
2. **A card diagram** (SVG) — the same layer/node/edge structure as the Mermaid version, rendered as pastel
   rounded cards with elbow connectors, in the same visual language as the deep8 engine's diagrams.
3. **A four-phase build order** (list of strings) — get one path working end-to-end, add the pattern's
   defining mechanism, add the governance gate, add observability/feedback — phrased using that use case's
   own agent/component names, not generic boilerplate.

This was extracted from the same production codebase (60-use-case Telecom/BSS-OSS/Finance catalog) as the
deep8-architecture-engine skill, and the worked example below was rendered and visually inspected across 6
of the 8 patterns before packaging — two real rendering-fidelity issues were found and documented in
`references/lessons-learned.md` in the process, not left implicit.

## The 8 patterns

| Pattern key | Shape |
|---|---|
| `orchestrator-worker` | Supervisor fans out to N workers, aggregates, optional human gate, then acts |
| `hierarchical` | Top orchestrator → N mid-managers → each manager's own leaves → consolidated action |
| `pipeline` | Fixed sequential stages, no fan-out |
| `blackboard` | Shared read/write store, one controller, N agents, then actions |
| `debate-critique` | Proposer ↔ critic loop, arbiter decides, then actions |
| `market-based` | Auctioneer + N bidder agents, then actions |
| `event-swarm` | Event bus + N reactive agents, then actions |
| `human-escalation` | Auto-agent chain → confidence gate → auto-resolve or human, then actions |

## Quick start

```python
import sys; sys.path.insert(0, "scripts")
from templates import orchestrator_worker as mmd_orchestrator_worker   # Mermaid version
from svg_patterns import BUILDERS as SVG_BUILDERS                      # SVG versions, keyed by pattern
from build_order import build_order_for

uc = {
    "title": "Multi-Agent Network Fault RCA & Auto-Remediation",
    "pattern": "orchestrator-worker",
    "orchestrator": "NOC Incident Orchestrator Agent",
    "workers": ["RAN Alarm Correlation Agent", "Transport/IP Topology Agent"],
    "data_sources": ["FM/PM Alarms (EMS)", "Network Topology (Netbox)"],
    "actions": ["Auto-remediation via Ansible/NETCONF", "ServiceNow Incident Update"],
    "human_gate": "SRE Approval for High-Blast-Radius Actions",   # optional
}

mmd = mmd_orchestrator_worker(uc["title"], uc["orchestrator"], uc["workers"],
                               uc["data_sources"], uc["actions"], uc.get("human_gate"))
svg = SVG_BUILDERS["orchestrator-worker"](uc["title"], uc["orchestrator"], uc["workers"],
                                           uc["data_sources"], uc["actions"], uc.get("human_gate"))
build_order = build_order_for(uc)   # -> list of 4 phase strings
```

Every pattern's Mermaid and SVG functions take **identical positional arguments** — see
`references/spec-format.md` for the exact signature and required `uc` keys per pattern (they differ pattern
to pattern; `orchestrator-worker` and `blackboard` do not take the same fields).

Write `svg` to a sibling `.svg` file and embed via `<img src="diagram.svg"/>` in the markdown doc — don't
inline raw SVG or Mermaid source directly into prose. Write `mmd` to a `.mmd` file (or a fenced ` ```mermaid `
code block) if a text-based flowchart is what's actually wanted instead of/alongside the rendered card SVG.

**Always validate every generated SVG before presenting it** — render to PNG with `cairosvg` and either view
it or at minimum confirm it parses without exceptions. This is not optional: two of the three issues in
`references/lessons-learned.md` only showed up on visual inspection, not from the code raising an exception.

## Known rendering limitation — read before using `blackboard`, `market-based`, or `event-swarm`

When the number of actions is smaller than the number of agents/bidders in these three patterns, the
action-wiring edges visually pass behind whichever agent card happens to share their column position,
creating a false impression that only some agents connect to actions. Full detail and the two workarounds
are in `references/lessons-learned.md` #1 — read this before batch-generating use cases with these three
patterns and an action count that doesn't match the agent count.

## Reference files

- `references/spec-format.md` — exact call signature and required `uc` dict keys for all 8 patterns, across
  Mermaid, SVG, and build-order.
- `references/lessons-learned.md` — the fan-out/action-count visual-occlusion issue, the unused `title`
  parameter, and the (verified-clean) ampersand-escaping check — read before extending or batch-using this
  engine.
- `scripts/svg_engine.py` — the underlying card/layout/connector renderer (`Diagram` class, `COLORS`). Shared
  with the deep8 engine; you generally don't need to touch this directly.
- `scripts/templates.py` — the 8 Mermaid pattern-builder functions, plus `PATTERNS` (pattern key → display
  name dict).
- `scripts/svg_patterns.py` — the 8 SVG pattern-builder functions (same names, same argument order as
  `templates.py`), plus `BUILDERS` (pattern key → function dict). Intentionally does **not** include the
  flagship one-off diagrams (`e2e_platform`, `decision_engineering_meta_architecture`,
  `rca_deep8_architecture`) from the source repo's version of this file — those are hand-authored content for
  one specific catalog, not reusable pattern logic, and don't belong in a general-purpose skill.
- `scripts/build_order.py` — the 8 build-order generator functions plus `build_order_for(uc)`, the public
  dispatch entry point.
- `scripts/example_spec.py` — runnable worked example covering 3 of the 8 patterns (run it directly to
  produce sample output files and confirm your environment is set up correctly before writing new specs).
