# 0003. Enforce action policy in a deterministic service, not the prompt

- **Status:** Accepted
- **Date:** 2026-10-16

## Context

Agents read untrusted content: logs, tickets, documents, web pages. Indirect prompt injection (OWASP LLM01) can make a model propose actions its instructions forbid. Instructions in a system prompt are not a security control.

## Decision

Every tool call passes a deterministic policy decision point before execution: OPA on Google Cloud, AgentCore Policy (Cedar) on AWS. Policies are code in Git, unit-tested in the delivery pipeline (gate D4), and evaluated outside the model's process. The model's output is treated as a *request*, never as an authorisation.

## Consequences

- A fooled model can propose a harmful action but cannot execute it.
- Every decision is logged with the rule that made it, which simplifies audit.
- Policy latency is on the hot path; keep it in-region and cache bundles.

## Alternatives considered

| Option | Why not |
| --- | --- |
| System-prompt rules only | Bypassable by injection; not auditable. |
| LLM-as-judge for authorisation | Non-deterministic and itself injectable. |
