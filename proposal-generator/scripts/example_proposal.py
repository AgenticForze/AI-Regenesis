# -*- coding: utf-8 -*-
"""
Complete, runnable worked example. Run this directly to confirm your environment is set up correctly:

    cd scripts && python3 example_proposal.py

Produces `example_proposal.md` plus `diagram.svg` in the current directory, for a FICTIONAL client
("Northwind Fiber") proposing a real catalog use case (the network fault RCA orchestrator-worker example
used elsewhere in this project's worked examples), quoted at the "Architecture Audit" service tier.

This example does NOT depend on the quick-reference-engine or deep8-architecture-engine skills being
installed — the use case and build order are inlined below (same use case as
quick-reference-engine/scripts/example_spec.py's ORCH_WORKER_UC, for continuity across skills) so this skill
is fully standalone. In real use, you'd import the actual output of those two engines instead of hand-typing
a use case here — see SKILL.md's "Quick start" for that version.
"""
from proposal_engine import render_proposal_markdown

# Same use case as quick-reference-engine's worked example, for continuity — see that skill's
# scripts/example_spec.py for where this would really come from (svg_patterns.BUILDERS + build_order_for).
UC = {
    "title": "Multi-Agent Network Fault RCA & Auto-Remediation",
    "pattern": "orchestrator-worker",
    "problem": (
        "A tier-1 operator's NOC receives thousands of correlated alarms per hour across RAN, transport, "
        "and core domains during a fault storm. Engineers spend 40-60 minutes just correlating alarms to "
        "find the true root cause before remediation even starts, driving SLA breaches and customer "
        "complaints."
    ),
}

BUILD_ORDER_PHASES = [
    "Phase 1 — one worker, no fan-out. Wire a single path end to end before adding parallelism.",
    "Phase 2 — add the fan-out. Bring the remaining worker agents online in parallel and build the "
    "orchestrator's aggregation logic.",
    "Phase 3 — add the governance gate. Wire in SRE approval for high-blast-radius actions.",
    "Phase 4 — observability and feedback. Trace every worker call and add a feedback loop.",
]

# A minimal stand-in for a real deep8_entry (normally the full dict from a *_deep8_data.py pack's
# TELECOM_SPECS list) — only its presence/absence matters to this engine, not its internal shape, so a
# lightweight placeholder is enough to exercise the "with Deep 8-Layer" branch honestly.
DEEP8_ENTRY_PLACEHOLDER = {"quick_slug": "network-fault-rca-remediation"}

DIAGRAM_SVG_PLACEHOLDER = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40">'
    '<rect width="100" height="40" fill="none"/>'
    '<text x="50" y="22" font-size="6" text-anchor="middle">Example diagram placeholder — '
    "in real use this is the actual SVG from svg_patterns.BUILDERS[uc['pattern']](...)</text></svg>"
)

# NOTE: "Northwind Fiber" below is FICTIONAL — invented for this example only, not a real company. Kept out
# of the client_name string itself (rather than e.g. "Northwind Fiber (fictional example client)") because
# client_name gets echoed verbatim several times across the rendered proposal — an inline annotation would
# repeat awkwardly every time. Say it once, here, instead.
if __name__ == "__main__":
    md = render_proposal_markdown(
        client_name="Northwind Fiber",
        uc=UC,
        build_order_phases=BUILD_ORDER_PHASES,
        tier_key="audit",
        price="$8,500 flat fee",
        timeframe="2 weeks from kickoff",
        deep8_entry=DEEP8_ENTRY_PLACEHOLDER,
        consultant_name="Example Consulting Co.",
        prepared_date="2026-08-12",
    )
    with open("example_proposal.md", "w") as f:
        f.write(md)
    with open("diagram.svg", "w") as f:
        f.write(DIAGRAM_SVG_PLACEHOLDER)
    with open("deep8_diagram.svg", "w") as f:
        f.write(DIAGRAM_SVG_PLACEHOLDER)

    print(f"Proposal written: {len(md)} chars -> example_proposal.md (+ 2 placeholder diagram.svg files)")
    print("Read it end to end before trusting the pattern for a real proposal — see SKILL.md's note on "
          "swapping the placeholder diagrams for real engine output.")
