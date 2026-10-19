# Changelog

All notable changes to this architecture are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/) applied to the blueprint: major for structural changes to layers or gates, minor for new chapters or platforms, patch for corrections.

## [Unreleased]

## [1.1.0] - 2026-10-17

### Added

- Architecture Explorer: framework-free web component with clickable diagrams, cross-cloud equivalents, security gate walkthrough, tool catalogue, cloud comparison, search, deep links and docs reader; standalone, embeddable and single-file builds.
- Tool catalogue: 31 MCP tools across 11 executor servers in `tools/catalog.yaml`, with generated README, MCP definitions and validation.
- `architecture-diagrams` Claude skill: spec-driven renderer with layout checks, icon set and icon gallery.
- Editable JSON specs for all ten diagrams, themed SVGs, and `scripts/build-diagrams.sh`.
- CI: catalogue validation, strict diagram rendering and explorer build; Pages now publishes the explorer at `/explorer/`.

### Changed

- Two diagram labels repositioned so they no longer overlap components.
- Explorer hides links to GitHub (PNG download, MCP definitions, repository files) until a real repository address is configured, instead of opening a "Page not found" page.

## [1.0.0] - 2026-10-16

### Added

- Cloud-neutral concepts: principles, operating loop, earned autonomy, security gate model, glossary.
- Google Cloud edition in 18 chapters.
- AWS edition in 19 chapters, including a Google Cloud to AWS service map.
- Ten icon diagrams (five per cloud) as SVG and PNG.
- Interactive single-page editions published with GitHub Pages.
- Templates: agent spec, autonomy promotion checklist, OpenTelemetry span schema, OPA and Cedar action policies.
- Six architecture decision records.
- Article: *Agentic Ops on Google Cloud: A Reference Architecture for the Enterprise*.
