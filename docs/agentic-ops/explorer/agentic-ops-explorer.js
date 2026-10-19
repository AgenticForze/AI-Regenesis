/*!
 * <agentic-ops-explorer> — interactive browser for the Agentic Ops Reference Architecture.
 * Framework-free web component (Shadow DOM), no runtime dependencies.
 * Optional: Mermaid is lazy-loaded from `mermaid-src` to draw sequence diagrams in chapters.
 *
 * Attributes
 *   src          URL of data.json, or "#element-id" of a <script type="application/json"> holding it
 *   cloud        gcp | aws                       (default gcp)
 *   view         diagrams | gates | tools | compare | docs   (default diagrams)
 *   theme        auto | light | dark             (default auto)
 *   routing      hash | none                     (default none; "hash" enables deep links)
 *   repo-url     base URL used for links to files outside the explorer
 *   repo-path    folder of the project inside that repository, e.g. "agentic-ops/"
 *   mermaid-src  ESM URL for Mermaid, or "none" to disable
 * Properties:  .data (set data directly), .navigate({view, cloud, diagram, node, doc, tool, gate})
 * Events:      ao-navigate (detail = state), ao-select (detail = {cloud, diagram, node})
 * Licence: MIT
 */
const VIEWS = [
  ["diagrams", "Diagrams"], ["gates", "Security gates"], ["tools", "Tools"], ["compare", "Compare clouds"], ["docs", "Docs"],
];
const DEFAULT_MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const CSS = `
:host{display:block;position:relative;height:var(--ao-height,100%);min-height:560px;color:var(--ink);background:var(--paper);
  font:15px/1.55 var(--ao-font,"IBM Plex Sans","Segoe UI",Roboto,Helvetica,Arial,sans-serif);--diagram-font:var(--ao-font,"IBM Plex Sans","Segoe UI",Roboto,Helvetica,Arial,sans-serif);
  border-radius:var(--ao-radius,0);overflow:hidden;contain:content}
*{box-sizing:border-box}
button,input,select{font:inherit;color:inherit}
button{cursor:pointer}
:focus-visible{outline:2px solid var(--signal);outline-offset:2px}
a{color:var(--signal)}
.app{display:flex;flex-direction:column;height:100%}
header{display:flex;align-items:center;gap:12px;padding:10px 16px;border-bottom:1px solid var(--rule);background:var(--sheet);flex-wrap:wrap}
.brand{font:700 15px/1.2 var(--ao-heading-font,"Schibsted Grotesk","IBM Plex Sans","Segoe UI",system-ui,sans-serif);margin-right:6px;white-space:nowrap}
nav.views{display:flex;gap:2px;flex-wrap:wrap}
nav.views button{border:0;background:none;padding:6px 10px;border-radius:6px;color:var(--ink-2)}
nav.views button[aria-current="page"]{background:var(--signal-soft);color:var(--ink);font-weight:600}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:7px;overflow:hidden}
.seg button{border:0;background:none;padding:5px 10px;color:var(--ink-2)}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--sheet)}
.spacer{flex:1}
.search{position:relative;min-width:200px;flex:0 1 300px}
.search input{width:100%;padding:6px 10px;border:1px solid var(--rule);border-radius:7px;background:var(--paper)}
.results{position:absolute;right:0;left:0;top:calc(100% + 4px);background:var(--sheet);border:1px solid var(--rule);border-radius:8px;
  box-shadow:0 10px 30px rgba(0,0,0,.18);max-height:60vh;overflow:auto;z-index:20;padding:4px}
.results .grp{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-2);padding:8px 8px 2px}
.results button{display:block;width:100%;text-align:left;border:0;background:none;padding:6px 8px;border-radius:6px}
.results button[aria-selected="true"],.results button:hover{background:var(--signal-soft)}
.results small{display:block;color:var(--ink-2);font-size:12px}
.iconbtn{border:1px solid var(--rule);background:var(--sheet);border-radius:7px;padding:5px 9px;min-width:34px}
main{flex:1;min-height:0;position:relative}
.view{height:100%;overflow:auto}
/* diagrams */
.dgrid{display:grid;grid-template-columns:220px minmax(0,1fr) 320px;height:100%}
.rail{border-right:1px solid var(--rule);padding:12px;overflow:auto;background:var(--sheet)}
.rail h3,.panel h3{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-2);margin:14px 0 6px}
.rail h3:first-child{margin-top:0}
.rail .dlist button{display:block;width:100%;text-align:left;border:0;background:none;padding:6px 8px;border-radius:6px;color:var(--ink-2)}
.rail .dlist button[aria-current="true"]{background:var(--signal-soft);color:var(--ink);font-weight:600}
.layers{display:flex;flex-direction:column;gap:2px}
.layers button{display:flex;align-items:center;gap:8px;border:0;background:none;padding:4px 6px;border-radius:6px;text-align:left;font-size:13px;color:var(--ink-2)}
.layers button[aria-pressed="true"]{background:var(--signal-soft);color:var(--ink)}
.dot{width:10px;height:10px;border-radius:3px;flex:none;background:var(--c)}
.stage{position:relative;display:flex;flex-direction:column;min-width:0}
.toolbar{display:flex;gap:6px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
.toolbar .t{font-weight:600;margin-right:auto}
.canvas{flex:1;min-height:0;position:relative;overflow:hidden;cursor:grab;touch-action:none}
.canvas.dragging{cursor:grabbing}
.canvas svg{width:100%;height:100%;display:block}
.hint{position:absolute;left:12px;bottom:10px;font-size:12px;color:var(--ink-2);background:var(--sheet);padding:3px 8px;border-radius:6px;border:1px solid var(--rule);pointer-events:none}
svg .node{cursor:pointer}
svg .node:hover .node-box,svg .node:focus .node-box{stroke:var(--signal);stroke-width:2}
svg .node,svg .edge,svg .edge-label,svg .zone{transition:opacity .15s}
svg.has-sel .node:not(.sel):not(.nb),svg.has-layer .node:not(.lay){opacity:.22}
svg.has-sel .edge:not(.on),svg.has-layer .edge{opacity:.12}
svg.has-sel .edge-label:not(.on),svg.has-layer .edge-label{opacity:.15}
svg .edge.on{stroke-width:2.8!important}
svg .node.sel .node-box{stroke:var(--signal);stroke-width:3}
.panel{border-left:1px solid var(--rule);padding:16px;overflow:auto;background:var(--sheet)}
.panel h2{font:700 18px/1.25 var(--ao-heading-font,"Schibsted Grotesk","IBM Plex Sans","Segoe UI",system-ui,sans-serif);margin:0 0 2px}
.panel .sub{color:var(--ink-2);margin:0 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:3px 8px;border-radius:999px;border:1px solid var(--rule);background:var(--paper)}
button.chip:hover{border-color:var(--signal)}
.links{list-style:none;margin:0;padding:0}
.links li{margin:2px 0}
.links button{border:0;background:none;padding:4px 6px;border-radius:6px;text-align:left;width:100%}
.links button:hover{background:var(--signal-soft)}
.links .lab{font-size:11px;color:var(--ink-2);margin-left:4px}
.mention{border-left:3px solid var(--rule);padding:2px 0 2px 10px;margin:8px 0;font-size:13px;color:var(--ink-2)}
.mention button{border:0;background:none;padding:0;color:var(--signal);font-weight:600;font-size:13px}
.muted{color:var(--ink-2)}
.empty{color:var(--ink-2);font-size:14px}
.equiv{display:flex;gap:8px;align-items:center;padding:8px 10px;border:1px dashed var(--rule);border-radius:8px;margin:10px 0}
.equiv button{margin-left:auto}
/* generic content */
.wrap{max-width:1180px;margin:0 auto;padding:20px 20px 40px}
.wrap>h1{font:800 26px/1.15 var(--ao-heading-font,"Schibsted Grotesk","IBM Plex Sans","Segoe UI",system-ui,sans-serif);margin:0 0 6px}
.lede{color:var(--ink-2);margin:0 0 18px;max-width:72ch}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--sheet)}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--rule)}
th{font-weight:600;background:color-mix(in srgb,var(--ink) 5%,var(--sheet));position:sticky;top:0}
tbody tr.click{cursor:pointer}
tbody tr.click:hover,tbody tr[aria-selected="true"]{background:var(--signal-soft)}
.tablebox{border:1px solid var(--rule);border-radius:8px;overflow:auto}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px;align-items:center}
.filters input,.filters select{padding:6px 9px;border:1px solid var(--rule);border-radius:7px;background:var(--sheet)}
mark{background:color-mix(in srgb,var(--gate) 30%,transparent);color:inherit;border-radius:2px}
/* gates */
.steps{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 16px}
.steps button{border:1px solid var(--rule);background:var(--sheet);border-radius:8px;padding:6px 10px;font-weight:600}
.steps button[aria-current="true"]{background:var(--ink);color:var(--sheet);border-color:var(--ink)}
.gatecard{background:var(--sheet);border:1px solid var(--rule);border-radius:10px;padding:18px}
.gatecard h2{margin:0 0 4px;font:700 20px/1.2 var(--ao-heading-font,"Schibsted Grotesk","IBM Plex Sans","Segoe UI",system-ui,sans-serif)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.col{border:1px solid var(--rule);border-radius:8px;padding:12px;border-top:4px solid var(--c)}
.col h4{margin:0 0 6px}
.col dt{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--ink-2);margin-top:8px}
.col dd{margin:2px 0 0}
ol.delivery{columns:2;padding-left:20px}
/* tools */
.tgrid{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:16px}
.meter{display:flex;gap:3px;margin:6px 0}
.meter span{flex:1;text-align:center;font-size:11px;padding:3px 0;border-radius:4px;background:var(--paper);border:1px solid var(--rule);color:var(--ink-2)}
.meter span.on{background:color-mix(in srgb,var(--auto) 22%,var(--sheet));color:var(--ink);border-color:var(--auto)}
.meter span.start{outline:2px solid var(--signal)}
/* compare */
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0 20px}
.pane{background:var(--sheet);border:1px solid var(--rule);border-radius:10px;overflow:hidden}
.pane h4{margin:0;padding:8px 12px;border-bottom:1px solid var(--rule)}
.pane svg{width:100%;height:auto;display:block}
/* docs */
.docs{display:grid;grid-template-columns:260px minmax(0,1fr);height:100%}
.toc{border-right:1px solid var(--rule);overflow:auto;padding:10px;background:var(--sheet);font-size:14px}
.toc details{margin:2px 0}
.toc summary{cursor:pointer;font-weight:600;padding:4px 6px}
.toc button{display:block;width:100%;text-align:left;border:0;background:none;padding:4px 8px 4px 16px;border-radius:6px;color:var(--ink-2)}
.toc button[aria-current="true"]{background:var(--signal-soft);color:var(--ink);font-weight:600}
article{padding:24px 28px 60px;overflow:auto;max-width:900px}
article h1{font:800 26px/1.15 var(--ao-heading-font,"Schibsted Grotesk","IBM Plex Sans","Segoe UI",system-ui,sans-serif)}
article h2{font:700 20px/1.2 var(--ao-heading-font,"Schibsted Grotesk","IBM Plex Sans","Segoe UI",system-ui,sans-serif);margin-top:28px}
article img{max-width:100%}
article pre{background:var(--sheet);border:1px solid var(--rule);border-radius:8px;padding:12px;overflow:auto;font-size:13px}
article blockquote{border-left:4px solid var(--gate);margin:12px 0;padding:6px 14px;background:var(--sheet)}
article table{display:block;overflow:auto}
.ao-embed{border:1px solid var(--rule);border-radius:10px;background:var(--sheet);margin:14px 0;overflow:hidden}
.ao-embed svg{width:100%;height:auto;display:block}
.ao-embed .bar{display:flex;justify-content:space-between;align-items:center;padding:6px 10px;border-top:1px solid var(--rule);font-size:13px;color:var(--ink-2)}
.mmd svg{max-width:100%;height:auto}
.err{padding:30px;color:var(--risk)}
.norepo{font-weight:500}
@media (max-width:980px){
  .dgrid{grid-template-columns:1fr;grid-template-rows:auto 60vh auto;height:auto}
  .rail{border-right:0;border-bottom:1px solid var(--rule)}
  .rail .dlist{display:flex;overflow:auto;gap:4px}.rail .dlist button{white-space:nowrap}
  .layers{flex-direction:row;flex-wrap:wrap}
  .panel{border-left:0;border-top:1px solid var(--rule)}
  .tgrid,.cols,.pair{grid-template-columns:1fr}
  .docs{grid-template-columns:1fr;height:auto}.toc{max-height:40vh;border-right:0;border-bottom:1px solid var(--rule)}
  .view{height:auto;min-height:100%}
  ol.delivery{columns:1}
}
@media (prefers-reduced-motion:reduce){svg .node,svg .edge,svg .edge-label{transition:none}}
`;

