# Running This Site Locally

## Why double-clicking files doesn't fully work

This is a Jekyll site. Most of what's under `docs/` (every use-case page, the skills page, pattern docs,
architecture docs) is **markdown source with front matter**, not finished HTML — Jekyll compiles it:
resolves `{{ '/skills/' | relative_url }}`-style template tags, wraps the content in `_layouts/default.html`,
and turns `permalink: /skills/` into a real `skills/index.html` file on disk. GitHub Pages runs that
compilation step automatically when it builds. Your local file browser doesn't, so:

- Opening a `.md` file directly shows raw markdown/YAML text, not a rendered page.
- Navigating to a folder that only contains an `.md` source (e.g. `docs/skills/`, which just has
  `index.md`) 404s, because there's no `index.html` there yet — Jekyll hasn't generated one.
- **`website/` is not the full site at all** — it only ever contains the standalone homepage artifact
  (`index.html`, `index.template.html`, `data.json`, `favicon.svg`). There's no `website/skills/`,
  `website/build/`, or `website/deep8/` on disk, so links to those from `website/index.html` will always
  404 locally. The real site — every page — lives under `docs/`.

The two files under `docs/` that genuinely are complete, standalone HTML (`docs/index.html` and
`docs/build/index.html`) will partially work by double-clicking, but `docs/build/index.html` will show its
YAML front matter as literal visible text at the top of the page, since nothing is stripping it out — that's
also a Jekyll job.

## Option A — run Jekyll locally (matches GitHub Pages exactly)

Requires Ruby. If you don't have it, see [Jekyll's installation docs](https://jekyllrb.com/docs/installation/)
for your OS first.

```bash
cd docs
bundle init                      # first time only
bundle add jekyll jekyll-seo-tag jekyll-sitemap
bundle exec jekyll serve
```

Then open **http://localhost:4000/AI-Regenesis/** (note the `/AI-Regenesis/` — it mirrors your real
`baseurl`, so links resolve exactly like the live site; going to plain `localhost:4000/` without that path
will 404 for the same reason). Every page, every nav link, every download will work identically to
production. Ctrl-C stops the server; rerun `bundle exec jekyll serve` any time after editing content.

## Option B — just push and let GitHub Pages build it

Since `docs/_config.yml`'s `url`/`baseurl` are already set correctly for
**https://agenticforze.github.io/AI-Regenesis/**, the simplest path is often to just commit and push — GitHub
rebuilds in 1–2 minutes (check the **Actions** tab for a green checkmark) and the live site is the real,
fully-compiled result. This project's own testing has relied on simulating Jekyll's output (via scripts) and
then verifying against the actual production URL — see the conversation history in this repo's docs for
examples — rather than double-clicking local files, for exactly the reasons above.

## Quick local sanity checks that DO work by double-clicking

- `docs/index.html` — the homepage, fully self-contained, no Jekyll needed.
- `docs/404.html` — will show its front matter as visible text at the top (harmless, just ugly), but the
  rest of the page renders.
- Any generated diagram `.svg` file — pure static images, always viewable directly.

Anything else — real navigation, the shared header/footer, `/skills/`, `/build/`'s actual working form
(it needs Jekyll to resolve its `{{ '/assets/js/diagram-engine.js' | relative_url }}` script tag correctly),
every use-case page — needs Option A or B above.
