# Pattern: Blackboard / Shared-Memory

Multiple specialist agents read and write to a **shared blackboard (memory store)**, while a **controller agent** decides which agent to trigger next and synthesizes posted findings. Best for problems where partial, heterogeneous evidence accumulates over time and no single agent has the full picture (fleet health, firm-wide risk).

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [IoT Device Fleet Anomaly Detection & Remediation](../docs/telecom/14-iot-fleet-anomaly-detection/README.md) |
| Financial Services | [Market Risk Management / VaR Monitoring](../docs/finance/12-market-risk-var-monitoring/README.md) |
| BSS/OSS | [Revenue Assurance & Leakage Detection](../docs/bssoss/03-revenue-assurance-leakage-detection/README.md) |
| BSS/OSS | [Customer 360 / Master Data Unification](../docs/bssoss/08-customer-360-master-data-unification/README.md) |

---
[← Back to home](../README.md)
