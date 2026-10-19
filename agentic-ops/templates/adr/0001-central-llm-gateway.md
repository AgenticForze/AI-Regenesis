# 0001. Put one gateway in front of every model

- **Status:** Accepted
- **Date:** 2026-10-16

## Context

Agents will use SLMs, in-house LLMs and several frontier models. If each team calls models directly, we lose cost attribution, cannot enforce which data reaches which model, cannot fail over, and cannot change models without rewriting agents.

## Decision

All model traffic goes through a single LLM gateway (layer L3). Agents request a *capability* and a *data class*; the gateway chooses the model, applies the semantic cache, enforces per-agent token budgets, pins restricted data to the in-house tier, records cost labels and handles regional failover.

## Consequences

- Model swaps become a routing change, not an agent release.
- Cost per agent, use case and incident becomes measurable.
- The gateway is now critical infrastructure: it needs multi-region deployment, its own SLO and circuit breakers.
- Some managed features (for example vendor prompt routing) are used behind the gateway rather than instead of it.

## Alternatives considered

| Option | Why not |
| --- | --- |
| Direct SDK calls from agents | No central control of data class, budget or failover. |
| Vendor-only router | Cannot route to in-house models or across clouds. |
