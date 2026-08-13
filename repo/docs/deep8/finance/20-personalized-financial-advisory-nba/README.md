---
layout: default
title: Next-Best-Action Recommendation Decisioning — Deep 8-Layer — AgenticWorks
description: Proactive financial recommendations must balance business value against
  genuine customer benefit. Without outcome tracking, there's no way to prove the…
permalink: /deep8/finance/20-personalized-financial-advisory-nba/
---

# Deep 8-Layer Regenerative Architecture: Next-Best-Action Recommendation Decisioning

**Domain:** Financial Services &nbsp;|&nbsp; **Quick Reference counterpart:** [Personalized Financial Advisory & Next-Best-Action]({{ '/finance/20-personalized-financial-advisory-nba/' | relative_url }}) (Debate-Critique-Arbiter (Reflective Loop))

This deep-8 view makes the minimum customer-wellbeing-benefit threshold a hard L4 policy the arbiter cannot override for revenue reasons — the direct lesson carried over from watching purely revenue-optimized recommenders erode long-term customer trust.

## 1. Problem Statement & Use Case

Proactive financial recommendations must balance business value against genuine customer benefit. Without outcome tracking, there's no way to prove the wellbeing critic actually improves customer outcomes rather than just suppressing profitable offers, and life-event detection needs careful pacing to avoid feeling surveillance-like.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Recommendation Confidence Gate enforces a hard minimum wellbeing-benefit threshold in L4 that the arbiter cannot override for revenue reasons — this is the single non-negotiable rule carried directly from the retrospective's core lesson.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (Claude) | Provides LLM Reasoning Core (Claude)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Household Financial Knowledge Graph | Provides Household Financial Knowledge Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Next-Best-Action Arbiter Agent | Next-Best-Action Arbiter Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Revenue-Optimized Product Recommendation Agent | Revenue-Optimized Product Recommendation Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Customer Financial Wellbeing Critic Agent | Customer Financial Wellbeing Critic Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Life-Event Detection Agent | Life-Event Detection Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | Minimum-Wellbeing-Benefit Policy (hard veto) | Enforces Minimum-Wellbeing-Benefit Policy (hard veto) as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Suitability-Documentation Guardrail | Enforces Suitability-Documentation Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Advisor-Escalation Rule Engine | Enforces Advisor-Escalation Rule Engine as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Advisor Outreach | Executes Advisor Outreach as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | In-App Personalized Recommendation | Executes In-App Personalized Recommendation as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Recommendation Outcome Tracking | Executes Recommendation Outcome Tracking as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Complex-Case Hold Queue | Executes Complex-Case Hold Queue as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | Wellbeing-Benefit Monitor | Continuously monitors for the failure mode Wellbeing-Benefit Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Recommendation-Trust Watchdog | Continuously monitors for the failure mode Recommendation-Trust Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Outcome Auditor | Continuously monitors for the failure mode Outcome Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Customer Financial Outcomes Dashboard | Gives leadership real-time visibility via Customer Financial Outcomes Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Revenue-vs-Wellbeing Scorecard | Gives leadership real-time visibility via Revenue-vs-Wellbeing Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Life-Event Response View | Gives leadership real-time visibility via Life-Event Response View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Recommendation Accuracy Tracker | Closes the feedback loop via Recommendation Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Uplift-Model Retraining Trigger | Closes the feedback loop via Uplift-Model Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake personalized advisory data in Postgres, a single Claude API call, and Revenue-Optimized Product Recommendation Agent producing a result that just gets printed, with Next-Best-Action Arbiter Agent just passing data through untouched. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 2 agents online and build Next-Best-Action Arbiter Agent's aggregation logic, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Recommendation Confidence Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Advisor Outreach approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
