# Embedding the explorer in a portal

Pick the option that matches how your portal accepts content. All three use the same build output in `explorer/dist/`.

## Option 1 — Web component (recommended)

Best for portals where you control the page: a React, Angular or Vue app, Backstage, or any CMS that allows script tags. The component renders in Shadow DOM, so its styles never leak into your portal and yours never break it.

1. Copy `agentic-ops-explorer.js` and `data.json` to your static assets, for example `/assets/agentic-ops/`.
2. Add to the page:

```html
<script type="module" src="/assets/agentic-ops/agentic-ops-explorer.js"></script>
<agentic-ops-explorer
  src="/assets/agentic-ops/data.json"
  cloud="gcp"
  view="diagrams"
  theme="auto"
  routing="none"
  repo-url="https://github.com/YOUR-ORG/agentic-ops-reference-architecture"
  style="height: 80vh; --ao-font: 'Your Brand Sans', sans-serif;">
</agentic-ops-explorer>
```

### Attributes

| Attribute | Values | Default | Notes |
| --- | --- | --- | --- |
| `src` | URL, or `#element-id` | `data.json` | `#id` reads JSON from a `<script type="application/json" id="…">` on the page |
| `cloud` | `gcp`, `aws` | `gcp` | Can be changed at runtime |
| `view` | `diagrams`, `gates`, `tools`, `compare`, `docs` | `diagrams` | Can be changed at runtime |
| `theme` | `auto`, `light`, `dark` | `auto` | Set this from your portal's theme switch |
| `routing` | `hash`, `none` | `none` | Use `hash` only when the explorer owns the page URL |
| `repo-url` | URL | from data | Base for links to files outside the explorer |
| `mermaid-src` | ESM URL, or `none` | jsDelivr Mermaid 11.4.1 | Point at an internal mirror, or disable |

### Styling hooks

Set these CSS custom properties on the element:

| Property | Purpose |
| --- | --- |
| `--ao-font` | Body and diagram font |
| `--ao-heading-font` | Heading font |
| `--ao-height` | Height (or set `height` directly) |
| `--ao-radius` | Corner radius of the whole component |

### JavaScript API

```js
const ex = document.querySelector("agentic-ops-explorer");

// Navigate from your portal's own menus or search
ex.navigate({ view: "diagrams", cloud: "aws", diagram: "security-gates", node: "g9-action-policy" });
ex.navigate({ view: "tools", tool: "db.failover" });
ex.navigate({ view: "docs", doc: "concepts-03-earned-autonomy" });

// React to user actions, e.g. sync your URL or analytics
ex.addEventListener("ao-navigate", (e) => console.log("state", e.detail));
ex.addEventListener("ao-select", (e) => console.log("component", e.detail.node.title));

// Provide data yourself (bundled, fetched with auth, or filtered)
ex.data = await fetch("/api/architecture/agentic-ops").then((r) => r.json());
```

In React, render the element as-is (`<agentic-ops-explorer src="…" />`) after importing the script once; attach listeners with a `ref`.

## Option 2 — iframe

Best for wikis and intranets that only allow embeds (Confluence, SharePoint, Notion, Google Sites). Host `explorer/dist/` anywhere static (GitHub Pages, an internal bucket, your portal's CDN), then embed:

```html
<iframe src="https://YOUR-HOST/explorer/#/diagrams/gcp/full-system-architecture"
        title="Agentic Ops architecture explorer"
        style="width:100%;height:85vh;border:0" loading="lazy"></iframe>
```

Deep links work inside the iframe because the standalone page uses `routing="hash"`.

## Option 3 — Single file

Best for portals that accept one uploaded HTML page, offline review packs, or attaching to a design review:

```bash
python3 explorer/build.py --single-file agentic-ops-explorer.html
```

The output inlines the component and all data (about 1 MB). It works from `file://` with no server.

## Content Security Policy

The component needs no third-party scripts. If your portal enforces CSP:

| Need | Directive |
| --- | --- |
| Load the component and data | `script-src 'self'`, `connect-src 'self'` (or the assets host) |
| Inline styles inside the shadow root and diagrams | `style-src 'self' 'unsafe-inline'` |
| Mermaid sequence diagrams in Docs (optional) | allow the `mermaid-src` host in `script-src`, or set `mermaid-src="none"` to show diagram source instead |
| Web fonts (optional) | your font host in `font-src` and `style-src`; otherwise system fonts are used |

## Keeping the portal in sync

Treat `data.json` as a build artefact of the repository. In your portal's pipeline, check out this repository, run `python3 explorer/build.py`, and publish `explorer/dist/`. Diagram, chapter or tool changes merged here then appear in the portal on the next build.

## Adding your own content

- **New diagram:** add a spec under `diagrams/specs/` named `<cloud>-<key>.json`, register the key in `DIAGRAM_TITLES` in `build.py`, rebuild.
- **New chapter or ADR:** add the Markdown file in the existing folders; it appears in Docs automatically.
- **New tool:** add it to `tools/catalog.yaml` and run `tools/build_catalog.py`.
- **Another cloud:** add `architecture/<cloud>/`, specs named `<cloud>-*.json`, and the cloud to `CLOUDS` in `build.py`.
