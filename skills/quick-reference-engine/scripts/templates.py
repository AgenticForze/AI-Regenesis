# -*- coding: utf-8 -*-
"""
Mermaid diagram templates for the 8 multi-agent architecture patterns used across this catalog.

Every diagram is organized as an explicit LAYERED ARCHITECTURE so the same visual language applies
whether you're looking at a fraud-detection swarm or a loan-underwriting hierarchy:

    L1  Data & Integration Layer   — source systems, feeds, external data the agents read
    L2  Orchestration Layer        — the coordinating "brain" (supervisor/controller/arbiter/auctioneer/
                                      escalation gate) that decides what happens next
    L3  Agent Layer                — the specialist/worker/domain agents that do the actual reasoning
    L4  Action & Execution Layer   — the systems of record that get written to / actions taken
    OBS Observability & Governance — cross-cutting: tracing/telemetry, immutable audit log, guardrail/
                                      policy enforcement, and (where the use case has one) the human
                                      review checkpoint — connected to every functional layer

Each pattern function below builds these subgraphs, wires the pattern-specific control flow between
them, and applies a shared classDef color legend so every generated diagram reads the same way.
"""

def _san(s):
    return s.replace('"', "'")

STYLE_BLOCK = """  classDef dataLayer fill:#0F2A28,stroke:#2FD3C7,stroke-width:1px,color:#E7ECF3;
  classDef orchLayer fill:#241B3D,stroke:#8C7CFF,stroke-width:1.5px,color:#E7ECF3;
  classDef agentLayer fill:#141A28,stroke:#4C8DFF,stroke-width:1px,color:#E7ECF3;
  classDef actionLayer fill:#3D2A1B,stroke:#E8B23C,stroke-width:1px,color:#E7ECF3;
  classDef obsLayer fill:#3D1B24,stroke:#FF7A66,stroke-width:1px,color:#E7ECF3;
  classDef obsNode fill:#2A1319,stroke:#FF7A66,stroke-width:1px,color:#E7ECF3,stroke-dasharray: 2 2;
  class L1 dataLayer;
  class L2 orchLayer;
  class L3 agentLayer;
  class L4 actionLayer;
  class OBS obsLayer;"""

STYLE_BLOCK_NO_L2 = STYLE_BLOCK.replace("  class L2 orchLayer;\n", "")

def _obs_block(human_gate_label=None):
    """Cross-cutting Observability & Governance layer, present in every diagram."""
    lines = ['  subgraph OBS["📊 Observability &amp; Governance Layer (cross-cutting)"]']
    lines.append('    TRACE["Tracing &amp; Telemetry<br/>(OpenTelemetry)"]:::obsNode')
    lines.append('    AUDIT["Immutable Audit Log"]:::obsNode')
    lines.append('    GUARD["Guardrails / Policy Engine"]:::obsNode')
    if human_gate_label:
        lines.append(f'    HUMAN{{"{_san(human_gate_label)}"}}:::obsNode')
    lines.append('  end')
    return lines

def _obs_wiring(has_l2=True, has_l3=True, has_l4=True):
    """Dotted 'emits telemetry to' edges from each functional layer into Observability — one edge per
    layer (not per node) to keep the diagram scannable at 40-node scale."""
    lines = []
    if has_l2: lines.append('  L2 -.telemetry.-> OBS')
    if has_l3: lines.append('  L3 -.telemetry.-> OBS')
    if has_l4: lines.append('  L4 -.audit.-> OBS')
    return lines


def orchestrator_worker(title, orchestrator, workers, data_sources, actions, human_gate=None):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Data &amp; Integration Layer"]')
    for i, d in enumerate(data_sources):
        L.append(f'    D{i}["{_san(d)}"]')
    L.append("  end")
    L.append('  subgraph L2["🧭 Orchestration Layer"]')
    L.append(f'    ORCH{{"{_san(orchestrator)}"}}')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (parallel specialists)"]')
    for i, w in enumerate(workers):
        L.append(f'    W{i}["{_san(w)}"]')
    L.append('    AGG["Aggregator / Synthesis Agent"]')
    for i in range(len(workers)):
        L.append(f"    W{i} --> AGG")
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    L.append("    ACT[/Action Agent/]")
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
        L.append(f"    ACT --> SYS{i}")
    L.append("  end")
    L.append("  L1 --> L2")
    for i in range(len(workers)):
        L.append(f"  ORCH --> W{i}")
    if human_gate:
        L.append("  AGG --> HUMAN")
        L.append("  HUMAN --> ACT")
    else:
        L.append("  AGG --> ACT")
    L.extend(_obs_block(human_gate))
    L.extend(_obs_wiring())
    L.append(STYLE_BLOCK)
    return "\n".join(L)


