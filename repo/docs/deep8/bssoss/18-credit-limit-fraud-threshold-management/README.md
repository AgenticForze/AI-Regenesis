---
layout: default
title: Credit & Fraud Threshold Decisioning — Deep 8-Layer — AgenticWorks
description: Dynamic credit limits and fraud thresholds must balance bad-debt exposure
  against not restricting legitimate high-usage customers. Static, per-line…
permalink: /deep8/bssoss/18-credit-limit-fraud-threshold-management/
---

# Deep 8-Layer Regenerative Architecture: Credit & Fraud Threshold Decisioning

**Domain:** BSS/OSS &nbsp;|&nbsp; **Quick Reference counterpart:** [Credit Limit & Fraud Threshold Management (BSS)]({{ '/bssoss/18-credit-limit-fraud-threshold-management/' | relative_url }}) (Debate-Critique-Arbiter (Reflective Loop))

This deep-8 view tracks customer friction (unnecessary restrictions) as a co-equal metric to bad-debt prevention from day one — the Quick view's own retrospective found it over-indexed on risk-prevention in v1, generating avoidable complaints from legitimate roaming customers.

## 1. Problem Statement & Use Case

Dynamic credit limits and fraud thresholds must balance bad-debt exposure against not restricting legitimate high-usage customers. Static, per-line thresholds misread family-plan usage sharing as anomalous, and no proactive warning before restriction meant customers were caught off guard.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Threshold Adjustment Confidence Gate always routes through the proactive spend-cap notification before any restriction — a hard requirement carried over from the Quick view's finding that a warning-then-restrict flow generated far fewer complaints than a hard cutoff.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (Claude) | Provides LLM Reasoning Core (Claude)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Usage-Pattern Knowledge Graph | Provides Usage-Pattern Knowledge Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Threshold Policy Arbiter Agent | Threshold Policy Arbiter Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Threshold Tightening Proposer Agent | Threshold Tightening Proposer Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Legitimate Usage Pattern Critic Agent | Legitimate Usage Pattern Critic Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Bad-Debt Outcome Feedback Agent | Bad-Debt Outcome Feedback Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | Friction-Cost Policy | Enforces Friction-Cost Policy as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Household-Usage Guardrail | Enforces Household-Usage Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Notification Rule Engine | Enforces Notification Rule Engine as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Risk Ops Review | Executes Risk Ops Review as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Dynamic Credit Limit Adjustment | Executes Dynamic Credit Limit Adjustment as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Real-Time Spend Cap Alert | Executes Real-Time Spend Cap Alert as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Threshold Hold Queue | Executes Threshold Hold Queue as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | Bad-Debt Monitor | Continuously monitors for the failure mode Bad-Debt Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Friction-Rate Watchdog | Continuously monitors for the failure mode Friction-Rate Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Adjustment Auditor | Continuously monitors for the failure mode Adjustment Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Bad-Debt-Prevented Dashboard | Gives leadership real-time visibility via Bad-Debt-Prevented Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Customer-Friction Scorecard | Gives leadership real-time visibility via Customer-Friction Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Threshold-by-Segment View | Gives leadership real-time visibility via Threshold-by-Segment View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Threshold Accuracy Tracker | Closes the feedback loop via Threshold Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Risk-Model Retraining Trigger | Closes the feedback loop via Risk-Model Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake credit/fraud thresholds data in Postgres, a single Claude API call, and Threshold Tightening Proposer Agent producing a result that just gets printed, with Threshold Policy Arbiter Agent just passing data through untouched. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 2 agents online and build Threshold Policy Arbiter Agent's aggregation logic, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Threshold Adjustment Confidence Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Risk Ops Review approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
