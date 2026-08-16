# RegAITraining — AI Foundations to Advanced Agentic AI

## Master Curriculum & Learning-Site Blueprint (v5)

Prepared: August 14, 2026 · v5 update: added a new **AI Roles in the Market** chapter (0.3) mapping every major AI/agentic job role to the curriculum, plus two small gap-fill chapters the role-mapping exercise surfaced (Conversational & Agent UX Design, and AI Product Strategy). See changelog and the full role-mapping reference in Section 8.

---

## Changelog

**v5 (Aug 14, 2026) — AI Roles chapter added:**

- **New Ch 0.3, "AI Roles in the Market: Definitions, Responsibilities & Your Curriculum Path"** — added to Phase 0. Defines the major AI/agentic job roles in the 2026 market, their responsibilities, which curriculum phases/chapters map to each role, and recommended industry certifications per role. Phase 0's remaining chapters shift down one slot (old 0.3→0.4, 0.4→0.5, 0.5→0.6).
- The role-mapping exercise (full table in **Section 8**) surfaced two genuine content gaps, closed with two new chapters: **8.9 Conversational & Agent UX Design** (Agent Foundations) and **15.11 AI Product Strategy: Business Case & ROI for Agentic Products** (Enterprise phase). A few other role-adjacent needs (deep data engineering, academic ML research methodology) were deliberately scoped out — see Section 8's gap analysis for the reasoning.
- Certifications referenced in the new role-mapping table were verified against current (2026) provider documentation rather than assumed from training knowledge — sources listed at the end of this document.

**v4 (Aug 14, 2026) — Second judge-LLM pass, targeted fixes (no renumbering):**

- **Ch 15.2 expanded**: added **Evals as CI/CD Quality Gates** — flakiness management for non-deterministic trajectory tests, synthetic dataset sampling for CI, and cost-capped regression testing, so automated pipelines can run agent evals without flaky builds or runaway API spend.
- **Ch 10.3 expanded**: added **Agent State Versioning & In-Flight Migration** — handling schema evolution for long-running persistent agent state when prompts/tools/memory schemas change mid-execution.
- **Ch 7.5 ↔ 13.7 cross-linked**: named and cross-referenced **Task-Specific Tool-Calling Distillation** — training small, fast SLMs to emit reliable function calls for high-frequency micro-agent steps in place of expensive frontier-model calls.
- Phase flow reviewed and confirmed correct: Phase 5 → 6 → 7 → 8 → 9 → 10 → 11/12 remains the uninterrupted Practitioner line, with Phase 13 still the optional Advanced Infrastructure Track. No phases moved or renumbered in v4.

**v3 (Aug 14, 2026) — Judge-LLM critique integrated:**

- **Moved** "Building Your Own Language Models: LLMs & SLMs" from Phase 8 to **Phase 13**, explicitly relabeled an **Advanced Infrastructure Track**, so the main Practitioner flow now runs uninterrupted: Prompting (5) → RAG (6) → Fine-Tuning (7) → Agent Foundations (8) → ... . Everything that was Phase 9–13 shifted down to 8–12 to fill the gap; Phases 14–18 keep their numbers.
- **Added 13 new chapters and expanded 4 existing ones** across Phases 5, 6, 8, 10, 13, 15, and 16 to close the gaps the critique identified: structured-output/schema enforcement, hybrid deterministic/non-deterministic orchestration, agent sandboxing & code execution, context engineering for agents, semantic caching, synthetic data generation, inference optimization/speculative decoding, LLM gateway/router patterns, multi-layered agent evaluation, agent identity/OAuth-OBO, and Telecom/Finance use-case gaps (TM Forum, network slicing, quant backtesting).
- The curriculum still runs **Phase 0 through Phase 18** (chapter count grew from ~150 to ~165+ pages; phase count unchanged at 19).

### Gap → Resolution Table (traceability against the critique)

| Critique item | Resolution |
|---|---|
| Dynamic context pruning/summarization/compaction for agents | New **Ch 8.6**, Agent Foundations |
| Structured output & schema enforcement (Pydantic, JSON Schema, Instructor, Outlines, Guidance, SGLang) | New **Ch 5.4**, Prompt Engineering |
| Determinism vs. non-determinism / hybrid workflow orchestration (Temporal, Prefect, Durable Functions) | New **Ch 10.4**, Agentic Architectures |
| Agent sandboxing & code execution (e2b, Docker-in-Docker, gVisor, WASM) | New **Ch 10.5**, Agentic Architectures |
| Temporal/state persistence engines for long-running agents | Folded into expanded **Ch 10.3** (+ cross-linked from 10.4) |
| LLM Gateway & Router pattern as standalone chapter | New **Ch 15.6**, Enterprise AgentOps |
| Semantic vs. exact-match caching (GPTCache, Redis vector caching) | New **Ch 6.7**, RAG & Knowledge Systems |
| Synthetic data generation & distillation (UltraFeedback, Evol-Instruct) | New **Ch 13.7**, Build-Your-Own-LLM track |
| GraphRAG vs. relational/hybrid RAG deep dive | Expanded **Ch 6.5 / 6.6** |
| Speculative decoding & inference optimization (vLLM, TensorRT-LLM, FlashAttention-3) | New **Ch 13.10**, Build-Your-Own-LLM track |
| Agent identity, OAuth for agents, On-Behalf-Of (OBO) flow | Expanded **Ch 15.5** |
| Multi-layered agent evaluation (unit tests, trajectory eval, red-teaming, HITL loop) | Expanded **Ch 15.2** |
| Telecom gap: TM Forum Open APIs, network slice/SLA optimization | Added to **Ch 16.3** |
| Finance gap: quantitative backtesting & algorithmic execution | Added to **Ch 16.1** |
| Phase 8 placement disrupts Practitioner flow | **Phase 8 moved → Phase 13**, relabeled Advanced Infrastructure Track |

**v4 additions:**

| Critique item | Resolution |
|---|---|
| Non-deterministic agent evals in CI/CD without flaky builds or runaway cost | Expanded **Ch 15.2**: flakiness management, synthetic dataset sampling for CI, cost-capped regression testing |
| Agent state schema evolution / breaking changes mid-execution for long-running agents | Expanded **Ch 10.3**: agent state versioning & in-flight migration strategies |
| Distilling small, fast tool-calling specialist models for high-frequency micro-agent steps | Cross-linked **Ch 7.5 ↔ 13.7**: Task-Specific Tool-Calling Distillation |

---

## 1. Purpose & Design Philosophy

This is the master plan for a continuously growing, GitHub-hosted knowledge management site (KMS) that teaches working professionals AI from first principles through extremely advanced Agentic AI. Two things make this different from a typical tutorial series: every concept is taught at two altitudes (a plain-language high-level pass and a rigorous deep-dive pass), and every concept is grounded in real, comparable, industry-specific use cases rather than toy examples.

Four design principles run through the whole curriculum:

**Dual-altitude explanation.** Every concept chapter opens with an intuition-first explanation a non-specialist can follow, then descends into the mechanics — math where it matters, architecture diagrams, code where useful — for readers who need to build or defend the concept technically.

