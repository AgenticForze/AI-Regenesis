# -*- coding: utf-8 -*-
"""
Generic Deep 8-Layer engine. Instead of hand-coding a bespoke Diagram-building function per use case
(as was done for the two pilots), every use case is described as a single structured dict (a "spec").
This module turns that spec into three things from one source of truth:
  1. The labeled flow diagram SVG (reusing the proven layout/edge-routing from the pilots)
  2. The 8-layer blueprint table SVG (reusing blueprint_table())
  3. The agent-level stack table + build order for the markdown doc / website JSON

Spec shape (see bssoss_deep8_data.py for real examples):
{
  "l1": [{"id","title","sub","external": bool}, ...],          # 2-6 items
  "l2": [{"id","title","sub"}, ...],                             # usually 3 items
  "l3_orch": {"id","title","sub"} or None,                       # single node, own row (omit for pipeline-style)
  "l3_workers": [{"id","title","sub"}, ...],
  "l4": [{"id","title","sub"}, ...],                              # usually 3 items
  "gate": {"id","title","sub"} or None,
  "l5": [{"id","title","sub","color","gate_branch": "auto"|"human"|"hold"|None}, ...],
  "l6": [{"id","title","sub"}, ...],
  "l7": [{"id","title","sub"}, ...],
  "l8": [{"id","title","sub"}, ...],
  "blueprint_rows": [ ...8 rows, same shape as blueprint_table() expects... ],
  "agent_stack": [ (layer, name, purpose, io, learn, prod), ... ],
  "build_order": [ "...", "...", ... ],
}
"""
from svg_engine import Diagram

LAYER_META = {
    "L8": ("channel", "Feedback & Reinforcement Loops",
           "The Learner — reviews results, catches mistakes, and automatically retrains the system to improve over time."),
    "L7": ("leadership", "Leadership Dashboard Layer",
           "The Scorecard — links AI actions to dollars, ROI, and ethics for executive oversight."),
    "L6": ("obs", "End-to-End Observability",
           "The Watchdog — monitors data health in real time and sounds the alarm on bias or drift."),
    "L5": ("action", "Execution & Interaction",
           "The Hands — turns the digital choice into a real-world task: a system update, a message, a human ask."),
    "L4": ("orch", "Decisions Engineering & SECI Framework",
           "The Rulebook — keeps the AI within business, ethical, and regulatory guardrails."),
    "L3": ("agent", "Agentic Core",
           "The Logic Engine — where agents reason, remember past context, and talk to each other."),
    "L2": ("memory", "Agent Intelligence & Models",
           "The Intelligence — core AI power (LLMs) and specialized knowledge graphs."),
    "L1": ("data", "Foundational Data & Infrastructure",
           "The Foundation — secure cloud, databases, and the raw data everything else sits on."),
}

LAYER_IO_DEFAULT = {
    "L2": "Agent requests → Model responses, usage telemetry",
    "L3": "Task context, Working Memory → Reasoning output, next-step decision",
    "L4": "Proposed action, policy rules → Pass/fail decision",
    "L5": "Approved decision → Executed action, system update",
    "L6": "Live execution/outcome telemetry → Alert, health score",
    "L7": "Outcome + financial data → Executive-facing metric",
    "L8": "Outcome-accuracy data, thresholds → Retraining trigger / updated memory",
}

LAYER_STACK_DEFAULT = {
    "L2": ("Claude API called directly", "LiteLLM / Portkey model-routing gateway with cost tracking"),
    "L3": ("LangGraph agent node + Claude API", "LangGraph on Temporal for durable, at-scale execution"),
    "L4": ("Plain Python rule functions", "Open Policy Agent (OPA) rules engine"),
    "L5": ("Mock REST endpoint (FastAPI)", "Real system API behind a common tool-calling interface"),
    "L6": ("Scheduled Python script / simple threshold check", "Statistical drift/anomaly detection service (e.g., Evidently AI)"),
    "L7": ("Streamlit or Metabase dashboard", "BI dashboard (Looker/Tableau) wired to a data warehouse"),
    "L8": ("Cron job checking a threshold", "Prefect/Airflow orchestrating scheduled retraining jobs"),
}


def _layer_key(code):
    return {"L1": "l1", "L2": "l2", "L4": "l4", "L6": "l6", "L7": "l7", "L8": "l8"}.get(code)


def auto_blueprint_rows(spec):
    import textwrap
    rows = []
    for code in ["L8", "L7", "L6", "L5", "L4", "L3", "L2", "L1"]:
        color, title, desc = LAYER_META[code]
        if code == "L3":
            items = ([spec["l3_orch"]] if spec.get("l3_orch") else []) + spec["l3_workers"]
        elif code == "L5":
            items = spec["l5"]
        else:
            items = spec[_layer_key(code)]
        solution = "; ".join(it["title"] for it in items) + "."
        prod_bits = [it.get("prod") for it in items if it.get("prod")]
        if not prod_bits and code in LAYER_STACK_DEFAULT:
            prod_bits = [LAYER_STACK_DEFAULT[code][1]]
        tools = " · ".join(prod_bits) if prod_bits else "—"
        rows.append({"layer": code, "color": color, "title": title, "desc": desc, "solution": solution, "tools": tools})
    return rows


