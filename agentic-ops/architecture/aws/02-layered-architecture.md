# Layered reference architecture

The same eleven layers as the Google Cloud edition, mapped to AWS. Components marked † are built or self-hosted; everything else is an AWS managed service.

| Layer | Name | Responsibility | Services |
| --- | --- | --- | --- |
| **L0** | Channels and triggers | How work reaches agents | Amazon Quick Suite, Slack / Teams bots †, ServiceNow / Jira webhooks †, CloudWatch alarms, DevOps Guru insights, EventBridge rules and Scheduler, AWS Health events, Ops console † |
| **L1** | Edge, identity and safety | Authenticate, rate-limit, sanitise | CloudFront, AWS WAF, Shield Advanced, Application Load Balancer, API Gateway, Verified Access, IAM Identity Center, Amazon Cognito, Bedrock Guardrails, Comprehend PII detection |
| **L2** | Agent orchestration | Supervisor, planners, domain agents, durable execution | AgentCore Runtime, AgentCore Memory, AgentCore Identity, AgentCore Policy (Cedar), AgentCore Registry, Strands Agents SDK †, A2A protocol, Step Functions, SQS, HITL approval service † |
| **L3** | Model gateway and router | One door to every model | LLM gateway (EKS) †, Bedrock Intelligent Prompt Routing, Bedrock cross-Region inference, ElastiCache for Valkey (semantic cache), API Gateway usage plans, Bedrock Prompt Management, Complexity classifier SLM † |
| **L4** | Model serving | Managed frontier models plus our own | Amazon Bedrock (Nova, Claude, Llama, Mistral), Bedrock Provisioned Throughput, Bedrock Custom Model Import, SageMaker AI endpoints, In-house LLMs on EKS (vLLM, Neuron) †, Trainium / Inferentia / P5 instances, SLMs on EKS + Karpenter †, Titan / Nova embeddings |
| **L5** | Knowledge and memory | Grounding, retrieval, memory | Bedrock Knowledge Bases, OpenSearch Serverless, Amazon S3 Vectors, Aurora PostgreSQL (pgvector), Neptune Analytics (topology, GraphRAG), AgentCore Memory, DynamoDB, Amazon Kendra, Amazon S3 |
| **L6** | Tools and actions | The only way agents change the world | AgentCore Gateway (MCP), Systems Manager Automation, SSM Change Manager, AWS Lambda, AgentCore Code Interpreter, CloudFormation / Terraform via CodeBuild, EKS API, AppFlow / partner connectors, Runbook library † |
| **L7** | Data and event backbone | Signals in, facts out | EventBridge, SQS / SNS, Kinesis Data Streams, Amazon MSK, Data Firehose, S3 Tables (Iceberg), Athena, Redshift, Glue Data Catalog / Lake Formation |
| **L8** | Observability and evaluation | Traces, metrics, logs, quality, cost | AgentCore Observability, ADOT (OpenTelemetry), AWS X-Ray, CloudWatch Logs, metrics, Application Signals, Amazon Managed Prometheus, Amazon Managed Grafana, AgentCore Evaluations, Bedrock model evaluation, QuickSight |
| **L9** | Security and governance | Boundaries, keys, posture, audit | AWS Organizations + SCPs / RCPs, Control Tower, IAM, permission boundaries, AWS KMS (XKS) / CloudHSM, Secrets Manager, GuardDuty, Security Hub, Security Lake, Macie, CloudTrail Lake, AWS Config, Audit Manager |
| **L10** | Platform and MLOps | Build, train, evaluate, ship | SageMaker AI Pipelines, SageMaker Model Registry, SageMaker HyperPod, Bedrock fine-tuning and distillation, CodePipeline / CodeBuild, Amazon ECR + Inspector, AWS Signer, Terraform / CDK landing zone † |
† built or self-hosted by us; everything else is a managed service.

---

[← Intent and principles](01-intent-and-principles.md) · [Index](README.md) · [End to end flow →](03-end-to-end-flow.md)
