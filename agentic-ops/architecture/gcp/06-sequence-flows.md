# Sequence flows

## 6.1 Autonomous incident remediation

A latency SLO burn alert on a GKE service, resolved end to end within policy.

```mermaid
sequenceDiagram
autonumber
participant MON as Cloud Monitoring
participant PS as Pub/Sub
participant TRI as Triage SLM
participant SUP as Supervisor
participant INC as Incident agent
participant KG as Spanner Graph and RAG
participant GW as LLM gateway
participant PDP as Policy engine
participant K8S as K8s MCP tool
participant ITSM as ServiceNow
participant OT as OTel and BigQuery
MON->>PS: SLO burn-rate alert (CloudEvent)
PS->>TRI: deliver event with trace_id
TRI->>TRI: classify P2, dedupe, map service
TRI->>ITSM: open incident, link trace_id
TRI->>SUP: A2A task "restore checkout latency"
SUP->>INC: delegate with context and budget
par Grounding
INC->>KG: topology, dependencies, last changes
INC->>KG: similar past incidents and runbooks
INC->>MON: pull metrics, logs, traces for last 30 min
end
INC->>GW: reason (capability=rca, data=internal)
GW-->>INC: hypotheses ranked, plan with rollback
INC->>PDP: authorise step "scale deployment 6 to 10"
PDP-->>INC: allow, autonomy L4, change window open
INC->>K8S: dry-run scale
K8S-->>INC: dry-run ok
INC->>K8S: apply with idempotency key
K8S-->>INC: applied
loop Verify every 60s up to 10 min
INC->>MON: check p95 latency and error budget
end
INC->>ITSM: resolve with RCA summary
INC->>SUP: task complete
INC-)OT: spans, tokens, cost, outcome
SUP-)OT: episode written to Memory Bank
```

*Figure 4. Every arrow is a span in Cloud Trace, joined by the trace\_id created at the alert.*

## 6.2 Human-in-the-loop approval for a high-risk action

```mermaid
sequenceDiagram
autonumber
participant CHG as Change agent
participant PDP as Policy engine
participant HITL as Approval service
participant CHAT as Google Chat card
actor OWN as Service owner
participant WF as Workflows
participant IM as Infra Manager
CHG->>PDP: authorise "failover Cloud SQL primary"
PDP-->>CHG: require approval, L2, owner group db-owners
CHG->>HITL: create approval (plan, blast radius, rollback, evidence)
HITL->>WF: start durable wait with 30 min SLA
HITL->>CHAT: interactive card to on-call owner
OWN->>CHAT: review evidence, approve
CHAT->>HITL: signed decision with user identity
HITL->>WF: resume
WF->>IM: execute Terraform change
IM-->>WF: applied
WF-->>CHG: result and post-checks
alt No response within SLA
WF->>CHAT: escalate to secondary on-call
else Rejected
WF-->>CHG: rejected with reason, agent replans
end
```

*Figure 5. Approvals are durable (Workflows), identity-bound and recorded in Cloud Audit Logs and the agent lake.*

## 6.3 Conversational request through Gemini Enterprise

```mermaid
sequenceDiagram
autonumber
actor USR as Engineer
participant GE as Gemini Enterprise
participant APG as Apigee and Model Armor
participant SUP as Supervisor
participant SVC as Service request agent
participant GW as LLM gateway
participant IAM as IAM MCP tool
USR->>GE: "give me read access to prod logs for payments for 4 hours"
GE->>APG: A2A call with user OAuth token
APG->>APG: authN, quota, prompt-injection scan
APG->>SUP: forward with user identity
SUP->>SVC: delegate
SVC->>GW: extract entities (SLM)
GW-->>SVC: resource, role, duration
SVC->>SVC: check entitlement policy and manager chain
SVC->>IAM: grant conditional role with expiry
IAM-->>SVC: binding created
SVC-->>GE: done, expires 16:40, audit link
GE-->>USR: confirmation
```

*Figure 6. The agent acts on behalf of the user; the user's identity, not the agent's, is what IAM Conditions evaluate.*

---

[← Model strategy and routing](05-model-strategy-and-routing.md) · [Index](README.md) · [Knowledge and memory →](07-knowledge-and-memory.md)
