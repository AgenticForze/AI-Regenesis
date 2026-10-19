# Intent and principles

Agentic Ops replaces ticket-driven, human-routed operations with a mesh of specialised agents that observe signals, reason over enterprise context, plan, act through governed tools, and learn from outcomes. Humans move from doing the work to setting policy, approving high-risk actions and handling novel situations.

The platform has to satisfy three constituencies at once: operators who need faster resolution with fewer pages, risk and compliance who need provable control over every autonomous action, and finance who need the cost of intelligence to fall per unit of work.

### Agents are workloads, not features

Every agent has an identity, a versioned spec, an SLO, a budget, an owner and a kill switch. It is deployed, observed and retired like any production service.

### Right model for the job

SLMs handle high-volume, narrow tasks; in-house LLMs handle restricted data; Gemini handles deep reasoning and multimodal. A central gateway decides, not individual teams.

### Autonomy is earned

Each action type starts in shadow mode and graduates through autonomy levels based on measured precision, blast radius and reversibility.

### Everything is a trace

Every perception, thought, model call, retrieval, tool call and approval is an OpenTelemetry span joined by one trace ID from trigger to outcome.

### Policy outside the prompt

Guardrails are enforced by deterministic policy services at the gateway and tool boundary, never only by instructions in a system prompt.

### Open protocols

MCP for tool access, A2A for agent-to-agent delegation, OpenTelemetry for telemetry, OCI images and Terraform for delivery. This limits lock-in at every seam.

---

[Index](README.md) · [Layered architecture →](02-layered-architecture.md)
