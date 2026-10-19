# Risks and key decisions

| Decision or risk | Position | Rationale |
| --- | --- | --- |
| AgentCore Runtime vs self-hosted agents on EKS | AgentCore by default; EKS for unusual networking or throughput | Framework-agnostic runtime keeps the choice reversible |
| Bedrock Custom Model Import vs EKS for in-house LLMs | Custom Model Import where architecture is supported and data class allows; EKS in the enclave for regulated data | Serverless hosting lowers operational load; EKS gives full control |
| Feature availability by Region | Validate AgentCore, Guardrails and model availability per Region | Some AgentCore features roll out to Regions at different times |
| Over-automation | Autonomy earned per action type | Shadow mode via Policy log-only, kill switch, automatic demotion |
| Running on two clouds | One architecture, two editions, shared protocols | MCP, A2A, OTel and Cedar/OPA policies-as-code keep agents portable |

---

[← Roadmap and kpis](17-roadmap-and-kpis.md) · [Index](README.md) · [Gcp to aws mapping →](19-gcp-to-aws-mapping.md)
