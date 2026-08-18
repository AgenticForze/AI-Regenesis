---
name: proposal-generator
description: Combines a Quick-Reference multi-agent pattern use case (and, optionally, its matching Deep 8-Layer spec) plus real engagement details — client name, service tier, price, timeframe — into client-ready proposal/pitch content, as structured markdown ready to hand to the docx or pptx skill. Use whenever asked to write a client proposal, consulting pitch, statement-of-work draft, or sales deck content for an AI/agentic architecture engagement, or to turn a catalog use case into something sendable to a prospective client. Distinct from quick-reference-engine and deep8-architecture-engine (which design the architecture itself) — this skill assumes that design work is already done and focuses on the client-facing document that sells it. Never invents a price, timeframe, or client detail — always requires them as real input.
---

# Proposal Generator

Turns an already-designed use case (Quick-Reference pattern, optionally paired with its Deep 8-Layer spec)
into client-ready proposal content — the direct bridge from Phase 3 (skills/catalog) to Phase 4 (the
consulting funnel) in the go-to-market roadmap. Produces markdown text sections; does not generate a `.docx`
or `.pptx` file itself (see "Handing off to docx/pptx" below) — that's the existing `docx`/`pptx` skills'
job, and they're already good at it.

**Never invents a number.** `price` and `timeframe` are required arguments with no default — this engine
raises `ProposalInputError` rather than guessing at what a real engagement should cost or how long it should
take. That's a business decision the person using this skill makes per engagement, not something baked into
the tool.

## What it produces

One markdown document, five sections:

1. **Executive Summary** — client + problem + which service tier is recommended, one paragraph.
2. **The Problem** — the use case's `problem` field, verbatim.
3. **Proposed Architecture** — names the Quick-Reference pattern (with correct grammar — see
   `references/lessons-learned.md` #4), references the attached diagram(s), and adds a paragraph on the
   8-layer framework mapping if a Deep 8-Layer spec was provided.
4. **Suggested Build Order** — the numbered build-order phases (normally from `build_order_for(uc)` in the
   `quick-reference-engine` skill).
5. **Recommended Engagement** — which rung of the service ladder (Architecture Audit / Workshop /
   Embedded Advisory / Certification Program — see `go-to-market-roadmap.md` Phase 4), the price, the
   timeframe, and a concrete next step.

## Quick start

```python
import sys; sys.path.insert(0, "scripts")
from proposal_engine import render_proposal_markdown

# uc: a quick-reference-engine use case (from a vertical pack, or a client's own problem shaped the
# same way — only title/problem/pattern are read, see references/spec-format.md)
uc = {"title": "...", "problem": "...", "pattern": "orchestrator-worker"}

# build_order_phases: normally build_order_for(uc) from the quick-reference-engine skill
build_order_phases = ["Phase 1 — ...", "Phase 2 — ...", "Phase 3 — ...", "Phase 4 — ..."]

md = render_proposal_markdown(
    client_name="Acme Corp",
    uc=uc,
    build_order_phases=build_order_phases,
    tier_key="audit",              # "audit" | "workshop" | "advisory" | "certification"
    price="$8,500 flat fee",       # required — always a real figure, never invented by this engine
    timeframe="2 weeks from kickoff",  # required, same reason
    deep8_entry=None,              # optional — pass a real *_deep8_data.py pack entry to include the
                                    # Deep 8-Layer paragraph and diagram, or leave None to omit it
    consultant_name="Your Name",   # optional
    prepared_date="2026-08-12",    # optional
)
```

## Handing off to docx/pptx

This skill's output is markdown text plus two diagram-filename references (`diagram.svg`,
`deep8_diagram.svg` by convention). To produce an actual Word document or slide deck:

1. Write the real SVGs at those filenames (from `svg_patterns.BUILDERS[...]` and, if used,
   `deep8_engine.build_deep8_diagram(...)` — see `references/spec-format.md`).
2. Convert them to PNG (`cairosvg`) since Word/PowerPoint don't embed SVG reliably.
3. Pass the markdown + PNGs to the `docx` (or `pptx`) skill's own document-creation flow — see that skill's
   `SKILL.md` for its specific gotchas (table widths, heading levels, etc.). Don't try to hand-roll the
   `.docx`/`.pptx` file structure inside this skill.

## Reference files

- `references/spec-format.md` — every argument's shape and requiredness, the `uc` dict's three required
  fields, the diagram-filename convention, and the full docx handoff steps.
- `references/lessons-learned.md` — four real issues found by reading the worked example's rendered output
  (a broken-acronym lowercasing bug, a duplicated heading, a client-name field getting an awkward
  parenthetical echoed repeatedly, and a wrong grammatical article) — all fixed, not just noted. Read before
  extending this engine, especially before adding new pattern names or new templated sentences.
- `scripts/proposal_engine.py` — `SERVICE_TIERS`, `assemble_proposal_sections(...)`,
  `render_proposal_markdown(...)`, and `ProposalInputError` (raised for any missing/invalid required
  argument — see `references/spec-format.md` for exactly which ones).
- `scripts/example_proposal.py` — one complete, runnable worked example (fictional client, real catalog use
  case, placeholder diagrams) — run it directly to confirm your environment is set up correctly and to see
  the full document shape before writing a real proposal.
