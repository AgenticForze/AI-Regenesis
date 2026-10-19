# Sequence flows

## 6.1 Autonomous incident remediation

```mermaid
sequenceDiagram
autonumber
participant CW as CloudWatch
participant EB as EventBridge
participant TRI as Triage SLM
participant SUP as Supervisor
participant INC as Incident agent
participant KG as Neptune and Knowledge Bases
participant GW as LLM gateway
participant POL as AgentCore Policy
participant AGW as AgentCore Gateway
participant SSM as SSM Automation
participant ITSM as ServiceNow
participant OBS as X-Ray and CloudWatch
CW->>EB: SLO burn alarm (Application Signals)
EB->>TRI: route event with trace_id
TRI->>ITSM: open incident, link trace_id
TRI->>SUP: A2A task "restore checkout latency"
SUP->>INC: delegate with context and budget
par Grounding
INC->>KG: dependencies and recent changes
INC->>KG: similar incidents and runbooks
INC->>CW: metrics, logs, traces for last 30 min
end
INC->>GW: reason (capability=rca, data=internal)
GW-->>INC: ranked hypotheses, plan with rollback
INC->>AGW: tool call "scale deployment 6 to 10"
AGW->>POL: evaluate Cedar policies
POL-->>AGW: permit, autonomy L4
AGW->>SSM: run Automation document (dry-run then apply)
SSM-->>AGW: success
loop Verify every 60s up to 10 min
INC->>CW: p95 latency and error budget
end
INC->>ITSM: resolve with RCA summary
INC-)OBS: spans, tokens, cost, outcome
```

*Figure 4. AgentCore Policy sits in the Gateway path, so the agent cannot reach a tool without a policy decision.*

## 6.2 Human-in-the-loop approval

```mermaid
sequenceDiagram
autonumber
participant CHG as Change agent
participant POL as AgentCore Policy
participant SF as Step Functions
participant SL as Slack or Teams card
actor OWN as Service owner
participant CM as SSM Change Manager
participant CFN as CloudFormation
CHG->>POL: tool call "failover Aurora cluster"
POL-->>CHG: requires approval, L2
CHG->>SF: start approval workflow with evidence
SF->>SL: interactive card with task token
OWN->>SL: review and approve
SL->>SF: SendTaskSuccess with approver identity
SF->>CM: open change request, record approval
CM->>CFN: execute change set
CFN-->>SF: complete, post-checks pass
SF-->>CHG: result
alt No response within SLA
SF->>SL: escalate to secondary on-call
else Rejected
SF-->>CHG: SendTaskFailure, agent replans
end
```

*Figure 5. Approvals are durable task tokens, identity-bound and recorded in CloudTrail and Change Manager.*

## 6.3 Conversational access request

```mermaid
sequenceDiagram
autonumber
actor USR as Engineer
participant QS as Quick Suite or Slack
participant API as API Gateway and Guardrails
participant SUP as Supervisor
participant SVC as Service request agent
participant ID as AgentCore Identity
participant IDC as IAM Identity Center tool
USR->>QS: "read access to prod logs for payments, 4 hours"
QS->>API: request with user OIDC token
API->>API: authN, usage plan, Guardrails screen
API->>SUP: forward with user identity
SUP->>SVC: delegate
SVC->>SVC: check entitlement policy and manager chain
SVC->>ID: obtain on-behalf-of token for tool
ID-->>SVC: scoped token
SVC->>IDC: assign permission set with 4h expiry
IDC-->>SVC: assignment created
SVC-->>QS: done, expires 16:40, audit link
```

*Figure 6. The user's identity, not the agent's, is what the entitlement check evaluates.*

---

[← Model strategy and routing](05-model-strategy-and-routing.md) · [Index](README.md) · [Knowledge and memory →](07-knowledge-and-memory.md)
