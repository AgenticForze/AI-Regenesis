# Model strategy and routing

| Tier | Models | Hosting | Used for |
| --- | --- | --- | --- |
| SLM | Fine-tuned 1–9B open models, distilled classifiers, Bedrock distilled models | EKS with Karpenter on Inferentia2 or G-family GPUs; SageMaker endpoints for steady load | Triage, intent, extraction, log parsing, PII tagging, routing |
| In-house LLM | Fine-tuned open-weight 30–70B models | EKS on Trainium / P5 with vLLM or Neuron; optionally Bedrock Custom Model Import for serverless hosting inside our account boundary | Reasoning over restricted data, RCA narratives, security telemetry |
| Frontier | Amazon Nova family, Anthropic Claude, Meta Llama, Mistral on Bedrock (latest GA versions) | Bedrock on-demand with cross-Region inference profiles; Provisioned Throughput for baseline | Complex planning, long context, multimodal, code generation |

```mermaid
flowchart TD
IN["Request from agent<br/>capability, data class, budget, SLO"] --> C1{"Semantic cache hit<br/>ElastiCache Valkey"}
C1 -- "yes" --> OUT["Return cached"]
C1 -- "no" --> C2{"Restricted or regulated data?"}
C2 -- "yes" --> LLM["In-house LLM<br/>enclave account"]
C2 -- "no" --> C3{"Complexity score"}
C3 -- "low" --> SLM["SLM tier"]
C3 -- "medium" --> MID["Bedrock fast model"]
C3 -- "high or multimodal" --> TOP["Bedrock frontier model"]
SLM --> V{"Confidence above threshold?"}
V -- "no" --> MID
V -- "yes" --> OUT2["Return and cache"]
MID --> OUT2
TOP --> OUT2
LLM --> OUT2
TOP -. "throttle or 5xx" .-> FB["Cross-Region inference profile,<br/>then alternate model family"]
```

*Figure 3. Cascade routing. Bedrock Intelligent Prompt Routing can serve as the within-family router; our gateway owns cross-tier decisions.*

The gateway also applies Bedrock prompt caching for large stable system prompts, enforces per-agent token budgets, tags every call with cost-allocation tags, and invokes Bedrock Guardrails on both input and output.

---

[← Agent topology and autonomy](04-agent-topology-and-autonomy.md) · [Index](README.md) · [Sequence flows →](06-sequence-flows.md)
