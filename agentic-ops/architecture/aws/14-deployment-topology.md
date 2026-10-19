# Account topology

```mermaid
flowchart TB
ORG["AWS Organizations<br/>Control Tower"] --> SEC["Security OU"]
ORG --> INF["Infrastructure OU"]
ORG --> PLT["Agentic Platform OU"]
ORG --> WKL["Workloads OU"]
SEC --> A1["Log Archive<br/>CloudTrail, Config, Object Lock"]
SEC --> A2["Security Tooling<br/>GuardDuty, Security Hub, Security Lake admin"]
INF --> A3["Network<br/>TGW, DX, Firewall, IPAM"]
INF --> A4["Shared Services<br/>CI/CD, ECR, Identity Center delegated admin"]
PLT --> A5["platform-prod<br/>AgentCore, gateway, tools, knowledge"]
PLT --> A6["models-prod<br/>EKS inference, SageMaker"]
PLT --> A7["enclave-prod<br/>restricted OU, in-house LLM"]
PLT --> A8["platform-nonprod<br/>dev, test, eval replay"]
WKL --> A9["Business unit accounts"]
A3 --- A5
A3 --- A6
A5 -. "PrivateLink" .-> A7
A5 -. "cross-account executor roles" .-> A9
```

*Figure 14. Multi-account layout. SCPs and RCPs at OU level enforce region restrictions, deny public resources, and block agent roles from IAM and organisation changes.*

---

[← Security gates](13-security-gates.md) · [Index](README.md) · [Agentops lifecycle →](15-agentops-lifecycle.md)
