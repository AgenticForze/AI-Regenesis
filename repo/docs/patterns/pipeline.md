---
layout: default
title: Sequential Pipeline Pattern — AgenticWorks
description: Agents execute in a strict sequential chain, each consuming the previous
  agent's output. Best for workflows with a natural linear order (ingest → analyze…
permalink: /patterns/pipeline/
---

# Pattern: Sequential Pipeline

Agents execute in a strict **sequential chain**, each consuming the previous agent's output. Best for workflows with a natural linear order (ingest → analyze → decide → generate) where later steps are meaningfully dependent on earlier ones and durability/retryability matters more than parallel speed.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [Proactive Capacity Planning & Traffic Forecasting]({{ '/telecom/03-capacity-planning-traffic-forecasting/' | relative_url }}) |
| Telecommunications | [Billing Dispute Investigation & Resolution]({{ '/telecom/10-billing-dispute-resolution/' | relative_url }}) |
| Telecommunications | [Roaming Partner Settlement Reconciliation]({{ '/telecom/13-roaming-settlement-reconciliation/' | relative_url }}) |
| Telecommunications | [Enterprise SLA Compliance Monitoring & Credit Automation]({{ '/telecom/17-enterprise-sla-compliance-monitoring/' | relative_url }}) |
| Financial Services | [Wealth Management: Robo-Advisory Portfolio Rebalancing]({{ '/finance/06-robo-advisory-portfolio-rebalancing/' | relative_url }}) |
| Financial Services | [Financial Planning & Analysis (FP&A) Forecasting]({{ '/finance/10-fpna-forecasting/' | relative_url }}) |
| Financial Services | [Customer Dispute & Chargeback Resolution]({{ '/finance/11-chargeback-dispute-resolution/' | relative_url }}) |
| Financial Services | [ESG Investment Screening & Compliance]({{ '/finance/15-esg-investment-screening/' | relative_url }}) |
| Financial Services | [Trade Settlement Reconciliation]({{ '/finance/19-trade-settlement-reconciliation/' | relative_url }}) |
| BSS/OSS | [Order-to-Activation Orchestration]({{ '/bssoss/01-order-to-activation-orchestration/' | relative_url }}) |
| BSS/OSS | [Mediation & CDR/xDR Processing Pipeline]({{ '/bssoss/06-mediation-cdr-xdr-processing/' | relative_url }}) |
| BSS/OSS | [Number Portability Orchestration]({{ '/bssoss/10-number-portability-orchestration/' | relative_url }}) |
| BSS/OSS | [Digital BSS/OSS Migration & Data Reconciliation]({{ '/bssoss/14-digital-bss-oss-migration-reconciliation/' | relative_url }}) |

---
[← Back to home]({{ '/' | relative_url }})
