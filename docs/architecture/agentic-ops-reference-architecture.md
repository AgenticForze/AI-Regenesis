---
layout: default
title: "Agentic Ops Reference Architecture (Google Cloud and AWS) — AI-Regenesis"
description: "An enterprise blueprint for running IT, cloud and business operations through governed AI agents: eleven layers, earned autonomy, a central model gateway, end-to-end tracing and twelve runtime security gates, on Google Cloud and AWS."
permalink: /architecture/agentic-ops-reference-architecture/
---

# Agentic Ops Reference Architecture

The 60 use cases in this catalog each solve one decision. This reference zooms out to the **operations platform** that runs agents like these in production: how agents are identified, governed, observed, secured and paid for when they are allowed to change real systems. It comes in two editions, **Google Cloud** and **AWS**, that share one layout so every component sits in the same place.

<p>
  <a href="{{ '/agentic-ops/explorer/' | relative_url }}"><strong>Open the Architecture Explorer</strong></a> ·
  <a href="{{ '/agentic-ops/gcp.html' | relative_url }}">Google Cloud edition</a> ·
  <a href="{{ '/agentic-ops/aws.html' | relative_url }}">AWS edition</a> ·
  <a href="https://github.com/AgenticForze/AI-Regenesis/tree/main/agentic-ops">Source, templates and skills</a>
</p>

<img src="{{ '/agentic-ops/diagrams/gcp-full-system-architecture.png' | relative_url }}" alt="Agentic Ops full system architecture across six trust zones on Google Cloud" width="100%"/>

## What it covers

| Area | In brief |
|---|---|
| **Eleven layers** | Channels, edge and safety, orchestration, model gateway, model serving, knowledge, tools, events, observability, security, MLOps, each with one job |
| **Three model tiers** | Small language models for volume, in-house LLMs for restricted data, frontier models (Gemini, or Bedrock models on AWS) for hard reasoning, all behind one gateway |
| **Earned autonomy** | Set per action type from L0 Observe to L4 Autonomous, promoted only on measured evidence and demoted automatically after an agent-caused severity-1 incident |
| **Twelve runtime gates** | Deterministic, independently owned checks from the edge to the audit trail, so no control depends on the model behaving well |
| **Everything is a trace** | Every model call, retrieval, policy decision, approval and tool call is an OpenTelemetry span under one trace ID |
| **Hybrid network** | Dedicated Interconnect or Direct Connect as primary, HA VPN as encrypted backup, private service access and default-deny egress |
| **Tool catalogue** | 31 MCP tools across 11 least-privilege executor servers, each with inputs, autonomy range, blast radius and gates |

## Explore it

The **Architecture Explorer** turns the whole reference into a browsable portal. Click any component on any diagram to see what it connects to, the tools that act on it, the chapters that discuss it, and its counterpart on the other cloud. Step through the security gates, filter the tool catalogue, compare clouds side by side, and read every chapter with live diagrams.

<p><a href="{{ '/agentic-ops/explorer/' | relative_url }}"><strong>Open the Architecture Explorer →</strong></a></p>

## How it relates to the rest of this catalog

The [E2E Platform Reference Architecture]({{ '/architecture/e2e-platform-architecture/' | relative_url }}) shows how the catalog's use cases fit one platform shape. Agentic Ops is the operating model for that platform on a specific cloud: the identities, policy engine, gateway, telemetry and network that let those agents act safely. The [Decision Engineering Meta-Architecture]({{ '/architecture/decision-engineering-meta-architecture/' | relative_url }}) maps one decision through eight layers; Agentic Ops supplies the controls that layer 4 (the conscience) and layer 6 (the nervous system) describe, as concrete services.

---
Created by Naga Gande. Text and diagrams CC BY 4.0, code and templates MIT, as stated in the [`agentic-ops/`](https://github.com/AgenticForze/AI-Regenesis/tree/main/agentic-ops) folder.
