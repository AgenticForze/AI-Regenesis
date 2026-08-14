# -*- coding: utf-8 -*-
"""
One builder per architecture pattern, each returning a rendered SVG string via the Diagram engine.
Takes the exact same parameters as the old Mermaid template functions in templates.py, so no changes
were needed to telecom_data.py / bssoss_data.py / finance_data.py.
"""
from svg_engine import Diagram, COLORS, esc

L_DATA = "Data & Integration"
L_ORCH = "Orchestration"
L_AGENT = "Specialist Agent"
L_ACTION = "Action & Execution"
L_OBS = "Observability & Governance"


def orchestrator_worker(title, orchestrator, workers, data_sources, actions, human_gate=None):
    d = Diagram()
    data_nodes = [d.node(f"d{i}", s, L_DATA, "data") for i, s in enumerate(data_sources)]
    d.add_row(data_nodes)
    orch = d.node("orch", orchestrator, L_ORCH, "orch")
    d.add_row([orch])
    workers_nodes = [d.node(f"w{i}", w, L_AGENT, "agent") for i, w in enumerate(workers)]
    d.add_row(workers_nodes)
    agg = d.node("agg", "Aggregator / Synthesis Agent", "Combines findings", "agent")
    d.add_row([agg])
    if human_gate:
        gate = d.node("gate", human_gate, "Human review", "obs")
        d.add_row([gate])
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    for n in data_nodes:
        d.edge(n.id, "orch")
    for n in workers_nodes:
        d.edge("orch", n.id)
        d.edge(n.id, "agg")
    if human_gate:
        d.edge("agg", "gate")
        for n in act_nodes:
            d.edge("gate", n.id)
    else:
        for n in act_nodes:
            d.edge("agg", n.id)
    return d.render()


def hierarchical(title, top, mid_layer, leaves_by_mid, actions):
    d = Diagram()
    top_n = d.node("top", top, L_ORCH, "orch")
    d.add_row([top_n])
    mid_nodes = [d.node(f"m{i}", m, "Domain Manager", "agent") for i, m in enumerate(mid_layer)]
    d.add_row(mid_nodes)
    leaf_nodes = []
    for i, leaves in enumerate(leaves_by_mid):
        for j, leaf in enumerate(leaves):
            leaf_nodes.append((i, d.node(f"l{i}_{j}", leaf, L_AGENT, "agent")))
    d.add_row([n for _, n in leaf_nodes])
    res = d.node("res", "Resolution / Reporting Agent", "Consolidates output", "agent")
    d.add_row([res])
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    for n in mid_nodes:
        d.edge("top", n.id)
    for i, n in leaf_nodes:
        d.edge(f"m{i}", n.id)
    d.edge("top", "res")
    for n in act_nodes:
        d.edge("res", n.id)
    return d.render()


def pipeline(title, stages, actions):
    d = Diagram()
    for i, s in enumerate(stages):
        n = d.node(f"s{i}", s, f"Stage {i+1} of {len(stages)}", "agent")
        d.add_row([n])
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    for i in range(len(stages) - 1):
        d.edge(f"s{i}", f"s{i+1}")
    for n in act_nodes:
        d.edge(f"s{len(stages)-1}", n.id)
    return d.render()


def blackboard(title, controller, agents, store_name, actions):
    d = Diagram()
    store = d.node("store", store_name, "Shared Data Layer", "data")
    d.add_row([store])
    ctrl = d.node("ctrl", controller, L_ORCH, "orch")
    d.add_row([ctrl])
    agent_nodes = [d.node(f"ag{i}", a, "Reads / writes blackboard", "agent") for i, a in enumerate(agents)]
    d.add_row(agent_nodes)
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    d.edge("store", "ctrl", bidir=True)
    for n in agent_nodes:
        d.edge("ctrl", n.id, dashed=True)
    for n in act_nodes:
        d.edge("ctrl", n.id)
    return d.render()


def debate_critique(title, proposer, critic, arbiter, refs, actions):
    d = Diagram()
    ref_nodes = [d.node(f"r{i}", r, L_DATA, "data") for i, r in enumerate(refs)]
    d.add_row(ref_nodes)
    p = d.node("p", proposer, "Proposes", "agent")
    c = d.node("c", critic, "Challenges", "agent")
    d.add_row([p, c])
    arb = d.node("arb", arbiter, "Final decision", "orch")
    d.add_row([arb])
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    for n in ref_nodes:
        d.edge(n.id, "p")
    d.edge("p", "c")
    d.edge("c", "p", dashed=True)
    d.edge("c", "arb")
    for n in act_nodes:
        d.edge("arb", n.id)
    return d.render()


