---
layout: default
title: Debate-Critique-Arbiter (Reflective Loop) Pattern — AgenticWorks
description: A proposer agent generates a hypothesis or recommendation; an independently-primed
  critic agent adversarially searches for what the proposer missed or got…
permalink: /patterns/debate-critique/
---

# Pattern: Debate-Critique-Arbiter (Reflective Loop)

A **proposer agent** generates a hypothesis or recommendation; an independently-primed **critic agent** adversarially searches for what the proposer missed or got wrong; an **arbiter agent** weighs both into a final, better-calibrated decision. Best for high-stakes classification/judgment tasks (fraud, surveillance, recommendations) where single-pass LLM reasoning is prone to confirmation bias.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [SIM-Swap & Account-Takeover Fraud Detection]({{ '/telecom/07-sim-swap-fraud-detection/' | relative_url }}) |
| Telecommunications | [Personalized Plan Recommendation & Upsell Agent]({{ '/telecom/20-personalized-plan-upsell-agent/' | relative_url }}) |
| Financial Services | [Contract & Loan Document Review (Legal/Credit Agent)]({{ '/finance/09-contract-loan-document-review/' | relative_url }}) |
| Financial Services | [Insider Trading & Market Abuse Surveillance]({{ '/finance/17-insider-trading-surveillance/' | relative_url }}) |
| Financial Services | [Personalized Financial Advisory & Next-Best-Action]({{ '/finance/20-personalized-financial-advisory-nba/' | relative_url }}) |
| BSS/OSS | [Charging & Rating Engine Anomaly Detection]({{ '/bssoss/07-charging-rating-anomaly-detection/' | relative_url }}) |
| BSS/OSS | [Promotions & Campaign Configuration Engine]({{ '/bssoss/15-promotions-campaign-configuration-engine/' | relative_url }}) |
| BSS/OSS | [Credit Limit & Fraud Threshold Management (BSS)]({{ '/bssoss/18-credit-limit-fraud-threshold-management/' | relative_url }}) |

---
[← Back to home]({{ '/' | relative_url }})