**Comparative framing.** Concepts are rarely taught in isolation. Each chapter places its subject next to the two or three things people confuse it with (RAG vs. fine-tuning, agent vs. workflow, LangGraph vs. CrewAI, OKF vs. RAG, deterministic DAGs vs. LLM-driven orchestration) and gives a straight answer on when to use which.

**Domain-grounded, not toy-grounded.** Every applicable chapter carries at least four worked use cases apiece in Financial Services, Healthcare, and Telecom — twelve per concept — so a learner in any of those industries can see the concept solving a problem that looks like their job. The Phase 16 domain deep dives go further with domain-native patterns (e.g., TM Forum APIs for Telecom, quant backtesting for Finance) beyond the standard 4×3 grid.

**Architecture-first for anything systems-level.** Wherever a concept has moving parts (RAG pipelines, agent loops, multi-agent topologies, enterprise agent platforms, gateway/routing layers), the chapter includes a labeled reference architecture diagram, not just prose.

Two phases in this plan (9 and 14) are deliberately **landscape/orientation phases** rather than full concept-standard phases — see Section 2.1 for how their lighter template differs from the standard seven-section contract. Phase 13 is a deliberately **advanced, optional infrastructure track** — see Section 3.

The curriculum runs in nineteen phases (Phase 0 through Phase 18), from "what is AI" through frontier agentic-AI research topics, capstone builds, and a contribution process so the site keeps growing after this initial plan is executed.

---

## 2. The Content Standard (applies to every concept chapter)

To keep quality consistent as dozens of contributors add chapters over time, every concept-level chapter in the foundational and agentic phases follows the same seven-section template. This is the "chapter contract" — a chapter isn't done until all seven sections are filled in.

1. **TL;DR / Intuition** — 3-5 sentences, no jargon, the elevator-pitch explanation plus one relatable analogy.
2. **High-Level Explanation** — how it works conceptually, for a working professional who won't implement it themselves; includes at least one custom diagram or illustration (SVG).
3. **Deep-Dive Explanation** — the technical mechanics: math, algorithms, pseudo-code, architecture, failure modes, and edge cases, for practitioners who will build with it.
4. **Comparison & Related Concepts** — a table contrasting this concept with 2-4 adjacent/competing concepts or technologies (what it is, is not, and when to reach for the alternative instead).
5. **Reference Architecture** (where applicable) — a labeled diagram showing how this concept fits into a real system, with component responsibilities called out.
6. **Industry Use Cases** — exactly 4 use cases each for Finance, Healthcare, and Telecom (12 total), each with: business problem, how the concept solves it, a one-paragraph solution sketch, and the primary risk/consideration to watch for in that domain.
7. **Check Your Understanding** — 3-5 self-check questions (and, where relevant, a small hands-on exercise linked to the capstone repo).

A reusable MDX template implementing this structure is specified in Section 4.4 so every new chapter starts from the same skeleton.

### 2.1 The Lighter "Landscape" Template (Phases 9 and 14 only)

Phases 9 (Agentic Frameworks Landscape) and 14 (Hyperscaler Foundations) exist specifically to give a **very high-level, breadth-first orientation** before the site goes deep elsewhere (Phase 12 for framework internals, Phase 15 for enterprise platform decisions). Chapters in these two phases use a reduced four-section template instead of the full seven:

1. **TL;DR / Intuition**
2. **High-Level Explanation** (what it is, who's behind it, what it's for — no implementation detail)
3. **Comparison Table** (HL trade-offs against its peers in the same landscape)
4. **Where to Go Deeper** (a pointer to the corresponding deep-dive chapter elsewhere in the curriculum)

Deep technical explanation, architecture diagrams, and the 4×3 domain use-case grid are intentionally deferred to the deep-dive phases these landscape phases point to, so the same ground isn't taught twice.

---

## 3. Learning Paths & Personas

The site should expose three suggested paths through the same content (via a landing page and sidebar filters), so different readers don't have to read all nineteen phases front-to-back:

- **Foundations Track** (new to AI): Phase 0 → 1 → 2 → 3 → 4 → 5, then a choice of RAG (Phase 6) or straight to Agent Foundations (Phase 8).
- **Practitioner / Builder Track** (some ML/GenAI experience, wants to build agents): Phase 5 → 6 → 7 → 8 → 9 (framework landscape) → 10 → 11 → 12, with capstones from Phase 18. This flow is now **uninterrupted** — Phase 13 (Build-Your-Own-LLM/SLM) sits outside the main line as an optional detour, not a required stop.
- **Advanced / Architect Track** (already building agentic systems, wants enterprise-grade and frontier depth): Phase 10 → 11 → 12 → 13 (optional infra track) → 14 (hyperscaler foundations) → 15 (enterprise governance) → 16 (domain deep dives) → 17 (frontier topics).

Each phase's index page states prerequisites explicitly so a reader arriving mid-curriculum knows what to backfill. **Phase 13 (Build-Your-Own-LLM/SLM) is explicitly labeled an Advanced Infrastructure Track** in the sidebar and landing page — most practitioners will fine-tune or use RAG rather than pretrain a model, but the material is there, positioned after the core agentic phases so it no longer interrupts the natural Prompting → RAG → Fine-Tuning → Agents flow that the v2 placement broke.

---

## 4. Learning-Site Architecture (Docusaurus + GitHub)

### 4.1 Stack

- **Framework:** Docusaurus 3 (React + MDX). Gives versioned docs, built-in sidebar/nav generation from folder structure, dark mode, i18n if needed later, and first-class Markdown/MDX so diagrams and interactive "use case cards" can be embedded as React components inside otherwise plain-Markdown chapters.
- **Diagrams:** Mermaid (via `@docusaurus/theme-mermaid`) for flow/sequence/architecture diagrams authored as text and version-controlled like code; hand-drawn/illustrative SVGs (concept illustrations, icon-style diagrams) authored separately (Excalidraw → exported SVG, or Figma → SVG) and stored as static assets. Mermaid for anything that will change often (architectures); static SVG for anything illustrative/decorative.
- **Search:** Algolia DocSearch (free for open-source docs) once the repo is public; local `@easyops-cn/docusaurus-search-local` as a placeholder until DocSearch is approved.
- **Hosting/CI:** GitHub Pages (or Vercel) via GitHub Actions — build + deploy on every merge to `main`; PR previews via Vercel or Netlify for content review.
- **Versioning:** Docusaurus docs versioning is available but not needed at launch — the site instead uses a visible **"Recently Added / Updated"** page (auto-generated from git history) to communicate continuous growth, since content additions matter more than API-style version snapshots here.

### 4.2 Repository Structure