def market_based(title, auctioneer, bidders, actions):
    d = Diagram()
    ctx = d.node("ctx", "Live Market / Resource State", L_DATA, "data")
    d.add_row([ctx])
    auc = d.node("auc", auctioneer, L_ORCH, "orch")
    d.add_row([auc])
    bidder_nodes = [d.node(f"b{i}", b, "Submits bids", "agent") for i, b in enumerate(bidders)]
    d.add_row(bidder_nodes)
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    d.edge("ctx", "auc")
    for n in bidder_nodes:
        d.edge(n.id, "auc")
    for n in act_nodes:
        d.edge("auc", n.id)
    return d.render()


def event_swarm(title, bus_name, agents, actions):
    d = Diagram()
    bus = d.node("bus", bus_name, "Event Bus", "data")
    d.add_row([bus])
    agent_nodes = [d.node(f"ag{i}", a, "Reactive agent", "agent") for i, a in enumerate(agents)]
    d.add_row(agent_nodes)
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    for n in agent_nodes:
        d.edge("bus", n.id)
        d.edge(n.id, "bus", dashed=True)
    for n in act_nodes:
        d.edge("bus", n.id)
    return d.render()


def human_escalation(title, auto_agents, escalation_gate, human_role, actions):
    d = Diagram()
    for i, a in enumerate(auto_agents):
        n = d.node(f"aa{i}", a, f"Automation step {i+1}", "agent")
        d.add_row([n])
    gate = d.node("gate", escalation_gate, "Confidence / risk check", "orch")
    d.add_row([gate])
    auto = d.node("auto", "Auto-resolve", "Low risk / high confidence", "agent")
    human = d.node("human", human_role, "High risk / low confidence", "obs")
    d.add_row([auto, human])
    act_nodes = [d.node(f"a{i}", a, L_ACTION, "action") for i, a in enumerate(actions)]
    d.add_row(act_nodes)

    for i in range(len(auto_agents) - 1):
        d.edge(f"aa{i}", f"aa{i+1}")
    d.edge(f"aa{len(auto_agents)-1}", "gate")
    d.edge("gate", "auto")
    d.edge("gate", "human")
    d.edge("human", "auto", dashed=True)
    for n in act_nodes:
        d.edge("auto", n.id)
    return d.render()


def e2e_platform():
    """Hand-authored, one-off: the full platform reference architecture across all three domains."""
    d = Diagram()
    ch = [
        d.node("ch0", "Customer App / Web", "Channel", "channel"),
        d.node("ch1", "Contact Center / Agent Desktop", "Channel", "channel"),
        d.node("ch2", "Partner & Wholesale Portals", "Channel", "channel"),
        d.node("ch3", "Internal Ops Consoles", "Channel", "channel"),
    ]
    d.add_row(ch)
    data = [
        d.node("da0", "API Gateway", "TM Forum Open APIs", "data"),
        d.node("da1", "Event Bus", "Kafka", "data"),
        d.node("da2", "Customer 360 / Master Data", "Data & Integration", "data"),
        d.node("da3", "Vector Store / Knowledge Base", "Data & Integration", "data"),
    ]
    d.add_row(data)
    orch = [
        d.node("meta", "Cross-Domain Meta-Orchestrator", "Orchestration", "orch"),
        d.node("s_t", "Telecom Domain Supervisor", "Orchestration", "orch"),
        d.node("s_b", "BSS/OSS Domain Supervisor", "Orchestration", "orch"),
        d.node("s_f", "Finance Domain Supervisor", "Orchestration", "orch"),
    ]
    d.add_row(orch)
    mesh = [
        d.node("mesh_t", "Telecom Agents", "20 use cases", "agent"),
        d.node("mesh_b", "BSS/OSS Agents", "20 use cases", "agent"),
        d.node("mesh_f", "Finance Agents", "20 use cases", "agent"),
    ]
    d.add_row(mesh)
    action = [
        d.node("ac0", "OSS / Network Systems", "Action & Execution", "action"),
        d.node("ac1", "Billing / CRM / Order Mgmt", "Action & Execution", "action"),
        d.node("ac2", "Core Banking / Trading Systems", "Action & Execution", "action"),
    ]
    d.add_row(action)
    obs = d.node("obs", "Observability & Governance Layer",
                  "Tracing · Audit · Guardrails · Agent Eval · Human Council", "obs")
    d.add_row([obs])

    d.edge("ch0", "da0"); d.edge("ch1", "da0"); d.edge("ch2", "da0"); d.edge("ch3", "da1")
    for n in data:
        d.edge(n.id, "meta")
    d.edge("meta", "s_t"); d.edge("meta", "s_b"); d.edge("meta", "s_f")
    d.edge("s_t", "mesh_t"); d.edge("s_b", "mesh_b"); d.edge("s_f", "mesh_f")
    d.edge("mesh_t", "ac0")
    d.edge("mesh_b", "ac1"); d.edge("mesh_b", "ac0")
    d.edge("mesh_f", "ac2")
    d.edge("meta", "obs", dashed=True)
    d.edge("mesh_t", "obs", dashed=True)
    d.edge("mesh_b", "obs", dashed=True)
    d.edge("mesh_f", "obs", dashed=True)
    d.edge("ac0", "obs", dashed=True)
    d.edge("ac2", "obs", dashed=True)
    return d.render()


