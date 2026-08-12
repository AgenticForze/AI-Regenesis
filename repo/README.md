# Multi-Agent Architecture Use Case Catalog — Telecom, BSS/OSS & Financial Services

A structured catalog of **60 real-world multi-agent AI architecture use cases** — 20 in Telecommunications
(network/RAN/customer-facing), 20 in BSS/OSS (order-to-cash, catalog, mediation, inventory, revenue assurance),
and 20 in Financial Services — each documented with a problem statement, an end-to-end agent architecture, a
technology stack per step, a clean layered architecture diagram, and an honest "what we'd improve if we rebuilt
this" retrospective.

📖 **Browse interactively:** open [`website/index.html`](website/index.html) in a browser. The left sidebar lists
every use case grouped **Domain → Architecture Pattern → Use Case**, each level independently expandable/
collapsible; click a domain to filter to it, a pattern to filter within that domain, or a leaf to open the full
write-up with its diagram. See [GitLab Pages setup](#gitlab-pages) below to host it for a team.

## Repository structure

```
.
├── README.md                     ← you are here
├── LICENSE
├── CONTRIBUTING.md
├── .gitlab-ci.yml                ← CI: lint markdown, validate mermaid, build & deploy Pages site
├── docs/
│   ├── architecture/
│   │   ├── e2e-platform-architecture.md              ← E2E platform reference, all domains at once
│   │   ├── e2e-platform-architecture.svg              ← its rendered diagram
│   │   ├── decision-engineering-meta-architecture.md  ← 8-layer flagship reference example
│   │   └── decision-engineering-meta-architecture.svg ← its rendered diagram
│   ├── telecom/
│   │   ├── README.md             ← Telecom domain index (20 use cases)
│   │   └── 01-network-fault-rca-remediation/
│   │       ├── README.md         ← full use case writeup, embeds architecture.svg
│   │       ├── architecture.svg  ← rendered diagram (primary visual)
│   │       └── architecture.mmd  ← Mermaid text source of the same structure (portable/editable)
│   │   ... (20 use case folders)
│   ├── bssoss/
│   │   ├── README.md             ← BSS/OSS domain index (20 use cases)
│   │   └── 01-order-to-activation-orchestration/ ...
│   │   ... (20 use case folders)
│   └── finance/
│       ├── README.md             ← Financial Services domain index (20 use cases)
│       └── 01-aml-transaction-monitoring-sar/ ...
│       ... (20 use case folders)
├── patterns/                     ← one doc per architecture pattern, cross-linking every use case that applies it
│   ├── orchestrator-worker.md
│   ├── hierarchical.md
│   ├── pipeline.md
│   ├── blackboard.md
│   ├── debate-critique.md
│   ├── market-based.md
│   ├── event-swarm.md
│   └── human-escalation.md
├── website/                      ← single-page navigator: collapsible sidebar (Domain → Pattern → Use Case)
│   ├── index.html                ← standalone, data inlined — open directly, no server needed
│   ├── index.template.html       ← source template (build.py injects catalog JSON into this)
│   └── data.json                 ← generated catalog data, also fetchable standalone
└── scripts/                      ← the generator that produced docs/ and website/index.html from structured data
    ├── svg_engine.py              ← layout engine: rounded cards, title+subtitle, elbow connectors
    ├── svg_patterns.py            ← one diagram builder per architecture pattern + the E2E platform diagram
    ├── templates.py               ← Mermaid text-source templates per architecture pattern (kept for portability)
    ├── telecom_data.py            ← structured source data, 20 telecom use cases
    ├── bssoss_data.py             ← structured source data, 20 BSS/OSS use cases
    ├── finance_data.py            ← structured source data, 20 finance use cases
    └── build.py                   ← renders docs/, patterns/, and website/index.html
```

## Reference architectures

Two documents sit outside the 60-use-case catalog, each showing how the pieces compose into a full system rather
than one workflow:

- [`docs/architecture/e2e-platform-architecture.md`](docs/architecture/e2e-platform-architecture.md) — how
  channels, orchestration, the agent mesh, and observability/governance fit together across all three domains
  at once.
- [`docs/architecture/decision-engineering-meta-architecture.md`](docs/architecture/decision-engineering-meta-architecture.md) —
  the 8-layer Integrated Decision Engineering Meta-Architecture (Base → Brain → Thinking Center → Conscience →
  Action → Nervous System → Leadership Portal → Self-Healing Loop) applied end-to-end to one high-stakes
  decision, with the AI Gateway, Agent Plane, four-part Memory Layer (short-term + long-term, explicitly
  labeled), conditional routing, and internal/external data stores all made explicit.

Both are pinned at the top of the website sidebar.

## Architecture patterns covered

Every diagram — per-use-case and the platform view — uses the same **layered architecture** visual language:
cream/tan cards for Data & Integration, blue for Orchestration, green for the Agent layer, amber for Action &
Execution, and lavender for the cross-cutting Observability & Governance layer (tracing, audit log, guardrails,
and any human review checkpoint). See
[`docs/architecture/e2e-platform-architecture.md`](docs/architecture/e2e-platform-architecture.md) for how all 60
use cases compose into one platform.

| Pattern | Best for |
|---|---|
| **Orchestrator-Worker** | Fan-out independent sub-investigations, fan-in to one decision (fraud checks, onboarding, RCA) |
| **Hierarchical (manager-of-managers)** | Domains-of-domains where each manager resolves local trade-offs (network domains, deal workstreams) |
| **Sequential Pipeline** | Linear workflows with strict step dependencies and durability needs (billing disputes, settlement) |
| **Blackboard / Shared-Memory** | Accumulating heterogeneous partial evidence, no single agent has the full picture (fleet health, firm-wide risk) |
| **Debate-Critique-Arbiter** | High-stakes judgment calls prone to single-pass confirmation bias (fraud, surveillance, recommendations) |
| **Market-Based / Auction** | Resource allocation among competing semi-autonomous stakeholders (dispatch, capacity trading, trading desks) |
| **Event-Driven Reactive Swarm** | Latency-critical always-on monitoring where central orchestration adds unacceptable lag (self-healing, CNP fraud) |
| **Human-in-the-Loop Escalation** | Regulated/high-consequence decisions needing a confidence/risk gate before autonomy |

See [`patterns/`](patterns/) for the full explanation of each, with every use case that applies it cross-linked.

## Use case index

### Telecommunications (20)
See [`docs/telecom/README.md`](docs/telecom/README.md) for the full table. Highlights: network fault RCA &
auto-remediation, 5G network slicing, self-healing closed-loop automation, churn win-back orchestration, SIM-swap
fraud detection, telecom SOC threat hunting, field workforce dispatch marketplace, predictive hardware maintenance.

### BSS/OSS (20)
See [`docs/bssoss/README.md`](docs/bssoss/README.md) for the full table. Highlights: order-to-activation
orchestration, product catalog & offer automation, revenue assurance & leakage detection, order fallout
auto-recovery, network inventory reconciliation, mediation/CDR processing, number portability orchestration,
customer 360/master data unification, dunning & collections with human escalation, API gateway governance.

### Financial Services (20)
See [`docs/finance/README.md`](docs/finance/README.md) for the full table. Highlights: AML transaction monitoring
& SAR filing, credit underwriting, algorithmic trading orchestration, card-not-present fraud detection, M&A due
diligence, insider trading surveillance, regulatory reporting, personalized financial advisory.

## How each use case is documented

Every use case folder contains one `README.md` with four required sections, matching the brief this catalog was
built to satisfy:

1. **Problem Statement & Use Case** — the business pain, why it's hard today, what "good" looks like.
2. **End-to-End Multi-Agent Architecture** — the agents/sub-agents table, plus a rendered Mermaid diagram showing
   data sources → orchestrating agent(s) → worker/specialist agents → aggregation/action agents → downstream
   systems, including any human-in-the-loop checkpoint.
3. **Technologies Used** — a concrete, named technology per architectural step (not generic placeholders).
4. **If We Rebuilt This** — a retrospective of concrete lessons learned / what would change on a second pass.

## Regenerating the catalog

The `docs/` folder and `website/data.json` are generated from the structured data in `scripts/`. To modify a use
case, edit `scripts/telecom_data.py` or `scripts/finance_data.py` (or `scripts/templates.py` for diagram styling),
then run:

```bash
python3 scripts/build.py
```

This regenerates every `docs/**/README.md`, `docs/**/architecture.mmd`, `patterns/*.md`, and `website/data.json`
deterministically from the source data — the website and docs never drift out of sync.

## GitLab Pages

`.gitlab-ci.yml` includes a `pages` job that copies `website/` to the Pages publish directory, so pushing to the
default branch publishes the navigator at `https://<namespace>.gitlab.io/<project>/` automatically.

## License

See [`LICENSE`](LICENSE).
