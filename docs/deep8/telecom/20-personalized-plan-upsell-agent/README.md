---
layout: default
title: Plan Upsell Recommendation Decisioning — Deep 8-Layer — AI-Regenesis
description: Generic upsell campaigns have low conversion and can push customers onto
  poor-fit plans. Fit thresholds were initially expert-guessed and too…
permalink: /deep8/telecom/20-personalized-plan-upsell-agent/
---

# Deep 8-Layer Regenerative Architecture: Plan Upsell Recommendation Decisioning

**Domain:** Telecommunications &nbsp;|&nbsp; **Quick Reference counterpart:** [Personalized Plan Recommendation & Upsell Agent]({{ '/telecom/20-personalized-plan-upsell-agent/' | relative_url }}) (Debate-Critique-Arbiter (Reflective Loop))

This deep-8 view mirrors the Finance domain's Next-Best-Action use case's core discipline — a hard minimum customer-fit threshold the arbiter cannot override for revenue reasons — applied here to telecom plan recommendations instead of financial products.

## 1. Problem Statement & Use Case

Generic upsell campaigns have low conversion and can push customers onto poor-fit plans. Fit thresholds were initially expert-guessed and too conservative, and the arbiter's explanation output turned out valuable enough for call-center agent trust that it should have been a first-class requirement from the start.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Upsell Confidence Gate enforces a minimum customer-fit threshold the arbiter cannot override purely for revenue reasons — the same non-negotiable pattern used in the Finance domain's Next-Best-Action use case, applied here to plan/device recommendations.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (Claude) | Provides LLM Reasoning Core (Claude)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Customer Usage Knowledge Graph | Provides Customer Usage Knowledge Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Recommendation Arbiter Agent | Recommendation Arbiter Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Revenue-Optimized Recommendation Agent | Revenue-Optimized Recommendation Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Customer-Fit Critic Agent | Customer-Fit Critic Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Offer Timing Agent | Offer Timing Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | Minimum-Fit-Threshold Policy (hard veto) | Enforces Minimum-Fit-Threshold Policy (hard veto) as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Downgrade-Justification Guardrail | Enforces Downgrade-Justification Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Offer-Fatigue Rule Engine | Enforces Offer-Fatigue Rule Engine as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Call-Center Agent Panel | Executes Call-Center Agent Panel as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | In-App/SMS Personalized Offer | Executes In-App/SMS Personalized Offer as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Offer Outcome Tracking | Executes Offer Outcome Tracking as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Low-Fit Hold Queue | Executes Low-Fit Hold Queue as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | Fit-Threshold Monitor | Continuously monitors for the failure mode Fit-Threshold Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Offer-Fatigue Watchdog | Continuously monitors for the failure mode Offer-Fatigue Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Outcome Auditor | Continuously monitors for the failure mode Outcome Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Upsell Conversion Dashboard | Gives leadership real-time visibility via Upsell Conversion Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Customer-Fit Scorecard | Gives leadership real-time visibility via Customer-Fit Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Offer-Fatigue View | Gives leadership real-time visibility via Offer-Fatigue View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Recommendation Accuracy Tracker | Closes the feedback loop via Recommendation Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Uplift-Model Retraining Trigger | Closes the feedback loop via Uplift-Model Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake plan upsell recommendation data in Postgres, a single Claude API call, and Revenue-Optimized Recommendation Agent producing a result that just gets printed, with Recommendation Arbiter Agent just passing data through untouched. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 2 agents online and build Recommendation Arbiter Agent's aggregation logic, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Upsell Confidence Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Call-Center Agent Panel approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

> ⚙️ **Built with the AI-Regenesis engine.** This layer breakdown, the blueprint table, and the build order
> were generated from a compact spec by the same engine packaged as the free
> [`deep8-architecture-engine` skill]({{ '/skills/#deep8-architecture-engine' | relative_url }}) — map
> your own use case onto the 8-layer framework the same way.

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
