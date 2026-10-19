# Google Cloud to AWS mapping

For teams running both editions, the equivalent services by function.

| Function | Google Cloud edition | AWS edition |
| --- | --- | --- |
| Agent runtime | Vertex AI Agent Engine, ADK | Bedrock AgentCore Runtime, Strands Agents |
| Agent memory | Agent Engine Sessions, Memory Bank | AgentCore Memory |
| Tool access | MCP servers on Cloud Run, Integration Connectors | AgentCore Gateway, Lambda, SSM Automation |
| Tool-call policy | OPA policy engine | AgentCore Policy (Cedar) |
| Frontier models | Gemini on Vertex AI | Amazon Nova, Anthropic Claude and others on Bedrock |
| Self-hosted models | GKE with TPU / GPU, GKE Inference Gateway | EKS with Trainium / Inferentia / GPU, Karpenter |
| Content safety | Model Armor, Sensitive Data Protection | Bedrock Guardrails, Comprehend, Macie |
| Retrieval | Vertex AI Search, RAG Engine, Vector Search | Bedrock Knowledge Bases, OpenSearch Serverless, S3 Vectors |
| Topology graph | Spanner Graph | Neptune Analytics |
| Events and workflows | Pub/Sub, Eventarc, Workflows | EventBridge, SQS, Step Functions |
| Observability | Cloud Trace, Logging, Managed Prometheus, Looker | X-Ray, CloudWatch, Managed Prometheus, Managed Grafana |
| Evaluation | Gen AI Evaluation Service | AgentCore Evaluations, Bedrock evaluation |
| Edge | Cloud Armor, global ALB, IAP | CloudFront, WAF, Shield, ALB, Verified Access |
| API gateway | Apigee X | API Gateway |
| Hybrid links | Dedicated Interconnect, HA VPN, NCC | Direct Connect, Site-to-Site VPN, Transit Gateway / Cloud WAN |
| Firewall and egress | Cloud NGFW, Secure Web Proxy | Network Firewall, egress VPC |
| Private service access | Private Service Connect, VPC-SC | PrivateLink, VPC endpoints, data perimeter SCPs / RCPs |
| Keys | Cloud KMS, Cloud HSM, Cloud EKM | AWS KMS, CloudHSM, external key store |
| Security analytics | Security Command Center, Google SecOps | Security Hub, GuardDuty, Security Lake, Detective |
| Resource hierarchy | Organization, folders, projects, Org Policy | Organizations, OUs, accounts, SCPs, Control Tower |

Service names reflect the AWS catalogue as of mid-2026. Validate Regional availability and quotas for AgentCore components, Bedrock models and Guardrails features during detailed design.

---

[← Risks and decisions](18-risks-and-decisions.md) · [Index](README.md)
