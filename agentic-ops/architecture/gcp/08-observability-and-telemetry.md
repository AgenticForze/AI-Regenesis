# Observability and telemetry

Observing an agentic system means observing three things at once: the infrastructure it runs on, the behaviour of the agents, and the quality of their decisions. We instrument all three with OpenTelemetry using the GenAI semantic conventions, and land everything in one analytical store.

## 8.1 Telemetry pipeline

![Telemetry pipeline from agents to evaluation](../../diagrams/png/gcp-telemetry-pipeline.png)
[SVG version](../../diagrams/svg/gcp-telemetry-pipeline.svg)

*Figure 7. One trace ID follows a request through all layers; BigQuery is the join point for cost, quality and outcome.*

## 8.2 Trace anatomy

Each agent episode is a root span with nested spans for every step. Attributes follow the OpenTelemetry `gen_ai.*` conventions plus our own `agent.*` namespace.

| Span | Key attributes |
| --- | --- |
| `agent.episode` | agent.id, agent.version, trigger.type, incident.id, autonomy.level, outcome, total\_cost\_usd |
| `agent.plan` | plan.steps, plan.hypotheses, plan.confidence |
| `gen_ai.chat` | gen\_ai.request.model, gen\_ai.usage.input\_tokens, gen\_ai.usage.output\_tokens, router.tier, cache.hit, ttft\_ms |
| `retrieval.query` | index, top\_k, latency\_ms, docs\_returned, acl\_filtered |
| `policy.decision` | rule.id, decision, risk.score, blast\_radius |
| `hitl.approval` | approver.id, wait\_ms, decision |
| `tool.call` | tool.name, mcp.server, idempotency\_key, dry\_run, status, side\_effect.id |
| `a2a.delegate` | from.agent, to.agent, task.id |

## 8.3 Golden signals for agents

### Operational

- Episode success rate and latency (p50, p95)
- Time to first token, tokens per second per model
- Tool error rate and retry rate
- Queue depth and age in Pub/Sub and Cloud Tasks
- GPU / TPU utilisation, KV-cache utilisation

### Quality

- Plan precision (actions later judged correct)
- Groundedness and faithfulness scores
- Hallucinated tool or parameter rate
- Human override and rollback rate
- User feedback score from Chat and ITSM

### Business

- MTTD and MTTR by severity
- Autonomous resolution rate
- Toil hours removed per week
- Change failure rate
- Tickets deflected

### Cost and safety

- Cost per episode and per resolved incident
- Cache hit rate and tier mix
- Model Armor blocks, DLP findings
- Policy denials and denied-then-retried attempts
- Loop detection triggers and budget stops

## 8.4 Evaluation

Evaluation runs continuously, not just before release. Offline, every agent version runs against a golden set of replayed incidents in Vertex AI Pipelines and is scored by the Gen AI Evaluation Service (trajectory match, tool-use correctness, groundedness, safety) plus LLM-as-judge rubrics calibrated against human labels. Online, a sampled 5–10% of production episodes are scored asynchronously and every human override is turned into a new labelled test case. Quality metrics are exported to Cloud Monitoring so that a regression pages the owning team exactly like a latency regression.

## 8.5 SLOs

| SLO | Target | Window |
| --- | --- | --- |
| Agent platform availability | 99.9% | 28 days |
| Triage latency (event to classified) | p95 < 5 s | 28 days |
| P1 time to first diagnosis | p90 < 3 min | 28 days |
| Autonomous action correctness | ≥ 99% | rolling 500 actions |
| HITL request delivered to approver | p99 < 30 s | 28 days |
| Gateway error rate | < 0.5% | 7 days |

---

[← Knowledge and memory](07-knowledge-and-memory.md) · [Index](README.md) · [Scalability and resilience →](09-scalability-and-resilience.md)
