# End-to-end flow

A CloudWatch alarm, ticket, chat message or EventBridge event enters through the edge, passes Bedrock Guardrails, is triaged by an SLM and handed to the supervisor on AgentCore Runtime. The supervisor delegates over A2A, domain agents ground themselves in Knowledge Bases, Neptune topology and AgentCore Memory, and every proposed action is checked by AgentCore Policy before an MCP tool behind AgentCore Gateway touches production.

![AWS end-to-end agentic operations flow](../../diagrams/png/aws-end-to-end-flow.png)
[SVG version](../../diagrams/svg/aws-end-to-end-flow.svg)

*Figure 1. Signal-to-outcome flow on AWS. Dotted lines are asynchronous telemetry and learning paths.*

## The operating loop

| Stage | What happens | Primary services | Emitted telemetry |
| --- | --- | --- | --- |
| 1. Perceive | Normalise the trigger into a canonical event, dedupe, correlate with open incidents. | EventBridge, SQS FIFO, Kinesis | `agent.event.received`, correlation ratio |
| 2. Ground | Retrieve topology, recent changes (CloudTrail, Config), runbooks, similar incidents, live metrics. | Neptune Analytics, Knowledge Bases, AgentCore Memory, CloudWatch | retrieval latency, hit rate |
| 3. Reason and plan | Rank hypotheses, produce a typed plan with expected effects and rollback. | LLM gateway, Bedrock, in-house LLM | tokens, model, TTFT |
| 4. Authorise | Cedar policies evaluate each tool call; risky steps route to a human. | AgentCore Policy, Step Functions, Slack / Teams | decision, policy ID, approval latency |
| 5. Act | Execute via MCP tools and SSM Automation with idempotency and dry-run. | AgentCore Gateway, Systems Manager, Lambda | tool status, side-effect ID |
| 6. Learn | Close ticket, write episodic memory, score with evaluations, feed tuning sets. | AgentCore Memory, AgentCore Evaluations, S3 Tables | outcome, MTTR, feedback |

---

[← Layered architecture](02-layered-architecture.md) · [Index](README.md) · [Agent topology and autonomy →](04-agent-topology-and-autonomy.md)
