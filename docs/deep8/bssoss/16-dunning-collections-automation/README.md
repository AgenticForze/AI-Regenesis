---
layout: default
title: Collections Risk & Hardship Decisioning — Deep 8-Layer — AI-Regenesis
description: Collections must run at scale while escalating hardship, dispute, or
  high-value cases to a human. The Quick view's own retrospective flags two…
permalink: /deep8/bssoss/16-dunning-collections-automation/
---

# Deep 8-Layer Regenerative Architecture: Collections Risk & Hardship Decisioning

**Domain:** BSS/OSS &nbsp;|&nbsp; **Quick Reference counterpart:** [Dunning & Prepaid/Postpaid Collections Automation]({{ '/bssoss/16-dunning-collections-automation/' | relative_url }}) (Human-in-the-Loop Escalation Chain)

This deep-8 view keeps the Quick view's non-negotiable rule — the risk gate can never be overridden for automated suspension — as an explicit L4 policy rather than an implicit design choice, and adds household-level (not per-line) value assessment as a first-class guardrail.

## 1. Problem Statement & Use Case

Collections must run at scale while escalating hardship, dispute, or high-value cases to a human. The Quick view's own retrospective flags two near-misses: suspending a customer with an active billing dispute, and nearly suspending a high-value multi-line household over one small overdue line.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Hardship/Dispute/High-Value Risk Gate blocks automated restriction for any flagged case by design — this gate has no override path, matching the Quick view's explicit requirement that this be non-negotiable from launch.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (Claude) | Provides LLM Reasoning Core (Claude)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Collections Risk Knowledge Graph | Provides Collections Risk Knowledge Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Payment Reminder Agent | Payment Reminder Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Grace Period & Partial Payment Agent | Grace Period & Partial Payment Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Service Restriction Agent | Service Restriction Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | Contact-Frequency Compliance Policy (Reg F) | Enforces Contact-Frequency Compliance Policy (Reg F) as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Hardship-Indicator Guardrail | Enforces Hardship-Indicator Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Dispute-Hold Rule Engine | Enforces Dispute-Hold Rule Engine as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Collections Specialist | Executes Collections Specialist as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Automated Reminder/Restriction Execution | Executes Automated Reminder/Restriction Execution as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Customer Continuity Adjustment | Executes Customer Continuity Adjustment as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Hardship Program Enrollment Queue | Executes Hardship Program Enrollment Queue as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | Restriction/Complaint Monitor | Continuously monitors for the failure mode Restriction/Complaint Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Contact-Frequency Watchdog | Continuously monitors for the failure mode Contact-Frequency Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Suspension Auditor | Continuously monitors for the failure mode Suspension Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Recovery-Rate Dashboard | Gives leadership real-time visibility via Recovery-Rate Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Complaint-Rate Scorecard | Gives leadership real-time visibility via Complaint-Rate Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Hardship Enrollment View | Gives leadership real-time visibility via Hardship Enrollment View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Risk-Gate Accuracy Tracker | Closes the feedback loop via Risk-Gate Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Escalation-Rule Retraining Trigger | Closes the feedback loop via Escalation-Rule Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake collections data in Postgres, a single Claude API call, and Payment Reminder Agent producing a result that just gets printed. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 2 agents online, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Hardship/Dispute/High-Value Risk Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Collections Specialist approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

> ⚙️ **Built with the AI-Regenesis engine.** This layer breakdown, the blueprint table, and the build order
> were generated from a compact spec by the same engine packaged as the free
> [`deep8-architecture-engine` skill]({{ '/skills/#deep8-architecture-engine' | relative_url }}) — map
> your own use case onto the 8-layer framework the same way.

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