class AgenticOpsExplorer extends HTMLElement {
  static get observedAttributes() { return ["cloud", "view", "theme"]; }

  constructor() {
    super();
    this.root = this.attachShadow({ mode: "open" });
    this.state = { view: "diagrams", cloud: "gcp", diagram: "full-system-architecture", node: null, layer: null,
      doc: null, tool: null, gate: "G1", compare: "full-system-architecture" };
    this.vb = null;
    this._data = null;
  }

  set data(d) { this._data = d; if (this.isConnected) this._boot(); }
  get data() { return this._data; }

  connectedCallback() {
    this.root.innerHTML = `<style>${CSS}</style><div class="app"><div class="err" role="status">Loading architecture…</div></div>`;
    this._applyTheme();
    if (this._data) return this._boot();
    const src = this.getAttribute("src") || "data.json";
    const load = src.startsWith("#")
      ? Promise.resolve(JSON.parse(document.querySelector(src).textContent))
      : fetch(src).then((r) => { if (!r.ok) throw new Error(r.status + " " + r.statusText); return r.json(); });
    load.then((d) => { this._data = d; this._boot(); })
      .catch((e) => { this.root.querySelector(".app").innerHTML = `<div class="err">Could not load architecture data from <code>${esc(src)}</code>: ${esc(e.message)}</div>`; });
  }