LAYER_PURPOSE_TEMPLATE = {
    "L2": "Provides {t}'s reasoning/knowledge capability to the Agentic Core.",
    "L3": "{t} — specialist agent in the Agentic Core's reasoning chain.",
    "L4": "Enforces {t} as a governance gate before any action reaches the Action Layer.",
    "L5": "Executes {t} as part of the Action & Execution layer once a decision is approved.",
    "L6": "Continuously monitors for the failure mode {t} is named to catch.",
    "L7": "Gives leadership real-time visibility via {t}.",
    "L8": "Closes the feedback loop via {t}, feeding outcomes back into memory.",
}


def _default_purpose(code, title):
    tmpl = LAYER_PURPOSE_TEMPLATE.get(code, "{t}")
    return tmpl.format(t=title)


def auto_agent_stack(spec):
    order = []
    for it in spec.get("l2", []):
        order.append(("L2", it))
    if spec.get("l3_orch"):
        order.append(("L3", spec["l3_orch"]))
    for it in spec.get("l3_workers", []):
        order.append(("L3", it))
    for it in spec.get("l4", []):
        order.append(("L4", it))
    for it in spec.get("l5", []):
        order.append(("L5", it))
    for it in spec.get("l6", []):
        order.append(("L6", it))
    for it in spec.get("l7", []):
        order.append(("L7", it))
    for it in spec.get("l8", []):
        order.append(("L8", it))

    rows = []
    for code, it in order:
        purpose = it.get("purpose", _default_purpose(code, it["title"]))
        io = it.get("io", LAYER_IO_DEFAULT.get(code, ""))
        learn = it.get("learn", LAYER_STACK_DEFAULT.get(code, ("", ""))[0])
        prod = it.get("prod", LAYER_STACK_DEFAULT.get(code, ("", ""))[1])
        rows.append((code, it["title"], purpose, io, learn, prod))
    return rows


def generic_build_order(domain_word, entry_name, orch_name, n_extra_workers, gate_name, l5_auto_name, human_name=None):
    phase3 = (f"**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, "
              f"then build the three-way {gate_name} routing into auto-execute / human review / hold.")
    phase4 = (f"**Phase 4 — complete L5.** Build the {human_name} approval screen and the hold/escalate queue; "
              f"this is the first point where a human is actually in the loop." if human_name else
              f"**Phase 4 — complete L5.** Wire the remaining L5 tool integrations behind the same tool-calling "
              f"interface as {l5_auto_name}.")
    orch_bit = f", with {orch_name} just passing data through untouched" if orch_name else ""
    phase2 = (f"**Phase 2 — build out L3, the Agentic Core.** "
              f"Bring the remaining {n_extra_workers} agent{'s' if n_extra_workers != 1 else ''} online"
              + (f" and build {orch_name}'s aggregation logic" if orch_name else "")
              + ", and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.")
    return [
        f"**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake {domain_word} data in Postgres, a single Claude "
        f"API call, and {entry_name} producing a result that just gets printed{orch_bit}. No memory, no "
        f"governance, no conditional routing yet.",
        phase2,
        phase3,
        phase4,
        "**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. "
        "This is usually the point where problems invisible in Phases 1–4 surface for the first time.",
        "**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-"
        "update job. These teach the least new technical ground but close the loop the manuscript calls "
        "\"regenerative.\"",
    ]


