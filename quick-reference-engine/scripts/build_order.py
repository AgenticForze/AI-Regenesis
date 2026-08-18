# -*- coding: utf-8 -*-
"""
Generates a "Suggested Build Order" section for every Quick Reference use case, tailored per
architecture pattern using that use case's own agent/component names (not generic boilerplate).
Four phases per use case: get one path working end-to-end, add the pattern's defining mechanism,
add governance/human oversight, add observability and feedback.
"""

def _orchestrator_worker(uc):
    orch = uc["orchestrator"]
    workers = uc["workers"]
    gate = uc.get("human_gate")
    return [
        f"**Phase 1 — one worker, no fan-out.** Wire a single path end to end: {workers[0]} reading "
        f"real data and producing a result, with {orch} just passing data through untouched. Prove the "
        f"data pipeline and one agent's reasoning before adding parallelism.",
        f"**Phase 2 — add the fan-out.** Bring the remaining {len(workers)-1} worker agent"
        f"{'s' if len(workers)>2 else ''} online in parallel and build {orch}'s aggregation/synthesis "
        f"logic. This is where the orchestrator-worker pattern is actually learned — watch for race "
        f"conditions and partial-failure handling here, not before.",
        (f"**Phase 3 — add the governance gate.** Wire in the human checkpoint: {gate}."
         if gate else
         "**Phase 3 — add the governance gate.** Add policy/guardrail checks the aggregator's output "
         "must clear before it reaches the action layer."),
        "**Phase 4 — observability and feedback.** Trace every worker call, monitor the aggregator's "
        "decision quality against real outcomes, and add a feedback loop that catches drift before it "
        "becomes a production incident.",
    ]

def _hierarchical(uc):
    top = uc["top"]
    mid = uc["mid_layer"]
    return [
        f"**Phase 1 — one branch only.** Build {top} talking to just {mid[0]} and that manager's own "
        f"leaf agents, ignoring the other {len(mid)-1} branch{'es' if len(mid)>2 else ''} entirely. Prove "
        f"one full manager-to-leaf chain before replicating it.",
        f"**Phase 2 — add the remaining branches.** Bring {', '.join(mid[1:])} online, each with their "
        f"own leaf agents. Build {top}'s cross-branch consolidation logic — this is the actual hard part "
        f"of the hierarchical pattern, not any single branch.",
        f"**Phase 3 — resolve cross-branch conflicts.** Real inputs will disagree across managers "
        f"(different branches recommending incompatible actions); add explicit conflict-resolution logic "
        f"at {top} rather than letting the last branch to report silently win.",
        "**Phase 4 — observability and feedback.** Trace decisions at every level of the hierarchy "
        "separately (top orchestrator, each manager, each leaf) so a bad outcome can be traced to the "
        "specific branch and level that caused it.",
    ]

def _pipeline(uc):
    stages = uc["stages"]
    return [
        f"**Phase 1 — the first two stages only.** Get {stages[0]} feeding {stages[1]} correctly, with "
        f"the rest of the pipeline stubbed out. Durability matters more than completeness here — make "
        f"sure a crash mid-pipeline doesn't lose or duplicate work.",
        f"**Phase 2 — the full chain.** Add the remaining {len(stages)-2} stage"
        f"{'s' if len(stages)-2!=1 else ''} in order, testing each newly-added stage against real output "
        f"from the stage before it, not synthetic test data.",
        "**Phase 3 — add retry and partial-failure handling.** Decide, stage by stage, what happens when "
        "that specific stage fails: retry, skip, or halt the whole pipeline. This decision is different "
        "per stage and shouldn't be a single global policy.",
        "**Phase 4 — observability and feedback.** Add per-stage tracing so a slow or wrong pipeline run "
        "can be attributed to one specific stage, and track output quality over time to catch silent "
        "degradation in an early stage before it compounds downstream.",
    ]

def _blackboard(uc):
    ctrl = uc["controller"]
    agents = uc["agents"]
    return [
        f"**Phase 1 — one agent writing to the blackboard.** Get {agents[0]} reading and writing the "
        f"shared store with {ctrl} just reading it back out, no synthesis logic yet. Prove the shared-state "
        f"read/write mechanics before adding more writers.",
        f"**Phase 2 — add the remaining agents.** Bring {', '.join(agents[1:])} online, each writing "
        f"independently to the blackboard. Build {ctrl}'s synthesis logic — deciding which agent to "
        f"trigger next and how to combine partial, sometimes-conflicting findings.",
        "**Phase 3 — add a minimum-evidence threshold.** An early blackboard system will over-synthesize "
        "from sparse data; require a minimum number of corroborating agent findings before the controller "
        "surfaces a conclusion.",
        "**Phase 4 — observability and feedback.** Snapshot the blackboard's state history so any "
        "synthesized conclusion can be traced back to exactly which agent findings produced it.",
    ]