```
regai-training/
├── docs/
│   ├── 00-orientation/
│   ├── 01-ai-ml-foundations/
│   ├── 02-deep-learning-foundations/
│   ├── 03-nlp-llm-foundations/
│   ├── 04-generative-ai-foundations/
│   ├── 05-prompt-engineering/                     # includes 5.4 structured output/schema enforcement
│   ├── 06-rag-knowledge-systems/                  # includes 6.7 semantic caching, 6.10 OKF
│   ├── 07-finetuning-alignment/
│   ├── 08-agents-foundations/                     # was 09- in v2; includes 8.6 context engineering
│   ├── 09-agentic-frameworks-landscape/           # was 10- in v2 — HL survey template
│   ├── 10-agentic-architectures/                  # was 11- in v2; includes 10.4 hybrid orchestration, 10.5 sandboxing
│   ├── 11-multi-agent-systems/                    # was 12- in v2
│   ├── 12-agentic-frameworks-protocols-deep-dive/ # was 13- in v2
│   ├── 13-build-your-own-llm-and-slm/             # MOVED from 08- in v2 — Advanced Infrastructure Track
│   ├── 14-hyperscaler-platforms/                  # HL survey template — unchanged position
│   ├── 15-enterprise-agentops-governance/         # includes 15.6 LLM gateway/router
│   ├── 16-domain-deep-dives/
│   │   ├── finance/                               # includes quant backtesting/algo execution
│   │   ├── healthcare/
│   │   └── telecom/                               # includes TM Forum APIs, network slicing
│   ├── 17-frontier-topics/
│   └── 18-capstones-and-contributing/
├── src/
│   └── components/
│       ├── UseCaseGrid.tsx        # renders the 4x3 domain use-case grid
│       ├── ComparisonTable.tsx    # standardized "vs" comparison table
│       ├── ArchitectureDiagram.tsx# wraps Mermaid + caption + component-responsibility list
│       ├── CheckYourUnderstanding.tsx
│       └── LearningPathCard.tsx
├── static/img/
│   ├── illustrations/             # hand-authored concept SVGs
│   └── architectures/             # exported architecture diagrams (if not inline Mermaid)
├── _templates/
│   ├── concept-chapter.mdx        # full 7-section skeleton (Section 2)
│   └── landscape-chapter.mdx      # lighter 4-section skeleton (Section 2.1), for Phases 9 & 14
├── .github/
│   ├── ISSUE_TEMPLATE/new-chapter-proposal.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/deploy.yml
├── docusaurus.config.ts
├── sidebars.ts                    # generated per-phase, mirrors docs/ folders; Phase 13 flagged "Advanced Track" in sidebar metadata
└── CONTRIBUTING.md
```

### 4.3 Continuous-Growth Workflow

