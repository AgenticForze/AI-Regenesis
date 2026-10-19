#!/usr/bin/env python3
"""Build the Architecture Explorer data bundle from the repository.

Reads diagram specs, themed SVGs, the tool catalogue and every Markdown chapter, and writes:
  explorer/dist/data.json                 data for <agentic-ops-explorer src="data.json">
  explorer/dist/agentic-ops-explorer.js   the web component (copied from src/)
  explorer/dist/index.html                standalone page
With --single-file PATH it also writes one self-contained HTML file (component + data inlined),
for portals or hosts that accept a single page.

Usage: python3 explorer/build.py [--repo-url URL] [--single-file out.html]
Requires: markdown, pyyaml (pip install markdown pyyaml)
"""
import argparse, glob, html, json, os, re, shutil, sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "skills", "architecture-diagrams", "scripts"))
from render import Diagram, LIGHT, DARK, LAYERS  # noqa: E402

DIAGRAM_TITLES = {"full-system-architecture": "Full system architecture", "end-to-end-flow": "End-to-end flow",
                  "hybrid-connectivity": "Hybrid connectivity", "security-gates": "Security gates G1–G12",
                  "telemetry-pipeline": "Telemetry pipeline"}
DIAGRAM_ORDER = list(DIAGRAM_TITLES)
DIAGRAM_CHAPTER = {"full-system-architecture": "11-full-system-architecture", "end-to-end-flow": "03-end-to-end-flow",
                   "hybrid-connectivity": "12-network-and-connectivity", "security-gates": "13-security-gates",
                   "telemetry-pipeline": "08-observability-and-telemetry"}
CLOUDS = {"gcp": "Google Cloud", "aws": "AWS"}
REPO_PATH = ""


def md_title(text):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else "Untitled"


def strip_nav(text):
    # remove the generated previous/next footer
    return re.sub(r"\n---\n\n(\[←|\[Index\]|\[Also available).*\Z", "\n", text, flags=re.S)


