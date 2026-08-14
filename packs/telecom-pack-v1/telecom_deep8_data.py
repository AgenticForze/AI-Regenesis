# -*- coding: utf-8 -*-
"""
Deep 8-Layer specs for the 18 remaining Telecommunications use cases (UC 1 and UC 5 are the two
hand-built pilots in deep8_data.py). Same spec-driven approach as bssoss_deep8_data.py and
finance_deep8_data.py — see scripts/deep8_engine.py for the engine these specs feed.
"""

def _ext(id_, title): return {"id": id_, "title": title, "sub": "External Data Store", "external": True}
def _int(id_, title): return {"id": id_, "title": title, "sub": "Internal Data Store"}
def _l2(id_, title, prod=None):
    d = {"id": id_, "title": title, "sub": "L2 · The Brain"}
    if prod: d["prod"] = prod
    return d
def _orch(id_, title): return {"id": id_, "title": title, "sub": "L3 · Orchestration"}
def _w(id_, title): return {"id": id_, "title": title, "sub": "L3 · Specialist"}
def _l4(id_, title): return {"id": id_, "title": title, "sub": "L4 · Governance"}
def _gate(id_, title): return {"id": id_, "title": title, "sub": "Conditional routing"}
def _l5_human(id_, title): return {"id": id_, "title": title, "sub": "Human-in-the-loop", "color": "leadership", "gate_branch": "human"}
def _l5_auto(id_, title): return {"id": id_, "title": title, "sub": "L5 · Tool Registry", "gate_branch": "auto"}
def _l5_plain(id_, title): return {"id": id_, "title": title, "sub": "L5 · Tool Registry"}
def _l5_hold(id_, title): return {"id": id_, "title": title, "sub": "Conditional: policy breach", "color": "obs", "gate_branch": "hold"}
def _l6(id_, title): return {"id": id_, "title": title, "sub": "L6 · Nervous System"}
def _l7(id_, title): return {"id": id_, "title": title, "sub": "L7 · Leadership Portal"}
def _l8(id_, title): return {"id": id_, "title": title, "sub": "L8 · Self-Healing"}


