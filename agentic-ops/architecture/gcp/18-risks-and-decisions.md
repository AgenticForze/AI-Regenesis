# Risks and key decisions

| Decision or risk | Position | Mitigation or rationale |
| --- | --- | --- |
| Agent runtime: Agent Engine vs self-hosted on GKE | Agent Engine by default; GKE for agents needing custom networking or extreme throughput | ADK runs on both, so the choice is reversible per agent |
| Build in-house LLMs | Fine-tune open weights, do not pre-train | Restricted data and cost at scale justify it; pre-training does not |
| Vendor concentration on Google Cloud | Accept, with open protocols at the seams | MCP, A2A, OTel, OCI and Terraform keep migration feasible |
| Over-automation causing outages | Autonomy earned per action type | Shadow mode, blast-radius limits, kill switch, automatic demotion |
| Model drift and silent quality decay | Continuous online evaluation | Quality SLOs page owners; version pinning in router |
| Skills and operating model | Create an AgentOps platform team and agent product owners per domain | SRE roles shift toward policy authoring, eval design and exception handling |
| Regulatory exposure (EU AI Act, sector rules) | Classify each agent's risk level at design time | Audit trail, human oversight, documentation generated from agent specs |

Service names reflect the Google Cloud catalogue as of mid-2026. Validate current GA status, regional availability and quotas for Agent Engine features, Memory Bank, GKE Inference Gateway and specific Gemini versions during detailed design.

---

[← Roadmap and kpis](17-roadmap-and-kpis.md) · [Index](README.md)
