# Pattern: Event-Driven Reactive Swarm

Lightweight agents subscribe to a shared **event bus** and react independently and asynchronously to relevant events, publishing their own findings/actions back to the bus. Best for latency-critical, always-on monitoring where centralized orchestration would add unacceptable latency (real-time fraud scoring, self-healing networks).

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [Self-Healing Network (Closed-Loop Automation)](../docs/telecom/04-self-healing-network-closed-loop/README.md) |
| Telecommunications | [Customer Sentiment & Social Listening to Action](../docs/telecom/15-sentiment-social-listening-action/README.md) |
| Financial Services | [Fraud Detection - Card-Not-Present Transactions](../docs/finance/04-card-not-present-fraud-detection/README.md) |
| BSS/OSS | [Order Fallout Detection & Auto-Recovery](../docs/bssoss/04-order-fallout-detection-recovery/README.md) |
| BSS/OSS | [API Gateway & TMF Open API Orchestration Governance](../docs/bssoss/17-api-gateway-tmf-governance/README.md) |

---
[← Back to home](../README.md)
