# AgentOps lifecycle

```mermaid
flowchart LR
D["Design<br/>agent spec, tools, Cedar"] --> B["Build<br/>Strands, SageMaker Studio"]
B --> U["Unit and contract tests"]
U --> E["Offline eval<br/>golden incident replay"]
E --> SH["Shadow mode<br/>Policy log-only"]
SH --> CA["Canary<br/>AgentCore endpoint versions"]
CA --> PR["Production"]
PR --> MO["Monitor<br/>CloudWatch, Evaluations"]
MO --> FB["Fine-tune and distil<br/>SageMaker, Bedrock"]
FB --> B
E -- "fails gate" --> B
CA -- "auto-rollback" --> SH
```

*Figure 15. Release gates: evaluation score ≥ previous version, no safety regressions, cost per episode within 10% of budget.*

---

[← Deployment topology](14-deployment-topology.md) · [Index](README.md) · [Finops →](16-finops.md)
