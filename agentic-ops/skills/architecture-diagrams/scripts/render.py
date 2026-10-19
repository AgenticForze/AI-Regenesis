#!/usr/bin/env python3
"""Spec-driven architecture diagram renderer.

Reads a JSON diagram spec (zones, nodes, edges, legend) and writes:
  <name>.svg         static SVG, light palette resolved (GitHub, docs, slides)
  <name>.themed.svg  SVG using CSS custom properties (embed in pages that define the tokens)
  <name>.png         2x PNG (needs cairosvg), plus <name>.dark.png with --dark
and prints layout warnings (text overflow, overlaps, edges crossing nodes, out-of-bounds).

Usage:
  render.py SPEC.json [SPEC.json ...] -o OUTDIR [--png] [--dark] [--strict]
  render.py --gallery icons.png          # icon reference sheet
  render.py --tokens                     # print the CSS token block for themed SVGs
  render.py --icons                      # list icon names
"""
import argparse, html, json, os, re, sys

from icons import ICONS

LIGHT = {"paper": "#EEF1F3", "sheet": "#FFFFFF", "ink": "#16212B", "ink-2": "#44525F", "rule": "#CBD3DA",
         "signal": "#1E5AA8", "auto": "#2E7D5B", "gate": "#B57612", "risk": "#AE2E24",
         "l0": "#5B6B7A", "l1": "#7A4FA3", "l2": "#1E5AA8", "l3": "#0E7C86", "l4": "#2E7D5B", "l5": "#8A6D1D",
         "l6": "#B5541B", "l7": "#4E6A2B", "l8": "#A3325A", "l9": "#34404C", "l10": "#3E5C8A"}
DARK = {"paper": "#10171E", "sheet": "#18222B", "ink": "#E6ECF1", "ink-2": "#A8B5C1", "rule": "#2E3B47",
        "signal": "#7FB0F0", "auto": "#6CC49A", "gate": "#E3AE4F", "risk": "#F08A80",
        "l0": "#8FA0AF", "l1": "#B18BD6", "l2": "#7FB0F0", "l3": "#5CC3CC", "l4": "#6CC49A", "l5": "#D2B35A",
        "l6": "#E6905A", "l7": "#9CC26A", "l8": "#E47FA3", "l9": "#9AA8B5", "l10": "#8DA9D6"}
FONT = "'IBM Plex Sans','Segoe UI',Roboto,Helvetica,Arial,sans-serif"
LAYERS = {"l0": "L0 Channels and external", "l1": "L1 Edge, identity and safety", "l2": "L2 Orchestration",
          "l3": "L3 Gateway and network transit", "l4": "L4 Model serving", "l5": "L5 Knowledge and memory",
          "l6": "L6 Tools and actions", "l7": "L7 Data and events", "l8": "L8 Observability",
          "l9": "L9 Security and governance", "l10": "L10 Platform and MLOps", "risk": "Restricted / security response",
          "gate": "Human approval", "auto": "Verified / pass", "signal": "Signal"}
COLORS = set(LIGHT) - {"paper", "sheet", "ink", "rule"}
EDGE_COLORS = ["ink-2", "risk", "auto", "gate", "signal"]
TITLE_PX, SUB_PX, LABEL_PX = 7.0, 5.6, 5.6   # approximate glyph widths used for overflow checks


def esc(s):
    return html.escape(str(s), quote=True)


