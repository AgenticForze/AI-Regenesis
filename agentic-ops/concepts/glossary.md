# Glossary

| Term | Meaning in this repository |
| --- | --- |
| **A2A** | Agent2Agent protocol, used for one agent to delegate a task to another and discover it through an agent card. |
| **Action type** | A specific kind of change an agent can make (for example "scale a deployment"). Autonomy is set per action type. |
| **Agent card** | A published description of an agent's skills and endpoint, used for discovery over A2A. |
| **Agent observability lake** | The analytical store (BigQuery or S3 Tables) that joins spans, cost, quality and outcomes. |
| **Autonomy level** | L0 Observe to L4 Autonomous; see [Earned autonomy](03-earned-autonomy.md). |
| **Blast radius** | The scope of systems and users a single action could affect if it goes wrong. |
| **Cascade routing** | Sending a request to the cheapest capable model first and escalating only on low confidence. |
| **Episode** | One agent run from trigger to outcome; the root span of a trace. |
| **Executor** | A narrow tool service that holds the only credentials able to change a system. Agents ask; executors act. |
| **Golden set** | Replayed past incidents with known good outcomes, used to evaluate every agent version. |
| **HITL** | Human in the loop: a durable, identity-bound approval step. |
| **Kill switch** | A flag that disables an agent or an action type within seconds. |
| **LLM gateway** | The single entry point to every model: routing, caching, budgets, data-class pinning, fallback, cost labels. |
| **MCP** | Model Context Protocol, the standard interface agents use to call tools. |
| **Plan precision** | Share of executed plan steps later judged correct; the main promotion metric. |
| **Restricted enclave** | A separately perimetered zone where the in-house LLM and regulated data live, with no internet egress. |
| **Side-effect ledger** | A durable record of every mutating action with its idempotency key, used for exactly-once semantics and audit. |
| **SLM** | Small language model, typically 1–9B parameters, fine-tuned for a narrow task. |
| **Toil** | Manual, repetitive, automatable operational work that scales linearly with the service (Google SRE). |

---

[← The security gate model](04-security-gate-model.md) · [Index](README.md)
