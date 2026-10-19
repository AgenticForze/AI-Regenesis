# Scalability and resilience

### Inference scaling

- EKS with Karpenter node pools across Inferentia, Trainium and GPU instance families
- KEDA scaling on queue depth and KV-cache utilisation
- Bedrock cross-Region inference profiles absorb burst
- Provisioned Throughput sized to steady baseline
- Capacity Blocks or Savings Plans for reserved accelerators

### Orchestration scaling

- AgentCore Runtime isolates each session in its own microVM and scales automatically
- EventBridge and SQS decouple ingest from reasoning; FIFO groups per incident
- Step Functions for long-running durable plans
- Priority queues reserve capacity for P1

### Failure handling

- Idempotency keys and a DynamoDB side-effect ledger
- Circuit breakers per model and tool; degrade to recommend-only
- Step, token and time caps per episode
- Kill switch via AppConfig feature flags, < 10 s propagation
- DLQs with replay

### Multi-Region and DR

- Active-active in two Regions behind Route 53 health-checked routing
- DynamoDB global tables for ledger and approvals
- Aurora Global Database and Neptune replicas
- RPO ≈ 0 for actions, RTO < 15 min
- Human runbooks remain the fallback

---

[← Observability and telemetry](08-observability-and-telemetry.md) · [Index](README.md) · [Security and governance →](10-security-and-governance.md)