class Diagram:
    def __init__(self, spec):
        self.spec = spec
        self.W, self.H = spec["width"], spec["height"]
        self.title = spec.get("title", "Architecture diagram")
        self.nodes = {}
        for n in spec.get("nodes", []):
            n = dict(n); n.setdefault("w", 200); n.setdefault("h", 56); n.setdefault("sub", None)
            if n["id"] in self.nodes:
                raise ValueError(f"duplicate node id {n['id']}")
            self.nodes[n["id"]] = n
        self.warnings = []

    # ---------- geometry ----------
    def anchor(self, ref):
        if isinstance(ref, (list, tuple)):
            return (float(ref[0]), float(ref[1]))
        m = re.fullmatch(r"([\w-]+)\.([lrtb])([+-]\d+(?:\.\d+)?)?", ref)
        if not m or m.group(1) not in self.nodes:
            raise ValueError(f"bad anchor '{ref}' (use nodeid.l|r|t|b with optional +N/-N offset)")
        n, side, off = self.nodes[m.group(1)], m.group(2), float(m.group(3) or 0)
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        return {"l": (x, y + h / 2 + off), "r": (x + w, y + h / 2 + off),
                "t": (x + w / 2 + off, y), "b": (x + w / 2 + off, y + h)}[side]

    def edge_points(self, e):
        if "points" in e:
            return [self.anchor(p) for p in e["points"]]
        p, q = self.anchor(e["from"]), self.anchor(e["to"])
        route, mid = e.get("route", "auto"), e.get("mid")
        via = [self.anchor(v) for v in e.get("via", [])]
        if via:
            return [p] + via + [q]
        if route == "straight" or abs(p[0] - q[0]) < .5 or abs(p[1] - q[1]) < .5:
            return [p, q]
        if route == "auto":
            route = "vh" if (isinstance(e["from"], str) and e["from"].split(".")[1][0] in "tb") else "hv"
        if route == "hv":
            mx = (p[0] + q[0]) / 2 if mid is None else mid
            return [p, (mx, p[1]), (mx, q[1]), q]
        my = (p[1] + q[1]) / 2 if mid is None else mid
        return [p, (p[0], my), (q[0], my), q]

    def node_at(self, pt, tol=1.5):
        for k, n in self.nodes.items():
            x, y, w, h = n["x"], n["y"], n["w"], n["h"]
            if x - tol <= pt[0] <= x + w + tol and y - tol <= pt[1] <= y + h + tol:
                on_border = (abs(pt[0] - x) <= tol or abs(pt[0] - x - w) <= tol or
                             abs(pt[1] - y) <= tol or abs(pt[1] - y - h) <= tol)
                if on_border:
                    return k
        return None

    # ---------- checks ----------
    def check(self, edges):
        W = self.warnings
        for k, n in self.nodes.items():
            avail = n["w"] - 58
            if len(n["title"]) * TITLE_PX > avail:
                W.append(f"node '{k}': title '{n['title']}' may overflow ({len(n['title'])} chars, ~{int(avail / TITLE_PX)} fit)")
            if n["sub"] and len(n["sub"]) * SUB_PX > avail:
                W.append(f"node '{k}': subtitle '{n['sub']}' may overflow ({len(n['sub'])} chars, ~{int(avail / SUB_PX)} fit)")
            if n["x"] < 0 or n["y"] < 0 or n["x"] + n["w"] > self.W or n["y"] + n["h"] > self.H:
                W.append(f"node '{k}' is outside the canvas")
            if n["icon"] not in ICONS:
                W.append(f"node '{k}': unknown icon '{n['icon']}'")
            if n["color"] not in COLORS:
                W.append(f"node '{k}': unknown color '{n['color']}'")
        ks = list(self.nodes)
        for i, a in enumerate(ks):
            A = self.nodes[a]
            for b in ks[i + 1:]:
                B = self.nodes[b]
                if A["x"] < B["x"] + B["w"] and B["x"] < A["x"] + A["w"] and A["y"] < B["y"] + B["h"] and B["y"] < A["y"] + A["h"]:
                    W.append(f"nodes '{a}' and '{b}' overlap")
        for z in self.spec.get("zones", []):
            if len(z["title"]) * 6.6 + 20 > z["w"] - 24:
                W.append(f"zone '{z['title']}': title pill wider than zone")
        for idx, (pts, e) in enumerate(edges):
            ends = {self.node_at(pts[0]), self.node_at(pts[-1])}
            for k, n in self.nodes.items():
                if k in ends:
                    continue
                x0, y0, x1, y1 = n["x"] + 2, n["y"] + 2, n["x"] + n["w"] - 2, n["y"] + n["h"] - 2
                for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                    if abs(ay - by) < .5 and y0 < ay < y1 and max(min(ax, bx), x0) < min(max(ax, bx), x1):
                        W.append(f"edge #{idx} ({e.get('label') or e.get('from', '')}) crosses node '{k}'"); break
                    if abs(ax - bx) < .5 and x0 < ax < x1 and max(min(ay, by), y0) < min(max(ay, by), y1):
                        W.append(f"edge #{idx} ({e.get('label') or e.get('from', '')}) crosses node '{k}'"); break
            lab = e.get("label")
            if lab:
                at = self.label_pos(pts, e)
                w = len(lab) * LABEL_PX + 14
                for k, n in self.nodes.items():
                    if (at[0] - w / 2 < n["x"] + n["w"] - 4 and n["x"] + 4 < at[0] + w / 2 and
                            at[1] - 9 < n["y"] + n["h"] - 4 and n["y"] + 4 < at[1] + 9):
                        W.append(f"edge label '{lab}' overlaps node '{k}' (set \"at\")"); break
        return W

    def label_pos(self, pts, e):
        if e.get("at"):
            return tuple(e["at"])
        best, bi = -1, 0
        for i in range(len(pts) - 1):
            L = abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1])
            if L > best:
                best, bi = L, i
        p, q = pts[bi], pts[bi + 1]
        return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)

    # ---------- render ----------
    def render(self, palette=None, background=False):
        """palette=None -> themed (CSS vars); dict -> static colours resolved."""
        def c(tok):
            return f"var(--{tok})" if palette is None else palette[tok]

        def mix(tok, pct, base):
            if palette is None:
                b = "transparent" if base == "transparent" else f"var(--{base})"
                return f"color-mix(in srgb,var(--{tok}) {pct}%,{b})"
            A = _rgb(palette[tok])
            if base == "transparent":
                return "rgba(%d,%d,%d,%.2f)" % (*A, pct / 100)
            B = _rgb(palette[base])
            return "#%02x%02x%02x" % tuple(round(A[i] * pct / 100 + B[i] * (1 - pct / 100)) for i in range(3))

        edges = [(self.edge_points(e), e) for e in self.spec.get("edges", [])]
        self.check(edges)
        font = "var(--diagram-font," + FONT + ")" if palette is None else FONT
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'viewBox="0 0 {self.W} {self.H}"' + ("" if palette is None else f' width="{self.W}" height="{self.H}"') +
             f' role="img" aria-label="{esc(self.title)}" class="aodiagram" style="font-family:{font}">',
             f"<title>{esc(self.title)}</title><defs>"]
        for col in EDGE_COLORS:
            o.append(f'<marker id="ar-{col}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                     f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" style="fill:{c(col)}"/></marker>')
        used = {n["icon"] for n in self.nodes.values()}
        for k in sorted(used & set(ICONS)):
            o.append(f'<symbol id="i-{k}" viewBox="0 0 24 24"><g style="fill:none;stroke:currentColor;stroke-width:1.7;'
                     f'stroke-linecap:round;stroke-linejoin:round">{ICONS[k]}</g></symbol>')
        o.append("</defs>")
        if background:
            o.append(f'<rect width="{self.W}" height="{self.H}" style="fill:{c("paper")}"/>')
        for z in self.spec.get("zones", []):
            x, y, w, h, t, col = z["x"], z["y"], z["w"], z["h"], z["title"], z["color"]
            da = "none" if z.get("style") == "solid" else "6 5"
            o.append(f'<g class="zone" data-title="{esc(t)}" data-layer="{col}">')
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" style="fill:{mix(col, 5, "transparent")};'
                     f'stroke:{mix(col, 55, "transparent")};stroke-width:1.3;stroke-dasharray:{da}"/>')
            tw = len(t) * 6.6 + 20
            o.append(f'<rect x="{x + 12}" y="{y - 10}" width="{tw}" height="20" rx="10" style="fill:{c(col)}"/>')
            o.append(f'<text x="{x + 12 + tw / 2}" y="{y + 4}" text-anchor="middle" style="fill:{c("sheet")};font-size:11px;font-weight:600">{esc(t)}</text>')
            if z.get("sub"):
                o.append(f'<text x="{x + w - 12}" y="{y + 18}" text-anchor="end" style="fill:{c("ink-2")};font-size:10px;font-style:italic">{esc(z["sub"])}</text>')
            o.append("</g>")
        labels = []
        for i, (pts, e) in enumerate(edges):
            st, col = e.get("style", "solid"), e.get("color", "ink-2")
            d = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts)
            da = {"solid": "none", "dash": "5 4", "dot": "2 4"}[st]
            me = f' marker-end="url(#ar-{col})"' if e.get("arrow", True) else ""
            fr, to = self.node_at(pts[0]) or "", self.node_at(pts[-1]) or ""
            o.append(f'<path class="edge" data-from="{fr}" data-to="{to}" d="{d}"{me} style="fill:none;stroke:{c(col)};'
                     f'stroke-width:1.6;stroke-dasharray:{da};stroke-linejoin:round"/>')
            if e.get("label"):
                labels.append((self.label_pos(pts, e), e["label"], col, fr, to))
        for k, n in self.nodes.items():
            x, y, w, h, col = n["x"], n["y"], n["w"], n["h"], n["color"]
            o.append(f'<g class="node" data-id="{esc(k)}" data-layer="{col}" tabindex="0" role="button" aria-label="{esc(n["title"])}">')
            o.append(f'<rect class="node-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="9" style="fill:{c("sheet")};'
                     f'stroke:{mix(col, 40, "rule")};stroke-width:1.2"/>')
            o.append(f'<rect x="{x}" y="{y + 8}" width="3" height="{h - 16}" rx="1.5" style="fill:{c(col)}"/>')
            ts = 38 if h >= 50 else 32
            tx, ty = x + 10, y + (h - ts) / 2
            o.append(f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="9" style="fill:{mix(col, 14, "sheet")}"/>')
            o.append(f'<use href="#i-{n["icon"]}" xlink:href="#i-{n["icon"]}" x="{tx + 8}" y="{ty + 8}" width="{ts - 16}" height="{ts - 16}" style="color:{c(col)}"/>')
            txx = tx + ts + 10
            if n["sub"]:
                o.append(f'<text x="{txx}" y="{y + h / 2 - 3}" style="fill:{c("ink")};font-size:12.5px;font-weight:600">{esc(n["title"])}</text>')
                o.append(f'<text x="{txx}" y="{y + h / 2 + 12}" style="fill:{c("ink-2")};font-size:10.5px">{esc(n["sub"])}</text>')
            else:
                o.append(f'<text x="{txx}" y="{y + h / 2 + 4}" style="fill:{c("ink")};font-size:12.5px;font-weight:600">{esc(n["title"])}</text>')
            o.append("</g>")
        for (at, lab, col, fr, to) in labels:
            w = len(lab) * LABEL_PX + 14
            o.append(f'<g class="edge-label" data-from="{fr}" data-to="{to}">')
            o.append(f'<rect x="{at[0] - w / 2:.1f}" y="{at[1] - 9:.1f}" width="{w:.1f}" height="18" rx="9" style="fill:{c("sheet")};stroke:{mix(col, 50, "rule")};stroke-width:1"/>')
            o.append(f'<text x="{at[0]:.1f}" y="{at[1] + 3.6:.1f}" text-anchor="middle" style="fill:{c(col)};font-size:10px;font-weight:500">{esc(lab)}</text></g>')
        leg = self.spec.get("legend")
        if leg:
            lx, ly = self.spec.get("legend_at", [self.W - 40 - sum(len(i["label"]) * 6 + 70 for i in leg), self.H - 36])
            o.append(f'<g class="legend" style="font-size:11px;fill:{c("ink-2")}">')
            for item in leg:
                da = {"solid": "none", "dash": "5 4", "dot": "2 4"}[item.get("style", "solid")]
                o.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 40}" y2="{ly}" style="stroke:{c(item["color"])};stroke-width:1.6;stroke-dasharray:{da}"/>')
                o.append(f'<text x="{lx + 48}" y="{ly + 4}">{esc(item["label"])}</text>')
                lx += len(item["label"]) * 6 + 70
            o.append("</g>")
        o.append("</svg>")
        return "\n".join(o)

    def manifest(self):
        """Machine-readable view used by the explorer: nodes, layers and connections."""
        edges = [(self.edge_points(e), e) for e in self.spec.get("edges", [])]
        out = []
        for pts, e in edges:
            out.append({"from": self.node_at(pts[0]), "to": self.node_at(pts[-1]), "label": e.get("label"),
                        "style": e.get("style", "solid"), "color": e.get("color", "ink-2")})
        zone_of = {}
        for k, n in self.nodes.items():
            cx, cy = n["x"] + n["w"] / 2, n["y"] + n["h"] / 2
            best = None
            for z in self.spec.get("zones", []):
                if z["x"] <= cx <= z["x"] + z["w"] and z["y"] <= cy <= z["y"] + z["h"]:
                    if best is None or z["w"] * z["h"] < best["w"] * best["h"]:
                        best = z
            zone_of[k] = best["title"] if best else None
        return {"title": self.title,
                "nodes": [{"id": k, "title": n["title"], "sub": n["sub"], "icon": n["icon"], "layer": n["color"],
                           "layer_name": LAYERS.get(n["color"], n["color"]), "zone": zone_of[k]} for k, n in self.nodes.items()],
                "edges": out}