TELECOM_SPECS = [

{
 "id": 2, "quick_slug": "5g-network-slicing-orchestration",
 "quick_title": "5G Network Slice Lifecycle Orchestration",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "5G Network Slice Design & Assurance Decisioning",
 "intro": ("This deep-8 view makes cross-domain conflict resolution an explicit L4 governance function — "
           "the Quick view's own retrospective found domain managers initially couldn't jointly resolve "
           "conflicting resource constraints, only escalate past each other."),
 "problem": ("Enterprises request bespoke 5G slices with different SLAs, and manually designing and assuring "
             "each slice across RAN, transport, and core takes weeks. Retrofitting a shared cross-domain data "
             "model after each domain manager had its own schema cost a full sprint in the Quick view's own "
             "build history."),
 "diagram_note": ("The Slice Readiness Confidence Gate routes any cross-domain resource conflict to a network "
                   "engineer rather than letting one domain manager silently override another; L4's shared "
                   "data-model policy is the fix for the schema-fragmentation issue the Quick view hit."),
 "spec": {
   "l1": [_int("int1", "TM Forum NEST/GST Intent Templates"), _int("int2", "RAN/Transport/Core Domain State"),
          _int("int3", "SLA Feasibility Model")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Cross-Domain SA5/TM Forum Knowledge Graph")],
   "l3_orch": _orch("orch", "Slice Lifecycle Orchestrator (E2E)"),
   "l3_workers": [_w("w1", "RAN Domain Manager Agent"), _w("w2", "Transport Domain Manager Agent"), _w("w3", "Core (5GC) Domain Manager Agent")],
   "l4": [_l4("g1", "Shared Cross-Domain Data-Model Policy"), _l4("g2", "Resource-Conflict Guardrail"), _l4("g3", "SLA Feasibility Rule Engine")],
   "gate": _gate("gate", "Slice Readiness Confidence Gate"),
   "l5": [_l5_human("human", "Network Engineer Review"), _l5_auto("a1", "OSS/BSS Order Fulfillment"),
          _l5_plain("a2", "SLA Dashboard for Enterprise Customer"), _l5_hold("hold", "Resource-Conflict Hold Queue")],
   "l6": [_l6("m1", "SLA Breach Monitor"), _l6("m2", "Cross-Domain Trace Watchdog"), _l6("m3", "Slice Provisioning Auditor")],
   "l7": [_l7("lead1", "Speed-to-Market Dashboard"), _l7("lead2", "SLA Compliance Scorecard"), _l7("lead3", "Slice Portfolio View")],
   "l8": [_l8("s1", "Slice Feasibility Accuracy Tracker"), _l8("s2", "Simulation-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("5G network slicing", "RAN Domain Manager Agent", "Slice Lifecycle Orchestrator (E2E)", 2,
                         "Slice Readiness Confidence Gate", "OSS/BSS Order Fulfillment", "Network Engineer Review"),
},

{
 "id": 3, "quick_slug": "capacity-planning-traffic-forecasting",
 "quick_title": "Proactive Capacity Planning & Traffic Forecasting",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Network Capacity Investment Decisioning",
 "intro": ("This deep-8 view adds scenario-comparison as a first-class L5 output rather than a single "
           "recommended plan — the Quick view's own retrospective wished it had offered upgrade-timing "
           "alternatives, not just one answer, from the start."),
 "problem": ("Network planning teams manually forecast capacity using spreadsheets, missing fast-moving "
             "demand shifts. Forecasting was a bottleneck when run strictly sequentially, and external "
             "event-signal quality (stale population data) silently degraded forecast accuracy for two "
             "release cycles before it was caught."),
 "diagram_note": ("The Capacity Investment Confidence Gate routes any capex decision above a threshold to "
                   "Finance/Network Planning leadership; L6's external-signal-quality watchdog specifically "
                   "exists to catch the stale-data failure mode the Quick view discovered only after two "
                   "release cycles."),
 "spec": {
   "l1": [_int("int1", "PM Counters / Subscriber Growth Data"), _ext("ext1", "Public Event/Census APIs"),
          _int("int2", "Historical Upgrade Outcomes")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Site/Region Demand Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Data Ingestion Agent"), _w("w2", "Forecasting Agent"),
                  _w("w3", "Congestion Risk Scoring Agent"), _w("w4", "Upgrade Prioritization Agent")],
   "l4": [_l4("g1", "Capex Budget Policy"), _l4("g2", "External-Signal-Quality Guardrail"), _l4("g3", "Business-Case Rule Engine")],
   "gate": _gate("gate", "Capacity Investment Confidence Gate"),
   "l5": [_l5_human("human", "Finance/Network Planning Review"), _l5_auto("a1", "Capacity Planning System Update"),
          _l5_plain("a2", "Field Ops Work Order"), _l5_hold("hold", "Signal-Quality Hold Queue")],
   "l6": [_l6("m1", "Forecast Accuracy Monitor"), _l6("m2", "External-Signal-Quality Watchdog"), _l6("m3", "Upgrade Auditor")],
   "l7": [_l7("lead1", "Capacity Plan Dashboard"), _l7("lead2", "Cost-Avoidance Scorecard"), _l7("lead3", "Congestion Risk View")],
   "l8": [_l8("s1", "Forecast Accuracy Tracker"), _l8("s2", "Recalibration Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("capacity planning", "Data Ingestion Agent", None, 3,
                         "Capacity Investment Confidence Gate", "Capacity Planning System Update", "Finance/Network Planning Review"),
},

{
 "id": 4, "quick_slug": "self-healing-network-closed-loop",
 "quick_title": "Self-Healing Network (Closed-Loop Automation)",
 "quick_pattern_label": "Event-Driven Reactive Swarm",
 "title": "Closed-Loop Network Remediation Decisioning",
 "intro": ("This deep-8 view makes the shared blast-radius rate-limiter — added only after two agents "
           "independently restarting adjacent CNFs caused a cascading outage in the Quick view — a "
           "non-negotiable L4 policy from the start, and separates 'decide' from 'act' permissions per agent "
           "as the Quick view's own retrospective recommended."),
 "problem": ("Transient network degradations need sub-minute autonomous reaction. A shared blast-radius "
             "guardrail was missing in v1, and lower-trust agents initially had the same execute authority as "
             "proven ones — the retrospective specifically calls for graduated trust based on track record."),
 "diagram_note": ("The Remediation Confidence Gate enforces a shared rate-limiter across all reactive agents "
                   "at L4, regardless of which agent is acting — this is the direct fix for the Quick view's "
                   "cascading-outage near-miss, and new agents start in 'recommend only' mode until proven "
                   "reliable over N cycles."),
 "spec": {
   "l1": [_int("int1", "Network Event Bus (Kafka)"), _int("int2", "Interface State-Change Log"), _int("int3", "CNF Health Metrics")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Fault-Class Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Link Flap Detector Agent"), _w("w2", "CNF Memory/Restart Agent"),
                  _w("w3", "Interference Mitigation Agent"), _w("w4", "Anomaly Novelty Detector Agent")],
   "l4": [_l4("g1", "Shared Blast-Radius Rate-Limiter Policy (hard veto)"), _l4("g2", "Decide/Act Separation Guardrail"), _l4("g3", "Cool-Down Memory Rule Engine")],
   "gate": _gate("gate", "Remediation Confidence Gate"),
   "l5": [_l5_human("human", "NOC Orchestrator Escalation"), _l5_auto("a1", "Automated Remediation (Ansible/K8s)"),
          _l5_plain("a2", "Closed-Loop Audit Log"), _l5_hold("hold", "Novel-Pattern Hold Queue")],
   "l6": [_l6("m1", "Blast-Radius Monitor"), _l6("m2", "Oscillation/Flap-Loop Watchdog"), _l6("m3", "Remediation Auditor")],
   "l7": [_l7("lead1", "Auto-Remediation Coverage Dashboard"), _l7("lead2", "Incident-Avoided Scorecard"), _l7("lead3", "Agent Trust-Tier View")],
   "l8": [_l8("s1", "Remediation Accuracy Tracker"), _l8("s2", "Trust-Tier Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("self-healing network", "Link Flap Detector Agent", None, 3,
                         "Remediation Confidence Gate", "Automated Remediation (Ansible/K8s)", "NOC Orchestrator Escalation"),
},

{
 "id": 6, "quick_slug": "contact-center-triage-resolution",
 "quick_title": "Intelligent Contact Center Triage & Resolution",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Contact Center Resolution Decisioning",
 "intro": ("This deep-8 view adds a shared session-state store as an explicit L3 memory function — the "
           "Quick view found domain managers initially couldn't see each other's context, causing duplicate "
           "retention offers on the same call."),
 "problem": ("Contact centers field billing, technical, and retention calls with misrouting inflating handle "
             "time. Intent-only routing missed customer-value signals that meaningfully cut escalations once "
             "added, and domain managers duplicating offers due to invisible cross-domain context was a real "
             "production issue."),
 "diagram_note": ("The Resolution Confidence Gate routes to a live human handoff with a structured 5-bullet "
                   "context summary — the Quick view found verbose handoffs were unusable, and redesigned this "
                   "specifically after agent feedback."),
 "spec": {
   "l1": [_int("int1", "Live Call/Chat Transcript"), _int("int2", "Knowledge Base (Confluence export)"), _int("int3", "NOC Outage Feed")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Intent/Resolution Knowledge Graph")],
   "l3_orch": _orch("orch", "Contact Center Orchestrator Agent"),
   "l3_workers": [_w("w1", "Billing Domain Manager Agent"), _w("w2", "Technical Support Domain Manager Agent"), _w("w3", "Sales/Retention Domain Manager Agent")],
   "l4": [_l4("g1", "Discount/Authority Limit Policy"), _l4("g2", "Duplicate-Offer Guardrail"), _l4("g3", "Handoff-Summary Rule Engine")],
   "gate": _gate("gate", "Resolution Confidence Gate"),
   "l5": [_l5_human("human", "Live Human Handoff"), _l5_auto("a1", "CRM Case Update"),
          _l5_plain("a2", "Customer Resolution via Chat/Voice"), _l5_hold("hold", "Complex-Case Hold Queue")],
   "l6": [_l6("m1", "Containment-Rate Monitor"), _l6("m2", "Silent-QA Watchdog"), _l6("m3", "Handoff-Quality Auditor")],
   "l7": [_l7("lead1", "Containment Rate Dashboard"), _l7("lead2", "CSAT Scorecard"), _l7("lead3", "Escalation-by-Domain View")],
   "l8": [_l8("s1", "Routing Accuracy Tracker"), _l8("s2", "Intent-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("contact center triage", "Billing Domain Manager Agent", "Contact Center Orchestrator Agent", 2,
                         "Resolution Confidence Gate", "CRM Case Update", "Live Human Handoff"),
},

{
 "id": 7, "quick_slug": "sim-swap-fraud-detection",
 "quick_title": "SIM-Swap & Account-Takeover Fraud Detection",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "SIM-Swap Fraud Decisioning",
 "intro": ("This deep-8 view keeps the proposer/critic independence discipline shared with the AML and "
           "insider-trading use cases — the same design lesson (shared context causes confirmation bias) "
           "was independently re-confirmed here."),
 "problem": ("SIM-swap fraud bypasses SMS 2FA to take over banking/crypto accounts. Letting the arbiter be a "
             "third LLM vote correlated too much with the proposer's own framing; calibrated scoring using "
             "both agents' extracted evidence separately was needed instead."),
 "diagram_note": ("The Fraud Risk Confidence Gate never lets the arbiter's determination be a simple vote — "
                   "L4's calibrated-scoring rule engine weighs the proposer's and critic's independently-"
                   "gathered evidence, not a re-ask of either agent's opinion."),
 "spec": {
   "l1": [_int("int1", "Account/Device History"), _int("int2", "SIM-Swap Request Metadata"), _int("int3", "Known Fraud Ring Patterns DB")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Fraud Graph Knowledge Graph", "Neo4j graph database")],
   "l3_orch": _orch("orch", "Fraud Decision Arbiter Agent"),
   "l3_workers": [_w("w1", "Fraud Hypothesis Proposer Agent"), _w("w2", "Legitimate-Explanation Critic Agent"), _w("w3", "Fraud Ring Pattern-Matching Agent")],
   "l4": [_l4("g1", "Calibrated-Scoring Policy"), _l4("g2", "False-Positive Customer-Friction Guardrail"), _l4("g3", "Step-Up Verification Rule Engine")],
   "gate": _gate("gate", "Fraud Risk Confidence Gate"),
   "l5": [_l5_human("human", "Fraud Analyst Review"), _l5_auto("a1", "Block/Hold SIM Swap"),
          _l5_plain("a2", "Step-Up Verification Request"), _l5_hold("hold", "Fraud Case Creation Queue")],
   "l6": [_l6("m1", "False-Positive Friction Monitor"), _l6("m2", "Red-Team Pattern Watchdog"), _l6("m3", "Block Auditor")],
   "l7": [_l7("lead1", "Fraud-Caught Dashboard"), _l7("lead2", "Customer-Friction Scorecard"), _l7("lead3", "Fraud-Ring Detection View")],
   "l8": [_l8("s1", "Arbitration Accuracy Tracker"), _l8("s2", "Red-Team Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("SIM-swap fraud", "Fraud Hypothesis Proposer Agent", "Fraud Decision Arbiter Agent", 2,
                         "Fraud Risk Confidence Gate", "Block/Hold SIM Swap", "Fraud Analyst Review"),
},

{
 "id": 8, "quick_slug": "telecom-soc-threat-hunting",
 "quick_title": "Telecom SOC Threat Hunting & Incident Response",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "SOC Threat Containment Decisioning",
 "intro": ("This deep-8 view adds a unified threat-narrative synthesis step as a first-class L3 output — "
           "the Quick view found analysts initially had to piece together outputs from 5 separate agents "
           "themselves."),
 "problem": ("Telecom networks face signaling exploits and DDoS against core infrastructure, overwhelming SOC "
             "analysts with alert volume. Signaling and IT-security data had incompatible time granularity, "
             "which standardizing on a common event-time schema earlier would have saved significant "
             "correlation-agent rework."),
 "diagram_note": ("The Containment Confidence Gate always requires two-person-rule sign-off for any "
                   "auto-containment above the defined blast radius — this SOC-specific two-person rule sits "
                   "in L4 alongside the more general confidence-based routing every other use case uses."),
 "spec": {
   "l1": [_int("int1", "SIEM (Splunk/Sentinel)"), _int("int2", "Signaling Firewall Logs"), _ext("ext1", "Threat Intel Feeds (STIX/TAXII)")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Kill-Chain Knowledge Graph")],
   "l3_orch": _orch("orch", "SOC Incident Response Orchestrator"),
   "l3_workers": [_w("w1", "Signaling Abuse Detection Agent"), _w("w2", "DDoS Detection Agent"),
                  _w("w3", "SIEM Correlation Agent"), _w("w4", "Threat Intelligence Enrichment Agent")],
   "l4": [_l4("g1", "Two-Person-Rule Containment Policy (hard veto)"), _l4("g2", "False-Positive Containment-Cost Guardrail"), _l4("g3", "SOAR Playbook Rule Engine")],
   "gate": _gate("gate", "Containment Confidence Gate"),
   "l5": [_l5_human("human", "SOC Tier-2 Analyst Approval"), _l5_auto("a1", "Auto-Block via Signaling Firewall"),
          _l5_plain("a2", "SOAR Playbook Execution"), _l5_hold("hold", "Analyst Case Hold Queue")],
   "l6": [_l6("m1", "Kill-Chain Narrative Monitor"), _l6("m2", "Containment-Cost Watchdog"), _l6("m3", "Playbook Auditor")],
   "l7": [_l7("lead1", "Threat Coverage Dashboard"), _l7("lead2", "Containment-Cost Scorecard"), _l7("lead3", "Kill-Chain View")],
   "l8": [_l8("s1", "Detection Accuracy Tracker"), _l8("s2", "Replay-Simulation Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("SOC threat hunting", "Signaling Abuse Detection Agent", "SOC Incident Response Orchestrator", 3,
                         "Containment Confidence Gate", "Auto-Block via Signaling Firewall", "SOC Tier-2 Analyst Approval"),
},

{
 "id": 9, "quick_slug": "field-workforce-dispatch-scheduling",
 "quick_title": "Field Workforce Dispatch & Dynamic Scheduling",
 "quick_pattern_label": "Market-Based / Auction Agents",
 "title": "Field Dispatch Allocation Decisioning",
 "intro": ("This deep-8 view adds an explainability layer as a first-class L7 component — the Quick view's "
           "own retrospective found dispatchers needed to see *why* a job was assigned to a given technician, "
           "not just receive a black-box optimizer output."),
 "problem": ("Dispatching technicians across a large geography with varying skills, SLA windows, and travel "
             "time is a hard combinatorial problem. Pure price-based bidding under-weighted technician "
             "fatigue, and re-auctioning on a fixed schedule caused unnecessary reassignment churn."),
 "diagram_note": ("The Dispatch Confidence Gate routes only genuinely ambiguous multi-technician conflicts to "
                   "a dispatcher; L7's explainability view gives every dispatcher visibility into the "
                   "auction's reasoning, not just its output, addressing the Quick view's black-box concern."),
 "spec": {
   "l1": [_int("int1", "Live Technician GPS/Skill Profile"), _int("int2", "Open Job Queue"), _int("int3", "SLA Risk Scoring Feed")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Skill/Route Knowledge Graph")],
   "l3_orch": _orch("orch", "Dispatch Clearing Agent"),
   "l3_workers": [_w("w1", "Technician Agent"), _w("w2", "Emergency Job Priority Agent"), _w("w3", "Sub-contractor Capacity Agent")],
   "l4": [_l4("g1", "Fatigue/Overtime Guardrail"), _l4("g2", "Sub-Contractor Cost-Visibility Policy"), _l4("g3", "Re-Auction Trigger Rule Engine")],
   "gate": _gate("gate", "Dispatch Confidence Gate"),
   "l5": [_l5_human("human", "Dispatcher Review"), _l5_auto("a1", "Work Order Assignment System"),
          _l5_plain("a2", "Technician Mobile App Push"), _l5_hold("hold", "SLA Breach Risk Hold")],
   "l6": [_l6("m1", "Fill-Rate Monitor"), _l6("m2", "Drive-Time Watchdog"), _l6("m3", "Assignment Auditor")],
   "l7": [_l7("lead1", "Fill-Rate Dashboard"), _l7("lead2", "SLA Compliance Scorecard"), _l7("lead3", "Assignment Explainability View")],
   "l8": [_l8("s1", "Assignment Accuracy Tracker"), _l8("s2", "Bid-Function Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("field workforce dispatch", "Technician Agent", "Dispatch Clearing Agent", 2,
                         "Dispatch Confidence Gate", "Work Order Assignment System", "Dispatcher Review"),
},

{
 "id": 10, "quick_slug": "billing-dispute-resolution",
 "quick_title": "Billing Dispute Investigation & Resolution",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Billing Dispute Resolution Decisioning",
 "intro": ("This deep-8 view keeps credit calculation strictly in a deterministic rules engine after the "
           "Quick view's own early prototype produced a plausible-but-wrong dollar amount — a hard lesson on "
           "where generative reasoning cannot be trusted, echoed across several other use cases in this "
           "catalog."),
 "problem": ("Billing disputes require pulling data across billing, rating, mediation, and CRM systems. "
             "Parallelizing evidence-gathering calls rather than running them sequentially cut latency "
             "significantly, and compliance-phrase review of the customer communication draft was needed "
             "after an early regulatory-language miss."),
 "diagram_note": ("The Resolution Confidence Gate keeps L4's credit-calculation determinism policy as a hard, "
                   "non-negotiable rule — the exact dollar amount is never LLM-generated, only the "
                   "investigation and communication drafting are."),
 "spec": {
   "l1": [_int("int1", "Billing/Rating System Records"), _int("int2", "Mediation Logs"), _int("int3", "CRM Dispute Ticket")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Billing Root-Cause Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Dispute Intake & Classification Agent"), _w("w2", "Cross-System Evidence Gathering Agent"),
                  _w("w3", "Root-Cause Determination Agent"), _w("w4", "Customer Communication Drafting Agent")],
   "l4": [_l4("g1", "Credit-Calculation Determinism Policy (hard veto)"), _l4("g2", "Compliance-Phrase Guardrail"), _l4("g3", "Systemic-Bug Detection Rule Engine")],
   "gate": _gate("gate", "Resolution Confidence Gate"),
   "l5": [_l5_human("human", "Billing Specialist Review"), _l5_auto("a1", "Billing System Credit/Adjustment"),
          _l5_plain("a2", "Customer Notification"), _l5_hold("hold", "Systemic-Bug Investigation Hold")],
   "l6": [_l6("m1", "Resolution-Time Monitor"), _l6("m2", "Compliance-Language Watchdog"), _l6("m3", "Credit Auditor")],
   "l7": [_l7("lead1", "Dispute Resolution-Time Dashboard"), _l7("lead2", "Credit-Accuracy Scorecard"), _l7("lead3", "Systemic-Issue View")],
   "l8": [_l8("s1", "Root-Cause Accuracy Tracker"), _l8("s2", "Classification Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("billing disputes", "Dispute Intake & Classification Agent", None, 3,
                         "Resolution Confidence Gate", "Billing System Credit/Adjustment", "Billing Specialist Review"),
},

{
 "id": 11, "quick_slug": "line-onboarding-kyc-automation",
 "quick_title": "New Line/Device Onboarding & KYC Automation",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Line Activation Decisioning",
 "intro": ("This deep-8 view adds explicit per-worker timeout/fallback behavior as a first-class L4 policy — "
           "the Quick view's own early version stalled the whole onboarding flow when one bureau API was "
           "slow, with no defined fallback."),
 "problem": ("Activating a new line requires identity verification, credit risk, and fraud screening in "
             "parallel. A slow credit bureau API could stall the entire flow without explicit per-agent "
             "timeouts, and conflating fraud-score and credit-score thresholds made bias/fairness audits "
             "harder than necessary."),
 "diagram_note": ("The Activation Confidence Gate always produces a compliant, actionable reason code on any "
                   "rejection — the Quick view specifically flagged opaque declines as a fair-lending risk; "
                   "L4 keeps fraud and credit thresholds tuned and audited separately, not conflated."),
 "spec": {
   "l1": [_ext("ext1", "Government ID / Document Scan"), _ext("ext2", "Credit Bureau Feed"), _int("int1", "Coverage Map API")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Applicant Risk Knowledge Graph")],
   "l3_orch": _orch("orch", "Onboarding Decision Orchestrator Agent"),
   "l3_workers": [_w("w1", "Identity Verification (KYC) Agent"), _w("w2", "Credit Risk Assessment Agent"),
                  _w("w3", "Device Financing Fraud Agent"), _w("w4", "Address/Coverage Validation Agent")],
   "l4": [_l4("g1", "Per-Agent Timeout/Fallback Policy"), _l4("g2", "Separated Fraud/Credit Threshold Guardrail"), _l4("g3", "Reason-Code Rule Engine")],
   "gate": _gate("gate", "Activation Confidence Gate"),
   "l5": [_l5_human("human", "Manual Review (Borderline Scores)"), _l5_auto("a1", "Line Activation/Provisioning System"),
          _l5_plain("a2", "Device Financing Approval"), _l5_hold("hold", "Rejection Reason-Code Queue")],
   "l6": [_l6("m1", "Timeout/Fallback Monitor"), _l6("m2", "Fair-Lending Bias Watchdog"), _l6("m3", "Activation Auditor")],
   "l7": [_l7("lead1", "Activation Conversion Dashboard"), _l7("lead2", "Fair-Lending Compliance Scorecard"), _l7("lead3", "Fraud-Caught View")],
   "l8": [_l8("s1", "Decision Accuracy Tracker"), _l8("s2", "Threshold Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("line onboarding", "Identity Verification (KYC) Agent", "Onboarding Decision Orchestrator Agent", 3,
                         "Activation Confidence Gate", "Line Activation/Provisioning System", "Manual Review (Borderline Scores)"),
},

{
 "id": 12, "quick_slug": "rf-cell-site-planning-optimization",
 "quick_title": "RF / Cell-Site Planning & Optimization",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "RF Parameter Change Decisioning",
 "intro": ("This deep-8 view makes digital-twin validation a mandatory L4 gate before any production RF "
           "change — added after an early direct-to-production tilt change caused unexpected coverage holes "
           "in an adjacent cluster."),
 "problem": ("Optimizing RF parameters across thousands of cells is a continuous multi-objective problem. "
             "Treating clusters as fully independent caused optimization thrashing at cluster boundaries, and "
             "RF engineers wanted the rationale behind a proposed change, not just the new parameter value."),
 "diagram_note": ("The RF Change Confidence Gate requires digital-twin simulation validation before any "
                   "parameter change reaches production — this is the direct, non-optional fix for the Quick "
                   "view's coverage-hole incident, not an optional check."),
 "spec": {
   "l1": [_int("int1", "PM Data / MDT Crowdsourced Data"), _int("int2", "Propagation Model (Atoll/iBwave)"), _int("int3", "Cluster Boundary Topology")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "RF Interference Knowledge Graph")],
   "l3_orch": _orch("orch", "Network-wide RF Optimization Orchestrator"),
   "l3_workers": [_w("w1", "Cluster Optimization Manager Agent"), _w("w2", "Coverage/Interference Analysis Agent"), _w("w3", "PCI/Neighbor-list Optimization Agent")],
   "l4": [_l4("g1", "Digital-Twin Validation Policy (hard veto)"), _l4("g2", "Inter-Cluster Interference Guardrail"), _l4("g3", "Change-Rationale Rule Engine")],
   "gate": _gate("gate", "RF Change Confidence Gate"),
   "l5": [_l5_human("human", "RF Engineer Review"), _l5_auto("a1", "Self-Organizing Network (SON) Parameter Push"),
          _l5_plain("a2", "RF Change Validation Report"), _l5_hold("hold", "KPI-Regression Rollback Hold")],
   "l6": [_l6("m1", "KPI-Regression Monitor"), _l6("m2", "Inter-Cluster Boundary Watchdog"), _l6("m3", "Change Auditor")],
   "l7": [_l7("lead1", "Network KPI Dashboard"), _l7("lead2", "Optimization Coverage Scorecard"), _l7("lead3", "Change-Rationale View")],
   "l8": [_l8("s1", "Optimization Accuracy Tracker"), _l8("s2", "Bayesian-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("RF optimization", "Coverage/Interference Analysis Agent", "Network-wide RF Optimization Orchestrator", 2,
                         "RF Change Confidence Gate", "Self-Organizing Network (SON) Parameter Push", "RF Engineer Review"),
},

{
 "id": 13, "quick_slug": "roaming-settlement-reconciliation",
 "quick_title": "Roaming Partner Settlement Reconciliation",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Roaming Settlement Reconciliation Decisioning",
 "intro": ("This deep-8 view adds per-partner fuzzy-matching threshold tuning as an explicit L4 policy — the "
           "Quick view found a single global threshold over-flagged discrepancies with some partners due to "
           "differing clock-sync tolerances."),
 "problem": ("Cross-carrier settlement requires reconciling TAP/CDR records and applying bilateral agreement "
             "terms. A global fuzzy-matching threshold doesn't fit every partner relationship, and email-based "
             "dispute packs slowed resolution compared to a self-service status portal."),
 "diagram_note": ("The Settlement Confidence Gate applies per-partner-tuned matching thresholds rather than "
                   "one global setting; L5 includes a partner self-service status portal in place of the "
                   "slower email-based dispute pack workflow."),
 "spec": {
   "l1": [_ext("ext1", "Partner TAP3/RAP Files"), _int("int1", "Internal CDR Records"), _int("int2", "Bilateral Agreement Terms")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Discrepancy Root-Cause Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "TAP/CDR Ingestion Agent"), _w("w2", "Bilateral Agreement Rate Agent"),
                  _w("w3", "Record Matching Agent"), _w("w4", "Discrepancy Detection Agent")],
   "l4": [_l4("g1", "Per-Partner Matching-Threshold Policy"), _l4("g2", "Multi-Currency FX Guardrail"), _l4("g3", "Dispute Pack Rule Engine")],
   "gate": _gate("gate", "Settlement Confidence Gate"),
   "l5": [_l5_human("human", "Roaming Ops Review"), _l5_auto("a1", "Settlement Invoice Generation"),
          _l5_plain("a2", "Partner Self-Service Status Portal"), _l5_hold("hold", "Dispute Case Hold Queue")],
   "l6": [_l6("m1", "Discrepancy Rate Monitor"), _l6("m2", "Clock-Sync Watchdog"), _l6("m3", "Invoice Auditor")],
   "l7": [_l7("lead1", "Settlement Cycle-Time Dashboard"), _l7("lead2", "Leakage-Recovery Scorecard"), _l7("lead3", "Partner Dispute View")],
   "l8": [_l8("s1", "Matching Accuracy Tracker"), _l8("s2", "Root-Cause Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("roaming settlement", "TAP/CDR Ingestion Agent", None, 3,
                         "Settlement Confidence Gate", "Settlement Invoice Generation", "Roaming Ops Review"),
},

{
 "id": 14, "quick_slug": "iot-fleet-anomaly-detection",
 "quick_title": "IoT Device Fleet Anomaly Detection & Remediation",
 "quick_pattern_label": "Blackboard / Shared-Memory",
 "title": "IoT Fleet Health Decisioning",
 "intro": ("This deep-8 view adds device-model-specific baselines and per-fleet partitioning from the "
           "start — the Quick view found a single global battery-drain baseline produced too many false "
           "positives across heterogeneous device types, and the blackboard grew unbounded for large fleets "
           "without TTL-based pruning."),
 "problem": ("Enterprise IoT fleets run millions of devices whose individual anomalies are hard to see but "
             "form clear patterns at fleet scale. The controller occasionally over-synthesized fleet-level "
             "trends from sparse data before a minimum-evidence threshold was added."),
 "diagram_note": ("The Fleet Health Confidence Gate requires a minimum-evidence threshold before any "
                   "fleet-level finding surfaces — L4's guardrail directly addresses the Quick view's "
                   "over-synthesis problem, and device-model-specific baselines replace the single global "
                   "baseline that caused false positives."),
 "spec": {
   "l1": [_int("int1", "IoT Connectivity Platform Stream"), _int("int2", "Device Model Baseline Registry"), _int("int3", "Enterprise Fleet Registry")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Device Fleet Knowledge Graph")],
   "l3_orch": _orch("orch", "Fleet Health Controller Agent"),
   "l3_workers": [_w("w1", "Connectivity Pattern Agent"), _w("w2", "Battery/Power Anomaly Agent"), _w("w3", "Security/Compromise Indicator Agent")],
   "l4": [_l4("g1", "Minimum-Evidence Threshold Policy"), _l4("g2", "Device-Model-Specific Baseline Guardrail"), _l4("g3", "TTL-Based Pruning Rule Engine")],
   "gate": _gate("gate", "Fleet Health Confidence Gate"),
   "l5": [_l5_human("human", "Enterprise Ops Team Alert"), _l5_auto("a1", "Customer Fleet Health Dashboard"),
          _l5_plain("a2", "Auto-Remediation (Firmware Push/Reboot)"), _l5_hold("hold", "Low-Evidence Hold Queue")],
   "l6": [_l6("m1", "False-Positive Rate Monitor"), _l6("m2", "Blackboard-Growth Watchdog"), _l6("m3", "Remediation Auditor")],
   "l7": [_l7("lead1", "Fleet Health Dashboard"), _l7("lead2", "Remediation Coverage Scorecard"), _l7("lead3", "Security Indicator View")],
   "l8": [_l8("s1", "Synthesis Accuracy Tracker"), _l8("s2", "Baseline Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("IoT fleet anomaly detection", "Connectivity Pattern Agent", "Fleet Health Controller Agent", 2,
                         "Fleet Health Confidence Gate", "Customer Fleet Health Dashboard", "Enterprise Ops Team Alert"),
},

{
 "id": 15, "quick_slug": "sentiment-social-listening-action",
 "quick_title": "Customer Sentiment & Social Listening to Action",
 "quick_pattern_label": "Event-Driven Reactive Swarm",
 "title": "Social Sentiment Response Decisioning",
 "intro": ("This deep-8 view keeps the Quick view's hard constraint — every public-facing response requires "
           "human approval, no exceptions — as a permanent L4 policy even as other automation in the system "
           "matures."),
 "problem": ("Service outages trend on social media faster than internal monitoring detects them. Sarcasm and "
             "negation handling was a major early accuracy gap, and internal teams were paged too often on "
             "minor sentiment noise before risk-scoring thresholds were calibrated."),
 "diagram_note": ("The Response Confidence Gate never allows a public post to auto-execute — L4's human-"
                   "approval policy for anything public-facing is absolute and doesn't loosen as the rest of "
                   "the system's automation matures, unlike most other gates in this catalog."),
 "spec": {
   "l1": [_ext("ext1", "Social Listening APIs (X/Reddit)"), _int("int1", "NOC Outage Feed"), _int("int2", "Brand-Voice Phrase Library")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Topic/Sentiment Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Social Mention Ingestion Agent"), _w("w2", "Sentiment/Topic Classification Agent"),
                  _w("w3", "Outage-Correlation Agent"), _w("w4", "PR Risk Scoring Agent")],
   "l4": [_l4("g1", "Public-Response Human-Approval Policy (hard veto)"), _l4("g2", "Internal-Alert Rate-Limit Guardrail"), _l4("g3", "Brand-Voice Rule Engine")],
   "gate": _gate("gate", "Response Confidence Gate"),
   "l5": [_l5_human("human", "Comms/PR Team Approval"), _l5_auto("a1", "Internal Team Alert (NOC/Billing/PR)"),
          _l5_plain("a2", "Trend Dashboard Update"), _l5_hold("hold", "Low-Confidence Sentiment Hold")],
   "l6": [_l6("m1", "Sarcasm/Negation Accuracy Monitor"), _l6("m2", "Alert-Rate Watchdog"), _l6("m3", "Response Auditor")],
   "l7": [_l7("lead1", "Reputational Risk Dashboard"), _l7("lead2", "Response-Time Scorecard"), _l7("lead3", "Trending-Topic View")],
   "l8": [_l8("s1", "Sentiment Accuracy Tracker"), _l8("s2", "Classifier Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("social sentiment response", "Social Mention Ingestion Agent", None, 3,
                         "Response Confidence Gate", "Internal Team Alert (NOC/Billing/PR)", "Comms/PR Team Approval"),
},

{
 "id": 16, "quick_slug": "spectrum-interference-detection",
 "quick_title": "Spectrum Interference Detection & Mitigation",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Spectrum Interference Mitigation Decisioning",
 "intro": ("This deep-8 view integrates equipment inventory data as a first-class L1 source from the start — "
           "the Quick view found many early 'interference' cases were actually the operator's own faulty "
           "equipment, missed by a triangulation-only flow."),
 "problem": ("Unlicensed spectrum use or faulty equipment degrades performance in hard-to-diagnose ways. "
             "Triangulation accuracy was highly sensitive to sensor density, and a historical interference-"
             "pattern library would have let recurring known sources be identified instantly instead of "
             "re-investigated each time."),
 "diagram_note": ("The Interference Confidence Gate cross-checks against the operator's own equipment "
                   "inventory before escalating to a regulatory filing — a source flagged as 'interference' "
                   "that turns out to be internal equipment routes to field investigation instead."),
 "spec": {
   "l1": [_int("int1", "Distributed Spectrum Sensors"), _int("int2", "Site Equipment Inventory"), _ext("ext1", "Regulatory Spectrum Database")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Historical Interference Pattern Knowledge Graph")],
   "l3_orch": _orch("orch", "Interference Investigation Orchestrator"),
   "l3_workers": [_w("w1", "Spectrum Sensor Data Agent"), _w("w2", "Interference Source Triangulation Agent"), _w("w3", "PM/KPI Impact Correlation Agent")],
   "l4": [_l4("g1", "Equipment-Inventory Cross-Check Policy"), _l4("g2", "Sensor-Density Confidence Guardrail"), _l4("g3", "Evidence-Citation Rule Engine")],
   "gate": _gate("gate", "Interference Confidence Gate"),
   "l5": [_l5_human("human", "RF Engineer Review"), _l5_auto("a1", "Frequency Reassignment Request"),
          _l5_plain("a2", "Field Investigation Work Order"), _l5_hold("hold", "Regulatory Filing Hold Queue")],
   "l6": [_l6("m1", "Triangulation-Accuracy Monitor"), _l6("m2", "Own-Equipment Watchdog"), _l6("m3", "Filing Auditor")],
   "l7": [_l7("lead1", "Interference Resolution Dashboard"), _l7("lead2", "Mitigation-Time Scorecard"), _l7("lead3", "Recurring-Source View")],
   "l8": [_l8("s1", "Triangulation Accuracy Tracker"), _l8("s2", "Pattern-Library Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("spectrum interference", "Spectrum Sensor Data Agent", "Interference Investigation Orchestrator", 2,
                         "Interference Confidence Gate", "Frequency Reassignment Request", "RF Engineer Review"),
},

{
 "id": 17, "quick_slug": "enterprise-sla-compliance-monitoring",
 "quick_title": "Enterprise SLA Compliance Monitoring & Credit Automation",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "SLA Credit Automation Decisioning",
 "intro": ("This deep-8 view adds proactive at-risk-of-breach alerting to network ops as a first-class L7 "
           "output, not just after-the-fact credit calculation — the Quick view found this turns the system "
           "from reactive accounting into a retention tool."),
 "problem": ("Enterprise SLA contracts carry financial penalties that operators often under- or over-report. "
             "Contract term interpretation needed human legal sign-off per template before automation — fully "
             "autonomous legal-language interpretation was too risky to trust blindly."),
 "diagram_note": ("The Credit Calculation Confidence Gate keeps L4's credit-calculation policy strictly "
                   "deterministic — the same lesson as the Billing Dispute use case — while L7 adds proactive "
                   "breach-risk alerting the Quick view found meaningfully changed the system's business value."),
 "spec": {
   "l1": [_int("int1", "Network Monitoring (ThousandEyes/SolarWinds)"), _int("int2", "Enterprise Contract Documents"), _int("int3", "Measurement-Window Exclusion Rules")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Contract-Term Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "SLA Metric Collection Agent"), _w("w2", "Contract Term Interpretation Agent"),
                  _w("w3", "Breach Detection & Duration Agent"), _w("w4", "Credit Calculation Agent")],
   "l4": [_l4("g1", "Credit-Calculation Determinism Policy (hard veto)"), _l4("g2", "Legal Sign-off Guardrail"), _l4("g3", "Measurement-Window Rule Engine")],
   "gate": _gate("gate", "Credit Calculation Confidence Gate"),
   "l5": [_l5_human("human", "Legal/Contract Ops Review"), _l5_auto("a1", "Automatic Billing Credit"),
          _l5_plain("a2", "At-Risk-of-Breach Proactive Alert"), _l5_hold("hold", "Contract-Amendment Hold Queue")],
   "l6": [_l6("m1", "Breach-Duration Monitor"), _l6("m2", "Contract-Version Watchdog"), _l6("m3", "Credit Auditor")],
   "l7": [_l7("lead1", "SLA Compliance Dashboard"), _l7("lead2", "Credit-Accuracy Scorecard"), _l7("lead3", "At-Risk Contracts View")],
   "l8": [_l8("s1", "Breach-Detection Accuracy Tracker"), _l8("s2", "Rule-Coverage Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("SLA credit automation", "SLA Metric Collection Agent", None, 3,
                         "Credit Calculation Confidence Gate", "Automatic Billing Credit", "Legal/Contract Ops Review"),
},

{
 "id": 18, "quick_slug": "wholesale-bandwidth-marketplace",
 "quick_title": "Wholesale Bandwidth Marketplace (Capacity Trading)",
 "quick_pattern_label": "Market-Based / Auction Agents",
 "title": "Wholesale Capacity Trading Decisioning",
 "intro": ("This deep-8 view adds a circuit-breaker for anomalous price swings as a first-class L4 policy, "
           "borrowed directly from financial-market safeguards — a gap the Quick view's own retrospective "
           "identified."),
 "problem": ("Operators with excess capacity in some routes and shortages in others could trade wholesale, "
             "but bilateral trust issues were the biggest adoption blocker, not the technology. Trades cleared "
             "faster than provisioning teams could fulfill them until provisioning-capacity awareness was "
             "added to the clearing logic."),
 "diagram_note": ("The Trade Clearing Confidence Gate incorporates provisioning-capacity awareness directly "
                   "into the matching logic — a trade only clears if it can actually be fulfilled, not just if "
                   "the price matched, per the Quick view's own fix."),
 "spec": {
   "l1": [_int("int1", "Live Market/Resource State"), _int("int2", "Operator Price/Risk Policy"), _int("int3", "Provisioning Capacity Feed")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Cross-Operator Trust Knowledge Graph")],
   "l3_orch": _orch("orch", "Marketplace Clearing Agent"),
   "l3_workers": [_w("w1", "Capacity-Seller Agent"), _w("w2", "Capacity-Buyer Agent"), _w("w3", "Contract Generation Agent")],
   "l4": [_l4("g1", "Anomalous-Price Circuit-Breaker Policy"), _l4("g2", "Provisioning-Capacity Guardrail"), _l4("g3", "Standard-Template Legal Rule Engine")],
   "gate": _gate("gate", "Trade Clearing Confidence Gate"),
   "l5": [_l5_human("human", "Legal Review (Non-Standard Terms)"), _l5_auto("a1", "Automated Wholesale Contract Generation"),
          _l5_plain("a2", "Capacity Provisioning Trigger"), _l5_hold("hold", "Anomalous-Price Hold Queue")],
   "l6": [_l6("m1", "Price-Trend Monitor"), _l6("m2", "Liquidity Watchdog"), _l6("m3", "Settlement Auditor")],
   "l7": [_l7("lead1", "Market Liquidity Dashboard"), _l7("lead2", "Trade Volume Scorecard"), _l7("lead3", "Price-Trend View")],
   "l8": [_l8("s1", "Clearing Accuracy Tracker"), _l8("s2", "Matching-Logic Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("wholesale capacity trading", "Capacity-Seller Agent", "Marketplace Clearing Agent", 2,
                         "Trade Clearing Confidence Gate", "Automated Wholesale Contract Generation", "Legal Review (Non-Standard Terms)"),
},

{
 "id": 19, "quick_slug": "predictive-maintenance-network-hardware",
 "quick_title": "Predictive Maintenance for Network Hardware",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Predictive Maintenance Scheduling Decisioning",
 "intro": ("This deep-8 view replaces naive score-averaging with correlated-failure-mode awareness at L4 — "
           "the Quick view's initial average-based site score under-weighted the fact that a cooling failure "
           "often causes a radio failure, not two independent risks."),
 "problem": ("Reactive maintenance on RRUs, batteries, and cooling systems leads to unplanned outages. Sensor "
             "data quality varied wildly by site vintage, and the initial site-risk fusion logic treated "
             "equipment failure modes as independent when they're often correlated."),
 "diagram_note": ("The Maintenance Priority Confidence Gate uses correlated-failure-mode fusion logic in L4 "
                   "rather than a naive average of independent equipment scores — the direct fix for the Quick "
                   "view's under-weighted correlated-failure problem."),
 "spec": {
   "l1": [_int("int1", "Site IoT Sensor Telemetry"), _int("int2", "Equipment Maintenance History"), _ext("ext1", "Weather Forecast API")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Equipment Failure-Mode Knowledge Graph")],
   "l3_orch": _orch("orch", "Site Health Orchestrator Agent"),
   "l3_workers": [_w("w1", "Battery/Power System Agent"), _w("w2", "RRU/Radio Hardware Agent"), _w("w3", "HVAC/Cooling Agent")],
   "l4": [_l4("g1", "Correlated-Failure-Mode Fusion Policy"), _l4("g2", "Sensor-Data-Quality Guardrail"), _l4("g3", "Cost-Benefit Scheduling Rule Engine")],
   "gate": _gate("gate", "Maintenance Priority Confidence Gate"),
   "l5": [_l5_human("human", "Field Ops Manager Review"), _l5_auto("a1", "Predictive Maintenance Work Order"),
          _l5_plain("a2", "Spare-Parts Pre-Positioning"), _l5_hold("hold", "Low-Data-Quality Hold Queue")],
   "l6": [_l6("m1", "Failure-Prediction Accuracy Monitor"), _l6("m2", "Sensor-Quality Watchdog"), _l6("m3", "Maintenance Auditor")],
   "l7": [_l7("lead1", "Site Risk Heatmap Dashboard"), _l7("lead2", "Outage-Avoided Scorecard"), _l7("lead3", "Maintenance Cost View")],
   "l8": [_l8("s1", "Prediction Accuracy Tracker"), _l8("s2", "RUL-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("predictive maintenance", "Battery/Power System Agent", "Site Health Orchestrator Agent", 2,
                         "Maintenance Priority Confidence Gate", "Predictive Maintenance Work Order", "Field Ops Manager Review"),
},

{
 "id": 20, "quick_slug": "personalized-plan-upsell-agent",
 "quick_title": "Personalized Plan Recommendation & Upsell Agent",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Plan Upsell Recommendation Decisioning",
 "intro": ("This deep-8 view mirrors the Finance domain's Next-Best-Action use case's core discipline — a "
           "hard minimum customer-fit threshold the arbiter cannot override for revenue reasons — applied "
           "here to telecom plan recommendations instead of financial products."),
 "problem": ("Generic upsell campaigns have low conversion and can push customers onto poor-fit plans. Fit "
             "thresholds were initially expert-guessed and too conservative, and the arbiter's explanation "
             "output turned out valuable enough for call-center agent trust that it should have been a "
             "first-class requirement from the start."),
 "diagram_note": ("The Upsell Confidence Gate enforces a minimum customer-fit threshold the arbiter cannot "
                   "override purely for revenue reasons — the same non-negotiable pattern used in the "
                   "Finance domain's Next-Best-Action use case, applied here to plan/device recommendations."),
 "spec": {
   "l1": [_int("int1", "CDR/Data-Usage Time Series"), _int("int2", "Plan Catalog & Pricing"), _int("int3", "Past Upgrade/Downgrade History")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Customer Usage Knowledge Graph")],
   "l3_orch": _orch("orch", "Recommendation Arbiter Agent"),
   "l3_workers": [_w("w1", "Revenue-Optimized Recommendation Agent"), _w("w2", "Customer-Fit Critic Agent"), _w("w3", "Offer Timing Agent")],
   "l4": [_l4("g1", "Minimum-Fit-Threshold Policy (hard veto)"), _l4("g2", "Downgrade-Justification Guardrail"), _l4("g3", "Offer-Fatigue Rule Engine")],
   "gate": _gate("gate", "Upsell Confidence Gate"),
   "l5": [_l5_human("human", "Call-Center Agent Panel"), _l5_auto("a1", "In-App/SMS Personalized Offer"),
          _l5_plain("a2", "Offer Outcome Tracking"), _l5_hold("hold", "Low-Fit Hold Queue")],
   "l6": [_l6("m1", "Fit-Threshold Monitor"), _l6("m2", "Offer-Fatigue Watchdog"), _l6("m3", "Outcome Auditor")],
   "l7": [_l7("lead1", "Upsell Conversion Dashboard"), _l7("lead2", "Customer-Fit Scorecard"), _l7("lead3", "Offer-Fatigue View")],
   "l8": [_l8("s1", "Recommendation Accuracy Tracker"), _l8("s2", "Uplift-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("plan upsell recommendation", "Revenue-Optimized Recommendation Agent", "Recommendation Arbiter Agent", 2,
                         "Upsell Confidence Gate", "In-App/SMS Personalized Offer", "Call-Center Agent Panel"),
},

]