def decision_engineering_meta_architecture():
    """
    Flagship reference example: the 8-layer Integrated Decision Engineering Meta-Architecture
    (L1 Base -> L8 Self-Healing Loop), applied to a concrete use case — Enterprise Customer
    Retention Investment Decisioning — with the AI Gateway / Agent Plane / Tool Registry / four-part
    Memory Layer internals from the companion "Core Architectural Components" model mapped onto it,
    explicit conditional edges (the Confidence & Risk Gate's three branches), and internal vs.
    external data stores (external stores rendered with a dashed card border).
    """
    d = Diagram()

    # L1 — The Base: external + internal data stores
    ext1 = d.node("ext1", "Credit Bureau Feed", "External Data Store", "data", external=True)
    ext2 = d.node("ext2", "Competitor Pricing Intel", "External Data Store", "data", external=True)
    ext3 = d.node("ext3", "Macroeconomic Indicators", "External Data Store", "data", external=True)
    int1 = d.node("int1", "Customer 360 / CRM DB", "Internal Data Store", "data")
    int2 = d.node("int2", "Billing & Usage (CDR) DB", "Internal Data Store", "data")
    int3 = d.node("int3", "Offer & Contract Catalog DB", "Internal Data Store", "data")
    d.add_row([ext1, ext2, ext3, int1, int2, int3], label=("L1", "Foundational Data & Infrastructure", None))

    # L2 — The Brain: AI Gateway + reasoning core
    gw = d.node("gw", "AI Gateway", "L2 · The Brain", "orch")
    llm = d.node("llm", "LLM Reasoning Core (Claude)", "L2 · The Brain", "agent")
    kg = d.node("kg", "Churn & Customer Knowledge Graph", "L2 · The Brain", "agent")
    d.add_row([gw, llm, kg], label=("L2", "Agent Intelligence & Models", None))

    # L3 — Thinking Center: Agent Plane
    plan = d.node("plan", "Planner Module", "L3 · Agent Plane", "agent")
    exec_ = d.node("exec", "Execution Manager", "L3 · Agent Plane", "agent")
    refl = d.node("refl", "Reflection Engine", "L3 · Agent Plane", "agent")
    conf = d.node("conf", "Confidence Scorer", "L3 · Agent Plane", "agent")
    d.add_row([plan, exec_, refl, conf], label=("L3", "Agentic Core", "Orchestration & Reasoning"))

    # L3 — Memory Layer (short-term + long-term), explicitly labeled
    mem_work = d.node("mem_work", "Working Memory", "Short-Term · current session", "memory")
    mem_epis = d.node("mem_epis", "Episodic Memory", "Long-Term · past campaigns", "memory")
    mem_sem = d.node("mem_sem", "Semantic Memory", "Long-Term · domain knowledge", "memory")
    mem_pol = d.node("mem_pol", "Policy Memory", "Long-Term · governance rules", "memory")
    d.add_row([mem_work, mem_epis, mem_sem, mem_pol])

    # L4 — The Conscience: rules, ethics, regulation
    rule_margin = d.node("rule_margin", "Discount & Margin Policy Engine", "L4 · The Conscience", "orch")
    rule_fair = d.node("rule_fair", "Fairness & Non-Discrimination Guardrail", "L4 · The Conscience", "orch")
    rule_reg = d.node("rule_reg", "Regulatory Constraint Engine (consumer protection)", "L4 · The Conscience", "orch")
    d.add_row([rule_margin, rule_fair, rule_reg], label=("L4", "Decisions Engineering & SECI Framework", "Governance & Logic"))

    # Conditional decision gate (the explicit conditional-edge branch point)
    gate = d.node("gate", "Confidence & Risk Gate", "Conditional routing", "orch")
    d.add_row([gate])

    # L5 — Action Layer: Tool Registry & APIs + human approval branch + hold/escalate branch
    # (ordered so the gate's three conditional targets — human, tool_crm, hold — sit 2 columns apart,
    # giving each condition label room to breathe; the tool-registry trio stays visually grouped)
    human = d.node("human", "Retention Manager Approval", "Human-in-the-loop", "leadership")
    tool_bill = d.node("tool_bill", "Billing Adjustment API", "L5 · Tool Registry", "action")
    tool_crm = d.node("tool_crm", "CRM Offer-Dispatch API", "L5 · Tool Registry", "action")
    tool_notify = d.node("tool_notify", "Notification Gateway (SMS/Email/Push)", "L5 · Tool Registry", "action")
    hold = d.node("hold", "Hold & Escalate Queue", "Conditional: policy breach", "obs")
    d.add_row([human, tool_bill, tool_crm, tool_notify, hold], label=("L5", "Execution & Interaction", "Action Layer"))

    # L6 — Nervous System (watchdog, cross-cutting feedback)
    drift = d.node("drift", "Drift & Bias Monitor", "L6 · Nervous System", "obs")
    dq = d.node("dq", "Data Quality Watchdog", "L6 · Nervous System", "obs")
    breaker = d.node("breaker", "Circuit Breaker / Auto-Pause", "L6 · Nervous System", "obs")
    d.add_row([drift, dq, breaker], label=("L6", "End-to-End Observability", "The Nervous System"))

    # L7 — Leadership Portal (scorecard)
    roi = d.node("roi", "Executive ROI Dashboard", "L7 · Leadership Portal", "leadership")
    ethics = d.node("ethics", "Ethics & Fairness Scorecard", "L7 · Leadership Portal", "leadership")
    capital = d.node("capital", "Capital Allocation View", "L7 · Leadership Portal", "leadership")
    d.add_row([roi, ethics, capital], label=("L7", "Leadership Dashboard Layer", "Accountability & Outcomes"))

    # L8 — Self-Healing Loop (the learner)
    outcome = d.node("outcome", "Outcome Tracker", "L8 · Self-Healing Loop", "obs")
    retrain = d.node("retrain", "Model Retraining Trigger", "L8 · Self-Healing Loop", "obs")
    update = d.node("update", "Memory & Policy Updater", "L8 · Self-Healing Loop", "obs")
    d.add_row([outcome, retrain, update], label=("L8", "Feedback & Reinforcement Loops", "Self-Healing"))

    # --- Edges: L1 -> L2 ---
    for n in [ext1, ext2, ext3, int1, int2, int3]:
        d.edge(n.id, "gw")
    d.edge("gw", "llm")
    d.edge("gw", "kg")

    # L2 -> L3 (Agent Plane)
    d.edge("llm", "plan")
    d.edge("kg", "plan")
    d.edge("plan", "exec")
    d.edge("exec", "refl")
    d.edge("refl", "conf")

    # Agent Plane <-> Memory (bidirectional read/write) — each from the adjacent Agent Plane row
    d.edge("plan", "mem_work", bidir=True, dashed=True)
    d.edge("exec", "mem_sem", bidir=True, dashed=True)
    d.edge("refl", "mem_epis", bidir=True, dashed=True)
    d.edge("conf", "mem_pol", bidir=True, dashed=True)

    # L3 -> L4 (Conscience checks before action)
    d.edge("conf", "rule_margin")
    d.edge("conf", "rule_fair")
    d.edge("conf", "rule_reg")

    # L4 -> Conditional Gate
    d.edge("rule_margin", "gate")
    d.edge("rule_fair", "gate")
    d.edge("rule_reg", "gate")

    # Conditional edges out of the gate — the three explicit branches
    d.edge("gate", "tool_crm", label="high confidence")
    d.edge("gate", "human", label="medium confidence")
    d.edge("gate", "hold", dashed=True, label="low confidence")
    d.edge("hold", "breaker")

    # L5 internal
    d.edge("tool_crm", "tool_bill")
    d.edge("tool_crm", "tool_notify")

    # L5 -> L6 (everything is observed, including human override decisions)
    d.edge("tool_crm", "drift", dashed=True)
    d.edge("human", "drift", dashed=True)
    d.edge("tool_notify", "dq", dashed=True)

    # L6 -> L7 (leadership sees the scorecard)
    d.edge("drift", "roi", dashed=True)
    d.edge("dq", "ethics", dashed=True)
    d.edge("breaker", "capital", dashed=True, label="drift/bias alarm → escalate")

    # L6/L7 -> L8 (outcomes feed the learner)
    d.edge("roi", "outcome", dashed=True)
    d.edge("outcome", "retrain")
    d.edge("retrain", "update")

    # L8 closes the loop back into L4 Conscience and L3 Memory (regenerative learning) —
    # unlabeled: these edges span many rows, and a label at the midpoint would land inside an
    # unrelated row; the loop-closing relationship is documented in the accompanying write-up instead
    d.edge("update", "mem_pol", dashed=True)
    d.edge("update", "mem_epis", dashed=True)

    return d.render()


