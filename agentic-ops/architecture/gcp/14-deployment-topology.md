# Deployment topology

```mermaid
flowchart TB
ORG["Organization"] --> F1["Folder: agentic-platform"]
ORG --> F2["Folder: shared-services"]
ORG --> F3["Folder: business-units"]
F1 --> P1["prj-agents-prod<br/>Agent Engine, Workflows, HITL"]
F1 --> P2["prj-models-prod<br/>GKE GPU / TPU, Vertex endpoints, gateway"]
F1 --> P3["prj-knowledge-prod<br/>Vertex AI Search, Vector Search, Spanner, AlloyDB"]
F1 --> P4["prj-tools-prod<br/>MCP servers, Integration Connectors"]
F1 --> P5["prj-agents-nonprod<br/>dev, test, eval replay"]
F2 --> S1["prj-network-hub<br/>Shared VPC, Cloud Interconnect, PSC"]
F2 --> S2["prj-observability<br/>metrics scope, BigQuery lake, Looker"]
F2 --> S3["prj-security<br/>KMS, SCC, SecOps, logging sinks"]
F2 --> S4["prj-cicd<br/>Cloud Build, Artifact Registry, Cloud Deploy"]
F3 --> B1["Workload projects<br/>managed estate"]
S1 --- P1
S1 --- P2
S1 --- P4
P4 -. "PSC" .-> B1
S1 -. "Interconnect" .-> ONP["On-prem and other clouds"]
```

*Figure 14. Landing-zone layout. Each platform project sits in its own VPC-SC perimeter with bridge rules only where needed.*

---

[← Security gates](13-security-gates.md) · [Index](README.md) · [Agentops lifecycle →](15-agentops-lifecycle.md)
