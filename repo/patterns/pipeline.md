# Pattern: Sequential Pipeline

Agents execute in a strict **sequential chain**, each consuming the previous agent's output. Best for workflows with a natural linear order (ingest → analyze → decide → generate) where later steps are meaningfully dependent on earlier ones and durability/retryability matters more than parallel speed.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [Proactive Capacity Planning & Traffic Forecasting](../docs/telecom/03-capacity-planning-traffic-forecasting/README.md) |
| Telecommunications | [Billing Dispute Investigation & Resolution](../docs/telecom/10-billing-dispute-resolution/README.md) |
| Telecommunications | [Roaming Partner Settlement Reconciliation](../docs/telecom/13-roaming-settlement-reconciliation/README.md) |
| Telecommunications | [Enterprise SLA Compliance Monitoring & Credit Automation](../docs/telecom/17-enterprise-sla-compliance-monitoring/README.md) |
| Financial Services | [Wealth Management: Robo-Advisory Portfolio Rebalancing](../docs/finance/06-robo-advisory-portfolio-rebalancing/README.md) |
| Financial Services | [Financial Planning & Analysis (FP&A) Forecasting](../docs/finance/10-fpna-forecasting/README.md) |
| Financial Services | [Customer Dispute & Chargeback Resolution](../docs/finance/11-chargeback-dispute-resolution/README.md) |
| Financial Services | [ESG Investment Screening & Compliance](../docs/finance/15-esg-investment-screening/README.md) |
| Financial Services | [Trade Settlement Reconciliation](../docs/finance/19-trade-settlement-reconciliation/README.md) |
| BSS/OSS | [Order-to-Activation Orchestration](../docs/bssoss/01-order-to-activation-orchestration/README.md) |
| BSS/OSS | [Mediation & CDR/xDR Processing Pipeline](../docs/bssoss/06-mediation-cdr-xdr-processing/README.md) |
| BSS/OSS | [Number Portability Orchestration](../docs/bssoss/10-number-portability-orchestration/README.md) |
| BSS/OSS | [Digital BSS/OSS Migration & Data Reconciliation](../docs/bssoss/14-digital-bss-oss-migration-reconciliation/README.md) |

---
[← Back to home](../README.md)
