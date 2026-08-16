# Contributing to RegAITraining

This site grows continuously — there's no "big launch" being held back. Every merge to `main`
deploys automatically and the new/updated chapter appears on the Recently Added page. Here's how
a chapter gets from idea to published page.

## 1. Open an issue

Start every new chapter (or substantial expansion) from an issue using the
[`new-chapter-proposal`](.github/ISSUE_TEMPLATE/new-chapter-proposal.md) template: concept, phase
and chapter number, why it belongs, and which domains' use cases will be hardest to source.

## 2. Author on a branch

Start from the shared skeleton so the Content Standard is enforced structurally, not just by
convention:

- `_templates/concept-chapter.mdx` — the full seven-section template, for Phases 1–8, 10–13,
  15–18.
- `_templates/landscape-chapter.mdx` — the lighter four-section template, **Phases 9 and 14
  only**.

Copy the relevant template into the correct `docs/<phase-folder>/` directory, fill in front
matter (`title`, `sidebar_label`, `phase`, `chapter`, `prerequisites`), and write the content.

Use the shared components rather than hand-rolled Markdown tables/lists for these sections:

| Section | Component |
|---|---|
| Comparison & Related Concepts / Comparison Table | `<ComparisonTable />` |
| Reference Architecture | `<ArchitectureDiagram />` (wraps Mermaid) |
| Industry Use Cases | `<UseCaseGrid />` |
| Check Your Understanding | `<CheckYourUnderstanding />` |

## 3. Open a PR

The [PR template](.github/PULL_REQUEST_TEMPLATE.md) mirrors the Content Standard — fill in every
checkbox honestly; a chapter isn't done until it's checked, not just written.

## 4. Review & merge

A reviewer checks the boxes above plus general accuracy. Merging to `main` triggers the GitHub
Actions build/deploy (`.github/workflows/deploy.yml`) and the chapter appears on the Recently
Added page automatically — no manual publish step.

## Local development

```bash
npm install
npm start        # local dev server with hot reload
npm run build     # production build — run this before opening a PR to catch broken links
```

## Quarterly review passes

Periodic judge-LLM review passes (the process that produced this site's v3/v4/v5 curriculum
revisions) are recommended quarterly to catch new production patterns before they become content
gaps. If you're running one, open a single tracking issue listing every gap found and link the
chapter PR that closes each one.
