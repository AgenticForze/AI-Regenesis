# AI-Regenesis — product site

A single-page redesign of the AI-Regenesis catalog: home, use-case catalog, use-case pages,
Deep 8-Layer views, pattern reference, reference architectures, diagram builder, and skills & packs.

## Run it

It is a static site. No build step, no dependencies, no server-side code.

Locally:

    python3 -m http.server 8000

then open http://localhost:8000/

## Deploy to GitHub Pages

1. Push the contents of this folder to a branch (`main` or `gh-pages`).
2. Settings → Pages → Source: *Deploy from a branch*, pick that branch and `/ (root)`.
3. The site serves from `index.html`.

**Keep the `.nojekyll` file at the repo root.** GitHub Pages runs Jekyll by default,
and Jekyll refuses to publish any folder whose name starts with an underscore — which
would drop `_ds/` and serve the site with no stylesheet at all. The empty `.nojekyll`
file turns Jekyll off. It is a hidden file, so check it survived the copy:

    ls -a

If you publish it under a repository subpath (`user.github.io/repo/`), no change is
needed — every asset reference in the page is relative.

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | The site. Everything renders from this one file. |
| `AI-Regenesis.dc.html` | The editable source of `index.html` (identical content). |
| `support.js` | Runtime the page loads. Required. |
| `case-data.js` | All 60 use-case write-ups — problem, agents, tech stack, build order, retrospective. |
| `packager.js` | Client-side ZIP writer — powers every download button. |
| `skills/`, `packs/` | Sources the download packages are built from — the seven folders `quick-reference-engine/`, `deep8-architecture-engine/`, `retrospective-generator/`, `proposal-generator/`, `telecom-pack-v1/`, `bssoss-pack-v1/`, `finance-pack-v1/`. |
| `docs/` | The imported SVG diagrams: 60 architecture diagrams, 60 Deep 8-Layer diagram/blueprint pairs, the reference architectures, and the favicon. |
| `_ds/` | The Organic design system: tokens, stylesheet, component bundle. |
| `github.md` | Source-repo association and screen map. |
| `.nojekyll` | Required for GitHub Pages — see above. Hidden file; don't lose it. |

## Content sources

Diagrams, write-ups and catalog data come from
[AgenticForze/AI-Regenesis](https://github.com/AgenticForze/AI-Regenesis).
Code MIT · content CC BY-NC 4.0. Created by Naga Gande.

## After deploying — a five-minute check

These are the things that only break once the site is on a real host:

1. **Styles load.** If the page renders as unstyled black text on white, `_ds/` was not
   published — the `.nojekyll` file is missing.
2. **A use-case page.** Catalog → any card. The architecture diagram should render at full
   size with legible labels, followed by the agent roster, technology table, build order and
   retrospective.
3. **Deep 8-Layer.** From a use-case page, "Open Deep 8-Layer view" — the L1–L8 flow diagram
   and the reference blueprint.
4. **A download.** Skills & packs → any "Download .zip". The archive is built in the browser,
   so it needs the source folders to be served; a 404 there means `quick-reference-engine/` and
   its siblings did not get pushed.
5. **The builder.** Build a diagram → edit a field. The diagram should re-render as you type,
   and "Download SVG" should produce a standalone file.

## Notes

- **No analytics, cookies or third-party requests.** Everything is served from your own origin.
- **Fonts** come from the design system's stylesheet. If the display face fails to load, headings
   fall back to a serif — the layout does not shift.
- **Editing content.** Use-case text lives in `case-data.js` as one object keyed
   `domain/slug`; diagrams are files under `docs/`. Neither requires touching `index.html`.
- **Re-syncing from upstream.** `github.md` records the source repo, branch and a screen map
   tying each screen to the repo files it was built from.
