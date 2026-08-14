# -*- coding: utf-8 -*-
"""
Complete, runnable worked example. Run this directly to confirm your environment is set up correctly
and to see all three artifacts produced for a use case, across a sample of the 8 patterns:

    cd scripts && python3 example_spec.py

Produces (in the current directory), for 3 of the 8 patterns (enough to exercise the different node/edge
shapes without writing 8 near-duplicate specs):
    <pattern>_diagram.mmd    - the Mermaid text source
    <pattern>_diagram.svg    - the rendered card diagram (via svg_engine.Diagram)
    <pattern>_build_order.txt - the four-phase build order

Copy any of the three use-case dicts below as your starting point for a new one — each pattern takes a
different, fixed set of fields; see references/spec-format.md for the full field list per pattern.
"""
from templates import orchestrator_worker as mmd_orchestrator_worker
from templates import blackboard as mmd_blackboard
from templates import human_escalation as mmd_human_escalation
from svg_patterns import BUILDERS as SVG_BUILDERS
from build_order import build_order_for

# ---------------------------------------------------------------------------
# Three worked use cases, one per pattern shape, adapted from the BSS/OSS batch.
# ---------------------------------------------------------------------------

ORCH_WORKER_UC = {
    "title": "Multi-Agent Network Fault RCA & Auto-Remediation",
    "pattern": "orchestrator-worker",
    "orchestrator": "NOC Incident Orchestrator Agent",
    "workers": ["RAN Alarm Correlation Agent", "Transport/IP Topology Agent",
                "Core Network (5GC/EPC) Agent", "Historical Ticket Similarity Agent"],
    "data_sources": ["FM/PM Alarms (EMS)", "Network Topology (Netbox)", "Past Incident Tickets (ServiceNow)"],
    "actions": ["Auto-remediation via Ansible/NETCONF", "ServiceNow Incident Update"],
    "human_gate": "SRE Approval for High-Blast-Radius Actions",
}

BLACKBOARD_UC = {
    "title": "Real-Time Fraud Ring Detection",
    "pattern": "blackboard",
    "controller": "Fraud Investigation Controller",
    "agents": ["Device Fingerprint Agent", "Transaction Graph Agent", "Behavioral Anomaly Agent"],
    "store_name": "Shared Fraud Signal Blackboard",
    "actions": ["Freeze Account", "Escalate to Fraud Analyst"],
}

HUMAN_ESCALATION_UC = {
    "title": "Loan Underwriting Exception Handling",
    "pattern": "human-escalation",
    "auto_agents": ["Document Verification Agent", "Credit Risk Scoring Agent"],
    "escalation_gate": "Underwriting Confidence Gate",
    "human_role": "Senior Underwriter",
    "actions": ["Auto-Approve Loan", "Route to Manual Review Queue"],
}

USE_CASES = [ORCH_WORKER_UC, BLACKBOARD_UC, HUMAN_ESCALATION_UC]

MMD_FN = {
    "orchestrator-worker": lambda uc: mmd_orchestrator_worker(
        uc["title"], uc["orchestrator"], uc["workers"], uc["data_sources"], uc["actions"], uc.get("human_gate")),
    "blackboard": lambda uc: mmd_blackboard(
        uc["title"], uc["controller"], uc["agents"], uc["store_name"], uc["actions"]),
    "human-escalation": lambda uc: mmd_human_escalation(
        uc["title"], uc["auto_agents"], uc["escalation_gate"], uc["human_role"], uc["actions"]),
}

SVG_FN = {
    "orchestrator-worker": lambda uc: SVG_BUILDERS["orchestrator-worker"](
        uc["title"], uc["orchestrator"], uc["workers"], uc["data_sources"], uc["actions"], uc.get("human_gate")),
    "blackboard": lambda uc: SVG_BUILDERS["blackboard"](
        uc["title"], uc["controller"], uc["agents"], uc["store_name"], uc["actions"]),
    "human-escalation": lambda uc: SVG_BUILDERS["human-escalation"](
        uc["title"], uc["auto_agents"], uc["escalation_gate"], uc["human_role"], uc["actions"]),
}

if __name__ == "__main__":
    for uc in USE_CASES:
        p = uc["pattern"]
        mmd = MMD_FN[p](uc)
        svg = SVG_FN[p](uc)
        order = build_order_for(uc)

        with open(f"{p}_diagram.mmd", "w") as f:
            f.write(mmd)
        with open(f"{p}_diagram.svg", "w") as f:
            f.write(svg)
        with open(f"{p}_build_order.txt", "w") as f:
            f.write("\n\n".join(order))

        print(f"{p}: mmd {len(mmd)} chars, svg {len(svg)} chars, "
              f"{len(order)} build-order phases -> {p}_diagram.{{mmd,svg}}, {p}_build_order.txt")

    print("\nNow validate the SVGs before trusting this output:")
    print("  pip install cairosvg --break-system-packages")
    print("  python3 -c \"import cairosvg; cairosvg.svg2png(url='orchestrator-worker_diagram.svg', "
          "write_to='orchestrator-worker_diagram.png')\"")
    print("  # then view the .png — repeat for the other 2 patterns, or all 8 if extending this example")
