# -*- coding: utf-8 -*-
"""
Structured source data for the Deep 8-Layer Regenerative Architecture pilots. Single source of truth:
build.py renders both the markdown doc and the website JSON payload from this, the same way the 60
Quick Reference use cases are data-driven from telecom_data.py / bssoss_data.py / finance_data.py.
"""

CHURN_RETENTION = {
    "dslug": "telecom", "id": 5,
    "quick_title": "Customer Churn Prediction & Win-Back Orchestration",
    "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
    "title": "Customer Retention Investment Decisioning",
    "intro": (
        "This is the full 8-layer Integrated Decision Engineering Meta-Architecture treatment of the same "
        "underlying business problem as Telecom Use Case 05. Where the Quick Reference view shows *one "
        "execution pattern* (orchestrator-worker: a supervisor fanning out to parallel specialist agents), "
        "this view shows the *entire enterprise stack* that problem sits inside — governance, memory, "
        "observability, executive accountability, and the regenerative feedback loop — mapped through the "
        "manuscript's L1–L8 model."
    ),
    "problem": (
        "A telecom/BSS-OSS operator loses hundreds of millions of dollars a year to preventable churn. "
        "Tactical retention bots score risk and dispatch offers, but treat retention as an isolated "
        "task-level workflow — disconnected from portfolio-level capital allocation, with no traceable "
        "governance layer to prevent retention offers from systematically favoring some customer segments "
        "over others, no real-time executive view of what retention spend is actually buying in ROI terms, "
        "and no closed feedback loop that learns which offers worked and recalibrates automatically. What's "
        "needed is the full Decision Engineering stack: accountable, auditable, and continuously-improving "
        "from raw CRM data up through the executive dashboard."
    ),
    "diagram_note": (
        "Dashed-border cards are external data stores; solid cream cards are internal systems of record. "
        "The memory row is explicitly split into Short-Term (Working Memory) and Long-Term (Episodic, "
        "Semantic, Policy Memory). The Confidence & Risk Gate branches three ways — high confidence "
        "(auto-execute), medium confidence (human review), low confidence (hold & escalate) — and the "
        "bottom band (L6 → L7 → L8) closes the regenerative loop back into L3's memory."
    ),
    "agent_stack": [
        ("L2", "AI Gateway", "Decouples the Agent Plane from the model provider; routes requests, controls prompts, tracks cost",
         "Agent Plane requests → Model responses, usage telemetry",
         "Claude API called directly", "LiteLLM / Portkey model-routing gateway with cost tracking"),
        ("L3", "Planner Module", "Decomposes a goal (e.g., \"reduce churn in segment X\") into an ordered set of sub-steps",
         "Goal, Working Memory context → Ordered task plan",
         "LangGraph planning node + Claude API", "LangGraph planning node on Temporal for durable execution"),
        ("L3", "Execution Manager", "Calls tools, validates results, retries on failure",
         "Plan step, tool specs → Tool call results",
         "LangGraph tool-calling node + mock FastAPI tools", "LangGraph execution node + real Tool Registry APIs"),
        ("L3", "Reflection Engine", "Internal critic — reviews output against expectations before the Confidence Scorer",
         "Execution results, Episodic Memory → Reviewed result, flagged discrepancies",
         "Claude critique-prompt pattern, no persistence", "Claude critique pattern + Episodic Memory read/write client"),
        ("L3", "Confidence Scorer", "Estimates certainty and risk; sole authority to route into the conditional gate",
         "Reflection output, Policy Memory → Confidence score, routing decision",
         "Simple rule-based heuristic scorer", "Calibrated scoring model + Policy Memory read client"),
        ("L4", "Discount & Margin Policy Engine", "Encodes tacit expert know-how as executable discount/margin rules",
         "Proposed offer terms → Pass/fail, adjusted terms",
         "Plain Python rule functions", "Open Policy Agent (OPA)"),
        ("L4", "Fairness & Non-Discrimination Guardrail", "Blocks offer patterns that would disadvantage a protected group",
         "Offer + segment data → Fairness pass/fail, bias flag",
         "Fairlearn (open source)", "Fairlearn/Aequitas pipeline run on every model version"),
        ("L4", "Regulatory Constraint Engine", "Enforces consumer-protection and consent rules on customer-facing actions",
         "Proposed action, consent data → Compliance pass/fail",
         "Plain Python rule functions", "Dedicated regulatory rules engine, legal-reviewed"),
        ("L5", "Retention Manager Approval", "Human checkpoint for medium-confidence or high-value decisions",
         "Case context, confidence score → Approve/reject",
         "Streamlit approval screen", "Retool or custom internal approval UI"),
        ("L5", "Hold & Escalate Queue", "Catches low-confidence or policy-breach decisions until resolved",
         "Held decision + reason → Escalation ticket",
         "Postgres table + manual polling", "Case/ticket queue (Jira Service Management) + alerting"),
        ("L6", "Drift & Bias Monitor", "Watches live offer-acceptance and fairness metrics for statistically significant drift",
         "Execution + outcome telemetry → Drift/bias alert",
         "Evidently AI (open source)", "Evidently AI Enterprise or a custom pipeline on Grafana/Prometheus"),
        ("L6", "Data Quality Watchdog", "Checks incoming data for completeness/freshness before it reaches the Agent Plane",
         "Raw data-store feeds → Data-quality score",
         "Great Expectations (open source)", "Great Expectations at scale, orchestrated by Airflow"),
        ("L6", "Circuit Breaker / Auto-Pause", "Can halt the whole campaign if Nervous System thresholds are breached",
         "Drift/bias alerts → Pause/resume signal",
         "A simple feature-flag toggle", "Automated circuit-breaker service integrated with paging"),
        ("L8", "Outcome Tracker", "Compares predicted vs. actual retention outcomes",
         "Executed decisions, billing/CRM outcomes → Outcome-accuracy dataset",
         "Scheduled Python script reading Postgres", "Outcome-tracking pipeline against a data warehouse"),
        ("L8", "Model Retraining Trigger", "Fires retraining when Outcome Tracker shows performance degradation",
         "Outcome-accuracy dataset, thresholds → Retraining job trigger",
         "Cron job checking a threshold", "Prefect/Airflow orchestrating scheduled retraining jobs"),
        ("L8", "Memory & Policy Updater", "Writes newly learned rules and outcomes back into Policy and Episodic Memory",
         "Retrained model output → Updated memory entries",
         "Script rewriting a JSON policy file", "Versioned policy store with approval gates + vector DB write client"),
    ],
    "build_order": [
        "**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake CRM data in Postgres, a single Claude API call, "
        "and a mock CRM endpoint that just prints the offer. No memory, no governance, no conditional routing "
        "yet. This proves the dumbest possible version of the pipeline end to end.",
        "**Phase 2 — build out L3, the Agentic Core.** Split the single call into Planner → Execution Manager "
        "→ Reflection Engine → Confidence Scorer, and add Working + Episodic memory (Chroma). This is where "
        "you actually learn agent orchestration, not before.",
        "**Phase 3 — add L4 and the conditional gate.** Wire in the three governance engines as hard gates, "
        "then build the three-way Confidence & Risk Gate routing into auto-execute / human review / hold.",
        "**Phase 4 — complete L5.** Build the Streamlit approval screen and the hold/escalate queue; this is "
        "the first point where a human is actually in the loop.",
        "**Phase 5 — add L6 observability.** Drop in Evidently AI for drift/bias and Great Expectations for "
        "data quality. This is usually the point where you discover problems that were invisible in Phases 1–4.",
        "**Phase 6 — add L7 and L8.** Build the executive dashboard last (Metabase against your Postgres "
        "decisions table) and the scheduled retraining/memory-update job. These teach the least new technical "
        "ground but close the loop the manuscript calls \"regenerative.\"",
    ],
}

