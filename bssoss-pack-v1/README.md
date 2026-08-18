# BSS/OSS Vertical Pack — v1

**What's in this pack:** the BSS/OSS domain's content for the AI-Regenesis catalog — 20 use cases as
Quick-Reference specs, and their matching Deep 8-Layer specs, as two pure-data Python files. No engine code,
no rendering logic — load these into the `quick-reference-engine` and `deep8-architecture-engine` skills (or
your own copy of the underlying scripts) to regenerate diagrams, tables, and build orders.

## Files

- `bssoss_data.py` — `BSSOSS`, a list of 20 dicts, one per use case (order-to-activation orchestration,
  product catalog automation, revenue assurance, order fallout recovery, network inventory reconciliation,
  mediation/CDR pipelines, and more). Same field shape as the Telecom pack — see `quick-reference-engine`'s
  `references/spec-format.md`.
- `bssoss_deep8_data.py` — `BSSOSS_SPECS`, a list of 20 dicts. Same field shape as the Telecom pack — see
  `deep8-architecture-engine`'s `references/spec-format.md`.

## Coverage note

Checked directly (id-set comparison, not assumed): all 20 `bssoss_data.py` use case ids have a matching
`bssoss_deep8_data.py` entry. Full 1:1 parity for this pack — unlike the Telecom pack, which is missing 2 of
20 (see that pack's README).

## Loading into the engines — verified, not just described

Same loading pattern as the Telecom pack (see that README for the full code sample); tested directly against
this pack's first entry (`bssoss_data.BSSOSS[0]`, pattern `"pipeline"`) before shipping — real SVG generated,
no exceptions, both the Quick-Reference and Deep 8-Layer engines.

```python
import bssoss_data
from svg_patterns import BUILDERS
from build_order import build_order_for
uc = bssoss_data.BSSOSS[0]
svg = BUILDERS[uc["pattern"]](uc["title"], uc["stages"], uc["actions"])   # pipeline pattern's actual args
order = build_order_for(uc)

import bssoss_deep8_data
from deep8_engine import build_deep8_diagram
entry = bssoss_deep8_data.BSSOSS_SPECS[0]
diagram_svg = build_deep8_diagram(entry["spec"])
```

Note the `pipeline` pattern's positional args (`title, stages, actions`) differ from `orchestrator-worker`'s
— check `uc["pattern"]` and use the matching signature from `spec-format.md`, don't assume every entry in
this pack takes the same call shape.

## License and status

CC BY-NC 4.0 — see `CONTENT-LICENSE.md` at the repo root. **Currently shipped free**, licensing terms attached
and ready to gate commercially once the Phase 3c resume trigger (real traffic/interest signal) is hit — see
the Telecom pack's README for the full rationale, which applies identically here.

## Product description (for the `/skills/` listing page)

> **BSS/OSS Vertical Pack** — 20 telecom back-office AI/agentic use cases (order orchestration, revenue
> assurance, fallout recovery, network inventory reconciliation, mediation pipelines, and more), each with a
> full Quick-Reference and Deep 8-Layer spec pair. Full 1:1 coverage across all 20 use cases. Drop straight
> into either engine skill to regenerate diagrams, blueprint tables, and build orders.
