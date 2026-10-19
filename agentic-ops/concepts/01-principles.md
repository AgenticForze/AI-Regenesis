# Principles

Six rules sit underneath every later decision. When two options look equally good, the one that better honours these wins.

| # | Principle | What it means in practice | What breaks without it |
| --- | --- | --- | --- |
| 1 | **Agents are workloads, not features** | Every agent has an identity, a versioned spec, an SLO, a budget, an owner and a kill switch, and ships through the same pipeline as any service. | Nobody can say who owns an agent, what it may do, or how to stop it. |
| 2 | **Right model for the job** | SLMs for high-volume narrow tasks, in-house LLMs for restricted data, frontier models for hard reasoning. Agents request capabilities; a central gateway picks the model. | Cost spirals, restricted data leaks to the wrong model, and swapping models means rewriting agents. |
| 3 | **Autonomy is earned** | Autonomy is set per action type and promoted only on measured evidence. | Either nothing is automated (too risky) or everything is (until the first outage). |
| 4 | **Everything is a trace** | Every perception, model call, retrieval, policy decision, approval and tool call is an OpenTelemetry span joined by one trace ID. | You cannot explain why an agent acted, what it cost, or whether quality is drifting. |
| 5 | **Policy lives outside the prompt** | Deterministic policy services at the gateway and tool boundary decide what is allowed. | A single prompt injection becomes a production change. |
| 6 | **Open protocols at every seam** | MCP for tools, A2A for agent delegation, OpenTelemetry, OPA or Cedar, OCI and Terraform. | The platform locks to one vendor's agent runtime and cannot follow the market. |

The most commonly broken principle is the fifth. If the only thing stopping an agent from deleting production is a sentence in its system prompt, there is no control.

---

[Index](README.md) · [The operating loop →](02-operating-loop.md)
