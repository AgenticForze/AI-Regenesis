# Knowledge and memory

| Memory type | Contents | Store |
| --- | --- | --- |
| Working | Task state, scratchpad, tool outputs | AgentCore Memory short-term, ElastiCache |
| Episodic | Past incidents and how they were resolved | AgentCore Memory episodic and long-term strategies |
| Semantic | Runbooks, architecture docs, postmortems | Bedrock Knowledge Bases on OpenSearch Serverless or S3 Vectors, sourced from S3, Confluence, SharePoint |
| Structural | Topology, ownership, dependencies | Neptune Analytics, fed by AWS Config, Resource Explorer, CMDB, service mesh |
| Quantitative | Metrics history, cost, capacity | CloudWatch, Managed Prometheus, Cost and Usage Reports in S3 Tables |
| Procedural | Approved tools and runbooks as code | SSM documents, Git, AgentCore Gateway targets |

Every chunk carries access-control metadata, and Knowledge Base metadata filters restrict retrieval to what the on-behalf-of user is entitled to read.

---

[← Sequence flows](06-sequence-flows.md) · [Index](README.md) · [Observability and telemetry →](08-observability-and-telemetry.md)
