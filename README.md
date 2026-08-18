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
| `docs/` | The imported SVG diagrams: 60 architecture diagrams, 60 Deep 8-Layer diagram/blueprint pairs, the reference architectures, and the favicon. |
| `_ds/` | The Organic design system: tokens, stylesheet, component bundle. |
| `github.md` | Source-repo association and screen map. |
| `.nojekyll` | Required for GitHub Pages — see above. Hidden file; don't lose it. |

## Content sources

Diagrams, write-ups and catalog data come from
[AgenticForze/AI-Regenesis](https://github.com/AgenticForze/AI-Regenesis).
Code MIT · content CC BY-NC 4.0. Created by Naga Gande.
