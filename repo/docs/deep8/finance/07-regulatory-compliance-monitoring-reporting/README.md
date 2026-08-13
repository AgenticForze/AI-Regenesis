---
layout: default
title: Regulatory Filing Readiness Decisioning — Deep 8-Layer — AgenticWorks
description: Banks must continuously monitor a patchwork of regulations and file numerous
  recurring reports. Data reconciliation exceptions, not report generation…
permalink: /deep8/finance/07-regulatory-compliance-monitoring-reporting/
---

# Deep 8-Layer Regenerative Architecture: Regulatory Filing Readiness Decisioning

**Domain:** Financial Services &nbsp;|&nbsp; **Quick Reference counterpart:** [Regulatory Compliance Monitoring & Reg Reporting]({{ '/finance/07-regulatory-compliance-monitoring-reporting/' | relative_url }}) (Hierarchical Multi-Agent (Manager-of-Managers))

This deep-8 view treats regulatory-change monitoring as a first-class L6 component from day one — the Quick view found new rule versions silently broke report templates before this monitoring existed.

## 1. Problem Statement & Use Case

Banks must continuously monitor a patchwork of regulations and file numerous recurring reports. Data reconciliation exceptions, not report generation itself, were the dominant cause of filing delays in the Quick view's own experience — and undetected regulatory-text changes silently broke report templates before change monitoring was added.

## 2. The 8-Layer Blueprint

<img src="blueprint.svg" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="diagram.svg" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** The Filing Readiness Confidence Gate keeps all financial calculations in deterministic, auditable engines — the LLM layer is used only for regulatory-text interpretation and change-impact summaries, never for the final numbers, matching the Quick view's explicit design principle.

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
| L2 | AI Gateway | Provides AI Gateway's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | LLM Reasoning Core (Claude) | Provides LLM Reasoning Core (Claude)'s reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L2 | Regulatory Requirement Knowledge Graph | Provides Regulatory Requirement Knowledge Graph's reasoning/knowledge capability to the Agentic Core. | Agent requests → Model responses, usage telemetry | Claude API called directly | LiteLLM / Portkey model-routing gateway with cost tracking |
| L3 | Regulatory Compliance Orchestrator | Regulatory Compliance Orchestrator — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Capital/Liquidity Reporting Manager Agent | Capital/Liquidity Reporting Manager Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Trade/Transaction Reporting Manager Agent | Trade/Transaction Reporting Manager Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L3 | Data Reconciliation Agent | Data Reconciliation Agent — specialist agent in the Agentic Core's reasoning chain. | Task context, Working Memory → Reasoning output, next-step decision | LangGraph agent node + Claude API | LangGraph on Temporal for durable, at-scale execution |
| L4 | Filing-Deadline Policy | Enforces Filing-Deadline Policy as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Calculation-Accuracy Guardrail | Enforces Calculation-Accuracy Guardrail as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L4 | Regulatory Change-Impact Rule Engine | Enforces Regulatory Change-Impact Rule Engine as a governance gate before any action reaches the Action Layer. | Proposed action, policy rules → Pass/fail decision | Plain Python rule functions | Open Policy Agent (OPA) rules engine |
| L5 | Compliance Officer Review | Executes Compliance Officer Review as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Regulatory Report Submission | Executes Regulatory Report Submission as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Internal Compliance Dashboard | Executes Internal Compliance Dashboard as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L5 | Reconciliation Exception Hold | Executes Reconciliation Exception Hold as part of the Action & Execution layer once a decision is approved. | Approved decision → Executed action, system update | Mock REST endpoint (FastAPI) | Real system API behind a common tool-calling interface |
| L6 | Filing Deadline Monitor | Continuously monitors for the failure mode Filing Deadline Monitor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Reconciliation Exception Watchdog | Continuously monitors for the failure mode Reconciliation Exception Watchdog is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L6 | Submission Auditor | Continuously monitors for the failure mode Submission Auditor is named to catch. | Live execution/outcome telemetry → Alert, health score | Scheduled Python script / simple threshold check | Statistical drift/anomaly detection service (e.g., Evidently AI) |
| L7 | Regulatory Calendar Dashboard | Gives leadership real-time visibility via Regulatory Calendar Dashboard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Filing Accuracy Scorecard | Gives leadership real-time visibility via Filing Accuracy Scorecard. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L7 | Cross-Jurisdiction View | Gives leadership real-time visibility via Cross-Jurisdiction View. | Outcome + financial data → Executive-facing metric | Streamlit or Metabase dashboard | BI dashboard (Looker/Tableau) wired to a data warehouse |
| L8 | Filing Accuracy Tracker | Closes the feedback loop via Filing Accuracy Tracker, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Rule-Change Retraining Trigger | Closes the feedback loop via Rule-Change Retraining Trigger, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |
| L8 | Policy Memory Updater | Closes the feedback loop via Policy Memory Updater, feeding outcomes back into memory. | Outcome-accuracy data, thresholds → Retraining trigger / updated memory | Cron job checking a threshold | Prefect/Airflow orchestrating scheduled retraining jobs |

## 5. Suggested Build Order (by Layer)

**Phase 1 — L1 + L2 + a stub L5, nothing else.** Fake regulatory reporting data in Postgres, a single Claude API call, and Data Reconciliation Agent producing a result that just gets printed, with Regulatory Compliance Orchestrator just passing data through untouched. No memory, no governance, no conditional routing yet.

**Phase 2 — build out L3, the Agentic Core.** Bring the remaining 2 agents online and build Regulatory Compliance Orchestrator's aggregation logic, and add Working + Episodic memory (Chroma). This is where the pattern is actually learned, not before.

**Phase 3 — add L4 and the conditional gate.** Wire in the governance engines as hard gates, then build the three-way Filing Readiness Confidence Gate routing into auto-execute / human review / hold.

**Phase 4 — complete L5.** Build the Compliance Officer Review approval screen and the hold/escalate queue; this is the first point where a human is actually in the loop.

**Phase 5 — add L6 observability.** Drop in a drift/anomaly detection service and a data-quality check. This is usually the point where problems invisible in Phases 1–4 surface for the first time.

**Phase 6 — add L7 and L8.** Build the executive dashboard last, and the scheduled retraining/memory-update job. These teach the least new technical ground but close the loop the manuscript calls "regenerative."

---
[← Back to Deep 8-Layer index]({{ '/deep8/' | relative_url }}) &nbsp;|&nbsp; [← Back to home]({{ '/' | relative_url }})