RETENTION_BLUEPRINT_ROWS = [
        {"layer": "L8", "color": "channel", "title": "Self-Healing Loop",
         "desc": "The Learner — reviews results, catches mistakes, and automatically retrains the system to improve over time.",
         "solution": "Outcome Tracker compares predicted vs. actual retention outcomes; Model Retraining Trigger fires on performance-degradation thresholds; Memory & Policy Updater writes new rules back into L3.",
         "tools": "Automated retraining pipeline · performance-threshold monitors · versioned policy store"},
        {"layer": "L7", "color": "leadership", "title": "Leadership Portal",
         "desc": "The Scorecard — links AI actions to dollars, ROI, and ethics for executive oversight.",
         "solution": "Executive ROI Dashboard, Ethics & Fairness Scorecard, and Capital Allocation View give the CFO/CRO/CCO a real-time link between retention spend and saved revenue.",
         "tools": "BI dashboard (Looker/Tableau) wired directly to outcome and financial data"},
        {"layer": "L6", "color": "obs", "title": "Nervous System",
         "desc": "The Watchdog — monitors data health in real time and sounds the alarm on bias or drift.",
         "solution": "Drift & Bias Monitor, Data Quality Watchdog, and a Circuit Breaker that can auto-pause the campaign the moment thresholds are breached.",
         "tools": "Statistical drift/bias detection · automated circuit-breaker service"},
        {"layer": "L5", "color": "action", "title": "Action Layer",
         "desc": "The Hands — turns the digital choice into a real-world task: an email, a CRM update, a human ask.",
         "solution": "Tool Registry (CRM offer-dispatch, billing adjustment, notification gateway APIs), a human approval gate, and a hold/escalate queue for the three conditional routes.",
         "tools": "CRM / billing / notification APIs behind a common tool-calling interface"},
        {"layer": "L4", "color": "orch", "title": "The Conscience",
         "desc": "The Rulebook — keeps the AI within business, ethical, and regulatory guardrails.",
         "solution": "Discount & Margin Policy Engine, Fairness & Non-Discrimination Guardrail, and a Regulatory Constraint Engine gate every decision before it can reach the Action Layer.",
         "tools": "Rules engine · fairness-testing library · regulatory rules engine"},
        {"layer": "L3", "color": "agent", "title": "Thinking Center",
         "desc": "The Logic Engine — where agents reason, remember past context, and talk to each other.",
         "solution": "Agent Plane (Planner, Execution Manager, Reflection Engine, Confidence Scorer) plus the four-part Memory Layer: Working, Episodic, Semantic, and Policy Memory.",
         "tools": "Planner/execution/reflection agent loop · vector DB for episodic & semantic memory · versioned rules store for policy memory"},
        {"layer": "L2", "color": "memory", "title": "The Brain",
         "desc": "The Intelligence — core AI power (LLMs) and specialized knowledge graphs.",
         "solution": "AI Gateway fronting the LLM reasoning core and a churn / customer knowledge graph.",
         "tools": "Claude via a model-routing gateway · graph database (Neo4j)"},
        {"layer": "L1", "color": "data", "title": "The Base",
         "desc": "The Foundation — secure cloud, databases, and the raw data everything else sits on.",
         "solution": "Internal data stores (CRM, billing/CDR, offer catalog) and external data stores (credit bureau, competitor pricing, macroeconomic indicators).",
         "tools": "CRM / billing warehouse · credit bureau API · competitor intelligence feed"},
]

