# 0005. Fine-tune open-weight models; do not pre-train

- **Status:** Accepted
- **Date:** 2026-10-16

## Context

Some data (security telemetry, regulated customer data) must stay inside our perimeter, and high-volume tasks are cheaper on small models. Pre-training a model from scratch is expensive and slow, and rarely beats a well-tuned open-weight base on narrow operational tasks.

## Decision

Build in-house capability by fine-tuning open-weight models: 1–9B parameter SLMs for triage and extraction, 30–70B models for reasoning over restricted data. Host them in the restricted enclave with signed weights, evaluation cards and shadow traffic before release. Distil frequent frontier-model tasks into SLMs over time.

## Consequences

- Restricted data never leaves the perimeter; cost per token falls at high utilisation.
- We own model lifecycle: tuning pipelines, evaluation, accelerator capacity.
- Licence terms of each open-weight base must be reviewed.

## Alternatives considered

| Option | Why not |
| --- | --- |
| Pre-train our own model | Cost and time not justified for operations tasks. |
| Frontier API for everything | Cannot meet data residency for restricted data; higher cost at volume. |
