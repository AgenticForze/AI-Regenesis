---
layout: default
title: Card-Not-Present Authorization Decisioning — Deep 8-Layer — AgenticWorks
description: Card-not-present fraud decisions must resolve in under 100ms. An early
  experiment routing borderline cases through an LLM blew the latency SLA;…
permalink: /deep8/finance/04-card-not-present-fraud-detection/
---

# Deep 8-Layer Regenerative Architecture: Card-Not-Present Authorization Decisioning

**Domain:** Financial Services &nbsp;|&nbsp; **Quick Reference counterpart:** [Fraud Detection - Card-Not-Present Transactions]({{ '/finance/04-card-not-present-fraud-detection/' | relative_url }}) (Event-Driven Reactive Swarm)

This deep-8 view keeps the Quick view's core discipline — the hot authorization path never calls an LLM, full stop — and tracks declined-legitimate-transaction cost as a co-equal metric to fraud caught, per the Quick view's own retrospective.

## 1. Problem Statement & Use Case

Card-not-present fraud decisions must resolve in under 100ms. An early experiment routing borderline cases through an LLM blew the latency SLA; separately, the system initially over-indexed on fraud recall without tracking the business cost of declining legitimate transactions.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Authorization Confidence Gate operates entirely within the real-time scoring path — L2's LLM Reasoning Core is explicitly offline-only, used for post-decision case investigation, never in the authorization hot path itself.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (offline case investigation only) | Provides LLM Reasoning Core (offline case investigation only)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Fraud Pattern Knowledge Graph | Provides Fraud Pattern Knowledge Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Real-Time Scoring Aggregator | Real-Time Scoring Aggregator — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Device Fingerprint Agent | Device Fingerprint Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Velocity/Behavioral Agent | Velocity/Behavioral Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Merchant Risk Agent | Merchant Risk Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Geolocation Consistency Agent | Geolocation Consistency Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | Decline-Rate Business-Impact Policy | Enforces Decline-Rate Business-Impact Policy as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | False-Positive Guardrail | Enforces False-Positive Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | 3DS Step-Up Rule Engine | Enforces 3DS Step-Up Rule Engine as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Fraud Case Investigator | Executes Fraud Case Investigator as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Approve/Decline Authorization Response | Executes Approve/Decline Authorization Response as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | 3DS Challenge Trigger | Executes 3DS Challenge Trigger as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Fraud Case Creation Queue | Executes Fraud Case Creation Queue as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | False-Positive/Negative Monitor | Continuously monitors for the failure mode False-Positive/Negative Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Decline-Rate Watchdog | Continuously monitors for the failure mode Decline-Rate Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Scoring Auditor | Continuously monitors for the failure mode Scoring Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Fraud-Caught Dashboard | Gives leadership real-time visibility via Fraud-Caught Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Decline-Rate Business-Impact Scorecard | Gives leadership real-time visibility via Decline-Rate Business-Impact Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Merchant Risk View | Gives leadership real-time visibility via Merchant Risk View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Scoring Accuracy Tracker | Closes the feedback loop via Scoring Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Aggregator-Weight Retraining Trigger | Closes the feedback loop via Aggregator-Weight Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake card-not-present fraud data in Postgres, a single Claude API call, and Device Fingerprint Agent producing a result that just gets printed, with Real-Time Scoring Aggregator just passing data through untouched. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 3 agents online and build Real-Time Scoring Aggregator's aggregation logic, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Authorization Confidence Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Fraud Case Investigator approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