RCA_BLUEPRINT_ROWS = [
        {"layer": "L8", "color": "channel", "title": "Feedback & Reinforcement Loops",
         "desc": "The Learner — reviews results, catches mistakes, and automatically retrains the system to improve over time.",
         "solution": "RCA Accuracy Tracker compares predicted vs. confirmed root cause; Remediation Playbook Retraining Trigger fires on accuracy degradation; Runbook & Policy Memory Updater writes new rules back into L3.",
         "tools": "Automated retraining pipeline · accuracy-threshold monitors · versioned runbook store"},
        {"layer": "L7", "color": "leadership", "title": "Leadership Dashboard Layer",
         "desc": "The Scorecard — links AI actions to dollars, ROI, and ethics for executive oversight.",
         "solution": "MTTR Reduction Dashboard, Network Reliability Scorecard, and Automation Coverage & Cost-Avoidance View give NOC and network leadership a real-time link between automation and reliability outcomes.",
         "tools": "BI dashboard (Looker/Tableau) wired directly to incident and cost-avoidance data"},
        {"layer": "L6", "color": "obs", "title": "End-to-End Observability",
         "desc": "The Watchdog — monitors data health in real time and sounds the alarm on bias or drift.",
         "solution": "Remediation Success/Failure Monitor, Alarm Storm Recurrence Detector, and a Blast-Radius Auditor that flags any remediation whose real-world impact exceeded its predicted scope.",
         "tools": "Streaming anomaly detection · automated blast-radius audit service"},
        {"layer": "L5", "color": "action", "title": "Execution & Interaction",
         "desc": "The Hands — turns the digital choice into a real-world task: an email, a CRM update, a human ask.",
         "solution": "Tool Registry (remediation execution via Ansible/NETCONF, ServiceNow update, NOC/Slack alert), an SRE approval gate, and an on-call escalation queue for the three conditional routes.",
         "tools": "Ansible/NETCONF automation · ServiceNow API · Slack/PagerDuty integration"},
        {"layer": "L4", "color": "orch", "title": "Decisions Engineering & SECI Framework",
         "desc": "The Rulebook — keeps the AI within business, ethical, and regulatory guardrails.",
         "solution": "Blast-Radius Risk Policy Engine, Change-Management Compliance Engine, and an SRE Runbook Rule Engine gate every remediation before it can reach the Action Layer.",
         "tools": "Rules engine · change-management (CAB) policy integration · SRE runbook codification"},
        {"layer": "L3", "color": "agent", "title": "Agentic Core",
         "desc": "The Logic Engine — where agents reason, remember past context, and talk to each other.",
         "solution": "NOC Incident Orchestrator fanning out to five specialist agents (RAN, Transport, Core, KPI, Historical Ticket) plus the four-part Memory Layer: Working, Episodic, Semantic, and Policy Memory.",
         "tools": "Orchestrator-worker agent graph · vector DB for episodic & semantic memory · versioned rules store for policy memory"},
        {"layer": "L2", "color": "memory", "title": "Agent Intelligence & Models",
         "desc": "The Intelligence — core AI power (LLMs) and specialized knowledge graphs.",
         "solution": "AI Gateway fronting the LLM reasoning core and a network topology knowledge graph.",
         "tools": "Claude via a model-routing gateway · graph database (Neo4j)"},
        {"layer": "L1", "color": "data", "title": "Foundational Data & Infrastructure",
         "desc": "The Foundation — secure cloud, databases, and the raw data everything else sits on.",
         "solution": "Internal data stores (network topology, streaming telemetry, past incident tickets) and an external data store (vendor EMS advisory feed).",
         "tools": "Netbox inventory · Kafka/gNMI telemetry pipeline · ServiceNow · vendor EMS API"},
]

