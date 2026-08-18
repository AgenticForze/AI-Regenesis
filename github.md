repo: AgenticForze/AI-Regenesis
branch: main

## Last sync

date: 2026-08-18T20:08:46Z

### Updated in this project

- Favicon: original repo geometry restored, re-tinted to the Organic ramps (sage/terracotta arcs, cream monogram on warm charcoal).

- Finalized: all 240 case assets verified present, every route walked, search now indexes all 60 write-ups and tech stacks, hero overflow and builder layout fixed.

- Builder now renders a real SVG from the spec, with SVG and .zip package downloads.
- Skills & packs downloads build genuine .zip archives in the browser from the imported `skills/` and `packs/` sources.
- All 184 diagrams stripped of their white background so they sit on the page ground.

- Imported all 60 use-case write-ups and inlined them: problem statement, agent roster, per-step tech stack, build order and retrospective now render on the page instead of linking out.

- Home page restructured to match the live site: wordmark, tagline, domain pills, stat row and the build-your-own CTA card.
- Skills & packs download links now point at the real `skills/` and `packs/` folders on GitHub (no packaged archives exist upstream).

- Built `AI-Regenesis.dc.html` — a product design of the site: home, catalog, use-case page, pattern reference, diagram builder, skills & packs.
- Catalog carries all 60 real use cases (titles, numbering, domain, architecture pattern) from the three domain indexes.
- Four use cases carry their full imported write-up (problem statement, agent roster, diagram): telecom 01 & 07, bssoss 03, finance 01. The rest deep-link to the live site.
- Pattern names, "best for" lines and build-order phases follow `README.md` and `docs/patterns/`.
- Imported all 60 Deep 8-Layer `diagram.svg` + `blueprint.svg` pairs — the Deep 8-Layer page now works in-product for every use case.
- Skills & packs page now previews real generated diagrams per engine and per vertical pack.
- Imported all 60 use-case `architecture.svg` files — every use-case page now shows its real generated diagram.
- Earlier import: 4 use-case architectures, 4 Deep 8-Layer diagram/blueprint pairs, the two reference architectures, and the favicon logo. Added Deep 8-Layer and Reference pages.

## Screen map

| Screen | Repo files |
| --- | --- |
| Home | README.md, BRAND.md |
| Catalog | docs/telecom/README.md, docs/bssoss/README.md, docs/finance/README.md |
| Use case page | docs/telecom/01-network-fault-rca-remediation/README.md, docs/telecom/07-sim-swap-fraud-detection/README.md, docs/bssoss/03-revenue-assurance-leakage-detection/README.md, docs/finance/01-aml-transaction-monitoring-sar/README.md |
| Patterns | README.md (pattern table), docs/patterns/orchestrator-worker.md |
| Builder | docs/build/index.html, skills/quick-reference-engine/SKILL.md |
| Deep 8-Layer page | docs/deep8/**/diagram.svg, docs/deep8/**/blueprint.svg, docs/deep8/README.md |
| Reference architectures | docs/architecture/*.svg |
| Skills & packs | docs/skills/index.md, packs/*/README.md |