def build_deep8_diagram(spec):
    d = Diagram()

    l1_nodes = [d.node(it["id"], it["title"], it["sub"], "data", external=it.get("external", False)) for it in spec["l1"]]
    d.add_row(l1_nodes, label=("L1", "Foundational Data & Infrastructure", None))

    l2_nodes = [d.node(it["id"], it["title"], it["sub"], it.get("color", "agent")) for it in spec["l2"]]
    d.add_row(l2_nodes, label=("L2", "Agent Intelligence & Models", None))

    has_orch = spec.get("l3_orch") is not None
    if has_orch:
        orch = spec["l3_orch"]
        orch_node = d.node(orch["id"], orch["title"], orch["sub"], "orch")
        d.add_row([orch_node], label=("L3", "Agentic Core", "Orchestration & Reasoning"))

    l3_worker_nodes = [d.node(it["id"], it["title"], it["sub"], it.get("color", "agent")) for it in spec["l3_workers"]]
    if has_orch:
        d.add_row(l3_worker_nodes)
    else:
        d.add_row(l3_worker_nodes, label=("L3", "Agentic Core", "Orchestration & Reasoning"))

    mem_specs = [
        ("mem_work", "Working Memory", "Short-Term · current session"),
        ("mem_epis", "Episodic Memory", "Long-Term · past cases"),
        ("mem_sem", "Semantic Memory", "Long-Term · domain knowledge"),
        ("mem_pol", "Policy Memory", "Long-Term · governance rules"),
    ]
    mem_nodes = [d.node(mid, title, sub, "memory") for mid, title, sub in mem_specs]
    d.add_row(mem_nodes)

    l4_nodes = [d.node(it["id"], it["title"], it["sub"], "orch") for it in spec["l4"]]
    d.add_row(l4_nodes, label=("L4", "Decisions Engineering & SECI Framework", "Governance & Logic"))

    has_gate = spec.get("gate") is not None
    if has_gate:
        gate = spec["gate"]
        gate_node = d.node(gate["id"], gate["title"], gate["sub"], "orch")
        d.add_row([gate_node])

    l5_nodes = [d.node(it["id"], it["title"], it["sub"], it.get("color", "action")) for it in spec["l5"]]
    d.add_row(l5_nodes, label=("L5", "Execution & Interaction", "Action Layer"))

    l6_nodes = [d.node(it["id"], it["title"], it["sub"], "obs") for it in spec["l6"]]
    d.add_row(l6_nodes, label=("L6", "End-to-End Observability", "The Nervous System"))

    l7_nodes = [d.node(it["id"], it["title"], it["sub"], "leadership") for it in spec["l7"]]
    d.add_row(l7_nodes, label=("L7", "Leadership Dashboard Layer", "Accountability & Outcomes"))

    l8_nodes = [d.node(it["id"], it["title"], it["sub"], "obs") for it in spec["l8"]]
    d.add_row(l8_nodes, label=("L8", "Feedback & Reinforcement Loops", "Self-Healing"))

    # --- standard edge topology (same proven shape as the two pilots) ---
    l2_entry = l2_nodes[0].id
    for n in l1_nodes:
        d.edge(n.id, l2_entry)
    for n in l2_nodes[1:]:
        d.edge(l2_entry, n.id)

    l3_entry = spec["l3_orch"]["id"] if has_orch else (l3_worker_nodes[0].id if l3_worker_nodes else l2_entry)
    for n in l2_nodes[1:] or [l2_nodes[0]]:
        d.edge(n.id, l3_entry)

    if has_orch:
        for n in l3_worker_nodes:
            d.edge(l3_entry, n.id)

    # memory hookups: rotate through workers/orch so every memory type gets at least one owner
    mem_owners = ([l3_entry] if has_orch else []) + [n.id for n in l3_worker_nodes]
    for i, (mid, _, _) in enumerate(mem_specs):
        if mem_owners:
            d.edge(mem_owners[i % len(mem_owners)], mid, bidir=True, dashed=True)

    # workers/orch -> L4 governance (fan into governance items round-robin)
    l4_ids = [n.id for n in l4_nodes]
    l3_sources = l3_worker_nodes if l3_worker_nodes else ([spec["l3_orch"]] if has_orch else [])
    for i, n in enumerate(l3_sources):
        target = l4_ids[i % len(l4_ids)] if l4_ids else None
        if target:
            src_id = n.id if hasattr(n, "id") else n["id"]
            d.edge(src_id, target)

    if has_gate:
        for n in l4_nodes:
            d.edge(n.id, gate_node.id)
        branch_labels = {"auto": "high confidence", "human": "medium confidence", "hold": "low confidence"}
        for it in spec["l5"]:
            branch = it.get("gate_branch")
            if branch:
                d.edge(gate_node.id, it["id"], dashed=(branch == "hold"), label=branch_labels.get(branch))
    else:
        for n in l4_nodes:
            for it in spec["l5"]:
                if it.get("gate_branch"):
                    d.edge(n.id, it["id"])
                    break

    # L5 internal chain (link action items in sequence, skipping human/hold branch nodes)
    action_chain = [it for it in spec["l5"] if not it.get("gate_branch") or it.get("gate_branch") == "auto"]
    for i in range(len(action_chain) - 1):
        d.edge(action_chain[i]["id"], action_chain[i + 1]["id"])

    # L5 -> L6 telemetry
    for i, n in enumerate(l6_nodes):
        src = spec["l5"][i % len(spec["l5"])]["id"]
        d.edge(src, n.id, dashed=True)

    # L6 -> L7
    for i, n in enumerate(l7_nodes):
        src = l6_nodes[i % len(l6_nodes)].id
        d.edge(src, n.id, dashed=True)

    # L7 -> L8 (first item only, matching pilot convention)
    if l7_nodes and l8_nodes:
        d.edge(l7_nodes[0].id, l8_nodes[0].id, dashed=True)

    # L8 internal chain
    for i in range(len(l8_nodes) - 1):
        d.edge(l8_nodes[i].id, l8_nodes[i + 1].id)

    # L8 closes the loop back into memory (unlabeled, long jump — matches pilot convention)
    if l8_nodes:
        d.edge(l8_nodes[-1].id, "mem_pol", dashed=True)
        d.edge(l8_nodes[-1].id, "mem_epis", dashed=True)

    return d.render()
