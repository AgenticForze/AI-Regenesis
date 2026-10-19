# End-to-end flow

A signal enters at L0, passes the safety edge, is triaged by a cheap SLM, and is handed to the supervisor. The supervisor plans, delegates to domain agents over A2A, and each agent grounds itself in memory and knowledge before proposing actions. Every action passes the policy decision point, and, depending on autonomy level, a human gate, before touching production through an MCP tool. Outcomes feed back into memory, evaluation and training.

![End-to-end agentic operations flow](../../diagrams/png/gcp-end-to-end-flow.png)
[SVG version](../../diagrams/svg/gcp-end-to-end-flow.svg)

*Figure 1. Signal-to-outcome flow. Dotted lines are asynchronous feedback paths.*

## The operating loop

Every agent, whatever its domain, runs the same six-stage loop so that telemetry, evaluation and policy can be applied uniformly.

| Stage | What happens | Primary services | Emitted telemetry |
| --- | --- | --- | --- |
| 1. Perceive | Normalise the trigger into a canonical event envelope (CloudEvents), dedupe, correlate with open incidents. | Pub/Sub, Dataflow, Eventarc | `agent.event.received`, correlation ratio |
| 2. Ground | Retrieve topology, recent changes, runbooks, similar past incidents, current metrics. | Spanner Graph, RAG Engine, Vector Search, BigQuery, Memory Bank | retrieval latency, hit rate, groundedness inputs |
| 3. Reason and plan | Hypothesise causes, rank them, produce a typed plan of tool calls with expected effects and rollback steps. | LLM router, Gemini, in-house LLM | tokens, model, TTFT, plan length |
| 4. Authorise | Evaluate each step against policy (blast radius, change window, data class, autonomy level); route to human if required. | OPA on Cloud Run, HITL service, Google Chat cards | decision, rule ID, approval latency |
| 5. Act | Execute via MCP tools with idempotency keys, dry-run first where supported, verify post-conditions. | MCP servers, Integration Connectors, Infra Manager | tool status, duration, side-effect record |
| 6. Learn | Close ticket, write episodic memory, capture human feedback, feed eval datasets and fine-tuning corpora. | Memory Bank, BigQuery, Vertex AI Pipelines | outcome, MTTR, feedback score |

---

[← Layered architecture](02-layered-architecture.md) · [Index](README.md) · [Agent topology and autonomy →](04-agent-topology-and-autonomy.md)
