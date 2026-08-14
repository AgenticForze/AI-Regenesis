# Finance Vertical Pack — v1

**What's in this pack:** the Finance domain's content for the AI-Regenesis catalog — 20 use cases as
Quick-Reference specs, and their matching Deep 8-Layer specs, as two pure-data Python files. No engine code,
no rendering logic — load these into the `quick-reference-engine` and `deep8-architecture-engine` skills (or
your own copy of the underlying scripts) to regenerate diagrams, tables, and build orders.

## Files

- `finance_data.py` — `FINANCE`, a list of 20 dicts, one per use case (AML transaction monitoring, credit
  underwriting, algorithmic trading orchestration, card-not-present fraud, KYC onboarding, robo-advisory
  rebalancing, and more). Same field shape as the other two packs — see `quick-reference-engine`'s
  `references/spec-format.md`.
- `finance_deep8_data.py` — `FINANCE_SPECS`, a list of 20 dicts. Same field shape as the other two packs —
  see `deep8-architecture-engine`'s `references/spec-format.md`.

## Coverage note

Checked directly (id-set comparison, not assumed): all 20 `finance_data.py` use case ids have a matching
`finance_deep8_data.py` entry. Full 1:1 parity for this pack, same as the BSS/OSS pack.

## Loading into the engines — verified, not just described

Tested directly against this pack's first entry (`finance_data.FINANCE[0]`, `"AML Transaction Monitoring &
SAR Filing"`, pattern `"orchestrator-worker"`) before shipping — real SVG generated, no exceptions, both
engines.

```python
import finance_data
from svg_patterns import BUILDERS
from build_order import build_order_for
uc = finance_data.FINANCE[0]
svg = BUILDERS[uc["pattern"]](uc["title"], uc["orchestrator"], uc["workers"],
                               uc["data_sources"], uc["actions"], uc.get("human_gate"))
order = build_order_for(uc)

import finance_deep8_data
from deep8_engine import build_deep8_diagram
entry = finance_deep8_data.FINANCE_SPECS[0]
diagram_svg = build_deep8_diagram(entry["spec"])
```

## A note specific to Finance content

Per this project's own style guideline (`CONTRIBUTING.md`): financial calculations in these use cases are
kept in deterministic rules engines, not LLM output — several `retrospective` entries in this pack call that
out explicitly as a lesson learned from the (fictional, illustrative) build process. Worth preserving that
framing if you adapt this content — it's a deliberate design stance in the source material, not an oversight
to "fix" when reusing these specs.

## License and status

CC BY-NC 4.0 — see `CONTENT-LICENSE.md` at the repo root. **Currently shipped free**, licensing terms attached
and ready to gate commercially once the Phase 3c resume trigger (real traffic/interest signal) is hit — see
the Telecom pack's README for the full rationale, which applies identically here.

## Product description (for the `/skills/` listing page)

> **Finance Vertical Pack** — 20 financial-services AI/agentic use cases (AML/SAR filing, credit
> underwriting, algorithmic trading, card-not-present fraud, KYC onboarding, robo-advisory, and more), each
> with a full Quick-Reference and Deep 8-Layer spec pair. Full 1:1 coverage across all 20 use cases. Drop
> straight into either engine skill to regenerate diagrams, blueprint tables, and build orders.
