---
layout: default
title: Catalog-to-Network Mapping Decisioning — Deep 8-Layer — AI-Regenesis
description: Translating a commercial catalog entry into the correct OSS API call
  sequence requires deep, often tribal-knowledge mapping logic that breaks whenever
  the…
permalink: /deep8/bssoss/12-service-catalog-network-activation-mapping/
---

# Deep 8-Layer Regenerative Architecture: Catalog-to-Network Mapping Decisioning

**Domain:** BSS/OSS &nbsp;|&nbsp; **Quick Reference counterpart:** [Service Catalog-to-Network Activation Mapping (TMF Open APIs)]({{ '/bssoss/12-service-catalog-network-activation-mapping/' | relative_url }}) (Hierarchical Multi-Agent (Manager-of-Managers))

This deep-8 view elevates API contract drift detection — the Quick view's highest-value addition found in hindsight — to a first-class, always-on L6 component rather than something built after production mapping failures had already occurred.

## 1. Problem Statement & Use Case

Translating a commercial catalog entry into the correct OSS API call sequence requires deep, often tribal-knowledge mapping logic that breaks whenever the catalog or an underlying vendor API changes. Undetected vendor API changes were, by the Quick view's own account, the dominant cause of production mapping failures.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Mapping Confidence & Drift Gate routes stable, previously-validated mappings to auto-execution, and anything touching a recently-changed API contract to engineer review before it can reach production.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (Claude) | Provides LLM Reasoning Core (Claude)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Catalog-to-Network Mapping Graph | Provides Catalog-to-Network Mapping Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Catalog-to-Network Mapping Orchestrator | Catalog-to-Network Mapping Orchestrator — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Access Network Domain Mapping Agent | Access Network Domain Mapping Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Core Network Domain Mapping Agent | Core Network Domain Mapping Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Mapping Validation Agent | Mapping Validation Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | API Contract Compatibility Policy | Enforces API Contract Compatibility Policy as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Engineer Review Guardrail | Enforces Engineer Review Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Mapping Change Authorization Rules | Enforces Mapping Change Authorization Rules as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Engineer Review | Executes Engineer Review as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | TMF641 Service Order Execution | Executes TMF641 Service Order Execution as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Regression Test Suite Run | Executes Regression Test Suite Run as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Mapping Change Hold Queue | Executes Mapping Change Hold Queue as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | API Contract Drift Monitor | Continuously monitors for the failure mode API Contract Drift Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Mapping Success Watchdog | Continuously monitors for the failure mode Mapping Success Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Change Auditor | Continuously monitors for the failure mode Change Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Mapping Success-Rate Dashboard | Gives leadership real-time visibility via Mapping Success-Rate Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Domain Coverage Scorecard | Gives leadership real-time visibility via Domain Coverage Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Drift Incident View | Gives leadership real-time visibility via Drift Incident View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Mapping Accuracy Tracker | Closes the feedback loop via Mapping Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Mapping-Rule Retraining Trigger | Closes the feedback loop via Mapping-Rule Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake catalog-to-network mapping data in Postgres, a single Claude API call, and Access Network Domain Mapping Agent producing a result that just gets printed, with Catalog-to-Network Mapping Orchestrator just passing data through untouched. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 2 agents online and build Catalog-to-Network Mapping Orchestrator's aggregation logic, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Mapping Confidence & Drift Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Engineer Review approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

> ⚙️ **Built with the AI-Regenesis engine.** This layer breakdown, the blueprint table, and the build order
> were generated from a compact spec by the same engine packaged as the free
> [`deep8-architecture-engine` skill]({{ '/skills/#deep8-architecture-engine' | relative_url }}) — map
> your own use case onto the 8-layer framework the same way.

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
