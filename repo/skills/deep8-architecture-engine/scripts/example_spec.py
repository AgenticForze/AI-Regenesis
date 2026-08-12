# -*- coding: utf-8 -*-
"""
Complete, runnable worked example. Run this directly to confirm your environment is set up correctly
and to see all four artifacts produced from one spec:

    cd scripts && python3 example_spec.py

Produces (in the current directory):
    example_diagram.svg      - the labeled 8-layer flow diagram
    example_blueprint.svg    - the reference blueprint table
    example_agent_stack.txt  - the agent-level stack table (as plain text; render as markdown/HTML in real use)
    example_build_order.txt  - the six-phase build order
"""
from deep8_engine import build_deep8_diagram, auto_blueprint_rows, auto_agent_stack, generic_build_order
from blueprint_table import blueprint_table

# A worked example: an order-fulfillment decisioning use case (adapted from the BSS/OSS batch).
# Copy this dict's shape as your starting point for a new use case.
EXAMPLE_SPEC = {
    "l1": [
        {"id": "ext1", "title": "Vendor Firmware Advisory Feed", "sub": "External Data Store", "external": True},
        {"id": "int1", "title": "Order Management System DB", "sub": "Internal Data Store"},
        {"id": "int2", "title": "Product Catalog DB", "sub": "Internal Data Store"},
        {"id": "int3", "title": "Network Provisioning Logs", "sub": "Internal Data Store"},
    ],
    "l2": [
        {"id": "gw", "title": "AI Gateway", "sub": "L2 · The Brain"},
        {"id": "llm", "title": "LLM Reasoning Core (Claude)", "sub": "L2 · The Brain"},
        {"id": "kg", "title": "Order/Catalog Knowledge Graph", "sub": "L2 · The Brain", "prod": "Neo4j graph database"},
    ],
    "l3_orch": {"id": "orch", "title": "Order Orchestration Agent", "sub": "L3 · Orchestration"},
    "l3_workers": [
        {"id": "w1", "title": "Order Validation Agent", "sub": "L3 · Specialist"},
        {"id": "w2", "title": "Provisioning Sequencing Agent", "sub": "L3 · Specialist"},
        {"id": "w3", "title": "Activation Confirmation Agent", "sub": "L3 · Specialist"},
    ],
    "l4": [
        {"id": "g1", "title": "Catalog Compliance Policy Engine", "sub": "L4 · Governance"},
        {"id": "g2", "title": "Fallout Risk Guardrail", "sub": "L4 · Governance"},
        {"id": "g3", "title": "Change-Management Rule Engine", "sub": "L4 · Governance"},
    ],
    "gate": {"id": "gate", "title": "Fulfillment Confidence & Risk Gate", "sub": "Conditional routing"},
    "l5": [
        # human at one end, hold at the other — see references/spec-format.md's ordering convention
        {"id": "human", "title": "Order Ops Approval", "sub": "Human-in-the-loop", "color": "leadership", "gate_branch": "human"},
        {"id": "a1", "title": "Billing Activation API", "sub": "L5 · Tool Registry", "gate_branch": "auto"},
        {"id": "a2", "title": "Network Provisioning API", "sub": "L5 · Tool Registry"},
        {"id": "a3", "title": "Customer Notification Gateway", "sub": "L5 · Tool Registry"},
        {"id": "hold", "title": "Fallout Hold Queue", "sub": "Conditional: policy breach", "color": "obs", "gate_branch": "hold"},
    ],
    "l6": [
        {"id": "m1", "title": "Fallout Recurrence Monitor", "sub": "L6 · Nervous System"},
        {"id": "m2", "title": "Data Quality Watchdog", "sub": "L6 · Nervous System"},
        {"id": "m3", "title": "Provisioning Auditor", "sub": "L6 · Nervous System"},
    ],
    "l7": [
        {"id": "lead1", "title": "Order Cycle-Time Dashboard", "sub": "L7 · Leadership Portal"},
        {"id": "lead2", "title": "Fallout Cost Scorecard", "sub": "L7 · Leadership Portal"},
        {"id": "lead3", "title": "Automation Coverage View", "sub": "L7 · Leadership Portal"},
    ],
    "l8": [
        {"id": "s1", "title": "Fulfillment Accuracy Tracker", "sub": "L8 · Self-Healing"},
        {"id": "s2", "title": "Retraining Trigger", "sub": "L8 · Self-Healing"},
        {"id": "s3", "title": "Policy Memory Updater", "sub": "L8 · Self-Healing"},
    ],
}

EXAMPLE_BUILD_ORDER_PARAMS = (
    "order fulfillment",                    # domain_word
    "Order Validation Agent",                # entry_name
    "Order Orchestration Agent",             # orch_name
    2,                                        # n_extra_workers (3 workers - 1 entry = 2)
    "Fulfillment Confidence & Risk Gate",    # gate_name
    "Billing Activation API",                # l5_auto_name
    "Order Ops Approval",                    # human_name
)


def main():
    diagram_svg = build_deep8_diagram(EXAMPLE_SPEC)
    blueprint_svg = blueprint_table(auto_blueprint_rows(EXAMPLE_SPEC))
    agent_stack = auto_agent_stack(EXAMPLE_SPEC)
    build_order = generic_build_order(*EXAMPLE_BUILD_ORDER_PARAMS)

    with open("example_diagram.svg", "w") as f:
        f.write(diagram_svg)
    with open("example_blueprint.svg", "w") as f:
        f.write(blueprint_svg)

    with open("example_agent_stack.txt", "w") as f:
        f.write(f"{'Layer':6}{'Agent Name':35}{'Purpose'}\n")
        f.write("-" * 100 + "\n")
        for layer, name, purpose, io, learn, prod in agent_stack:
            f.write(f"{layer:6}{name:35}{purpose}\n")

    with open("example_build_order.txt", "w") as f:
        for i, phase in enumerate(build_order, 1):
            f.write(f"{phase}\n\n")

    print(f"Diagram: {len(diagram_svg)} chars -> example_diagram.svg")
    print(f"Blueprint: {len(blueprint_svg)} chars -> example_blueprint.svg")
    print(f"Agent stack: {len(agent_stack)} rows -> example_agent_stack.txt")
    print(f"Build order: {len(build_order)} phases -> example_build_order.txt")
    print()
    print("Now validate the SVGs before trusting this output:")
    print("  pip install cairosvg --break-system-packages")
    print("  python3 -c \"import cairosvg; cairosvg.svg2png(url='example_diagram.svg', write_to='example_diagram.png')\"")
    print("  # then view example_diagram.png")


if __name__ == "__main__":
    main()
