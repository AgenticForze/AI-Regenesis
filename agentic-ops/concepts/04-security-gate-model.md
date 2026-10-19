# The security gate model

Agents are a new class of privileged identity that can be tricked. The gate model places deterministic controls where a compromised prompt cannot reach them. Every gate is independently owned, logged, and fails closed.

## Runtime gates

| Gate | Question it answers | Typical owner |
| --- | --- | --- |
| G1 Edge | Is this traffic allowed to reach us at all? | Network security |
| G2 Identity | Who or what is calling, from what device and context? | Identity |
| G3 API contract | Is the request well-formed, authorised and within quota? | API platform |
| G4 Input safety | Does the input or retrieved content contain injection, secrets or PII? | AI security |
| G5 Agent authorisation | May this caller invoke this agent, and may it delegate to that one? | Platform |
| G6 Model gateway | Which model may see this data class, and is there budget left? | Platform |
| G7 Retrieval ACL | Is the on-behalf-of user entitled to every retrieved document? | Data governance |
| G8 Output safety | Is the response safe, grounded and schema-valid? | AI security |
| G9 Action policy | Is this action allowed at this autonomy level, now, on this target? | Service owners |
| G10 Human approval | Has a named, independent human approved it? | Service owners |
| G11 Execution guard | Are credentials scoped and short-lived, and did the dry-run pass? | Platform |
| G12 Verify and audit | Did the change do what was expected, and is it recorded immutably? | Security operations |

See the drawn chain for each cloud: [Google Cloud](../architecture/gcp/13-security-gates.md) · [AWS](../architecture/aws/13-security-gates.md).

## The defence-in-depth test

Pick the most likely attack, indirect prompt injection through data an agent reads, and check that **at least three gates stop it independently**:

1. G4 flags the injected instruction in retrieved content.
2. G9 denies the action because it is not on the agent's allow-list.
3. G11 has no credential that could perform it, because the agent's identity cannot invoke that executor.

If any one of those depends on the model behaving well, the design is not finished.

## Delivery gates

Agents, prompts, tools, policies and models ship through the same pipeline:

| Gate | Check |
| --- | --- |
| D1 | Code scan: SAST, secrets, IaC lint |
| D2 | Dependencies: SCA, licences, SBOM |
| D3 | Image and model: vulnerability scan, weight hash, signature |
| D4 | Policy tests: unit tests for OPA or Cedar, tool contract tests |
| D5 | Offline evaluation: quality and safety on golden incident replays |
| D6 | Red team: injection and misuse suites |
| D7 | Attestation and change approval |
| D8 | Progressive rollout: shadow, canary, SLO-guarded automatic rollback |

---

[← Earned autonomy](03-earned-autonomy.md) · [Index](README.md) · [Glossary →](glossary.md)