def _rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def tokens_css(selector=":root"):
    light = ";".join(f"--{k}:{v}" for k, v in LIGHT.items())
    dark = ";".join(f"--{k}:{v}" for k, v in DARK.items())
    return (f"{selector}{{{light}}}\n@media (prefers-color-scheme:dark){{{selector}:not([data-theme=\"light\"]){{{dark}}}}}\n"
            f"{selector}[data-theme=\"dark\"]{{{dark}}}\n")


def gallery_svg():
    names = sorted(ICONS)
    cols, cw, ch = 8, 130, 74
    rows = (len(names) + cols - 1) // cols
    W, H = cols * cw + 20, rows * ch + 20
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="font-family:{FONT}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    for i, n in enumerate(names):
        x, y = 10 + (i % cols) * cw, 10 + (i // cols) * ch
        o.append(f'<rect x="{x + 45}" y="{y + 4}" width="40" height="40" rx="9" fill="#DCE7F5"/>')
        o.append(f'<g transform="translate({x + 53},{y + 12}) scale(1)" style="fill:none;stroke:#1E5AA8;stroke-width:1.7;'
                 f'stroke-linecap:round;stroke-linejoin:round">{ICONS[n]}</g>')
        o.append(f'<text x="{x + 65}" y="{y + 62}" text-anchor="middle" font-size="11" fill="#16212B">{n}</text>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("specs", nargs="*")
    ap.add_argument("-o", "--out", default=".")
    ap.add_argument("--png", action="store_true", help="also write 2x PNG (requires cairosvg)")
    ap.add_argument("--dark", action="store_true", help="also write dark PNG")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any warning")
    ap.add_argument("--gallery")
    ap.add_argument("--tokens", action="store_true")
    ap.add_argument("--icons", action="store_true")
    a = ap.parse_args()
    if a.tokens:
        print(tokens_css()); return
    if a.icons:
        print("\n".join(sorted(ICONS))); return
    if a.gallery:
        import cairosvg
        cairosvg.svg2png(bytestring=gallery_svg().encode(), write_to=a.gallery, scale=2); print(a.gallery); return
    if not a.specs:
        ap.error("give at least one spec")
    os.makedirs(a.out, exist_ok=True)
    total = 0
    for sp in a.specs:
        spec = json.load(open(sp))
        name = os.path.splitext(os.path.basename(sp))[0]
        d = Diagram(spec)
        static = d.render(LIGHT, background=True)
        open(os.path.join(a.out, f"{name}.svg"), "w").write(static)
        open(os.path.join(a.out, f"{name}.themed.svg"), "w").write(d.render(None))
        if a.png or a.dark:
            import cairosvg
            if a.png:
                cairosvg.svg2png(bytestring=static.encode(), write_to=os.path.join(a.out, f"{name}.png"), output_width=d.W * 2)
            if a.dark:
                cairosvg.svg2png(bytestring=Diagram(spec).render(DARK, background=True).encode(),
                                 write_to=os.path.join(a.out, f"{name}.dark.png"), output_width=d.W * 2)
        ws = sorted(set(d.warnings))
        total += len(ws)
        print(f"{name}: {len(d.nodes)} nodes, {len(spec.get('edges', []))} edges, {len(ws)} warning(s)")
        for w in ws:
            print("  WARN", w)
    if a.strict and total:
        sys.exit(1)


if __name__ == "__main__":
    main()
