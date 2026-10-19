# 0002. Set autonomy per action type, earned with evidence

- **Status:** Accepted
- **Date:** 2026-10-16

## Context

Granting autonomy per agent forces an all-or-nothing choice: either the incident agent can do everything it knows how to do, or nothing. Risk teams cannot approve that, and operators lose the easy wins.

## Decision

Autonomy is configured per action type on a five-level scale (L0 Observe to L4 Autonomous). Promotion is one level at a time against an evidence gate (≥ 200 executions or 30 days, ≥ 98% plan precision, zero agent-caused Sev-1, exercised rollback, owner sign-off). Any agent-caused Sev-1 demotes the action type two levels automatically. See [Earned autonomy](../../concepts/03-earned-autonomy.md).

## Consequences

- Low-risk, reversible actions automate quickly; high-risk ones stay gated.
- Requires plan-precision measurement, which in turn requires evaluation and labelling.
- Policy configuration grows with the number of action types; it must live in Git with tests.

## Alternatives considered

| Option | Why not |
| --- | --- |
| Autonomy per agent | Too coarse; blocks safe automation or allows unsafe. |
| Fixed human approval for everything | Removes most of the value; approval fatigue. |