def hierarchical(title, top, mid_layer, leaves_by_mid, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Intent / Request Layer"]')
    L.append('    REQ(["Incoming Request / Intent"])')
    L.append("  end")
    L.append('  subgraph L2["🧭 Orchestration Layer"]')
    L.append(f'    TOP{{"{_san(top)}"}}')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (manager-of-managers)"]')
    for i, m in enumerate(mid_layer):
        L.append(f'    subgraph L3_{i}["{_san(m)}"]')
        L.append(f'      M{i}(("{_san(m)}<br/>Domain Manager"))')
        for j, leaf in enumerate(leaves_by_mid[i]):
            L.append(f'      L{i}_{j}["{_san(leaf)}"]')
            L.append(f"      M{i} --> L{i}_{j}")
        L.append("    end")
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    L.append('    RES["Resolution / Reporting Agent"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
        L.append(f"    RES --> SYS{i}")
    L.append("  end")
    L.append("  L1 --> L2")
    L.append("  REQ --> TOP")
    for i in range(len(mid_layer)):
        L.append(f"  TOP --> M{i}")
    L.append("  L3 --> L4")
    L.append("  TOP --> RES")
    L.extend(_obs_block())
    L.extend(_obs_wiring())
    L.append(STYLE_BLOCK)
    return "\n".join(L)


def pipeline(title, stages, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Input Layer"]')
    L.append('    IN(["Trigger / Incoming Record"])')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Pipeline Layer (sequential)"]')
    for i, s in enumerate(stages):
        L.append(f'    S{i}["{_san(s)}"]')
    for i in range(len(stages) - 1):
        L.append(f"    S{i} --> S{i+1}")
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
    L.append("  end")
    L.append("  IN --> L3")
    for i in range(len(actions)):
        L.append(f'  S{len(stages)-1} --> SYS{i}')
    L.extend(_obs_block())
    L.append('  L3 -.telemetry (per-stage span).-> OBS')
    L.append('  L4 -.audit.-> OBS')
    L.append(STYLE_BLOCK_NO_L2)
    return "\n".join(L)


def blackboard(title, controller, agents, store_name, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Data Layer"]')
    L.append(f'    BB[("{_san(store_name)}")]')
    L.append("  end")
    L.append('  subgraph L2["🧭 Orchestration Layer"]')
    L.append(f'    CTRL{{"{_san(controller)}"}}')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (read/write blackboard)"]')
    for i, a in enumerate(agents):
        L.append(f'    A{i}["{_san(a)}"]')
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
    L.append("  end")
    L.append("  L1 <--> L2")
    for i in range(len(agents)):
        L.append(f"  A{i} <--> BB")
        L.append(f"  CTRL -.trigger.-> A{i}")
    for i in range(len(actions)):
        L.append(f'  CTRL --> SYS{i}')
    L.extend(_obs_block())
    L.extend(_obs_wiring())
    L.append(STYLE_BLOCK)
    return "\n".join(L)


def debate_critique(title, proposer, critic, arbiter, refs, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Data &amp; Integration Layer"]')
    for i, r in enumerate(refs):
        L.append(f'    R{i}[("{_san(r)}")]')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (proposer ⇄ critic)"]')
    L.append(f'    P["{_san(proposer)}"]')
    L.append(f'    C["{_san(critic)}"]')
    L.append("    P --> C")
    L.append("    C -- revise --> P")
    L.append("  end")
    L.append('  subgraph L2["🧭 Orchestration / Decision Layer"]')
    L.append(f'    ARB{{"{_san(arbiter)}"}}')
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
    L.append("  end")
    L.append("  L1 --> L3")
    for i in range(len(refs)):
        L.append(f"  R{i} --> P")
    L.append("  C --> ARB")
    L.append("  ARB -- reject/loop --> P")
    for i in range(len(actions)):
        L.append(f'  ARB -- approve --> SYS{i}')
    L.extend(_obs_block())
    L.extend(_obs_wiring())
    L.append(STYLE_BLOCK)
    return "\n".join(L)


def market_based(title, auctioneer, bidders, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Data &amp; Integration Layer"]')
    L.append('    CTX(["Live Market / Resource State"])')
    L.append("  end")
    L.append('  subgraph L2["🧭 Orchestration Layer"]')
    L.append(f'    AUC{{"{_san(auctioneer)}"}}')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (bidders)"]')
    for i, b in enumerate(bidders):
        L.append(f'    B{i}["{_san(b)}"]')
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
    L.append("  end")
    L.append("  L1 --> L2")
    L.append("  CTX --> AUC")
    for i in range(len(bidders)):
        L.append(f"  B{i} -- bid --> AUC")
        L.append(f"  AUC -- clear price --> B{i}")
    for i in range(len(actions)):
        L.append(f'  AUC --> SYS{i}')
    L.extend(_obs_block())
    L.extend(_obs_wiring())
    L.append(STYLE_BLOCK)
    return "\n".join(L)


def event_swarm(title, bus_name, agents, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Data &amp; Integration Layer"]')
    L.append(f'    BUS{{"{_san(bus_name)}"}}')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (reactive, decentralized)"]')
    for i, a in enumerate(agents):
        L.append(f'    A{i}["{_san(a)}"]')
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
    L.append("  end")
    L.append("  L1 --> L3")
    for i in range(len(agents)):
        L.append(f"  BUS -- event --> A{i}")
        L.append(f"  A{i} -- publish --> BUS")
    for i in range(len(actions)):
        L.append(f'  BUS --> SYS{i}')
    L.extend(_obs_block())
    L.append('  L3 -.telemetry.-> OBS')
    L.append('  L4 -.audit.-> OBS')
    L.append(STYLE_BLOCK_NO_L2)
    return "\n".join(L)


def human_escalation(title, auto_agents, escalation_gate, human_role, actions):
    L = ["flowchart TB"]
    L.append('  subgraph L1["🔗 Input Layer"]')
    L.append('    IN(["Incoming Case / Event"])')
    L.append("  end")
    L.append('  subgraph L3["🤖 Agent Layer (automation chain)"]')
    for i, a in enumerate(auto_agents):
        L.append(f'    A{i}["{_san(a)}"]')
        if i > 0:
            L.append(f"    A{i-1} --> A{i}")
    L.append("  end")
    L.append('  subgraph L2["🧭 Orchestration / Escalation Gate Layer"]')
    L.append(f'    GATE{{"{_san(escalation_gate)}"}}')
    L.append("  end")
    L.append('  subgraph L4["⚙️ Action &amp; Execution Layer"]')
    L.append('    AUTO["Auto-resolve Agent"]')
    for i, a in enumerate(actions):
        L.append(f'    SYS{i}[("{_san(a)}")]')
        L.append(f"    AUTO --> SYS{i}")
    L.append("  end")
    L.append("  IN --> L3")
    L.append(f"  A{len(auto_agents)-1} --> GATE")
    L.append("  GATE -- low risk / high confidence --> AUTO")
    L.extend(_obs_block(human_role))
    L.append("  GATE -- high risk / low confidence --> HUMAN")
    L.append("  HUMAN -- decision --> AUTO")
    L.append('  L3 -.telemetry.-> OBS')
    L.append('  L4 -.audit.-> OBS')
    L.append(STYLE_BLOCK)
    return "\n".join(L)


PATTERNS = {
    "orchestrator-worker": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
    "hierarchical": "Hierarchical Multi-Agent (Manager-of-Managers)",
    "pipeline": "Sequential Pipeline",
    "blackboard": "Blackboard / Shared-Memory",
    "debate-critique": "Debate-Critique-Arbiter (Reflective Loop)",
    "market-based": "Market-Based / Auction Agents",
    "event-swarm": "Event-Driven Reactive Swarm",
    "human-escalation": "Human-in-the-Loop Escalation Chain",
}