def blueprint_table(rows=None):
    """
    Two-column-style blueprint table: left side is the reference model (layer badge, title, manuscript
    description); right side is split into this use case's architecture/solution for that layer and the
    tools/technologies used. Ordered L8 -> L1 to match the manuscript's own table presentation (top of the
    stack first). This is a plain table renderer, not the node/edge Diagram engine — rows stack vertically
    with three text columns of independently-wrapped, variable-height content.
    """
    import textwrap as _tw
    COL1_W, COL2_W, COL3_W = 400, 520, 420
    PAD = 16
    LINE_H = 17
    TITLE_LINE_H = 21
    HEADER_H = 50
    CANVAS_W = COL1_W + COL2_W + COL3_W

    rows = rows if rows is not None else RETENTION_BLUEPRINT_ROWS

    def wrap(text, width):
        return _tw.wrap(text, width=width, break_long_words=False)

    processed = []
    for r in rows:
        title_lines = wrap(r["title"], 22)
        desc_lines = wrap(r["desc"], 38)
        sol_lines = wrap(r["solution"], 60)
        tools_lines = wrap(r["tools"], 44)
        col1_h = len(title_lines) * TITLE_LINE_H + 6 + len(desc_lines) * LINE_H
        col2_h = len(sol_lines) * LINE_H
        col3_h = len(tools_lines) * LINE_H
        row_h = max(col1_h, col2_h, col3_h, 70) + 2 * PAD
        processed.append((r, title_lines, desc_lines, sol_lines, tools_lines, row_h))

    canvas_h = HEADER_H + sum(p[-1] for p in processed) + 2

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {canvas_h:.0f}" '
        f'font-family="\'Inter\',\'IBM Plex Sans\',-apple-system,sans-serif">',
        f'<rect width="{CANVAS_W}" height="{canvas_h:.0f}" fill="#FFFFFF"/>',
        f'<rect x="0" y="0" width="{CANVAS_W}" height="{HEADER_H}" fill="#F4F5F7"/>',
    ]
    headers = [
        ("Reference Blueprint (Manuscript Model)", COL1_W / 2),
        ("Use Case Blueprint — Architecture & Solution", COL1_W + COL2_W / 2),
        ("Tools & Technologies", COL1_W + COL2_W + COL3_W / 2),
    ]
    for label, cx in headers:
        svg.append(
            f'<text x="{cx:.1f}" y="{HEADER_H/2+5:.1f}" text-anchor="middle" font-size="13" '
            f'font-weight="700" fill="#333B4A">{esc(label)}</text>'
        )
    svg.append(f'<line x1="0" y1="{HEADER_H}" x2="{CANVAS_W}" y2="{HEADER_H}" stroke="#D8DCE2" stroke-width="1.5"/>')
    svg.append(f'<line x1="{COL1_W}" y1="0" x2="{COL1_W}" y2="{canvas_h:.0f}" stroke="#E2E5EA" stroke-width="1"/>')
    svg.append(f'<line x1="{COL1_W+COL2_W}" y1="0" x2="{COL1_W+COL2_W}" y2="{canvas_h:.0f}" stroke="#E2E5EA" stroke-width="1"/>')

    y = HEADER_H
    for i, (r, title_lines, desc_lines, sol_lines, tools_lines, row_h) in enumerate(processed):
        c = COLORS[r["color"]]
        row_bg = "#FBFBFA" if i % 2 else "#FFFFFF"
        svg.append(f'<rect x="0" y="{y:.1f}" width="{CANVAS_W}" height="{row_h:.1f}" fill="{row_bg}"/>')
        svg.append(f'<rect x="0" y="{y:.1f}" width="5" height="{row_h:.1f}" fill="{c["stroke"]}"/>')

        badge_cx, badge_cy = 38, y + 30
        svg.append(f'<circle cx="{badge_cx}" cy="{badge_cy:.1f}" r="18" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.5"/>')
        svg.append(
            f'<text x="{badge_cx}" y="{badge_cy+5:.1f}" text-anchor="middle" font-size="13.5" '
            f'font-weight="700" fill="{c["title"]}">{r["layer"]}</text>'
        )

        tx, ty = badge_cx + 30, y + 26
        for line in title_lines:
            svg.append(
                f'<text x="{tx}" y="{ty:.1f}" font-size="14.5" font-weight="700" fill="{c["title"]}">{esc(line)}</text>'
            )
            ty += TITLE_LINE_H
        dy = ty + 5
        for line in desc_lines:
            svg.append(f'<text x="20" y="{dy:.1f}" font-size="11.5" fill="#6B7280">{esc(line)}</text>')
            dy += LINE_H

        sx, sy = COL1_W + 18, y + PAD + 12
        for line in sol_lines:
            svg.append(f'<text x="{sx}" y="{sy:.1f}" font-size="12" fill="#374151">{esc(line)}</text>')
            sy += LINE_H

        tx3, ty3 = COL1_W + COL2_W + 18, y + PAD + 12
        for line in tools_lines:
            svg.append(
                f'<text x="{tx3}" y="{ty3:.1f}" font-size="11.5" font-family="\'IBM Plex Mono\',monospace" '
                f'fill="#3E6D93">{esc(line)}</text>'
            )
            ty3 += LINE_H

        y += row_h
        svg.append(f'<line x1="0" y1="{y:.1f}" x2="{CANVAS_W}" y2="{y:.1f}" stroke="#EDEEF1" stroke-width="1"/>')

    svg.append("</svg>")
    return "\n".join(svg)