def md_tables(text):
    out = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*-", lines[i + 1]):
            head = [c.strip() for c in lines[i].strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append([c.strip() for c in lines[j].strip("|").split("|")])
                j += 1
            out.append((head, rows))
            i = j
        else:
            i += 1
    return out


def plain(md):
    s = re.sub(r"```.*?```", " ", md, flags=re.S)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`#>|†]", " ", s)
    return re.sub(r"\s+", " ", s)


class Docs:
    """Collect every Markdown page, rewrite links, render to HTML."""

    def __init__(self, repo_url):
        self.repo_url = repo_url.rstrip("/")
        self.pages = []
        self.by_path = {}

    def add(self, path, group, order):
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        text = strip_nav(open(path, encoding="utf-8").read())
        pid = re.sub(r"[^a-z0-9]+", "-", rel.lower().replace(".md", "")).strip("-")
        page = {"id": pid, "path": rel, "group": group, "order": order, "title": md_title(text), "md": text}
        self.pages.append(page)
        self.by_path[rel] = page

    def render(self):
        for p in self.pages:
            base = os.path.dirname(p["path"])

            def link(m):
                label, url = m.group(1), m.group(2)
                if re.match(r"^(https?:|mailto:|#)", url):
                    return m.group(0)
                target, _, frag = url.partition("#")
                rel = os.path.normpath(os.path.join(base, target)).replace(os.sep, "/")
                if rel.endswith("README.md") and rel not in self.by_path:
                    rel = rel  # fall through to repo link
                if rel in self.by_path:
                    return f"[{label}](#doc:{self.by_path[rel]['id']})"
                if os.path.isdir(os.path.join(ROOT, rel)):
                    return f"[{label}](REPO_URL/tree/main/{REPO_PATH}{rel})"
                return f"[{label}](REPO_URL/blob/main/{REPO_PATH}{rel})"

            def image(m):
                alt, url = m.group(1), m.group(2)
                if re.match(r"^https?:", url):
                    return m.group(0)
                rel = os.path.normpath(os.path.join(base, url)).replace(os.sep, "/")
                mm = re.match(r"diagrams/(?:png|svg)/(gcp|aws)-([\w-]+)\.(?:png|svg)$", rel)
                if mm:
                    return f'\n\n<div class="ao-embed" data-diagram="{mm.group(1)}-{mm.group(2)}"></div>\n\n'
                return f"![{alt}](REPO_URL/raw/main/{REPO_PATH}{rel})"

            md = re.sub(r"^\[!\[.*shields\.io.*$\n?", "", p["md"], flags=re.M)   # badges are decorative on GitHub only
            md = re.sub(r"^!\[[^\]]*\]\(https://img\.shields\.io[^)]*\)\s*$\n?", "", md, flags=re.M)
            md = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", image, md)
            md = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", link, md)
            md = re.sub(r"^\[SVG version\]\(.*\)$", "", md, flags=re.M)
            body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
            body = body.replace('<code class="language-mermaid">', '<code class="language-mermaid ao-mermaid">')
            p["html"] = body
            p["text"] = plain(p["md"])
            del p["md"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-url", default="https://github.com/AgenticForze/AI-Regenesis")
    ap.add_argument("--repo-path", default="agentic-ops/",
                    help="folder of this project inside the repository, with trailing slash (\"\" if it is the repo root)")
    ap.add_argument("--single-file")
    a = ap.parse_args()
    global REPO_PATH
    REPO_PATH = a.repo_path if (not a.repo_path or a.repo_path.endswith("/")) else a.repo_path + "/"

    # ---------- docs ----------
    docs = Docs(a.repo_url)
    docs.add(os.path.join(ROOT, "README.md"), "Overview", 0)
    for i, f in enumerate(sorted(glob.glob(os.path.join(ROOT, "concepts", "*.md")))):
        docs.add(f, "Concepts", i)
    for cloud in CLOUDS:
        for i, f in enumerate(sorted(glob.glob(os.path.join(ROOT, "architecture", cloud, "*.md")))):
            docs.add(f, f"{CLOUDS[cloud]} edition", i)
    for i, f in enumerate(sorted(glob.glob(os.path.join(ROOT, "templates", "adr", "*.md")))):
        docs.add(f, "Decisions (ADRs)", i)
    for i, f in enumerate(sorted(glob.glob(os.path.join(ROOT, "articles", "20*.md")))):
        docs.add(f, "Articles", i)
    for f in ["templates/autonomy-promotion-checklist.md", "templates/otel-span-schema.md", "tools/README.md", "BIBLIOGRAPHY.md"]:
        if os.path.exists(os.path.join(ROOT, f)):
            docs.add(os.path.join(ROOT, f), "Reference", len(docs.pages))
    raw_md = {p["path"]: p["md"] for p in docs.pages}
    docs.render()

    # ---------- diagrams ----------
    diagrams = []
    pos_index = {}
    for cloud in CLOUDS:
        for key in DIAGRAM_ORDER:
            spec_path = os.path.join(ROOT, "diagrams", "specs", f"{cloud}-{key}.json")
            if not os.path.exists(spec_path):
                continue
            spec = json.load(open(spec_path))
            d = Diagram(spec)
            man = d.manifest()
            svg = d.render(None)
            chapter = docs.by_path.get(f"architecture/{cloud}/{DIAGRAM_CHAPTER[key]}.md")
            nodes = []
            for n in man["nodes"]:
                sn = d.nodes[n["id"]]
                n["pos"] = [sn["x"], sn["y"]]
                pos_index[(cloud, key, sn["x"], sn["y"])] = n["id"]
                nodes.append(n)
            diagrams.append({"id": f"{cloud}-{key}", "cloud": cloud, "key": key, "title": DIAGRAM_TITLES[key],
                             "aria": man["title"], "svg": svg, "nodes": nodes, "edges": man["edges"],
                             "chapter": chapter["id"] if chapter else None,
                             "png": f"diagrams/png/{cloud}-{key}.png", "width": spec["width"], "height": spec["height"]})
    # equivalents across clouds: same diagram, same position
    for dg in diagrams:
        other = "aws" if dg["cloud"] == "gcp" else "gcp"
        for n in dg["nodes"]:
            eq = pos_index.get((other, dg["key"], n["pos"][0], n["pos"][1]))
            n["equivalent"] = {"cloud": other, "diagram": f"{other}-{dg['key']}", "node": eq} if eq else None

    # ---------- tools ----------
    tools = json.load(open(os.path.join(ROOT, "tools", "catalog.json")))

    # ---------- mentions and related tools for each node ----------
    sentences = []
    for p in docs.pages:
        if p["group"] in ("Overview", "Reference", "Articles"):
            continue
        for line in raw_md[p["path"]].splitlines():
            line = line.strip()
            if not line or line.startswith(("```", "#", "![", "---")) or re.match(r"^\|\s*-", line):
                continue
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[0] in ("Layer", "Gate", "Zone", "Agent", "Tier", "Threat", "Link", "Where", "Function", "Span", "Stage"):
                    continue
                parts = [plain(" — ".join(c for c in cells if c))]
            else:
                parts = re.split(r"(?<=[.!?])\s+", plain(line))
            for s in parts:
                s = s.strip()
                if 25 < len(s) < 420:
                    sentences.append((p, s))
    generic = {"telemetry", "alerts", "agents", "infrastructure", "rollback", "supervisor", "slms", "models"}

    def terms(n):
        out = []
        if n["title"].lower() not in generic and len(n["title"]) > 3:
            out.append(n["title"])
        for part in re.split(r",| \+ | and ", n.get("sub") or ""):
            part = part.strip()
            if len(part) >= 4 and part.lower() not in generic:
                out.append(part)
        return out

    for dg in diagrams:
        cloud_group = f"{CLOUDS[dg['cloud']]} edition"
        for n in dg["nodes"]:
            ts = [t.lower() for t in terms(n)]
            hits = {}
            for p, s in sentences:
                if p["group"] not in (cloud_group, "Concepts", "Decisions (ADRs)"):
                    continue
                sl = s.lower()
                score = sum(2 if t == n["title"].lower() else 1 for t in ts if t in sl)
                if score and (p["id"] not in hits or hits[p["id"]][0] < score):
                    hits[p["id"]] = (score, s, p["title"])
            n["mentions"] = [{"doc": k, "title": v[2], "snippet": v[1]} for k, v in
                             sorted(hits.items(), key=lambda kv: -kv[1][0])[:4]]
            rel = []
            for t in tools["tools"]:
                field = (t["gcp"] if dg["cloud"] == "gcp" else t["aws"]).lower()
                if any(len(x) >= 3 and x in field for x in ts):
                    rel.append(t["name"])
            if "executor" in n["title"].lower() or "mcp" in n["title"].lower():
                rel = [t["name"] for t in tools["tools"] if t["category"] == "act"]
            n["tools"] = rel[:12]

    # ---------- gates and mapping ----------
    gates = {}
    for cloud in CLOUDS:
        md = raw_md.get(f"architecture/{cloud}/13-security-gates.md", "")
        for head, rows in md_tables(md):
            if head and head[0] == "Gate":
                for r in rows:
                    rec = dict(zip(head, r))
                    gid = rec["Gate"].split()[0]
                    gates.setdefault(gid, {"id": gid, "name": rec["Gate"][len(gid):].strip()})[cloud] = rec
                break
    concept_md = raw_md.get("concepts/04-security-gate-model.md", "")
    for head, rows in md_tables(concept_md):
        if head[:2] == ["Gate", "Question it answers"]:
            for r in rows:
                gid = r[0].split()[0]
                if gid in gates:
                    gates[gid]["question"] = r[1]
                    gates[gid]["owner"] = r[2]
        if head == ["Gate", "Check"]:
            delivery = [{"id": r[0], "check": r[1]} for r in rows]
    mapping = []
    for head, rows in md_tables(raw_md.get("architecture/aws/19-gcp-to-aws-mapping.md", "")):
        if head[0] == "Function":
            mapping = [{"function": r[0], "gcp": r[1], "aws": r[2]} for r in rows]

    data = {"version": "1.1.0", "title": "Agentic Ops Reference Architecture", "repo_url": a.repo_url, "repo_path": REPO_PATH,
            "clouds": CLOUDS, "layers": LAYERS, "tokens": {"light": LIGHT, "dark": DARK},
            "diagrams": diagrams, "tools": tools, "gates": [gates[k] for k in sorted(gates, key=lambda g: int(g[1:]))],
            "delivery_gates": delivery, "mapping": mapping,
            "docs": [{k: p[k] for k in ("id", "path", "group", "order", "title", "html", "text")} for p in docs.pages]}

    dist = os.path.join(HERE, "dist")
    os.makedirs(dist, exist_ok=True)
    js = open(os.path.join(HERE, "src", "agentic-ops-explorer.js"), encoding="utf-8").read()
    open(os.path.join(dist, "agentic-ops-explorer.js"), "w", encoding="utf-8").write(js)
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    open(os.path.join(dist, "data.json"), "w", encoding="utf-8").write(payload)
    shutil.copy(os.path.join(HERE, "src", "index.html"), os.path.join(dist, "index.html"))
    print(f"data.json {len(payload) // 1024} KB: {len(diagrams)} diagrams, {len(tools['tools'])} tools, "
          f"{len(data['gates'])} gates, {len(mapping)} mappings, {len(docs.pages)} pages")
    if a.single_file:
        page = open(os.path.join(HERE, "src", "index.html"), encoding="utf-8").read()
        safe = payload.replace("</", "<\\/")
        page = page.replace('<script type="module" src="agentic-ops-explorer.js"></script>',
                            f'<script id="ao-data" type="application/json">{safe}</script>\n'
                            f'<script type="module">{js}</script>')
        page = page.replace('src="data.json"', 'src="#ao-data"')
        open(a.single_file, "w", encoding="utf-8").write(page)
        print(f"single file {os.path.getsize(a.single_file) // 1024} KB -> {a.single_file}")


if __name__ == "__main__":
    main()
