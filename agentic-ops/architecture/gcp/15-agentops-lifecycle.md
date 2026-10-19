# AgentOps lifecycle

Agents, prompts, tools, policies and models are all versioned artefacts that move through one pipeline.

```mermaid
flowchart LR
D["Design<br/>agent spec, tools, policy"] --> B["Build<br/>ADK, Colab Enterprise"]
B --> U["Unit and contract tests<br/>tool mocks"]
U --> E["Offline eval<br/>golden incident replay"]
E --> SH["Shadow mode in prod<br/>L0"]
SH --> CA["Canary<br/>Cloud Deploy, 5% traffic"]
CA --> PR["Production<br/>autonomy per action type"]
PR --> MO["Monitor<br/>SLOs, online eval"]
MO --> FB["Feedback and fine-tune<br/>Vertex AI Pipelines"]
FB --> B
E -- "fails gate" --> B
CA -- "auto-rollback" --> SH
```

*Figure 15. Release gates: offline eval score ≥ previous version, no safety regressions, cost per episode within 10% of budget.*

---

[← Deployment topology](14-deployment-topology.md) · [Index](README.md) · [Finops →](16-finops.md)
