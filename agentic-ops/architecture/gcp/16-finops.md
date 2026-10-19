# FinOps for intelligence

- **Attribute everything.** Labels on every model call (agent, use case, cost centre) flow into BigQuery billing export joined with the agent lake, giving cost per resolved incident and per business outcome.
- **Push work down the tiers.** Target 70%+ of tokens on SLMs and cache; review the tier mix monthly and distil frequent Gemini tasks into SLMs.
- **Buy baseline, rent burst.** Provisioned Throughput and committed-use discounts for GPUs/TPUs cover steady load; spot and DWS flex-start for training and batch evaluation.
- **Budgets as guardrails.** Per-agent daily token budgets enforced at the gateway, with Cloud Billing budgets and Pub/Sub alerts on anomalies.
- **Context discipline.** Context caching for large stable prompts, retrieval over stuffing, and summarised memory rather than raw history.

---

[← Agentops lifecycle](15-agentops-lifecycle.md) · [Index](README.md) · [Roadmap and kpis →](17-roadmap-and-kpis.md)
