---
title: "Glossary & Notation Conventions"
sidebar_label: "0.5 Glossary & Notation Conventions"
sidebar_position: 5
chapter: "0.5"
---

# Glossary & Notation Conventions

A living reference for terms and notation used consistently across the site. Individual
chapters don't redefine these — they link back here.

## Conventions used throughout the site

- **Chapter IDs** are written `phase.chapter`, e.g. `10.4` means Phase 10, chapter 4. The flight
  label at the top of every page (e.g. `Chapter 10.4 · Phase 10`) uses this same numbering.
- **`[v3]` / `[v4]` / `[v5]` tags** on a chapter title mark content added or expanded in that
  review pass — see the site's Changelog for what each pass covered.
- **"HL survey"** on a chapter marks it as using the lighter four-section landscape template
  (Phases 9 and 14 only) rather than the full seven-section Content Standard.
- Code blocks use language-tagged fencing (` ```python `, ` ```bash `, etc.) and are always
  runnable/copy-pasteable as written — no partial snippets presented as complete.
- Mermaid diagrams are used for anything architectural that will change over time (flow charts,
  sequence diagrams); static SVG illustrations are used for anything conceptual/decorative.

## Core terms

| Term | Definition |
|---|---|
| **Agent** | A system that uses an LLM to decide its own sequence of actions (tool calls, sub-tasks) toward a goal, rather than following a fixed, human-authored control flow. See 8.1 and 8.8 for the full agent-vs-workflow-vs-copilot distinction. |
| **RAG (Retrieval-Augmented Generation)** | Augmenting an LLM's response with content retrieved from an external knowledge source at inference time, rather than relying solely on what the model learned during training. See Phase 6. |
| **Fine-tuning** | Further training a pretrained model's weights on a smaller, task- or domain-specific dataset. See Phase 7. |
| **SLM (Small Language Model)** | A language model deliberately sized down from frontier-scale LLMs for cost, latency, privacy, or on-device deployment reasons. See 13.11–13.13. |
| **Tool / Function Calling** | A model's ability to emit a structured request to invoke an external function/API, whose result is then fed back into the model's context. See 5.3, 5.4, 8.4. |
| **Trajectory (agent eval)** | The full sequence of an agent's tool calls and intermediate reasoning steps toward an answer — evaluated separately from whether the final answer was correct. See 15.2. |
| **OBO (On-Behalf-Of) flow** | An OAuth pattern where an agent acts using a token scoped to a specific human user's permissions, rather than a standing service-account identity. See 15.5. |
| **Autonomy Level (L0–L5)** | A framework for describing how much of a task an agent is trusted to complete without human approval, from L0 (no autonomy) to L5 (fully autonomous). See 10.8. |
| **Landing zone** | The pre-configured, governed cloud environment (network, IAM, guardrails) an enterprise agent platform is deployed into. See 15.10. |

## Notation

- Model/architecture math uses standard ML notation (bold lowercase for vectors, bold uppercase
  for matrices) — introduced locally in each Deep-Dive section where first used, not assumed.
- Architecture diagrams always label data flow direction explicitly; an unlabeled arrow is
  considered a chapter bug — please file an issue if you find one.

*This glossary grows as new chapters introduce new recurring terms — see the Contribution Guide
(Phase 18) for how to propose an addition.*
