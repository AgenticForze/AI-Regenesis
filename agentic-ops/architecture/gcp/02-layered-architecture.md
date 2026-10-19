# Layered reference architecture

Eleven layers, each with a single responsibility. Colours are used consistently in every diagram that follows. Components marked † are built or self-hosted; everything else is a Google Cloud managed service.

| Layer | Name | Responsibility | Services |
| --- | --- | --- | --- |
| **L0** | Channels and triggers | How work reaches agents: people, alerts, events, schedules | Gemini Enterprise (Agentspace), Google Chat, Teams / Slack bots †, ServiceNow / Jira webhooks †, Cloud Monitoring alerts, Eventarc, Pub/Sub, Cloud Scheduler, Ops console (Cloud Run) † |
| **L1** | Edge, identity and safety | Authenticate, rate-limit, sanitise every inbound request | Cloud Load Balancing, Cloud Armor, Apigee (AI gateway policies), Identity-Aware Proxy, Cloud Identity / Workforce Identity Federation, Model Armor, Sensitive Data Protection |
| **L2** | Agent orchestration | Supervisor, planners, domain agents, sessions, durable execution | Vertex AI Agent Engine, Agent Development Kit (ADK), A2A protocol, Agent Engine Sessions, Workflows, Cloud Tasks, Agent registry and catalog †, Policy decision point (OPA) †, HITL approval service † |
| **L3** | Model gateway and router | One door to every model: routing, caching, quotas, fallback | LLM gateway (GKE) †, GKE Inference Gateway, Apigee token quotas, Memorystore for Redis (semantic cache), Complexity classifier SLM †, Prompt registry † |
| **L4** | Model serving | Managed frontier models plus our own LLMs and SLMs | Gemini Pro / Flash / Flash-Lite (Vertex AI), Provisioned Throughput, Model Garden (open and partner models), Vertex AI Endpoints, In-house LLMs on GKE (vLLM, TPU / H100) †, SLMs on Cloud Run GPU (L4) †, Vertex AI embeddings, Fine-tuned Gemma / Llama variants † |
| **L5** | Knowledge and memory | Grounding, retrieval, episodic and long-term memory | Vertex AI Search, Vertex AI RAG Engine, Vector Search, AlloyDB AI (pgvector), Spanner Graph (CMDB topology), Agent Engine Memory Bank, Firestore, BigQuery, Cloud Storage |
| **L6** | Tools and actions | The only way agents change the world | MCP servers (Cloud Run) †, Application Integration, Integration Connectors, Cloud Run functions, Infrastructure Manager (Terraform), Cloud Build, GKE / Config Sync, Runbook library †, Code execution sandbox |
| **L7** | Data and event backbone | Signals in, facts out, at stream and batch speed | Pub/Sub, Dataflow, BigQuery (incl. continuous queries), Datastream, Managed Service for Apache Kafka, Dataplex Universal Catalog |
| **L8** | Observability and evaluation | Traces, metrics, logs, quality, cost | OpenTelemetry SDK + Collector †, Cloud Trace, Cloud Logging + Log Analytics, Managed Service for Prometheus, Cloud Monitoring SLOs, Error Reporting / Profiler, Gen AI Evaluation Service, Looker |
| **L9** | Security and governance | Boundaries, keys, posture, audit | IAM + Workload Identity, VPC Service Controls, Cloud KMS (CMEK), Secret Manager, Security Command Center, Google SecOps (SIEM / SOAR), Binary Authorization, Org Policy, Cloud Audit Logs, Assured Workloads |
| **L10** | Platform and MLOps | Build, train, evaluate, ship | Vertex AI Pipelines, Vertex AI Model Registry, Vertex AI Experiments, Vertex AI tuning, Artifact Registry, Cloud Build, Cloud Deploy, Colab Enterprise, Terraform landing zone † |
† built or self-hosted by us; everything else is a managed service.

---

[← Intent and principles](01-intent-and-principles.md) · [Index](README.md) · [End to end flow →](03-end-to-end-flow.md)
