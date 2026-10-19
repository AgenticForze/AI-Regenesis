# 0004. Separate reasoning identities from action identities

- **Status:** Accepted
- **Date:** 2026-10-16

## Context

If the identity an agent reasons under can also change production, any compromise of the reasoning path (prompt injection, a bad model version, a bug) is a compromise of production.

## Decision

Agents run under a reasoning identity that can call models, retrieval and other agents but holds no permission to mutate systems. Narrow executor services, one per tool family, hold the only mutating credentials, issued just in time and scoped per call. Agents may invoke only the executors listed in their spec.

## Consequences

- Blast radius of a compromised agent is limited to what its permitted executors can do, after policy.
- More identities to manage; automate creation from the agent spec.
- Executors become a reusable, audited catalogue shared across agents.

## Alternatives considered

| Option | Why not |
| --- | --- |
| One service account per agent with all permissions | Policy becomes the only control; no defence in depth. |