def _debate_critique(uc):
    proposer = uc["proposer"]
    critic = uc["critic"]
    arbiter = uc["arbiter"]
    return [
        f"**Phase 1 — the proposer alone.** Get {proposer} producing a hypothesis from real data, with "
        f"no critic yet — this is just a single-pass classifier/recommender at this stage, and that's fine.",
        f"**Phase 2 — add the critic, fully independent.** Build {critic} with no visibility into the "
        f"proposer's reasoning — separate context, separate prompt. This independence is the entire point "
        f"of the pattern; skipping it turns the critic into a rubber stamp.",
        f"**Phase 3 — add {arbiter} and calibrate.** Build the arbitration logic, then run it against a "
        f"set of cases with known-correct outcomes to calibrate how much weight the critic's pushback "
        f"should carry before trusting it on live decisions.",
        "**Phase 4 — observability and feedback.** Track how often the arbiter overrides the proposer "
        "and whether those overrides were actually correct — this tells you whether the critic is earning "
        "its place in the pipeline or just adding latency.",
    ]

def _market_based(uc):
    auc = uc["auctioneer"]
    bidders = uc["bidders"]
    return [
        f"**Phase 1 — two bidders, manual clearing.** Get {bidders[0]} and {bidders[1] if len(bidders)>1 else bidders[0]} "
        f"submitting bids with {auc} clearing them on a fixed schedule — no real-time re-clearing yet.",
        f"**Phase 2 — add the remaining bidders and automate clearing.** Bring the rest of the bidder "
        f"population online and move {auc} to event-triggered (not just scheduled) clearing.",
        "**Phase 3 — add hard guardrails independent of the market mechanism.** A pure auction can clear "
        "at a technically-valid but operationally-bad price; add a guardrail service that can veto a "
        "clearing result regardless of what the market mechanism decided.",
        "**Phase 4 — observability and feedback.** Track clearing-price trends and bidder participation "
        "over time — a market that's stopped clearing efficiently is a slow-motion failure that won't "
        "show up in any single transaction.",
    ]

def _event_swarm(uc):
    bus = uc["bus_name"]
    agents = uc["agents"]
    return [
        f"**Phase 1 — one reactive agent.** Get {agents[0]} subscribed to {bus} and reacting to real "
        f"events, with no other agents listening yet. Prove the event-driven mechanics work under real "
        f"event volume before adding more subscribers.",
        f"**Phase 2 — add the remaining agents.** Bring {', '.join(agents[1:])} online as independent "
        f"subscribers. Test what happens when multiple agents react to the *same* event — this is where "
        f"swarm-specific bugs (duplicate actions, conflicting responses) show up.",
        "**Phase 3 — add rate limits and blast-radius guardrails.** A reactive swarm with no shared "
        "coordination can act on the same trigger repeatedly; add per-agent and global rate limits before "
        "connecting real downstream actions.",
        "**Phase 4 — observability and feedback.** Add distributed tracing across the event bus so a "
        "cascading reaction across multiple agents can be reconstructed after the fact, not just guessed at.",
    ]

def _human_escalation(uc):
    auto_agents = uc["auto_agents"]
    gate = uc["escalation_gate"]
    human = uc["human_role"]
    return [
        f"**Phase 1 — the automation chain, no gate yet.** Get {' → '.join(auto_agents)} working end to "
        f"end against real data, routing every single case to {human} for now — automation logic before "
        f"automation trust.",
        f"**Phase 2 — add {gate} in shadow mode.** Let the gate score every case and log what it *would* "
        f"route, but keep sending everything to {human} regardless. Compare the gate's decisions against "
        f"what the human actually did.",
        f"**Phase 3 — turn on auto-resolve for the highest-confidence tier only.** Once shadow-mode data "
        f"shows the gate agrees with {human} at very high confidence, let only that top tier bypass the "
        f"human — keep everything else routed to review.",
        "**Phase 4 — observability and feedback.** Track the auto-resolve tier's real-world accuracy "
        "continuously, not just at launch, and be willing to narrow the auto-resolve criteria back down "
        "if accuracy drifts.",
    ]

BUILDERS = {
    "orchestrator-worker": _orchestrator_worker,
    "hierarchical": _hierarchical,
    "pipeline": _pipeline,
    "blackboard": _blackboard,
    "debate-critique": _debate_critique,
    "market-based": _market_based,
    "event-swarm": _event_swarm,
    "human-escalation": _human_escalation,
}

def build_order_for(uc):
    return BUILDERS[uc["pattern"]](uc)
