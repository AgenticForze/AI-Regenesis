# Pattern: Debate-Critique-Arbiter (Reflective Loop)

A **proposer agent** generates a hypothesis or recommendation; an independently-primed **critic agent** adversarially searches for what the proposer missed or got wrong; an **arbiter agent** weighs both into a final, better-calibrated decision. Best for high-stakes classification/judgment tasks (fraud, surveillance, recommendations) where single-pass LLM reasoning is prone to confirmation bias.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [SIM-Swap & Account-Takeover Fraud Detection](../docs/telecom/07-sim-swap-fraud-detection/README.md) |
| Telecommunications | [Personalized Plan Recommendation & Upsell Agent](../docs/telecom/20-personalized-plan-upsell-agent/README.md) |
| Financial Services | [Contract & Loan Document Review (Legal/Credit Agent)](../docs/finance/09-contract-loan-document-review/README.md) |
| Financial Services | [Insider Trading & Market Abuse Surveillance](../docs/finance/17-insider-trading-surveillance/README.md) |
| Financial Services | [Personalized Financial Advisory & Next-Best-Action](../docs/finance/20-personalized-financial-advisory-nba/README.md) |
| BSS/OSS | [Charging & Rating Engine Anomaly Detection](../docs/bssoss/07-charging-rating-anomaly-detection/README.md) |
| BSS/OSS | [Promotions & Campaign Configuration Engine](../docs/bssoss/15-promotions-campaign-configuration-engine/README.md) |
| BSS/OSS | [Credit Limit & Fraud Threshold Management (BSS)](../docs/bssoss/18-credit-limit-fraud-threshold-management/README.md) |

---
[← Back to home](../README.md)
