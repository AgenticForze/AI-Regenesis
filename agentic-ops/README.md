<div align="center">

# Agentic Ops Reference Architecture

**An enterprise blueprint for running operations through governed AI agents, on Google Cloud and AWS.**

[![License: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-1E5AA8)](LICENSE)
[![License: MIT](https://img.shields.io/badge/code-MIT-2E7D5B)](LICENSE-CODE)
![Clouds](https://img.shields.io/badge/clouds-Google%20Cloud%20%7C%20AWS-44525F)
![Status](https://img.shields.io/badge/status-v1.1%20blueprint-B57612)

[Architecture Explorer](https://agenticforze.github.io/AI-Regenesis/agentic-ops/explorer/) ·
[Interactive pages](https://agenticforze.github.io/AI-Regenesis/agentic-ops/) ·
[Google Cloud edition](architecture/gcp/README.md) ·
[AWS edition](architecture/aws/README.md) ·
[Article](articles/2026-10-agentic-ops-on-google-cloud.md)

</div>

![Full system architecture across trust zones](diagrams/png/gcp-full-system-architecture.png)

## Why this exists

Most enterprise AI pilots in operations stop at a chatbot that can explain an alert but cannot fix it. Moving from *answering* to *acting* is an architecture problem, not a model problem: agents need identities, budgets, policy enforced outside the prompt, end-to-end traces, and a way to earn autonomy with evidence.

This repository is a vendor-aware, opinionated reference for that platform. It is written for enterprise architects, platform and SRE leaders, and security teams who need to design, review or challenge an agentic operations programme.

## What's inside

| Path | What you'll find |
| --- | --- |
| [`concepts/`](concepts/) | Cloud-neutral ideas: principles, operating loop, earned autonomy, security gate model, glossary |
| [`architecture/gcp/`](architecture/gcp/README.md) | Full Google Cloud design in 18 chapters, from layers to roadmap |
| [`architecture/aws/`](architecture/aws/README.md) | The same design on AWS in 19 chapters, including a GCP ↔ AWS service map |
| [`diagrams/`](diagrams/) | Icon diagrams for both clouds: editable JSON specs, SVG, themed SVG and PNG |
| [`tools/`](tools/README.md) | MCP tool catalogue: 31 tools across 11 executor servers, with generated MCP definitions |
| [`explorer/`](explorer/README.md) | Interactive Architecture Explorer, a web component you can host or embed in your portal |
| [`skills/`](skills/README.md) | Claude skills, starting with `architecture-diagrams` for drawing and editing the diagrams |
| [`templates/`](templates/) | Agent spec, autonomy promotion checklist, OPA and Cedar policies, OTel span schema |
| [`templates/adr/`](templates/adr/) | Architecture decision records for the key design choices |
| [`articles/`](articles/) | Long-form writing about the architecture |
| [`site/`](site/) | Interactive single-page editions and landing page; `scripts/publish-site.sh` copies them to `../docs/agentic-ops/` for GitHub Pages |
| [`scripts/`](scripts/) | Build helpers, such as rebuilding every diagram from its spec |

## The architecture in one minute

<table>
<tr><td width="50%">

**Eleven layers**, each with one job: channels, edge and safety, orchestration, model gateway, model serving, knowledge, tools, events, observability, security, MLOps.

**Three model tiers** behind one gateway: SLMs for volume, in-house LLMs for restricted data, frontier models for hard reasoning.

**Earned autonomy** per action type, from L0 observe to L4 autonomous, with an evidence-based promotion rule.

</td><td width="50%">

**Twelve runtime gates** that fail closed, so no control depends on the model behaving well.

**Everything is a trace**: every model call, retrieval, policy decision, approval and tool call is an OpenTelemetry span under one trace ID.

**Open seams**: MCP for tools, A2A between agents, OpenTelemetry, OPA or Cedar, Terraform.

</td></tr>
</table>

![End-to-end agentic operations flow](diagrams/png/gcp-end-to-end-flow.png)

## Diagrams

| | Google Cloud | AWS |
| --- | --- | --- |
| Full system architecture | [PNG](diagrams/png/gcp-full-system-architecture.png) · [SVG](diagrams/svg/gcp-full-system-architecture.svg) | [PNG](diagrams/png/aws-full-system-architecture.png) · [SVG](diagrams/svg/aws-full-system-architecture.svg) |
| End-to-end flow | [PNG](diagrams/png/gcp-end-to-end-flow.png) · [SVG](diagrams/svg/gcp-end-to-end-flow.svg) | [PNG](diagrams/png/aws-end-to-end-flow.png) · [SVG](diagrams/svg/aws-end-to-end-flow.svg) |
| Hybrid connectivity | [PNG](diagrams/png/gcp-hybrid-connectivity.png) · [SVG](diagrams/svg/gcp-hybrid-connectivity.svg) | [PNG](diagrams/png/aws-hybrid-connectivity.png) · [SVG](diagrams/svg/aws-hybrid-connectivity.svg) |
| Security gates G1–G12 | [PNG](diagrams/png/gcp-security-gates.png) · [SVG](diagrams/svg/gcp-security-gates.svg) | [PNG](diagrams/png/aws-security-gates.png) · [SVG](diagrams/svg/aws-security-gates.svg) |
| Telemetry pipeline | [PNG](diagrams/png/gcp-telemetry-pipeline.png) · [SVG](diagrams/svg/gcp-telemetry-pipeline.svg) | [PNG](diagrams/png/aws-telemetry-pipeline.png) · [SVG](diagrams/svg/aws-telemetry-pipeline.svg) |

Sequence diagrams, routing logic, topology and lifecycle flows are written in Mermaid inside the chapters, so GitHub renders them directly and you can edit them as text.

## Explore it interactively

The **[Architecture Explorer](explorer/README.md)** turns the repository into a browsable portal: click any component on any diagram to see its connections, the tools that act on it, the chapters that discuss it and its equivalent on the other cloud; step through the security gates; filter the tool catalogue; compare clouds side by side; and read every chapter with live diagrams.

It is one framework-free web component, so you can host it on GitHub Pages, drop it into an existing architecture portal with a single script tag, embed it in Confluence or SharePoint with an iframe, or ship it as one offline HTML file. See [EMBEDDING.md](explorer/EMBEDDING.md).

```html
<script type="module" src="agentic-ops-explorer.js"></script>
<agentic-ops-explorer src="data.json" cloud="gcp" view="diagrams"></agentic-ops-explorer>
```

## How to use this

- **Architects:** start with [`concepts/`](concepts/), then read the edition for your cloud. Use the [ADRs](templates/adr/) as a starting point for your own decision log.
- **Platform teams:** copy the [agent spec](templates/agent-spec.yaml), [policies](templates/policies/), [span schema](templates/otel-span-schema.md) and [tool catalogue](tools/README.md) into your own repos.
- **Editing diagrams:** change the JSON in [`diagrams/specs/`](diagrams/specs/) and run `./scripts/build-diagrams.sh`, or ask Claude with the [`architecture-diagrams` skill](skills/architecture-diagrams/SKILL.md).
- **Security and risk:** go straight to the security gates chapter ([GCP](architecture/gcp/13-security-gates.md), [AWS](architecture/aws/13-security-gates.md)) and the [promotion checklist](templates/autonomy-promotion-checklist.md).
- **Presenting:** the PNGs are exported at 2× for slides; the SVGs scale without loss.

> [!NOTE]
> Service names reflect the Google Cloud and AWS catalogues as of October 2026. Several services are new or rolling out by region, so validate availability and quotas during detailed design. IP ranges, capacity figures and roadmap targets are illustrative.

## Contributing

Disagreement is welcome. Open an issue to challenge a decision, or a pull request to improve a chapter. See [CONTRIBUTING.md](CONTRIBUTING.md) for templates and conventions.

## Citation and licence

If you reference this work, please cite it using [CITATION.cff](CITATION.cff) (GitHub shows a "Cite this repository" button).

- Text and diagrams: [CC BY 4.0](LICENSE)
- Code, policies and templates: [MIT](LICENSE-CODE)

Sources are listed in [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md).

---

Created by **Naga Gande** as part of [AI-Regenesis](../README.md), the reference architecture library for agentic AI.
