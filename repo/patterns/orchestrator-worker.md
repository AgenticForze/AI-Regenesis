# Pattern: Orchestrator-Worker (Supervisor fan-out/fan-in)

A central **orchestrator (supervisor) agent** decomposes an incoming task, fans it out to specialized **worker agents** running in parallel, then aggregates their outputs into a single decision or artifact. Best for tasks that decompose cleanly into independent sub-investigations (fraud checks, alarm correlation, onboarding checks) that must complete within a bounded time budget.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [Multi-Agent Network Fault RCA & Auto-Remediation](../docs/telecom/01-network-fault-rca-remediation/README.md) |
| Telecommunications | [Customer Churn Prediction & Win-Back Orchestration](../docs/telecom/05-churn-prediction-winback/README.md) |
| Telecommunications | [Telecom SOC Threat Hunting & Incident Response](../docs/telecom/08-telecom-soc-threat-hunting/README.md) |
| Telecommunications | [New Line/Device Onboarding & KYC Automation](../docs/telecom/11-line-onboarding-kyc-automation/README.md) |
| Telecommunications | [Spectrum Interference Detection & Mitigation](../docs/telecom/16-spectrum-interference-detection/README.md) |
| Telecommunications | [Predictive Maintenance for Network Hardware](../docs/telecom/19-predictive-maintenance-network-hardware/README.md) |
| Financial Services | [AML Transaction Monitoring & SAR Filing](../docs/finance/01-aml-transaction-monitoring-sar/README.md) |
| Financial Services | [Customer Onboarding & KYC (Retail & Business Banking)](../docs/finance/05-customer-onboarding-kyc-finance/README.md) |
| Financial Services | [Insurance Claims Processing & Fraud Detection](../docs/finance/08-insurance-claims-processing-fraud/README.md) |
| Financial Services | [Collections & Delinquency Management](../docs/finance/13-collections-delinquency-management/README.md) |
| Financial Services | [Treasury Cash Management & Liquidity Forecasting](../docs/finance/16-treasury-cash-liquidity-forecasting/README.md) |
| BSS/OSS | [Network Inventory Discovery & Reconciliation](../docs/bssoss/05-network-inventory-discovery-reconciliation/README.md) |
| BSS/OSS | [Wholesale/Partner Interconnect Onboarding](../docs/bssoss/11-wholesale-partner-interconnect-onboarding/README.md) |
| BSS/OSS | [Trouble Ticket Management & Cross-Domain Assurance (OSS)](../docs/bssoss/13-trouble-ticket-cross-domain-assurance/README.md) |
| BSS/OSS | [Legacy System Decommissioning & Data Archival](../docs/bssoss/20-legacy-system-decommissioning-archival/README.md) |

---
[← Back to home](../README.md)
