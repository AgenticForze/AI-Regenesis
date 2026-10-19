# FinOps for intelligence

- **Attribute everything.** Cost-allocation tags and Bedrock application inference profiles per agent and use case, joined with the agent lake in Athena for cost per resolved incident.
- **Push work down the tiers.** Target 70%+ of tokens on SLMs and cache; use Bedrock Model Distillation to move frequent frontier tasks into smaller models.
- **Buy baseline, rent burst.** Provisioned Throughput and Savings Plans for steady load; Spot and Capacity Blocks for training and batch evaluation; Bedrock batch inference at lower cost for offline scoring.
- **Budgets as guardrails.** AWS Budgets actions and Cost Anomaly Detection alerts, plus hard per-agent token caps at the gateway.
- **Context discipline.** Prompt caching, retrieval over stuffing, summarised memory.

---

[← Agentops lifecycle](15-agentops-lifecycle.md) · [Index](README.md) · [Roadmap and kpis →](17-roadmap-and-kpis.md)
