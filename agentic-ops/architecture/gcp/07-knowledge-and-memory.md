# Knowledge and memory

Operations reasoning fails without accurate context. We separate memory by lifetime and by shape, and keep a single source of truth for each.

| Memory type | Contents | Store | Freshness |
| --- | --- | --- | --- |
| Working | Current task state, scratchpad, tool outputs | Agent Engine Sessions, Memorystore | Seconds; TTL per task |
| Episodic | What happened in past incidents and how they were resolved | Agent Engine Memory Bank, BigQuery | Written at task close |
| Semantic | Runbooks, architecture docs, postmortems, vendor docs | Vertex AI Search, RAG Engine over GCS, Drive, Confluence | Incremental re-index hourly |
| Structural | Service topology, ownership, dependencies, config items | Spanner Graph (fed from Cloud Asset Inventory, CMDB, service mesh) | Streaming via Pub/Sub |
| Quantitative | Metrics history, cost, capacity, SLOs | BigQuery, Managed Prometheus | Near real time |
| Procedural | Approved tool definitions and runbook-as-code | Git plus MCP server registry | Released via CI/CD |

Retrieval uses hybrid search (keyword plus vector) with re-ranking, and every chunk carries access-control metadata so that agents acting for a user only retrieve what that user is entitled to see.

---

[← Sequence flows](06-sequence-flows.md) · [Index](README.md) · [Observability and telemetry →](08-observability-and-telemetry.md)
