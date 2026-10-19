# Roadmap and KPIs

| Phase | Timeline | Scope | Exit criteria |
| --- | --- | --- | --- |
| 0. Foundations | Months 0–3 | Landing zone, VPC-SC, gateway, OTel pipeline, agent lake, triage SLM, knowledge agent | All model traffic via gateway; end-to-end traces live |
| 1. Assist | Months 3–6 | Incident RCA and change risk agents at L0–L1; HITL service; golden eval sets | Diagnosis accepted by SREs in ≥ 70% of P2–P4 |
| 2. Act | Months 6–12 | Top 25 runbooks automated at L2–L3; service request agent; FinOps agent; in-house LLM in production | 30% of P3–P4 resolved without human action |
| 3. Autonomous | Months 12–18 | L4 for proven actions; SecOps agent; cross-domain supervisor; business ops domains onboarded | MTTR down 50%; 60% autonomous resolution of eligible incidents |
| 4. Self-improving | 18 months + | Continuous distillation to SLMs, agents that propose new runbooks and policies for review | Cost per resolved incident down 40% year on year |

---

[← Finops](16-finops.md) · [Index](README.md) · [Risks and decisions →](18-risks-and-decisions.md)
