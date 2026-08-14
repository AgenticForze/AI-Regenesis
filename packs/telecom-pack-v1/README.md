# Telecom Vertical Pack — v1

**What's in this pack:** the Telecom domain's content for the AI-Regenesis catalog — 20 use cases as
Quick-Reference specs, and their matching Deep 8-Layer specs, as two pure-data Python files. No engine code,
no rendering logic — load these into the `quick-reference-engine` and `deep8-architecture-engine` skills (or
your own copy of the underlying scripts) to regenerate diagrams, tables, and build orders.

## Files

- `telecom_data.py` — `TELECOM`, a list of 20 dicts, one per use case. Each has `id`, `slug`, `title`,
  `pattern` (one of the 8 Quick-Reference pattern keys), `problem`, pattern-specific fields (see
  `quick-reference-engine`'s `references/spec-format.md` for the exact shape per pattern), `agents_table`,
  `tech_table`, and `retrospective`.
- `telecom_deep8_data.py` — `TELECOM_SPECS`, a list of **18** dicts (see coverage note below). Each has `id`,
  `quick_slug`/`quick_title`/`quick_pattern_label` (linking back to the matching `telecom_data.py` entry),
  `title`, `intro`, `problem`, `diagram_note`, `spec` (the actual Deep 8-Layer spec — `l1` through `l8`, `gate`
  — see `deep8-architecture-engine`'s `references/spec-format.md`), and `build_order_params` (a tuple, ready
  to unpack into `generic_build_order(*params)`).

## Coverage note — read before assuming 1:1 parity

`telecom_data.py` has use case ids 1–20. `telecom_deep8_data.py` covers ids **2–20 except 5** (18 of 20) —
use cases 1 and 5 have a Quick-Reference view but no Deep 8-Layer view yet. Checked directly (`set
difference` on the id fields), not assumed. If you're building a page or index from this pack, don't assume
every Quick-Reference use case has a matching Deep 8-Layer entry — check `quick_slug` against
`telecom_data.py`'s `slug` field, or just check for KeyError/missing id, before rendering a "view Deep 8-Layer
version" link.

## Loading into the engines — verified, not just described

Tested directly: both files import with zero dependencies beyond the Python standard library, and both load
correctly into their respective engine skill's functions.

```python
# Quick-Reference engine
import telecom_data
from svg_patterns import BUILDERS       # from the quick-reference-engine skill
from build_order import build_order_for

uc = telecom_data.TELECOM[0]
svg = BUILDERS[uc["pattern"]](uc["title"], uc["orchestrator"], uc["workers"],
                               uc["data_sources"], uc["actions"], uc.get("human_gate"))
order = build_order_for(uc)

# Deep 8-Layer engine
import telecom_deep8_data
from deep8_engine import build_deep8_diagram, auto_blueprint_rows, auto_agent_stack, generic_build_order
from blueprint_table import blueprint_table

entry = telecom_deep8_data.TELECOM_SPECS[0]
diagram_svg   = build_deep8_diagram(entry["spec"])
blueprint_svg = blueprint_table(auto_blueprint_rows(entry["spec"]))
agent_stack   = auto_agent_stack(entry["spec"])
build_order   = generic_build_order(*entry["build_order_params"])
```

Both snippets above were run end-to-end against this pack before shipping it (fresh SVGs generated, no
exceptions) — not just written and assumed correct.

## License and status

This content is licensed under **CC BY-NC 4.0** — see `CONTENT-LICENSE.md` at the repo root for full terms.
**Currently shipped free**, alongside the free skill downloads, while commercial packaging/pricing decisions
are paused pending real traffic/interest signal. The license terms are attached now so this pack is ready to
gate commercially later without any rework — nothing about the pack itself changes when that happens, only
how it's distributed.

## Product description (for the `/skills/` listing page)

> **Telecom Vertical Pack** — 20 real-world telecom AI/agentic use cases (network fault RCA, 5G slicing,
> fraud, churn, and more), each with a Quick-Reference multi-agent pattern spec and (for 18 of the 20) a
> matching Deep 8-Layer regenerative-architecture spec. Drop straight into either engine skill to regenerate
> diagrams, blueprint tables, and build orders — or use as worked examples for writing your own specs.
