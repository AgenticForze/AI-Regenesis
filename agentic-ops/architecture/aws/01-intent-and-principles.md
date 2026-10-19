# Intent and principles

Agentic Ops replaces ticket-driven, human-routed operations with a mesh of specialised agents that observe signals, reason over enterprise context, plan, act through governed tools, and learn from outcomes. The principles are cloud-neutral and identical to the Google Cloud edition; only the services change.

### Agents are workloads

Every agent has an IAM identity, a versioned spec, an SLO, a budget, an owner and a kill switch, and runs in AgentCore Runtime like any production service.

### Right model for the job

SLMs on Inferentia for volume, in-house LLMs on EKS for restricted data, Bedrock models (Amazon Nova, Anthropic Claude and others) for deep reasoning. One gateway decides.

### Autonomy is earned

Each action type starts in shadow mode and graduates through autonomy levels based on measured precision, blast radius and reversibility.

### Everything is a trace

AgentCore Observability and ADOT emit OpenTelemetry spans for every step, joined by one trace ID from alarm to outcome in X-Ray and CloudWatch.

### Policy outside the prompt

AgentCore Policy (Cedar) intercepts every tool call, and SCPs and IAM boundaries cap what any agent role can ever do, regardless of what the model says.

### Open protocols

MCP through AgentCore Gateway, A2A between agents, OpenTelemetry, OCI images and Terraform or CDK keep every seam portable.

---

[Index](README.md) · [Layered architecture →](02-layered-architecture.md)
