---
layout: default
title: Blackboard / Shared-Memory Pattern — AI-Regenesis
description: Multiple specialist agents read and write to a shared blackboard (memory
  store), while a controller agent decides which agent to trigger next and…
permalink: /patterns/blackboard/
---

# Pattern: Blackboard / Shared-Memory

Multiple specialist agents read and write to a **shared blackboard (memory store)**, while a **controller agent** decides which agent to trigger next and synthesizes posted findings. Best for problems where partial, heterogeneous evidence accumulates over time and no single agent has the full picture (fleet health, firm-wide risk).

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [IoT Device Fleet Anomaly Detection & Remediation]({{ '/telecom/14-iot-fleet-anomaly-detection/' | relative_url }}) |
| Financial Services | [Market Risk Management / VaR Monitoring]({{ '/finance/12-market-risk-var-monitoring/' | relative_url }}) |
| BSS/OSS | [Revenue Assurance & Leakage Detection]({{ '/bssoss/03-revenue-assurance-leakage-detection/' | relative_url }}) |
| BSS/OSS | [Customer 360 / Master Data Unification]({{ '/bssoss/08-customer-360-master-data-unification/' | relative_url }}) |

---
[← Back to home]({{ '/' | relative_url }})