  attributeChangedCallback(name) {
    if (name === "theme") this._applyTheme();
    else if (this._data) this.navigate({ [name]: this.getAttribute(name) });
  }

  _applyTheme() {
    const t = this.getAttribute("theme") || "auto";
    if (t === "auto") this.removeAttribute("data-theme"); else this.setAttribute("data-theme", t);
  }

  _tokens() {
    const tk = this._data.tokens;
    const vars = (o) => Object.entries(o).map(([k, v]) => `--${k}:${v}`).join(";");
    const soft = (o) => `--signal-soft:color-mix(in srgb,${o.signal} 16%,${o.sheet})`;
    return `:host{${vars(tk.light)};${soft(tk.light)}}
@media (prefers-color-scheme:dark){:host(:not([data-theme="light"])){${vars(tk.dark)};${soft(tk.dark)}}}
:host([data-theme="dark"]){${vars(tk.dark)};${soft(tk.dark)}}`;
  }

  _boot() {
    const d = this._data;
    this.repo = (this.getAttribute("repo-url") || d.repo_url || "").replace(/\/$/, "");
    if (/YOUR-[A-Z-]+/.test(this.repo)) this.repo = "";   // placeholder address: hide links that would 404
    this.repoPath = this.hasAttribute("repo-path") ? this.getAttribute("repo-path") : (d.repo_path || "");
    this.diagrams = Object.fromEntries(d.diagrams.map((x) => [x.id, x]));
    this.docs = Object.fromEntries(d.docs.map((x) => [x.id, x]));
    this.tools = Object.fromEntries(d.tools.tools.map((x) => [x.name, x]));
    this._buildIndex();
    this.root.innerHTML = `<style>${CSS}</style><style>${this._tokens()}</style>
      <div class="app">
        <header>
          <div class="brand">${esc(d.title)}</div>
          <nav class="views" aria-label="Views">${VIEWS.map(([k, l]) => `<button data-view="${k}">${l}</button>`).join("")}</nav>
          <span class="spacer"></span>
          <div class="seg" role="group" aria-label="Cloud">${Object.entries(d.clouds).map(([k, l]) => `<button data-cloud="${k}">${esc(l)}</button>`).join("")}</div>
          <div class="search"><input type="search" placeholder="Search components, tools, docs…" aria-label="Search" autocomplete="off"><div class="results" hidden role="listbox"></div></div>
          <button class="iconbtn theme" title="Toggle light / dark" aria-label="Toggle light or dark theme">◐</button>
        </header>
        <main><div class="view" tabindex="-1"></div></main>
      </div>`;
    const $ = (s) => this.root.querySelector(s);
    this.$view = $(".view");
    this.root.querySelectorAll("[data-view]").forEach((b) => b.onclick = () => this.navigate({ view: b.dataset.view }));
    this.root.querySelectorAll("[data-cloud]").forEach((b) => b.onclick = () => this.navigate({ cloud: b.dataset.cloud, node: null }));
    $(".theme").onclick = () => {
      const cur = this.getAttribute("theme") || "auto";
      const dark = cur === "dark" || (cur === "auto" && matchMedia("(prefers-color-scheme: dark)").matches);
      this.setAttribute("theme", dark ? "light" : "dark");
    };
    this._wireSearch($(".search input"), $(".results"));
    this.root.addEventListener("click", (e) => {
      const a = e.composedPath().find((n) => n.tagName === "A");
      if (!a) return;
      const href = a.getAttribute("href") || "";
      if (href.startsWith("#doc:")) { e.preventDefault(); this.navigate({ view: "docs", doc: href.slice(5) }); }
      else if (/^https?:/.test(href)) { a.target = "_blank"; a.rel = "noopener"; }
    });
    const init = {
      view: this.getAttribute("view") || this.state.view,
      cloud: this.getAttribute("cloud") || this.state.cloud,
    };
    this.routing = this.getAttribute("routing") === "hash";
    if (this.routing) {
      Object.assign(init, this._parseHash());
      window.addEventListener("hashchange", () => { const h = this._parseHash(); if (Object.keys(h).length) this.navigate(h, true); });
    }
    this.navigate(init, true);
  }