1. New chapters start from an **issue** using the "new-chapter-proposal" template (concept, phase/chapter number, why it belongs, which domains' use cases are hardest to source).
2. Authoring happens on a branch, using the `_templates/concept-chapter.mdx` skeleton (or `landscape-chapter.mdx` for Phases 9/14) so the relevant content contract is enforced structurally, not just by convention.
3. PR review checklist (in `PULL_REQUEST_TEMPLATE.md`) mirrors the Content Standard: TL;DR present, HL + deep-dive both present (or HL + comparison only, for landscape chapters), comparison table present, architecture diagram present if applicable, 4 use cases × 3 domains present where required, self-check present.
4. Merge to `main` triggers the GitHub Actions build/deploy and the chapter automatically appears on the "Recently Added" page via a small script that reads git log dates per doc file.
5. A lightweight `CHANGELOG.md` (or an auto-generated "Release Notes" doc page) tracks phase completion percentage so the roadmap in Section 6 stays honest as a public tracker. Periodic **judge-LLM review passes** (like the one that produced v3) are recommended quarterly to catch new production patterns before they become gaps.

### 4.4 Concept Chapter Skeleton (starting point for every new page)

```mdx
---
title: "<Concept Name>"
phase: <0-18>
chapter: "<e.g. 10.4>"
prerequisites: ["<chapter-id>", "<chapter-id>"]
---

## TL;DR
<3-5 sentence intuition + analogy>

## High-Level Explanation
<conceptual walkthrough for a non-implementer>
<img/illustration>

## Deep-Dive Explanation
<mechanics, math, pseudo-code, failure modes>

## Comparison & Related Concepts
<ComparisonTable rows={[...]} />

## Reference Architecture
<ArchitectureDiagram mermaid={`...`} components={[...]} />

## Industry Use Cases
<UseCaseGrid
  finance={[4 use cases]}
  healthcare={[4 use cases]}
  telecom={[4 use cases]}
/>

## Check Your Understanding
<CheckYourUnderstanding questions={[...]} />
```

---

## 5. Full Curriculum Map

Nineteen phases (0–18). Each chapter listed below is a page (or small page cluster) in the site. Chapters in Phases 1–8, 10–13, and 15–18 follow the full seven-section Content Standard from Section 2, including the 4×3 domain use-case grid where the concept is domain-applicable. Chapters in **Phases 9 and 14** (marked "HL survey") intentionally use the lighter four-section landscape template from Section 2.1. **New or expanded chapters from the v3 judge-critique pass are marked `[v3]`; the v4 follow-up fixes are marked `[v4]`; the v5 AI Roles chapter and its gap-fill chapters are marked `[v5]`.**

### Phase 0 — Program Orientation *(orientation, not concept-standard)*

- 0.1 Welcome & How to Use This Knowledge Base
- 0.2 Learning Paths & Personas (Foundations / Practitioner / Advanced Architect)
- **0.3 `[v5]` AI Roles in the Market: Definitions, Responsibilities & Your Curriculum Path** — a market map of the ~15 major AI/agentic job roles (from Data Scientist through Multi-Agent Systems Architect through AI Governance Specialist), what each role is actually responsible for day to day, which phases/chapters of this curriculum are core vs. supplementary for that role, what's deliberately out of this curriculum's scope for that role (with pointers elsewhere), and which industry certifications are worth pursuing per role. Full reference table in **Section 8** below; this chapter is that table plus the narrative explanation.
- 0.4 Prerequisites Self-Assessment
- 0.5 Glossary & Notation Conventions
- 0.6 The Content Standard, Explained to Learners

### Phase 1 — AI & Machine Learning Foundations

- 1.1 What Is Artificial Intelligence? History, AI Winters, Narrow vs. General AI
- 1.2 A Taxonomy of AI: Rule-Based → ML → Deep Learning → Generative → Agentic
- 1.3 Machine Learning Foundations: Supervised, Unsupervised, Reinforcement Learning
- 1.4 Core ML Concepts: Features, Train/Validation/Test, Bias-Variance, Overfitting
- 1.5 Classical ML Algorithms Landscape (Regression, Trees/Forests, SVM, Clustering) — Comparison
- 1.6 Evaluation Metrics (Accuracy, Precision/Recall, F1, ROC-AUC, RMSE)
- 1.7 Data Foundations: Pipelines, Feature Engineering, Data Quality
- 1.8 Math Refresher for AI: Linear Algebra, Probability, Statistics, Optimization
- 1.9 Ethics & Responsible AI Foundations (Bias, Fairness, Explainability Primer)

### Phase 2 — Deep Learning Foundations

- 2.1 Neural Networks 101: From Perceptron to MLP
- 2.2 Backpropagation & Optimization (Gradient Descent, Momentum, Adam, LR Schedules)
- 2.3 Convolutional Neural Networks: Architecture & Use Cases
- 2.4 Sequence Models Before Transformers: RNN, LSTM, GRU
- 2.5 The Transformer Architecture — Deep Dive (Self-Attention, Multi-Head Attention, Positional Encoding)
- 2.6 Transfer Learning & the Pretrain-Then-Adapt Paradigm
- 2.7 Deep Learning Frameworks Compared (PyTorch vs. TensorFlow vs. JAX)
- 2.8 Hardware for AI: GPUs, TPUs, Training vs. Inference Compute Economics

### Phase 3 — NLP & Language Model Foundations

- 3.1 NLP Fundamentals: Tokenization, Embeddings, Vector Semantics
- 3.2 From Word2Vec to Contextual Embeddings (BERT-Era Shift)
- 3.3 Language Modeling Objectives: Causal LM vs. Masked LM vs. Seq2Seq
- 3.4 Evolution of LLMs: GPT / BERT / T5 Families — Encoder vs. Decoder vs. Encoder-Decoder Compared
- 3.5 Tokenizers Deep Dive: BPE, WordPiece, SentencePiece
- 3.6 Scaling Laws & Emergent Abilities
- 3.7 The 2026 Model Landscape: Open vs. Closed, Size Classes, Choosing a Base Model

### Phase 4 — Generative AI Foundations

- 4.1 What Is Generative AI? Generative vs. Discriminative Models
- 4.2 Generative Model Families Compared: LLMs, Diffusion Models, GANs, VAEs
- 4.3 How LLMs Generate Text: Decoding Strategies (Greedy, Beam, Top-k/Top-p, Temperature)
- 4.4 Multimodal Generative AI: Text-to-Image, Text-to-Video, Speech
- 4.5 Context Windows, Memory Limits & Cost/Latency Trade-offs
- 4.6 Hallucination: Causes, Types, and Mitigation Strategies (Primer)
- 4.7 Responsible GenAI: Content Safety, Watermarking, Provenance

### Phase 5 — Prompt Engineering & LLM Application Development

- 5.1 Prompting Fundamentals: Zero-Shot, Few-Shot, Instruction Following
- 5.2 Advanced Prompting Patterns: Chain-of-Thought, Self-Consistency, Tree-of-Thought
- 5.3 Structured Outputs & Tool/Function Calling — the Basics
- **5.4 `[v3]` Structured Output Enforcement & Constrained Decoding — Deep Dive**: schema-first generation with Pydantic/JSON Schema, libraries (Instructor, Outlines), and grammar-constrained decoding engines (Guidance, SGLang) — why "ask nicely for JSON" fails at scale and what replaces it in production tool-calling pipelines.
- 5.5 System Prompts, Guardrails & Prompt-Injection Defense
- 5.6 Prompt Optimization & Evaluation (Versioning, A/B Testing Prompts)
- 5.7 Architecture Patterns for Your First LLM App (API Wrapper → Chat App → Workflow)
- 5.8 Prompting vs. Fine-Tuning vs. RAG — A Decision Framework

### Phase 6 — Retrieval-Augmented Generation & Knowledge Systems

- 6.1 Why RAG? The Limits of Parametric Knowledge
- 6.2 Embeddings & Vector Search Foundations
- 6.3 Vector Databases Compared (Pinecone, Weaviate, Milvus, pgvector, FAISS, Chroma)
- 6.4 RAG Architecture Deep Dive: Ingestion, Chunking, Retrieval, Reranking, Generation
- 6.5 Advanced RAG Patterns: Hybrid Search, Reranking, HyDE, **`[v3 expanded]` GraphRAG vs. Relational/Hybrid RAG** (LLM-driven knowledge-graph extraction, when graph traversal beats vector similarity, and hybrid retrieval that blends both), Agentic RAG
- 6.6 Knowledge Graphs + LLMs *(cross-linked with 6.5's GraphRAG deep dive)*
- **6.7 `[v3]` Caching Infrastructure for GenAI & Agents**: exact-match caching vs. semantic caching (GPTCache, Redis vector caching) for cutting cost and latency in repeated agent-loop calls; cache invalidation strategies for RAG-backed answers.
- 6.8 Evaluating RAG Systems: Retrieval Metrics, Faithfulness, RAGAS
- 6.9 RAG Reference Architecture Blueprint
- 6.10 Open Knowledge Format (OKF): A Portable, Agent-Readable Knowledge Standard — Google Cloud's June 2026 open specification: markdown files with YAML frontmatter, cross-linked into a knowledge graph, designed so producers (data teams, enrichment agents) and consumers (agents, search indexes, visualizers) can share curated organizational knowledge without a proprietary SDK or vector index. Covers the bundle structure and required/reserved metadata fields, how agents read *and update* OKF documents (vs. static document search), and a direct **OKF vs. RAG/vector-DB comparison**. Use cases: a Finance data-catalog agent that documents its own tables via OKF, a Healthcare clinical-terminology wiki an agent keeps current, a Telco network-inventory knowledge base agents both read and maintain.

### Phase 7 — Fine-Tuning, Alignment & Model Customization

- 7.1 When to Fine-Tune vs. Prompt vs. RAG: A Decision Framework
- 7.2 Full Fine-Tuning vs. Parameter-Efficient Fine-Tuning (LoRA, QLoRA, Adapters, Prefix-Tuning) — Compared
- 7.3 Alignment Techniques Deep Dive: Instruction Tuning, RLHF, RLAIF, DPO
- 7.4 Domain Adaptation & Continual Pretraining
- 7.5 Model Compression: Distillation, Quantization, Pruning *(`[v4]` cross-linked with 13.7 for **Task-Specific Tool-Calling Distillation** — training small, fast SLMs to reliably emit function calls for high-frequency micro-agent steps, replacing expensive frontier-model calls in production loops)*
- 7.6 Evaluating & Benchmarking Fine-Tuned Models
- 7.7 Deployment Considerations for Custom Models *(cross-links to 13.10 Inference Optimization for serving-time depth)*

### Phase 8 — AI Agents: Foundations

- 8.1 What Is an "Agent"? From Classical AI Agents to LLM Agents
- 8.2 Anatomy of an LLM Agent: Perception, Reasoning, Memory, Action, Tools
- 8.3 The Agent Loop: Plan → Act → Observe → Reflect (ReAct and Beyond)
- 8.4 Tool Use & Function Calling — Deep Dive
- 8.5 Memory Systems for Agents: Short-Term, Long-Term, Episodic, Semantic — Compared
- **8.6 `[v3]` Context Engineering for Agents**: dynamic context pruning, rolling summarization, and context-compaction strategies for long, multi-turn agent loops — why high-step agents fail (context overflow and mid-context "distraction") and the patterns that prevent it, building directly on 8.5's memory systems and 4.5's context-window limits.
- 8.7 Planning & Reasoning Strategies: CoT, ReAct, Reflexion, Plan-and-Execute, Graph-of-Thought
- 8.8 Terminology Untangled: Agent vs. Workflow vs. Assistant vs. Copilot vs. Chatbot
- **8.9 `[v5]` Conversational & Agent UX Design**: turn-taking, clarification-seeking, trust calibration (when an agent should show its reasoning vs. just act), progress/status disclosure during long-running tool calls, and error recovery patterns for user-facing agents — the human-interaction layer that the Conversational AI Designer role (Section 8) needs and the rest of the curriculum doesn't otherwise cover.
- 8.10 Single-Agent Reference Architecture Blueprint *(was 8.9)*

### Phase 9 — Agentic Frameworks Landscape (High-Level Survey) *(HL survey template)*

- 9.1 Why an Ecosystem Landscape Chapter? How to Read This Phase
- 9.2 Orchestration Frameworks at a Glance: LangChain/LangGraph, CrewAI, AutoGen, Semantic Kernel, OpenAI Agents SDK — What Each One Is, in Plain Language
- 9.3 Cloud-Native Agent Builders at a Glance: Google Agent Development Kit (ADK) / Vertex AI Agent Builder, AWS Bedrock Agents, Microsoft Azure AI Foundry Agent Service / Copilot Studio, Oracle AI Agent Studio *(points forward to Phase 14 for platform depth)*
- 9.4 Protocol Layer at a Glance: MCP and A2A in One Page *(points forward to Phase 12 for the deep dive)*
- 9.5 Open-Source vs. Managed/Proprietary Frameworks — HL Trade-offs
- 9.6 How to Pick a Starting Framework for Your First Project (a simple decision flowchart)
- 9.7 Landscape Comparison Table: Framework, Backing Org, License, Best For, Learning Curve

### Phase 10 — Agentic AI Architectures & Design Patterns

- 10.1 The Four Core Agentic Design Patterns: Reflection, Tool Use, Planning, Multi-Agent Collaboration
- 10.2 Reactive vs. Deliberative vs. Hybrid Agent Architectures
- 10.3 State-Machine & Graph-Based Agent Orchestration *(`[v3 expanded]` now includes Temporal-style durable execution engines and state-persistence patterns for agent state that must survive app restarts or span multi-day asynchronous workflows; `[v4 expanded]` also covers **Agent State Versioning & In-Flight Migration** — handling schema evolution for long-running, persistent agent state when system prompts, tool signatures, or memory schemas change mid-execution, via versioned state schemas, migration functions for in-flight instances, and safe rollout patterns like dual-write and shadow migration so breaking changes don't strand running agents)*
- **10.4 `[v3]` Hybrid Deterministic / Non-Deterministic Orchestration**: why critical-path steps shouldn't be left to free-form LLM step selection, and how to combine deterministic state machines/DAGs (Temporal, Prefect, Azure Durable Functions) with non-deterministic LLM agent nodes in one workflow — includes a decision framework for which steps go in which layer.
- **10.5 `[v3]` Agent Sandboxing & Code Execution Environments**: how agents securely execute LLM-generated Python/Bash — e2b, Docker-in-Docker, gVisor, and WASM sandboxes compared on isolation strength, startup latency, and cost; ties forward to 15.4's security chapter.
- 10.6 Human-in-the-Loop Patterns: Approval Gates, Escalation, Oversight
- 10.7 Error Handling, Self-Correction & Guardrails in Agents
- 10.8 Agent Autonomy Levels (L0–L5 Framework) — Compared
- 10.9 Cost, Latency & Reliability Engineering for Agents
- 10.10 Reference Architectures: RAG Agent, Tool-Using Agent, Autonomous Research Agent

### Phase 11 — Multi-Agent Systems & Orchestration

- 11.1 Why Multi-Agent? Decomposition, Specialization, Parallelism
- 11.2 Multi-Agent Topologies: Sequential, Hierarchical, Peer-to-Peer, Debate, Blackboard — Compared
- 11.3 Agent Communication Protocols & Message Passing
- 11.4 Role Design & Prompt Specialization for Sub-Agents
- 11.5 Coordination, Consensus & Conflict Resolution Among Agents
- 11.6 Shared Memory & State Management Across Agents
- 11.7 Multi-Agent Orchestration Frameworks Compared (LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Semantic Kernel)
- 11.8 Multi-Agent Reference Architecture Blueprints

### Phase 12 — Agentic AI Tooling, Frameworks & Protocols (Deep Dive)

- 12.1 Framework Landscape Recap & Selection Criteria *(links back to Phase 9)*
- 12.2 LangChain & LangGraph — Deep Dive
- 12.3 CrewAI — Deep Dive
- 12.4 AutoGen & Semantic Kernel — Deep Dive
- 12.5 OpenAI Agents SDK / Assistants API — Deep Dive
- 12.6 Model Context Protocol (MCP) — Deep Dive & Architecture
- 12.7 Agent-to-Agent (A2A) Protocols & Interoperability Standards
- 12.8 The Wider Tool Ecosystem: Vector Stores, Orchestration, Observability
- 12.9 Framework Comparison Matrix (Features, Maturity, Ecosystem, Learning Curve)

### Phase 13 — Building Your Own Language Models: LLMs & SLMs *(`[v3 moved]` Advanced Infrastructure Track — optional, moved here from Phase 8 in v2)*

> **Why this moved:** in v2, this phase sat between Fine-Tuning and Agent Foundations, forcing every reader through low-level distributed-training infrastructure before they could reach agents — the thing most Practitioners actually came for. It now sits after the core agentic phases (8–12), clearly flagged as an advanced/optional track, so the main learning line stays Prompting → RAG → Fine-Tuning → Agents without a detour.

- 13.1 Why Build Your Own Model? Build vs. Buy vs. Fine-Tune — A Decision Framework
- 13.2 Pretraining Data Pipelines: Sourcing, Cleaning, Deduplication, Filtering, Licensing & Copyright Considerations
- 13.3 Tokenizer Design & Training for a New Model
- 13.4 Model Architecture Design Choices: Dense vs. Mixture-of-Experts (MoE), Context-Length Strategies, Positional Encoding Choices
- 13.5 Distributed Training Infrastructure: Data/Tensor/Pipeline Parallelism, ZeRO/FSDP, Checkpointing
- 13.6 The Pretraining Run: Curriculum, Hyperparameters, Loss Curves, Compute Budgeting (Chinchilla-Style Scaling)
- **13.7 `[v3]` Synthetic Data Generation & Data Distillation**: building high-quality instruction-following datasets with frontier models (UltraFeedback- and Evol-Instruct-style patterns) to train lower-cost domain SLMs — data-quality filtering, diversity control, and avoiding synthetic-data collapse. `[v4]` Includes **Task-Specific Tool-Calling Distillation** as a named enterprise pattern (cross-linked with 7.2/7.5): capturing frontier-model tool-call trajectories, filtering for schema-valid and successful calls, and distilling them into a small function-calling-specialist SLM for high-frequency micro-agent steps.
- 13.8 Post-Training Your Base Model: SFT, RLHF/DPO Recap & Model Cards (cross-links Phase 7)
- 13.9 Evaluating a Newly Trained Base Model: Benchmarks, Contamination Checks, Red-Teaming
- **13.10 `[v3]` Inference Optimization & Speculative Decoding**: vLLM, TensorRT-LLM, and FlashAttention-3 for serving throughput; speculative decoding mechanics and when it pays off; cross-linked from 7.7's deployment chapter.
- 13.11 Small Language Models (SLMs): What They Are, Why They Exist, and When to Choose One Over an LLM
- 13.12 Building SLMs: Distillation from Larger Models, Pruning, and Architecture Choices for On-Device/Edge Deployment *(draws on 13.7's synthetic-data patterns)*
- 13.13 LLM vs. SLM — Comparison Table (Capability, Cost, Latency, Privacy, Deployment Footprint)
- 13.14 Case Study Blueprint: Standing Up a Small, Domain-Specific Model End-to-End

### Phase 14 — Hyperscaler AI & Agentic Platforms: High-Level Foundations *(HL survey template)*

- 14.1 Why Hyperscaler Platforms Matter for Enterprise Agentic AI
- 14.2 Google Cloud AI & Agentic Foundations: Vertex AI, Gemini Models, Agent Builder/ADK, and OKF (Section 6.10) as a Google Cloud–Originated Knowledge Standard
- 14.3 AWS AI & Agentic Foundations: Bedrock, SageMaker, Bedrock Agents, Amazon Q
- 14.4 Microsoft AI & Agentic Foundations: Azure OpenAI, Azure AI Foundry, Copilot Studio, Semantic Kernel
- 14.5 Oracle AI & Agentic Foundations: OCI AI Services, Oracle Cloud AI Agent Studio, Fusion AI
- 14.6 Other Notable Platforms (Brief Pointers): IBM watsonx, NVIDIA AI Enterprise/NIM
- 14.7 Hyperscaler Comparison Matrix: AI/ML Services, Agent Tooling, Pricing Model, Data Residency, Compliance Certifications
- 14.8 Multi-Cloud & Portability Considerations for Agentic AI
- 14.9 Choosing a Hyperscaler: A Decision Framework Tied to Domain Needs (Finance/Health/Telco Compliance Considerations)

### Phase 15 — Enterprise Agentic AI: Governance, Security, Evaluation & Operations

- 15.1 The AgentOps/LLMOps Lifecycle: Dev → Eval → Deploy → Monitor → Improve
- **15.2 `[v3/v4 expanded]` Evaluating Agentic Systems — The Multi-Layered Testing Pyramid**: deterministic unit/assertion testing at the base, trajectory evaluation (was the tool-call sequence optimal, not just the final answer?), LLM-as-judge scoring, automated red-teaming/vulnerability benchmarking, and a human-in-the-loop feedback integration loop that feeds evaluation findings back into prompts/fine-tuning data. `[v4]` Also covers **Evals as CI/CD Quality Gates**: flakiness management for non-deterministic trajectory tests (retry/quorum voting on judge calls so a single noisy run doesn't fail a build), synthetic dataset sampling for CI (a small, representative regression set on every commit instead of the full eval suite), and cost-capped regression testing (a hard budget ceiling per pipeline run, with the full suite deferred to a scheduled nightly job).
- 15.3 Observability & Tracing for Agents (Tooling Compared)
- 15.4 Security for Agentic AI: Prompt Injection, Tool Misuse, Data Exfiltration, Sandboxing *(cross-links 10.5's sandboxing/code-execution deep dive)*
- **15.5 `[v3 expanded]` Identity, Access & Permissions for Agents**: agent service accounts and non-human identity, OAuth for agents, user delegation, and the OAuth2 On-Behalf-Of (OBO) flow for agents acting on behalf of an enterprise employee, plus least-privilege design.
- **15.6 `[v3]` LLM Gateway & Router Patterns**: semantic routing across models, fallback chains, multi-region load balancing, and rate-limiting at the gateway layer (LiteLLM, Portkey, Kong AI Gateway) — the standalone deep dive the v2 plan only gestured at from the enterprise architecture diagram.
- 15.7 Governance, Risk & Compliance: NIST AI RMF, ISO 42001, EU AI Act — Mapped to Agentic AI
- 15.8 Cost Management & FinOps for Agentic Systems *(cross-links 15.6's gateway chapter and 6.7's caching chapter as primary cost levers)*
- 15.9 Responsible AI & Human Oversight for Autonomous Agents
- 15.10 Enterprise Reference Architecture: Landing Zone, Guardrails, Model Gateway (→ 15.6), Agent Registry
- **15.11 `[v5]` AI Product Strategy: Business Case, ROI Modeling & Build-Measure-Learn for Agentic Products**: how an AI Product Manager scopes and justifies an agentic AI initiative — cost-of-build vs. cost-of-status-quo framing, leading/lagging metrics for agent products, staged rollout (pilot → limited release → full production) tied back to the autonomy-level framework in 10.8, and a lightweight business-case template.

### Phase 16 — Domain Deep Dives: Finance, Healthcare, Telecom *(capstone-depth modules)*

- **16.1 `[v3 expanded]` Financial Services Agentic AI** — Regulatory Landscape (SR 11-7, SEC, MAS) + Core Use Cases: Research Copilot, Underwriting Agent, Fraud-Investigation Agent, Compliance-Monitoring Agent, and **Quantitative Backtesting & Algorithmic Execution Agent** (backtesting agent-driven strategies against historical market data before live deployment, and the guardrails that belong around automated execution) + Architecture Blueprint
- 16.2 Healthcare Agentic AI — Regulatory Landscape (HIPAA, FDA SaMD, Clinical Safety) + Core Use Cases (Clinical Documentation Agent, Prior-Authorization Agent, Care-Coordination Agent, Clinical-Trial-Matching Agent) + Architecture Blueprint
- **16.3 `[v3 expanded]` Telecom Agentic AI** — Regulatory/Operational Landscape + Core Use Cases: Network-Ops/AIOps Agent, Customer-Care Agent, Churn-Prevention Agent, Field-Service Dispatch Agent, **TM Forum Open API-Driven Agent Workflow Integration** (standardizing agent-to-BSS/OSS interactions via TM Forum Open APIs), and **Network Slice Management & SLA Optimization Agent** (real-time decision agents managing 5G network slices against SLA commitments) + Architecture Blueprint
- 16.4 Cross-Domain Patterns & Lessons Learned — Comparison Table

### Phase 17 — Advanced & Frontier Agentic AI Topics

- 17.1 Autonomous, Long-Horizon Agents (Continuous-Operation Agent Lineage)
- 17.2 Multi-Modal Agents: Vision, Voice, Computer-Use / Browser-Use Agents
- 17.3 Bridge to Embodied AI & Robotics-Adjacent Agentic Workflows
- 17.4 Self-Improving Agents & Automated Prompt/Tool Optimization
- 17.5 Agent Economies & Multi-Agent Marketplaces (Agent-to-Agent Negotiation & Payments)
- 17.6 Reasoning Models & Test-Time Compute — Impact on Agent Design
- 17.7 AI Safety & Alignment for Autonomous Agentic Systems (Frontier Risk Primer)
- 17.8 Simulation & Evaluation Environments for Agents (SWE-bench, WebArena, AgentBench — Compared)
- 17.9 Emerging Standards & the Road Ahead *(living page, updated continuously — tracks things like OKF's evolution, new gateway/caching tooling, and any successors)*

### Phase 18 — Capstones, Projects & Contribution Path

- 18.1 Capstone Project Briefs — One End-to-End Agent Build per Domain (Finance / Health / Telecom)
- 18.2 Build-Along Tutorials (Step-by-Step, Linked to Companion Code Repo)
- 18.3 Portfolio & Assessment Rubric
- 18.4 Suggested Certification / External Learning-Path Mapping
- 18.5 Contribution Guide — How New Chapters and Use Cases Get Added as the Site Grows

---

## 6. AI Roles in the Market — Full Reference (Content Draft for Chapter 0.3)

This section is the working content for the new Chapter 0.3. It exists so a reader — or a hiring manager, or someone mapping their own career — can go from "what job am I aiming for" straight to "which chapters do I actually need," without reading all nineteen phases to find out.

### 6.1 Role Map

Fifteen roles cover the AI/agentic job market as of 2026, grouped into six clusters. "Core Curriculum Path" lists the phases that role should treat as required reading; everything else in the curriculum is optional depth for that role.

| Role | What They Actually Do | Core Curriculum Path | Recommended Certifications |
|---|---|---|---|
| **Data Scientist** | EDA, feature engineering, classical ML model selection/tuning, translating findings into business recommendations | Phase 1 (full), 2.1–2.2, 4.1 | AWS Certified Machine Learning Engineer – Associate; Google Cloud Professional Machine Learning Engineer; Azure Data Scientist Associate (DP-100) |
| **Data Engineer (AI-Focused)** | Builds/maintains ingestion pipelines, feature stores, and the plumbing that feeds training data and RAG corpora | 1.7, 6.2–6.4, 6.7, 13.2 (advanced) | Google Cloud Professional Data Engineer; AWS Certified Data Engineer – Associate *(general data-eng certs — complementary, not AI-specific)* |
| **Generative AI Engineer / LLM App Developer** | Builds production LLM-powered apps: prompt pipelines, RAG integration, vector DB wiring, output validation | Phases 3–6 (full), 5.4, 15.2 | AWS Certified AI Practitioner; Google Cloud Generative AI Leader; Azure AI Engineer Associate (AI-102); Databricks Certified Generative AI Engineer Associate |
| **Prompt Engineer** *(increasingly folded into the GenAI Engineer role)* | Prompt design, testing, versioning, few-shot curation, guardrail authoring | Phase 5 (full), esp. 5.1, 5.2, 5.4, 5.6 | Same as GenAI Engineer, above |
| **LLM / Foundation Model Engineer** | Pretrains and fine-tunes base models; manages distributed training infra; evaluates base-model quality | Phase 2 (full), Phase 7 (full), Phase 13 (full) | NVIDIA-Certified Associate: Generative AI; Databricks Certified Generative AI Engineer Associate (partial); a cloud ML-engineer cert as infra baseline |
| **AI Agent Developer / Agentic AI Engineer** | Builds single-agent and tool-using agents; implements memory/context management; integrates a framework | Phase 8 (full), Phase 9, Phase 10 (full), relevant part of Phase 12 | No dedicated agentic-AI certification exists industry-wide yet (verified 2026) — closest proxies are framework-specific learning paths (LangChain Academy, CrewAI) and cloud agent-builder training paths (AWS/Google/Azure) |
| **Multi-Agent Systems Architect** | Designs multi-agent topologies, inter-agent protocols, coordination/consensus strategies at scale | Phase 10 (full, incl. 10.4/10.5), Phase 11 (full), Phase 12 (full) | Same as Agent Developer, above, plus a general architecture credential (e.g., TOGAF) if operating at enterprise-architect level |
| **AI Solutions / Enterprise Architect** | End-to-end architecture spanning model, data, agent, and platform layers; hyperscaler selection; landing-zone design | Phase 14 (full), Phase 15 (full), relevant Phase 16 domain | Pair a cloud AI cert with that provider's architect cert: Google Cloud Generative AI Leader + Professional Cloud Architect; AWS Certified AI Practitioner + Solutions Architect Professional; Azure AI Engineer Associate + Solutions Architect Expert; OCI AI Foundations Associate + OCI Generative AI Professional |
| **MLOps / LLMOps / AgentOps Engineer** | CI/CD for models and agents, evaluation pipelines, observability, FinOps | Phase 15 (full, esp. 15.1–15.3, 15.6, 15.8) | Databricks Certified Generative AI Engineer Associate; a cloud ML-engineer cert; general SRE/DevOps certs as complementary background |
| **AI Platform / Infrastructure Engineer** | GPU/TPU cluster management, distributed-training infra, inference-serving optimization | 2.8, 13.5, 13.10 | NVIDIA-Certified Associate: Generative AI; NVIDIA AI infrastructure training; cloud architect-level certs |
| **AI Security Engineer / Red-Teamer** | Adversarial testing, prompt-injection defense, execution-sandboxing review, vulnerability benchmarking | 10.5, 15.2 (red-teaming sub-section), 15.4 | OWASP Top 10 for LLM Applications training/certificate; general security credentials (CISSP, OSCP) as complementary background — no mature AI-specific security cert exists industry-wide yet |
| **AI Governance, Risk & Compliance (GRC) Specialist** | Regulatory mapping (EU AI Act, NIST AI RMF, ISO 42001), risk assessments, model-risk management | 1.9, 15.6, 15.7, 15.9 | IAPP AI Governance Professional (AIGP); ISO/IEC 42001 Lead Implementer or Lead Auditor; NIST AI RMF practitioner training |
| **Responsible AI / AI Ethics Lead** | Bias/fairness audits, human-oversight design, ethics-review processes | 1.9, 15.9 | Same governance certs as GRC Specialist, above, plus a university/Coursera Responsible AI specialization |
| **AI Product Manager** | Defines agentic-product requirements, prioritizes use cases, owns the business case/ROI, cross-functional coordination | Phase 0 (full), 5.7–5.8, relevant Phase 16 domain, **15.11 `[v5]`** | Google Cloud Generative AI Leader; an AI-focused product-management certificate program; general PM credentials (CSPO, etc.) as complementary background |
| **Domain-Specific AI Specialist** *(e.g., Quant AI Engineer/Finance, Clinical AI Specialist/Health, Network AI Engineer/Telco)* | Applies the full agentic stack to one regulated domain's workflows | Full technical stack (Phases 5–12) + relevant **Phase 16** domain chapter + 15.6/15.7 mapped to that domain | One hyperscaler AI cert (any provider) **plus** a domain credential — e.g., a finance/AI credential for Quant roles, HIMSS-style health-IT credentials for Clinical AI, TM Forum certifications for Telco |

### 6.2 Gap Analysis — What This Exercise Found Missing

Building the role map above meant checking every role's real day-to-day needs against the nineteen phases already planned. Two genuine gaps surfaced and are now closed (see Section 5):

- **Conversational & Agent UX design** had no home anywhere in the curriculum — prompting (Phase 5) covers how to talk *to* a model, and agent architecture (Phase 8) covers how an agent reasons, but nothing covered how a user-facing agent should *behave toward a human* (when to explain itself, how to recover from a misunderstood request, how to signal it's still working on a long tool call). Closed with new **Chapter 8.9**.
- **AI Product Strategy / business case building** was assumed but never taught — the AI Product Manager role showed up constantly in the mapping table but had no chapter that was actually theirs. Closed with new **Chapter 15.11**.

Two other needs surfaced but were deliberately left **out of scope**, with a stated reason rather than a chapter added just to check a box:

- **General-purpose data engineering at scale** (Spark/Flink/Airflow, streaming architectures, warehouse modeling) is a full discipline of its own; this curriculum covers the AI-specific slice of it (1.7, 6.2–6.4) and treats broader data-engineering skill as a prerequisite/complementary track rather than something to re-teach here.
- **Academic ML research methodology** (experimental design, causal inference, novel architecture research) is what separates an Applied Research Scientist from an ML Engineer; this curriculum is built for working professionals applying AI, not for research-degree-level theory, so it points to academic/university resources rather than adding that depth here.

### 6.3 How This Differs From Chapter 18.4

Chapter 18.4 ("Suggested Certification / External Learning-Path Mapping," Phase 18) still exists and isn't redundant with this one: **Chapter 0.3** (this section) is the *entry-point* map — "here's the job market, here's your role, here's your path" — read before a learner starts. **Chapter 18.4** is the *exit-point* detail — specific exam-prep guidance, study-plan sequencing, and external course links for the certifications a learner has decided to pursue after finishing their track.

---

## 7. Build Roadmap (Suggested Milestones)

| Milestone | Scope | Deliverable |
|---|---|---|
| M0 | Repo & site scaffold | Docusaurus site live on GitHub Pages with Phase 0 content (incl. `[v5]` the AI Roles map, 0.3), empty phase shells, both chapter templates, CI/CD |
| M1 | Phases 1–2 | AI/ML + Deep Learning foundations fully written to Content Standard |
| M2 | Phases 3–4 | NLP/LLM + Generative AI foundations |
| M3 | Phase 5 | Prompting, incl. `[v3]` structured-output/constrained-decoding chapter (5.4) |
| M4 | Phase 6 | RAG & Knowledge Systems, incl. `[v3]` semantic caching (6.7) and OKF (6.10) |
| M5 | Phase 7 | Fine-Tuning & Alignment |
| M6 | Phase 8 | Agent Foundations, incl. `[v3]` context-engineering chapter (8.6) and `[v5]` Conversational & Agent UX Design (8.9) |
| M7 | Phases 9–12 | Framework landscape survey, Architectures (incl. `[v3]` hybrid orchestration 10.4 and sandboxing 10.5), Multi-Agent, deep framework/protocol dives — the flagship agentic core |
| M8 | Phase 13 | Advanced Infrastructure Track (Build-Your-Own-LLM/SLM), incl. `[v3]` synthetic data (13.7) and inference optimization (13.10) |
| M9 | Phase 14 | Hyperscaler platform foundations |
| M10 | Phase 15 | Enterprise AgentOps/Governance, incl. `[v3]` expanded evaluation (15.2), expanded identity/OAuth (15.5), new gateway/router chapter (15.6), and `[v5]` AI Product Strategy (15.11) |
| M11 | Phase 16 | Finance/Health/Telco domain deep dives, incl. `[v3]` quant backtesting and TM Forum/network-slicing use cases |
| M12 | Phases 17–18 | Frontier topics + Capstones; open contribution process goes live |

Each milestone ships as a deployed increment (the site is public and growing from M0 onward, not held back for a "big launch"), consistent with the "continuously growing" requirement. Note M6/M7 are now sequential and uninterrupted (no infrastructure detour), and M8 (the former early-Phase-8 material) has moved later in the build order to match its new position in the curriculum.

---

## 8. Immediate Next Steps

1. v5 adds the AI Roles map (0.3) and its two gap-fill chapters (8.9, 15.11) on top of a curriculum that already passed two rounds of judge-LLM review — ready to scaffold. (v3 covered the Phase 8 move and ~15 new/expanded chapters; v4 closed three production blind spots; v5 adds role-to-chapter traceability so the site can answer "what do I need to learn for job X" directly.)
2. Scaffold the GitHub repo and Docusaurus site per Section 4.2 (I can do this next).
3. Build the reusable MDX components (`UseCaseGrid`, `ComparisonTable`, `ArchitectureDiagram`) referenced in Section 4.4, plus the lighter `landscape-chapter.mdx` template for Phases 9 and 14.
4. Write Phase 0 and the first 2-3 Phase 1 chapters as a quality baseline for future contributors to match.
5. Set up the GitHub Actions deploy pipeline so the site is live and growable from day one.
6. Consider scheduling a recurring judge-LLM review pass (quarterly) against the live site, the same way this v3 pass was produced, to keep pace with new production patterns.

---

## Sources

**For the OKF chapter (6.10), verified Aug 14, 2026:**

- [Google Cloud Blog — How the Open Knowledge Format can improve data sharing](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
- [MarkTechPost — Google Cloud Introduces Open Knowledge Format (OKF)](https://www.marktechpost.com/2026/06/16/google-cloud-introduces-open-knowledge-format-okf-a-vendor-neutral-markdown-spec-for-giving-ai-agents-curated-context/)

**For the AI Roles certification table (Section 6), verified Aug 14, 2026:**

- [Top AI Certifications from Google, Microsoft & AWS (2026)](https://topaicertifications.com/best-ai-certifications-from-google-microsoft-aws/)
- [Oracle Cloud Infrastructure AI Foundations Associate — K21 Academy](https://k21academy.com/oci-ai/oracle-cloud-infrastructure-ai-foundations-associate/)
- [Oracle Cloud Infrastructure Generative AI Professional — Coursera](https://www.coursera.org/learn/oracle-cloud-infrastructure-generative-ai-professional)
- [Databricks Certified Generative AI Engineer Associate — Databricks](https://www.databricks.com/learn/certification/genai-engineer-associate)
- [AI Governance Certification Guide 2026: AIGP, ISO 42001, and Career Paths](https://www.glacis.io/guide-ai-governance-certification)
- [ISO 42001 & NIST AI RMF: Mastering responsible AI governance in 2026](https://www.trustcloud.ai/ai/iso-42001-nist-ai-rmf-practical-steps-for-responsible-ai-governance/)