def rca_deep8_architecture():
    """
    Deep 8-Layer pilot #2: Multi-Agent Network Fault RCA & Auto-Remediation (Telecom Use Case 01),
    mapped through the same L1-L8 manuscript model as the retention example, but built around this
    use case's actual orchestrator-worker fan-out rather than a linear plan-execute-reflect chain —
    showing the 8-layer model flexibly accommodates different internal orchestration patterns.
    """
    d = Diagram()

    # L1 — Foundational Data & Infrastructure
    ext1 = d.node("ext1", "Vendor EMS Advisory Feed", "External Data Store", "data", external=True)
    int1 = d.node("int1", "Network Topology DB (Netbox)", "Internal Data Store", "data")
    int2 = d.node("int2", "Streaming Telemetry (Kafka/gNMI)", "Internal Data Store", "data")
    int3 = d.node("int3", "Past Incident Tickets (ServiceNow)", "Internal Data Store", "data")
    d.add_row([ext1, int1, int2, int3], label=("L1", "Foundational Data & Infrastructure", None))

    # L2 — Agent Intelligence & Models
    gw = d.node("gw", "AI Gateway", "L2 · The Brain", "orch")
    llm = d.node("llm", "LLM Reasoning Core (Claude)", "L2 · The Brain", "agent")
    kg = d.node("kg", "Topology Knowledge Graph", "L2 · The Brain", "agent")
    d.add_row([gw, llm, kg], label=("L2", "Agent Intelligence & Models", None))

    # L3 — Agentic Core: orchestrator alone, then workers, then memory (unlabeled, adjacent)
    orch = d.node("orch", "NOC Incident Orchestrator", "L3 · Orchestration", "orch")
    d.add_row([orch], label=("L3", "Agentic Core", "Orchestration & Reasoning"))

    ran = d.node("ran", "RAN Alarm Correlation Agent", "L3 · Specialist", "agent")
    transport = d.node("transport", "Transport/IP Topology Agent", "L3 · Specialist", "agent")
    core = d.node("core", "Core Network Agent", "L3 · Specialist", "agent")
    kpi = d.node("kpi", "Performance-KPI Deviation Agent", "L3 · Specialist", "agent")
    hist = d.node("hist", "Historical Ticket Similarity Agent", "L3 · Specialist", "agent")
    d.add_row([ran, transport, core, kpi, hist])

    mem_work = d.node("mem_work", "Working Memory", "Short-Term · current incident", "memory")
    mem_epis = d.node("mem_epis", "Episodic Memory", "Long-Term · past RCA outcomes", "memory")
    mem_sem = d.node("mem_sem", "Semantic Memory", "Long-Term · topology & vendor knowledge", "memory")
    mem_pol = d.node("mem_pol", "Policy Memory", "Long-Term · blast-radius rules", "memory")
    d.add_row([mem_work, mem_epis, mem_sem, mem_pol])

    # L4 — Decisions Engineering & SECI Framework
    blast = d.node("blast", "Blast-Radius Risk Policy Engine", "L4 · Governance", "orch")
    change = d.node("change", "Change-Management Compliance Engine", "L4 · Governance", "orch")
    runbook = d.node("runbook", "SRE Runbook Rule Engine", "L4 · Governance", "orch")
    d.add_row([blast, change, runbook], label=("L4", "Decisions Engineering & SECI Framework", "Governance & Logic"))

    # Conditional decision gate
    gate = d.node("gate", "RCA Confidence & Blast-Radius Gate", "Conditional routing", "orch")
    d.add_row([gate])

    # L5 — Execution & Interaction
    sre = d.node("sre", "SRE Approval Gate", "Human-in-the-loop", "leadership")
    svcnow = d.node("svcnow", "ServiceNow Incident Update", "L5 · Tool Registry", "action")
    remediate = d.node("remediate", "Remediation Execution Agent", "L5 · Tool Registry", "action")
    noc = d.node("noc", "NOC Dashboard / Slack Alert", "L5 · Tool Registry", "action")
    escalate = d.node("escalate", "On-Call Escalation Queue", "Conditional: low confidence", "obs")
    d.add_row([sre, svcnow, remediate, noc, escalate], label=("L5", "Execution & Interaction", "Action Layer"))

    # L6 — End-to-End Observability
    success = d.node("success", "Remediation Success/Failure Monitor", "L6 · Nervous System", "obs")
    storm = d.node("storm", "Alarm Storm Recurrence Detector", "L6 · Nervous System", "obs")
    audit = d.node("audit", "Blast-Radius Auditor", "L6 · Nervous System", "obs")
    d.add_row([success, storm, audit], label=("L6", "End-to-End Observability", "The Nervous System"))

    # L7 — Leadership Dashboard Layer
    mttr = d.node("mttr", "MTTR Reduction Dashboard", "L7 · Leadership Portal", "leadership")
    reliability = d.node("reliability", "Network Reliability Scorecard", "L7 · Leadership Portal", "leadership")
    coverage = d.node("coverage", "Automation Coverage & Cost-Avoidance View", "L7 · Leadership Portal", "leadership")
    d.add_row([mttr, reliability, coverage], label=("L7", "Leadership Dashboard Layer", "Accountability & Outcomes"))

    # L8 — Feedback & Reinforcement Loops
    accuracy = d.node("accuracy", "RCA Accuracy Tracker", "L8 · Self-Healing", "obs")
    retrain = d.node("retrain", "Remediation Playbook Retraining Trigger", "L8 · Self-Healing", "obs")
    update = d.node("update", "Runbook & Policy Memory Updater", "L8 · Self-Healing", "obs")
    d.add_row([accuracy, retrain, update], label=("L8", "Feedback & Reinforcement Loops", "Self-Healing"))

    # --- Edges ---
    for n in [ext1, int1, int2, int3]:
        d.edge(n.id, "gw")
    d.edge("gw", "llm")
    d.edge("gw", "kg")
    d.edge("llm", "orch")
    d.edge("kg", "orch")

    for n in [ran, transport, core, kpi, hist]:
        d.edge("orch", n.id)

    d.edge("orch", "mem_work", bidir=True, dashed=True)
    d.edge("hist", "mem_epis", bidir=True, dashed=True)
    d.edge("transport", "mem_sem", bidir=True, dashed=True)
    d.edge("blast", "mem_pol", bidir=True, dashed=True)

    d.edge("ran", "blast")
    d.edge("transport", "blast")
    d.edge("core", "change")
    d.edge("kpi", "change")
    d.edge("hist", "runbook")

    d.edge("blast", "gate")
    d.edge("change", "gate")
    d.edge("runbook", "gate")

    d.edge("gate", "remediate", label="high confidence")
    d.edge("gate", "sre", label="medium confidence")
    d.edge("gate", "escalate", dashed=True, label="low confidence")
    d.edge("escalate", "audit")

    d.edge("remediate", "svcnow")
    d.edge("remediate", "noc")

    d.edge("remediate", "success", dashed=True)
    d.edge("sre", "success", dashed=True)
    d.edge("noc", "storm", dashed=True)

    d.edge("success", "mttr", dashed=True)
    d.edge("storm", "reliability", dashed=True)
    d.edge("audit", "coverage", dashed=True, label="blast-radius alarm → escalate")

    d.edge("mttr", "accuracy", dashed=True)
    d.edge("accuracy", "retrain")
    d.edge("retrain", "update")

    d.edge("update", "mem_pol", dashed=True)
    d.edge("update", "mem_epis", dashed=True)

    return d.render()


BUILDERS = {
    "orchestrator-worker": orchestrator_worker,
    "hierarchical": hierarchical,
    "pipeline": pipeline,
    "blackboard": blackboard,
    "debate-critique": debate_critique,
    "market-based": market_based,
    "event-swarm": event_swarm,
    "human-escalation": human_escalation,
}
