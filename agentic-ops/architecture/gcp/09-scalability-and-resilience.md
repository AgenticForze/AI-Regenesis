# Scalability and resilience

### Inference scaling

- GKE with GPU and TPU node pools; Horizontal Pod Autoscaler on queue depth and KV-cache utilisation, not CPU
- GKE Inference Gateway for model-aware load balancing and LoRA adapter routing on shared base models
- Custom compute classes with fallback between accelerator types; DWS flex-start for batch fine-tuning
- SLMs on Cloud Run GPU scale to zero outside business hours
- Gemini Provisioned Throughput sized to p70 load; pay-as-you-go absorbs burst

### Orchestration scaling

- Agent Engine scales agent runtimes horizontally; agents are stateless between steps with state in Sessions
- Pub/Sub decouples ingestion from reasoning; ordering keys per incident preserve sequence
- Cloud Tasks for rate-limited tool calls to fragile downstream systems
- Workflows for long-running, durable plans that survive restarts
- Priority lanes: P1 events bypass batch queues and reserve capacity

### Failure handling

- Idempotency keys on every mutating tool call; exactly-once side-effect ledger in Spanner
- Circuit breakers per model and per tool; graceful degradation to L1 recommend-only mode
- Loop guards: maximum steps, tokens and wall-clock per episode
- Global kill switch per agent and per action type, propagated in < 10 s
- Dead-letter topics with automated replay after fixes

### Multi-region and DR

- Active-active in two regions for gateway, orchestration and tools behind global load balancing
- Spanner multi-region for side-effect ledger and graph; BigQuery multi-region for the lake
- Vertex AI endpoints in both regions; in-house LLM warm standby
- RPO ≈ 0 for approvals and actions, RTO < 15 min for the platform
- If the agent platform is down, operations fall back to existing human runbooks: agents are never a single point of failure

## Capacity model (illustrative)

| Workload | Volume per day | Tier mix | Peak concurrency |
| --- | --- | --- | --- |
| Event triage | 2–5 million events | ~98% SLM, 2% Flash | 3,000 req/s |
| Incident diagnosis | 5,000–20,000 episodes | 60% in-house LLM, 40% Gemini | 400 concurrent episodes |
| Service requests | 30,000 requests | 80% SLM, 20% Flash-Lite | 150 req/s |
| Knowledge Q&A | 50,000 queries | 30% cache, 70% Flash | 250 req/s |

---

[← Observability and telemetry](08-observability-and-telemetry.md) · [Index](README.md) · [Security and governance →](10-security-and-governance.md)
