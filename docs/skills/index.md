---
layout: default
title: "Skills & Packs — Free Downloads — AI-Regenesis"
description: "Download the AI-Regenesis engine skills and vertical content packs — free while we gauge real interest. Drop straight into Claude Code, Claude Cowork, or your own scripts."
permalink: /skills/
---

# Skills & Packs

Everything below is **free to download right now**. This project's paid tier (pricing, checkout, licensed
bundles) is intentionally on hold until there's real evidence people want it — downloads from this page are
themselves how we're gathering that evidence. See [`CONTENT-LICENSE.md`]({{ site.github.repository_url }}/blob/main/CONTENT-LICENSE.md)
for the terms the vertical packs ship under (code in the skills themselves is MIT).

Every skill below was built, rendered, and re-tested from its own packaged `.skill` file before being listed
here — not just written and assumed to work. Each skill's `references/lessons-learned.md` (inside the
download) documents the real issues found doing that, in case you're extending one of these yourself.

## Engine skills

Drop-in packages for Claude Code, Claude Cowork, or your own Python environment — each is a standalone
`scripts/` + `references/` + `SKILL.md` folder, zero dependency on the rest of this repo.

<div class="skill-card" id="quick-reference-engine" markdown="1">

### Quick-Reference Engine

Generates the Quick Reference multi-agent architecture view — a Mermaid + SVG diagram and a four-phase build
order — for any of the 8 named multi-agent patterns (Orchestrator-Worker, Hierarchical, Sequential Pipeline,
Blackboard, Debate-Critique-Arbiter, Market-Based, Event-Driven Swarm, Human-in-the-Loop Escalation), from
one compact spec per use case.

[**Download `quick-reference-engine.skill`**]({{ '/downloads/skills/quick-reference-engine.skill' | relative_url }}){: .download-link data-download="quick-reference-engine" }
&nbsp;·&nbsp; [Try it live in your browser, no download]({{ '/build/' | relative_url }})

</div>

<div class="skill-card" id="deep8-architecture-engine" markdown="1">

### Deep 8-Layer Architecture Engine

Generates the full 8-layer Decision Engineering Meta-Architecture view (L1 Foundational Data through L8
Feedback & Reinforcement Loops) — a labeled flow diagram, a reference blueprint table, and an agent-level
tools/technologies stack, from one compact spec per use case. This is the engine behind every Deep 8-Layer
page in the catalog.

[**Download `deep8-architecture-engine.skill`**]({{ '/downloads/skills/deep8-architecture-engine.skill' | relative_url }}){: .download-link data-download="deep8-architecture-engine" }

</div>

<div class="skill-card" id="retrospective-generator" markdown="1">

### Retrospective Generator

An **audit tool**, not a generation tool — interviews you about a real, already-deployed AI/agentic system
(16 structured questions across the same L1-L8 framework) and produces a governance-style gap report with
severity-ranked findings and actionable recommendations. The automated version of the Architecture Audit
consulting engagement below.

[**Download `retrospective-generator.skill`**]({{ '/downloads/skills/retrospective-generator.skill' | relative_url }}){: .download-link data-download="retrospective-generator" }

</div>

<div class="skill-card" id="proposal-generator" markdown="1">

### Proposal Generator

Combines a Quick-Reference use case (and optionally its Deep 8-Layer spec) with real engagement
details — client name, price, timeframe — into client-ready proposal content, ready to hand to a Word or
slide-deck skill. Never invents a price or timeframe; both are required inputs.

[**Download `proposal-generator.skill`**]({{ '/downloads/skills/proposal-generator.skill' | relative_url }}){: .download-link data-download="proposal-generator" }

</div>

## Vertical content packs

Pure-data bundles — the 20 use cases (Quick-Reference + Deep 8-Layer specs) for one domain, no engine code.
Load into either engine skill above to regenerate diagrams, tables, and build orders for that domain, or use
as a reference for writing your own specs.

<div class="skill-card" id="telecom-pack" markdown="1">

### Telecom Vertical Pack

20 telecom use cases (network fault RCA, 5G slicing, fraud, churn, and more). 18 of the 20 currently have a
matching Deep 8-Layer spec — see the pack's own `README.md` for exactly which two don't yet.

[**Download `telecom-pack-v1.zip`**]({{ '/downloads/packs/telecom-pack-v1.zip' | relative_url }}){: .download-link data-download="telecom-pack" }

</div>

<div class="skill-card" id="bssoss-pack" markdown="1">

### BSS/OSS Vertical Pack

20 telecom back-office use cases (order orchestration, revenue assurance, fallout recovery, mediation
pipelines, and more). Full 1:1 Quick-Reference / Deep 8-Layer coverage across all 20.

[**Download `bssoss-pack-v1.zip`**]({{ '/downloads/packs/bssoss-pack-v1.zip' | relative_url }}){: .download-link data-download="bssoss-pack" }

</div>

<div class="skill-card" id="finance-pack" markdown="1">

### Finance Vertical Pack

20 financial-services use cases (AML/SAR filing, credit underwriting, algorithmic trading, KYC onboarding,
robo-advisory, and more). Full 1:1 Quick-Reference / Deep 8-Layer coverage across all 20.

[**Download `finance-pack-v1.zip`**]({{ '/downloads/packs/finance-pack-v1.zip' | relative_url }}){: .download-link data-download="finance-pack" }

</div>

## What's not here yet, on purpose

Pricing, checkout, and licensed/paid bundles for any of the above are intentionally not built yet — that
work is paused until download activity or direct inbound interest gives a real signal it's worth building.
If you'd use a paid tier of any of this, saying so (via whatever contact method is on the site) is more
useful to us right now than the pricing page would be.

<style>
.skill-card{
  background:var(--surface-2); border:1px solid var(--line); border-radius:8px;
  padding:18px 20px; margin:16px 0;
}
.skill-card h3{margin-top:0;}
.download-link{
  display:inline-block; margin-top:8px; font-family:var(--mono); font-size:13px;
  padding:8px 14px; background:var(--accent); color:#0B0E13 !important; border-radius:6px;
  text-decoration:none; font-weight:600;
}
.download-link:hover{opacity:.88;}
</style>
