# 0006. Use the cloud's managed agent runtime by default

- **Status:** Accepted
- **Date:** 2026-10-16

## Context

Agents need session state, scaling, isolation, identity and tracing. We can build that on Kubernetes or use Vertex AI Agent Engine (Google Cloud) or Bedrock AgentCore Runtime (AWS).

## Decision

Run agents on the managed runtime by default. Use GKE or EKS only for agents with unusual networking, throughput or framework needs. Build agents with frameworks that run on both (ADK, Strands or others), and keep tool access on MCP and delegation on A2A, so the choice stays reversible per agent.

## Consequences

- Less platform code to own; faster start.
- Feature availability varies by region and changes quickly; validate during design.
- Some vendor coupling at the runtime layer, contained by open protocols at the seams.

## Alternatives considered

| Option | Why not |
| --- | --- |
| Self-host everything on Kubernetes | More undifferentiated work; slower to production. |