RCA_REMEDIATION = {
    "dslug": "telecom", "id": 1,
    "quick_title": "Multi-Agent Network Fault RCA & Auto-Remediation",
    "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
    "title": "Network Fault RCA & Auto-Remediation",
    "intro": (
        "This is the second pilot for the Deep 8-Layer view, chosen deliberately for contrast with the "
        "retention example: where retention's L3 is a linear Planner → Execution → Reflection → Confidence "
        "chain, this use case's L3 keeps its native orchestrator-worker fan-out (one orchestrator, five "
        "parallel specialist agents) — showing the 8-layer model accommodates different internal "
        "orchestration shapes rather than forcing every use case into the same L3 pattern."
    ),
    "problem": (
        "A tier-1 operator's NOC receives thousands of correlated alarms per hour during a fault storm. "
        "Engineers spend 40–60 minutes correlating alarms to find the true root cause before remediation "
        "even starts, driving SLA breaches. Beyond the tactical fix (compress the correlation step), the "
        "deeper problem this deep-8 view addresses is the same one retention has: no governance layer "
        "stopping a high-blast-radius auto-remediation from making things worse, no executive visibility "
        "into what automation is actually saving in MTTR and cost-avoidance terms, and no closed loop that "
        "learns from confirmed root causes to get better at RCA over time."
    ),
    "diagram_note": (
        "L3's Agentic Core is deliberately drawn as orchestrator-then-workers (matching the Quick Reference "
        "pattern) rather than the retention example's linear plan-execute-reflect chain. The RCA Confidence "
        "& Blast-Radius Gate branches three ways — high confidence (auto-remediate), medium confidence or "
        "high blast-radius (SRE approval), low confidence (on-call escalation) — and L8 closes the loop by "
        "comparing predicted root cause against what engineers actually confirmed."
    ),
    "agent_stack": [
        ("L2", "AI Gateway", "Decouples the Agentic Core from the model provider; routes requests, controls prompts, tracks cost",
         "Agent requests → Model responses, usage telemetry",
         "Claude API called directly", "LiteLLM / Portkey model-routing gateway"),
        ("L3", "NOC Incident Orchestrator", "Fans out an alarm burst to domain agents, aggregates hypotheses, ranks root cause by confidence",
         "Alarm burst, Working Memory → Dispatched sub-tasks, aggregated RCA hypothesis",
         "LangGraph supervisor node + Claude", "LangGraph supervisor on Temporal, Kafka consumer group"),
        ("L3", "RAN Alarm Correlation Agent", "Deduplicates and correlates RAN alarms against topology",
         "FM/PM alarms, topology graph → Correlated RAN fault hypothesis",
         "Python + NetworkX graph correlation", "Neo4j graph-traversal service"),
        ("L3", "Transport/IP Topology Agent", "Traces fiber/microwave/IP path failures via topology graph",
         "Topology DB, telemetry → Transport fault hypothesis",
         "Python + NetworkX", "Neo4j + vendor SR-TE controller integration"),
        ("L3", "Core Network Agent", "Inspects 5GC/EPC VNF health via Kubernetes/OSS APIs",
         "K8s pod status, signaling logs → Core fault hypothesis",
         "kubectl API calls in a script", "Kubernetes operator + OSS API integration"),
        ("L3", "Performance-KPI Deviation Agent", "Detects statistically abnormal KPI drops via time-series models",
         "PM counters → KPI anomaly flag",
         "Prophet (open source) on a CSV export", "Prophet/Nixtla ensemble on streaming telemetry"),
        ("L3", "Historical Ticket Similarity Agent", "RAG search over past incident tickets for proven fixes",
         "Incident description, ticket archive → Similar past ticket + suggested fix",
         "Chroma + Claude embeddings", "pgvector/Weaviate + embeddings pipeline"),
        ("L4", "Blast-Radius Risk Policy Engine", "Determines whether a proposed remediation is high blast-radius",
         "Proposed remediation action → Risk tier",
         "Plain Python rule functions", "Open Policy Agent (OPA)"),
        ("L4", "Change-Management Compliance Engine", "Ensures remediation follows change windows / CAB policy",
         "Proposed action, change calendar → Compliance pass/fail",
         "Python rules checking a calendar file", "Integration with ITSM change-management module"),
        ("L4", "SRE Runbook Rule Engine", "Encodes tacit SRE know-how as executable remediation rules",
         "Fault hypothesis → Candidate remediation playbook",
         "Python if/else rule set", "OPA + versioned runbook store"),
        ("L5", "SRE Approval Gate", "Human checkpoint for medium-confidence or high-blast-radius remediations",
         "Case context, risk score → Approve/reject",
         "Streamlit approval screen", "Retool or ChatOps (Slack approval workflow)"),
        ("L5", "On-Call Escalation Queue", "Catches low-confidence RCA; nothing executes until resolved",
         "Held case + reason → Escalation ticket",
         "Postgres table + manual polling", "PagerDuty/ServiceNow integration"),
        ("L6", "Remediation Success/Failure Monitor", "Watches whether executed remediations actually resolved the fault",
         "Remediation execution, post-action telemetry → Success/failure signal",
         "Scheduled script comparing before/after KPIs", "Streaming anomaly detection service"),
        ("L6", "Alarm Storm Recurrence Detector", "Detects whether the same alarm storm recurs after remediation",
         "Alarm stream → Recurrence alert",
         "Simple count-based script", "Streaming pattern-matching service"),
        ("L6", "Blast-Radius Auditor", "Flags remediations whose real-world impact exceeded predicted scope",
         "Predicted vs. actual blast radius → Audit flag",
         "Manual comparison script", "Automated blast-radius audit service"),
        ("L8", "RCA Accuracy Tracker", "Compares predicted vs. confirmed root cause",
         "RCA hypothesis, confirmed root cause → Accuracy dataset",
         "Scheduled script", "Outcome-tracking pipeline + data warehouse"),
        ("L8", "Remediation Playbook Retraining Trigger", "Fires retraining when RCA accuracy degrades",
         "Accuracy dataset, threshold → Retraining trigger",
         "Cron job", "Prefect/Airflow"),
        ("L8", "Runbook & Policy Memory Updater", "Writes new rules and outcomes back into Policy and Episodic Memory",
         "Retrained output → Updated memory entries",
         "Script rewriting a JSON file", "Versioned policy store + vector DB write client"),
    ],
    "build_order": [
        "**Phase 1 — L1 + L2 + one worker only.** Fake alarm data in Postgres, a Claude API call, and just the "
        "RAN Alarm Correlation Agent producing a hypothesis that gets printed to a log — no orchestrator "
        "fan-out, no remediation yet.",
        "**Phase 2 — build out L3's fan-out.** Add the NOC Incident Orchestrator and the remaining four "
        "worker agents running in parallel, plus Working + Episodic memory (Chroma). This is where the "
        "orchestrator-worker pattern is actually learned — watch for partial-failure handling when one "
        "worker times out.",
        "**Phase 3 — add L4 and the conditional gate.** Wire in the three governance engines, then build the "
        "three-way RCA Confidence & Blast-Radius Gate.",
        "**Phase 4 — complete L5.** Build the SRE approval screen and on-call escalation queue; connect the "
        "Remediation Execution Agent to a sandboxed network config target, never production equipment, until "
        "L6 is in place.",
        "**Phase 5 — add L6 observability before trusting any auto-remediation.** This phase is "
        "non-negotiable before Phase 4's execution agent touches anything real — the Blast-Radius Auditor "
        "specifically exists to catch remediations that did more than intended.",
        "**Phase 6 — add L7 and L8.** Build the MTTR/reliability dashboard and the RCA-accuracy retraining "
        "loop last.",
    ],
}

PILOTS = [CHURN_RETENTION, RCA_REMEDIATION]
