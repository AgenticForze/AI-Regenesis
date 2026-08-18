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