  /* ---------------- routing ---------------- */
  _parseHash() {
    const p = location.hash.replace(/^#\/?/, "").split("/").map(decodeURIComponent).filter(Boolean);
    if (!p.length || !VIEWS.some(([k]) => k === p[0])) return {};
    const s = { view: p[0] };
    if (p[0] === "diagrams") { if (p[1]) s.cloud = p[1]; if (p[2]) s.diagram = p[2]; s.node = p[3] || null; }
    if (p[0] === "docs" && p[1]) s.doc = p[1];
    if (p[0] === "tools") s.tool = p[1] || null;
    if (p[0] === "gates" && p[1]) s.gate = p[1];
    if (p[0] === "compare" && p[1]) s.compare = p[1];
    return s;
  }
  _hash() {
    const s = this.state;
    const parts = { diagrams: [s.cloud, s.diagram, s.node], docs: [s.doc], tools: [s.tool], gates: [s.gate], compare: [s.compare] }[s.view] || [];
    return "#/" + [s.view, ...parts.filter(Boolean)].map(encodeURIComponent).join("/");
  }

  navigate(patch, fromRoute = false) {
    if (!this._data) { Object.assign(this.state, patch); return; }
    const prevView = this.state.view;
    Object.assign(this.state, patch);
    const s = this.state;
    if (!this.diagrams[`${s.cloud}-${s.diagram}`]) s.diagram = "full-system-architecture";
    if (s.node && !this.diagrams[`${s.cloud}-${s.diagram}`].nodes.some((n) => n.id === s.node)) s.node = null;
    if (s.view === "docs" && !this.docs[s.doc]) s.doc = this._data.docs[0].id;
    this.root.querySelectorAll("[data-view]").forEach((b) => b.setAttribute("aria-current", b.dataset.view === s.view ? "page" : "false"));
    this.root.querySelectorAll("[data-cloud]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.cloud === s.cloud)));
    const sameDiagram = s.view === "diagrams" && prevView === "diagrams" && this._shown === `${s.cloud}-${s.diagram}`;
    if (sameDiagram) { this._select(s.node); this._layer(s.layer); }
    else { this["_view_" + s.view](); }
    if (this.routing && !fromRoute) {
      const h = this._hash();
      if (location.hash !== h) history.pushState(null, "", h);
    }
    this.dispatchEvent(new CustomEvent("ao-navigate", { detail: { ...s }, bubbles: true, composed: true }));
  }

  /* ---------------- search ---------------- */
  _buildIndex() {
    const d = this._data, idx = [];
    for (const dg of d.diagrams) for (const n of dg.nodes)
      idx.push({ type: "Components", label: n.title, sub: `${n.sub || ""} · ${d.clouds[dg.cloud]} · ${dg.title}`, text: "",
        go: { view: "diagrams", cloud: dg.cloud, diagram: dg.key, node: n.id } });
    for (const t of d.tools.tools)
      idx.push({ type: "Tools", label: t.name, sub: t.description, text: `${t.gcp} ${t.aws}`, go: { view: "tools", tool: t.name } });
    for (const g of d.gates)
      idx.push({ type: "Gates", label: `${g.id} ${g.name}`, sub: g.question || "", text: "", go: { view: "gates", gate: g.id } });
    for (const p of d.docs)
      idx.push({ type: "Docs", label: p.title, sub: `${p.group}`, text: p.text, go: { view: "docs", doc: p.id } });
    this.index = idx;
  }
  _wireSearch(input, box) {
    let items = [], sel = -1;
    const close = () => { box.hidden = true; sel = -1; };
    const run = () => {
      const q = input.value.trim().toLowerCase();
      if (q.length < 2) return close();
      const toks = q.split(/\s+/);
      const scored = [];
      for (const it of this.index) {
        const l = it.label.toLowerCase(), hay = (it.label + " " + it.sub + " " + it.text).toLowerCase();
        if (!toks.every((t) => hay.includes(t))) continue;
        let sc = l.startsWith(q) ? 100 : l.includes(q) ? 60 : toks.every((t) => (it.label + " " + it.sub).toLowerCase().includes(t)) ? 30 : 5;
        if (it.type === "Components" && it.go.cloud === this.state.cloud) sc += 3;
        scored.push([sc, it]);
      }
      scored.sort((a, b) => b[0] - a[0]);
      const byType = {};
      for (const [, it] of scored) { (byType[it.type] ||= []).length < 6 && byType[it.type].push(it); }
      items = Object.values(byType).flat();
      box.innerHTML = items.length ? Object.entries(byType).map(([t, arr]) => `<div class="grp">${t}</div>` + arr.map((it) =>
        `<button role="option" data-i="${items.indexOf(it)}">${esc(it.label)}<small>${esc(it.sub).slice(0, 140)}</small></button>`).join("")).join("")
        : `<div class="grp">No matches</div>`;
      box.hidden = false;
      box.querySelectorAll("button").forEach((b) => b.onclick = () => { this.navigate(items[+b.dataset.i].go); input.value = ""; close(); });
    };
    input.addEventListener("input", run);
    input.addEventListener("keydown", (e) => {
      const bs = [...box.querySelectorAll("button")];
      if (e.key === "Escape") { close(); input.blur(); }
      else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); if (!bs.length) return;
        sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + bs.length) % bs.length;
        bs.forEach((b, i) => b.setAttribute("aria-selected", String(i === sel))); bs[sel].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && bs.length) { (bs[sel >= 0 ? sel : 0]).click(); }
    });
    input.addEventListener("blur", () => setTimeout(close, 150));
  }

  /* ---------------- diagrams ---------------- */
  _view_diagrams() {
    const s = this.state, d = this._data;
    const dg = this.diagrams[`${s.cloud}-${s.diagram}`];
    const ORDER = ["l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9", "l10", "gate", "risk", "auto", "signal"];
    const layersUsed = [...new Set(dg.nodes.map((n) => n.layer))].sort((a, b) => ORDER.indexOf(a) - ORDER.indexOf(b));
    this.$view.innerHTML = `<div class="dgrid">
      <aside class="rail">
        <h3>${esc(d.clouds[s.cloud])} diagrams</h3>
        <div class="dlist">${d.diagrams.filter((x) => x.cloud === s.cloud).map((x) =>
          `<button data-dg="${x.key}" aria-current="${x.key === s.diagram}">${esc(x.title)}</button>`).join("")}</div>
        <h3>Highlight a layer</h3>
        <div class="layers">${layersUsed.map((l) => `<button data-layer="${l}" aria-pressed="${s.layer === l}"><span class="dot" style="--c:var(--${l})"></span>${esc(d.layers[l] || l)}</button>`).join("")}</div>
      </aside>
      <section class="stage">
        <div class="toolbar"><span class="t">${esc(dg.aria)}</span>
          <button class="iconbtn" data-z="out" aria-label="Zoom out">−</button>
          <button class="iconbtn" data-z="in" aria-label="Zoom in">+</button>
          <button class="iconbtn" data-z="fit">Fit</button>
          ${dg.chapter ? `<a class="iconbtn" href="#doc:${dg.chapter}">Read chapter</a>` : ""}
          ${this.repo ? `<a class="iconbtn" href="${esc(this.repo)}/raw/main/${esc(this.repoPath)}${dg.png}">PNG</a>` : ""}
        </div>
        <div class="canvas" aria-label="Diagram canvas">${dg.svg}<div class="hint">Click a component · drag to pan · scroll or pinch to zoom</div></div>
      </section>
      <aside class="panel" aria-live="polite"></aside>
    </div>`;
    this._shown = dg.id;
    this.$view.querySelectorAll("[data-dg]").forEach((b) => b.onclick = () => this.navigate({ diagram: b.dataset.dg, node: null, layer: null }));
    this.$view.querySelectorAll("[data-layer]").forEach((b) => b.onclick = () => this.navigate({ layer: s.layer === b.dataset.layer ? null : b.dataset.layer }));
    const canvas = this.$view.querySelector(".canvas"), svg = canvas.querySelector("svg");
    this.svg = svg; this.dg = dg;
    this._panZoom(canvas, svg, dg);
    svg.querySelectorAll(".node").forEach((g) => {
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); this.navigate({ node: g.dataset.id }); } });
    });
    this.$view.querySelectorAll("[data-z]").forEach((b) => b.onclick = () => {
      if (b.dataset.z === "fit") return this._setVB([0, 0, dg.width, dg.height]);
      const f = b.dataset.z === "in" ? 0.8 : 1.25, [x, y, w, h] = this.vb;
      this._zoomAt(x + w / 2, y + h / 2, f);
    });
    this._select(s.node);
    this._layer(s.layer);
  }

  _setVB(v) { this.vb = v; this.svg.setAttribute("viewBox", v.map((n) => n.toFixed(1)).join(" ")); }
  _zoomAt(px, py, f) {
    const [x, y, w, h] = this.vb, dg = this.dg;
    const nw = Math.min(Math.max(w * f, dg.width / 8), dg.width * 1.6);
    const k = nw / w;
    this._setVB([px - (px - x) * k, py - (py - y) * k, w * k, h * k]);
  }
  _panZoom(canvas, svg, dg) {
    this._setVB([0, 0, dg.width, dg.height]);
    const toSvg = (cx, cy) => { const p = svg.createSVGPoint(); p.x = cx; p.y = cy; return p.matrixTransform(svg.getScreenCTM().inverse()); };
    canvas.addEventListener("wheel", (e) => {
      if (!e.ctrlKey && !e.metaKey && Math.abs(e.deltaY) < 1) return;
      e.preventDefault(); const p = toSvg(e.clientX, e.clientY);
      this._zoomAt(p.x, p.y, Math.exp(e.deltaY * 0.0015));
    }, { passive: false });
    const pts = new Map(); let start = null, moved = false, pinch = null;
    canvas.addEventListener("pointerdown", (e) => {
      pts.set(e.pointerId, e); canvas.setPointerCapture(e.pointerId); moved = false;
      if (pts.size === 1) start = { x: e.clientX, y: e.clientY, vb: [...this.vb], target: e.target };
      if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = { d: Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY), vb: [...this.vb] }; }
    });
    canvas.addEventListener("pointermove", (e) => {
      if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, e);
      if (pts.size === 2 && pinch) {
        const [a, b] = [...pts.values()], d = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
        const m = toSvg((a.clientX + b.clientX) / 2, (a.clientY + b.clientY) / 2);
        this.vb = [...pinch.vb]; this._zoomAt(m.x, m.y, pinch.d / d); moved = true; return;
      }
      if (!start) return;
      const dx = e.clientX - start.x, dy = e.clientY - start.y;
      if (!moved && Math.hypot(dx, dy) < 4) return;
      moved = true; canvas.classList.add("dragging");
      const r = svg.getBoundingClientRect(), sc = Math.min(r.width / start.vb[2], r.height / start.vb[3]);
      this._setVB([start.vb[0] - dx / sc, start.vb[1] - dy / sc, start.vb[2], start.vb[3]]);
    });
    const end = (e) => {
      if (!pts.has(e.pointerId)) return; pts.delete(e.pointerId); canvas.classList.remove("dragging");
      if (pts.size < 2) pinch = null;
      if (!moved && start && pts.size === 0) {
        const g = start.target.closest && start.target.closest(".node");
        this.navigate({ node: g ? g.dataset.id : null });
      }
      if (pts.size === 0) start = null;
    };
    canvas.addEventListener("pointerup", end); canvas.addEventListener("pointercancel", end);
  }

  _layer(l) {
    if (!this.svg) return;
    this.svg.classList.toggle("has-layer", !!l && !this.state.node);
    this.svg.querySelectorAll(".node").forEach((g) => g.classList.toggle("lay", g.dataset.layer === l));
    this.$view.querySelectorAll("[data-layer]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.layer === l)));
  }

  _select(id) {
    const svg = this.svg, dg = this.dg, d = this._data, panel = this.$view.querySelector(".panel");
    if (!svg || !panel) return;
    svg.classList.toggle("has-sel", !!id);
    svg.classList.toggle("has-layer", !id && !!this.state.layer);
    const nb = new Set();
    svg.querySelectorAll(".edge,.edge-label").forEach((e) => {
      const on = !!id && (e.dataset.from === id || e.dataset.to === id);
      e.classList.toggle("on", on);
      if (on) { nb.add(e.dataset.from); nb.add(e.dataset.to); }
    });
    svg.querySelectorAll(".node").forEach((g) => { g.classList.toggle("sel", g.dataset.id === id); g.classList.toggle("nb", nb.has(g.dataset.id)); });
    if (!id) {
      const counts = dg.nodes.length, zones = [...new Set(dg.nodes.map((n) => n.zone).filter(Boolean))];
      panel.innerHTML = `<h2>${esc(dg.title)}</h2><p class="sub">${esc(d.clouds[dg.cloud])} edition</p>
        <p class="empty">Select any component to see what it connects to, where the docs discuss it, the tools it relates to, and its equivalent on the other cloud.</p>
        <h3>In this diagram</h3><p>${counts} components, ${dg.edges.length} connections</p>
        ${zones.length ? `<h3>Zones</h3><ul class="links">${zones.map((z) => `<li class="muted">${esc(z)}</li>`).join("")}</ul>` : ""}`;
      return;
    }
    const n = dg.nodes.find((x) => x.id === id);
    if (!n) return;
    const cw = this.$view.querySelector(".canvas")?.clientWidth || 1000;
    if (cw < 700) {   // small screens: zoom to the selected component
      const w = 520, h = w * ((this.vb && this.vb[3] / this.vb[2]) || 0.7);
      this._setVB([n.pos[0] + 100 - w / 2, n.pos[1] + 28 - h / 2, w, h]);
    }
    const byId = Object.fromEntries(dg.nodes.map((x) => [x.id, x]));
    const inc = dg.edges.filter((e) => e.to === id && e.from), out = dg.edges.filter((e) => e.from === id && e.to);
    const li = (e, other) => `<li><button data-node="${other}">${esc(byId[other]?.title || other)}${e.label ? `<span class="lab">${esc(e.label)}</span>` : ""}</button></li>`;
    const eq = n.equivalent && n.equivalent.node ? this.diagrams[n.equivalent.diagram].nodes.find((x) => x.id === n.equivalent.node) : null;
    panel.innerHTML = `<h2>${esc(n.title)}</h2><p class="sub">${esc(n.sub || "")}</p>
      <div class="chips"><span class="chip"><span class="dot" style="--c:var(--${n.layer})"></span>${esc(n.layer_name)}</span>${n.zone ? `<span class="chip">${esc(n.zone)}</span>` : ""}</div>
      ${eq ? `<div class="equiv"><span><span class="muted">On ${esc(d.clouds[n.equivalent.cloud])}:</span> <strong>${esc(eq.title)}</strong><br><small class="muted">${esc(eq.sub || "")}</small></span>
        <button class="iconbtn" data-eq>Switch</button></div>` : ""}
      ${inc.length ? `<h3>Receives from</h3><ul class="links">${inc.map((e) => li(e, e.from)).join("")}</ul>` : ""}
      ${out.length ? `<h3>Sends to</h3><ul class="links">${out.map((e) => li(e, e.to)).join("")}</ul>` : ""}
      ${n.tools.length ? `<h3>Related tools</h3><div class="chips">${n.tools.map((t) => `<button class="chip" data-tool="${esc(t)}">${esc(t)}</button>`).join("")}</div>` : ""}
      ${n.mentions.length ? `<h3>Discussed in</h3>${n.mentions.map((m) => `<div class="mention"><button data-doc="${m.doc}">${esc(m.title)}</button><br>${esc(m.snippet)}</div>`).join("")}` : ""}`;
    panel.querySelectorAll("[data-node]").forEach((b) => b.onclick = () => this.navigate({ node: b.dataset.node }));
    panel.querySelectorAll("[data-tool]").forEach((b) => b.onclick = () => this.navigate({ view: "tools", tool: b.dataset.tool }));
    panel.querySelectorAll("[data-doc]").forEach((b) => b.onclick = () => this.navigate({ view: "docs", doc: b.dataset.doc }));
    const eb = panel.querySelector("[data-eq]");
    if (eb) eb.onclick = () => this.navigate({ cloud: n.equivalent.cloud, node: n.equivalent.node });
    this.dispatchEvent(new CustomEvent("ao-select", { detail: { cloud: dg.cloud, diagram: dg.key, node: { ...n } }, bubbles: true, composed: true }));
  }

  /* ---------------- gates ---------------- */
  _view_gates() {
    const d = this._data, s = this.state;
    const g = d.gates.find((x) => x.id === s.gate) || d.gates[0];
    const col = (cloud, c) => {
      const r = g[cloud]; if (!r) return "";
      return `<div class="col" style="--c:var(--${c})"><h4>${esc(d.clouds[cloud])}</h4><dl>
        <dt>Checks</dt><dd>${esc(r.Checks)}</dd><dt>Services</dt><dd>${esc(r.Services)}</dd>
        ${r.Owner ? `<dt>Owner</dt><dd>${esc(r.Owner)}</dd>` : ""}<dt>On failure</dt><dd>${esc(r["On failure"])}</dd></dl></div>`;
    };
    const i = d.gates.indexOf(g);
    this.$view.innerHTML = `<div class="wrap"><h1>Security gates</h1>
      <p class="lede">Every request passes twelve deterministic gates that are independently owned, logged and fail closed. No gate depends on the model behaving well.</p>
      <div class="steps" role="tablist">${d.gates.map((x) => `<button data-g="${x.id}" aria-current="${x.id === g.id}" title="${esc(x.name)}">${x.id}</button>`).join("")}</div>
      <div class="gatecard"><h2>${esc(g.id)} ${esc(g.name)}</h2>
        ${g.question ? `<p class="lede" style="margin:0">${esc(g.question)}</p>` : ""}
        ${g.owner ? `<div class="chips"><span class="chip">Owner: ${esc(g.owner)}</span></div>` : ""}
        <div class="cols">${col("gcp", "l2")}${col("aws", "l6")}</div>
        <div class="filters" style="margin-top:14px">
          <button class="iconbtn" data-step="-1" ${i === 0 ? "disabled" : ""}>← Previous</button>
          <button class="iconbtn" data-step="1" ${i === d.gates.length - 1 ? "disabled" : ""}>Next →</button>
          <span class="spacer"></span><button class="iconbtn" data-show>Show on the ${esc(d.clouds[s.cloud])} gate diagram</button>
        </div></div>
      <h2 style="margin-top:28px">Delivery gates</h2>
      <p class="lede">Agents, prompts, tools, policies and models ship through the same pipeline.</p>
      <ol class="delivery">${(d.delivery_gates || []).map((x) => `<li><strong>${esc(x.id)}</strong> ${esc(x.check)}</li>`).join("")}</ol></div>`;
    this.$view.querySelectorAll("[data-g]").forEach((b) => b.onclick = () => this.navigate({ gate: b.dataset.g }));
    this.$view.querySelectorAll("[data-step]").forEach((b) => b.onclick = () => this.navigate({ gate: d.gates[i + +b.dataset.step].id }));
    this.$view.querySelector("[data-show]").onclick = () => {
      const dg = this.diagrams[`${s.cloud}-security-gates`];
      const node = dg && dg.nodes.find((n) => n.title.startsWith(g.id + " "));
      this.navigate({ view: "diagrams", diagram: "security-gates", node: node ? node.id : null });
    };
  }

  /* ---------------- tools ---------------- */
  _view_tools() {
    const d = this._data, s = this.state, servers = Object.fromEntries(d.tools.servers.map((x) => [x.id, x]));
    this.$view.innerHTML = `<div class="wrap"><h1>Tool catalogue</h1>
      <p class="lede">The only way agents change anything. Each server is an MCP server with its own least-privilege identity; every call passes action policy and, where required, human approval.</p>
      <div class="filters">
        <input type="search" data-f="q" placeholder="Filter tools" aria-label="Filter tools">
        <select data-f="cat" aria-label="Category"><option value="">All categories</option>${["read", "act", "workflow", "control"].map((c) => `<option>${c}</option>`).join("")}</select>
        <select data-f="srv" aria-label="Server"><option value="">All servers</option>${d.tools.servers.map((x) => `<option value="${x.id}">${esc(x.title)}</option>`).join("")}</select>
        <label><input type="checkbox" data-f="mut"> Mutating only</label>
        <span class="muted" data-count></span>
      </div>
      <div class="tgrid"><div class="tablebox"><table><thead><tr><th>Tool</th><th>Category</th><th>Autonomy</th><th>Blast radius</th></tr></thead><tbody></tbody></table></div>
      <aside class="panel" style="border:1px solid var(--rule);border-radius:10px"></aside></div></div>`;
    const tb = this.$view.querySelector("tbody"), f = (k) => this.$view.querySelector(`[data-f="${k}"]`);
    const draw = () => {
      const q = f("q").value.toLowerCase(), cat = f("cat").value, srv = f("srv").value, mut = f("mut").checked;
      const rows = d.tools.tools.filter((t) => (!cat || t.category === cat) && (!srv || t.server === srv) && (!mut || t.mutating) &&
        (!q || (t.name + " " + t.description + " " + t.gcp + " " + t.aws).toLowerCase().includes(q)));
      this.$view.querySelector("[data-count]").textContent = `${rows.length} of ${d.tools.tools.length}`;
      tb.innerHTML = rows.map((t) => `<tr class="click" data-t="${t.name}" tabindex="0" aria-selected="${t.name === s.tool}"><td><code>${esc(t.name)}</code><br><small class="muted">${esc(servers[t.server].title)}</small></td>
        <td>${t.category}</td><td>${t.default_autonomy} → ${t.max_autonomy}</td><td>${esc(t.blast_radius)}</td></tr>`).join("");
      tb.querySelectorAll("tr").forEach((r) => { r.onclick = () => this.navigate({ tool: r.dataset.t }); r.onkeydown = (e) => { if (e.key === "Enter") r.click(); }; });
    };
    ["q", "cat", "srv", "mut"].forEach((k) => f(k).addEventListener("input", draw));
    draw();
    const panel = this.$view.querySelector(".panel"), t = this.tools[s.tool];
    if (!t) { panel.innerHTML = `<p class="empty">Select a tool to see its inputs, autonomy range, gates and the services it calls on each cloud.</p>`; return; }
    const L = ["L0", "L1", "L2", "L3", "L4"], di = L.indexOf(t.default_autonomy), mi = L.indexOf(t.max_autonomy);
    panel.innerHTML = `<h2><code>${esc(t.name)}</code></h2><p class="sub">${esc(t.description)}</p>
      <div class="chips"><span class="chip">${t.category}</span><span class="chip">${t.mutating ? "mutating" : "read-only"}</span>
      <span class="chip">dry-run: ${t.dry_run ? "yes" : "no"}</span>${t.approval ? `<span class="chip">approval: ${esc(t.approval)}</span>` : ""}</div>
      <h3>Autonomy (start → ceiling)</h3><div class="meter">${L.map((l, i) => `<span class="${i <= mi ? "on" : ""} ${i === di ? "start" : ""}">${l}</span>`).join("")}</div>
      <h3>Inputs</h3><table><tbody>${Object.entries(t.inputs).map(([k, v]) => `<tr><td><code>${esc(k)}</code></td><td>${esc(v.type)}${v.enum ? ` (${v.enum.map(esc).join(", ")})` : ""}${v.optional ? " · optional" : ""}</td></tr>`).join("")}</tbody></table>
      <h3>Implementation</h3><p><strong>Google Cloud:</strong> ${esc(t.gcp)}<br><strong>AWS:</strong> ${esc(t.aws)}</p>
      <h3>Gates</h3><div class="chips">${t.gates.map((g) => `<button class="chip" data-gate="${g}">${g}</button>`).join("")}</div>
      ${t.notes ? `<p class="muted">${esc(t.notes)}</p>` : ""}
      ${this.repo ? `<p><a href="${esc(this.repo)}/blob/main/${esc(this.repoPath)}tools/mcp/${t.server}.json">MCP definition</a></p>` : ""}`;
    panel.querySelectorAll("[data-gate]").forEach((b) => b.onclick = () => this.navigate({ view: "gates", gate: b.dataset.gate }));
  }

  /* ---------------- compare ---------------- */
  _view_compare() {
    const d = this._data, s = this.state, key = s.compare;
    const keys = [...new Set(d.diagrams.map((x) => x.key))];
    const pane = (cloud) => { const dg = this.diagrams[`${cloud}-${key}`]; return dg ? `<div class="pane" data-cloud-pane="${cloud}"><h4>${esc(d.clouds[cloud])}</h4>${dg.svg}</div>` : ""; };
    this.$view.innerHTML = `<div class="wrap"><h1>Compare clouds</h1>
      <p class="lede">Both editions share one layout, so every component sits in the same place. Click a component on either side to highlight its counterpart.</p>
      <div class="filters"><select data-k aria-label="Diagram">${keys.map((k) => `<option value="${k}" ${k === key ? "selected" : ""}>${esc(d.diagrams.find((x) => x.key === k).title)}</option>`).join("")}</select></div>
      <div class="pair">${pane("gcp")}${pane("aws")}</div>
      <h2>Service mapping</h2>
      <div class="filters"><input type="search" data-mq placeholder="Filter by function or service" aria-label="Filter mapping"></div>
      <div class="tablebox"><table><thead><tr><th>Function</th><th>${esc(d.clouds.gcp)}</th><th>${esc(d.clouds.aws)}</th></tr></thead><tbody></tbody></table></div></div>`;
    this.$view.querySelector("[data-k]").onchange = (e) => this.navigate({ compare: e.target.value });
    const panes = [...this.$view.querySelectorAll("[data-cloud-pane]")];
    panes.forEach((p) => p.addEventListener("click", (e) => {
      const g = e.target.closest(".node"); panes.forEach((q) => q.querySelectorAll(".node").forEach((n) => n.classList.remove("sel")));
      panes.forEach((q) => q.querySelector("svg").classList.toggle("has-sel", !!g));
      if (!g) return;
      const cloud = p.dataset.cloudPane, n = this.diagrams[`${cloud}-${key}`].nodes.find((x) => x.id === g.dataset.id);
      g.classList.add("sel");
      if (n.equivalent && n.equivalent.node) {
        const other = this.$view.querySelector(`[data-cloud-pane="${n.equivalent.cloud}"] .node[data-id="${n.equivalent.node}"]`);
        if (other) other.classList.add("sel");
      }
    }));
    const tb = this.$view.querySelector("tbody"), mq = this.$view.querySelector("[data-mq]");
    const hl = (t, q) => q ? esc(t).replace(new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "ig"), (m) => `<mark>${m}</mark>`) : esc(t);
    const draw = () => {
      const q = mq.value.trim();
      tb.innerHTML = d.mapping.filter((r) => !q || (r.function + r.gcp + r.aws).toLowerCase().includes(q.toLowerCase()))
        .map((r) => `<tr><td><strong>${hl(r.function, q)}</strong></td><td>${hl(r.gcp, q)}</td><td>${hl(r.aws, q)}</td></tr>`).join("");
    };
    mq.addEventListener("input", draw); draw();
  }

  /* ---------------- docs ---------------- */
  _view_docs() {
    const d = this._data, s = this.state, page = this.docs[s.doc];
    const groups = {};
    for (const p of d.docs) (groups[p.group] ||= []).push(p);
    this.$view.innerHTML = `<div class="docs"><nav class="toc" aria-label="Documents">${Object.entries(groups).map(([g, ps]) =>
      `<details ${ps.some((p) => p.id === page.id) || g === "Overview" ? "open" : ""}><summary>${esc(g)}</summary>${ps.sort((a, b) => a.order - b.order)
        .map((p) => `<button data-doc="${p.id}" aria-current="${p.id === page.id}">${esc(p.title)}</button>`).join("")}</details>`).join("")}</nav>
      <article>${this._repoLinks(page.html)}</article></div>`;
    this.$view.querySelectorAll("[data-doc]").forEach((b) => b.onclick = () => this.navigate({ doc: b.dataset.doc }));
    const art = this.$view.querySelector("article");
    art.querySelectorAll(".ao-embed").forEach((el) => {
      const dg = this.diagrams[el.dataset.diagram]; if (!dg) return;
      el.innerHTML = `${dg.svg}<div class="bar"><span>${esc(dg.aria)}</span><button class="iconbtn">Explore interactively</button></div>`;
      el.querySelector("button").onclick = () => this.navigate({ view: "diagrams", cloud: dg.cloud, diagram: dg.key, node: null });
    });
    this.$view.scrollTop = 0; art.scrollTop = 0;
    this._mermaid(art);
  }

  _repoLinks(html) {
    if (this.repo) return html.replaceAll("REPO_URL", esc(this.repo));
    // No repository configured: keep the link text, drop links and images that would point nowhere.
    return html
      .replace(/<a href="REPO_URL[^"]*">(.*?)<\/a>/g, '<span class="norepo">$1</span>')
      .replace(/<img[^>]*src="REPO_URL[^"]*"[^>]*>/g, "");
  }

  async _mermaid(scope) {
    const blocks = [...scope.querySelectorAll("code.ao-mermaid")];
    const src = this.getAttribute("mermaid-src") || DEFAULT_MERMAID;
    if (!blocks.length || src === "none") return;
    try {
      if (!AgenticOpsExplorer._mm) AgenticOpsExplorer._mm = import(src).then((m) => m.default || m);
      const mermaid = await AgenticOpsExplorer._mm;
      const dark = this.getAttribute("data-theme") === "dark" || (!this.hasAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
      mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "neutral", securityLevel: "strict", fontFamily: "inherit" });
      for (const [i, code] of blocks.entries()) {
        try {
          const { svg } = await mermaid.render(`aomm${Date.now()}${i}`, code.textContent);
          const div = document.createElement("div"); div.className = "mmd"; div.innerHTML = svg;
          code.parentElement.replaceWith(div);
        } catch (e) { /* leave source visible */ }
      }
    } catch (e) { /* Mermaid unavailable (offline or blocked by CSP): source stays visible */ }
  }
}

if (!customElements.get("agentic-ops-explorer")) customElements.define("agentic-ops-explorer", AgenticOpsExplorer);
export { AgenticOpsExplorer };
