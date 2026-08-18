# -*- coding: utf-8 -*-
"""
Clean, light, card-based SVG diagram renderer — replaces the dense dark Mermaid diagrams with the
"rounded card, title + subtitle, soft elbow connector" style. Same underlying layer semantics as before
(Data & Integration -> Orchestration -> Agent -> Action & Execution, plus cross-cutting Observability &
Governance), but laid out as simple top-to-bottom rows of cards, matching the reference style exactly:
white background, pastel rounded rectangles, bold title + muted subtitle, thin gray rounded elbow arrows.
"""
import textwrap

BOX_W = 250
BOX_H = 92
ROW_GAP = 78
COL_GAP = 26
MARGIN = 46
TITLE_SIZE = 15.5
SUB_SIZE = 12.5
TITLE_LINE_H = 20
SUB_LINE_H = 17
CORNER_R = 16
ARROW_COLOR = "#9AA3AE"
ARROW_COL_W = 34
ROWLABEL_BADGE_W = 42
ROWLABEL_BOX_X = ARROW_COL_W + 6
ROWLABEL_BOX_W = 196
SPINE_X = ROWLABEL_BOX_X + ROWLABEL_BADGE_W + ROWLABEL_BOX_W + 22
GUTTER_W = SPINE_X + 40
SPINE_COLOR = "#D64545"
ROWLABEL_BORDER = "#1A1A1A"

COLORS = {
    "data":       {"fill": "#F2EEE3", "stroke": "#C7BC9E", "title": "#4A4432", "sub": "#8C8365"},
    "orch":       {"fill": "#DCEBFB", "stroke": "#5B93C9", "title": "#1C4A73", "sub": "#3E6D93"},
    "agent":      {"fill": "#DBF2E7", "stroke": "#4FAE83", "title": "#1B5E3D", "sub": "#3D8261"},
    "action":     {"fill": "#FBE8CE", "stroke": "#D89A3F", "title": "#7A4E12", "sub": "#9C6B22"},
    "obs":        {"fill": "#EAE1F8", "stroke": "#9575CD", "title": "#4A2E7A", "sub": "#6B4A9E"},
    "channel":    {"fill": "#EDEFF3", "stroke": "#AEB4C0", "title": "#333B4A", "sub": "#7B828F"},
    "leadership": {"fill": "#FBE1E6", "stroke": "#D9748C", "title": "#7A2B3F", "sub": "#9C4F60"},
    "memory":     {"fill": "#E4F0F6", "stroke": "#5FA3C0", "title": "#1D4E5F", "sub": "#3E7B93"},
}
LABEL_BG = "#FFFFFF"
LABEL_BORDER = "#D8DCE2"
LABEL_TEXT = "#51586A"

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def _wrap(text, width, max_lines):
    lines = textwrap.wrap(text, width=width, break_long_words=False)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        if len(last) > width - 1:
            last = last[: width - 1]
        lines[-1] = last.rstrip() + "…"
    return lines


class Node:
    def __init__(self, id_, title, subtitle, color_key, external=False):
        self.id = id_
        self.title_lines = _wrap(title, 24, 3)
        self.sub_lines = _wrap(subtitle, 30, 2)
        self.color_key = color_key
        self.external = external  # True -> dashed card border (external/third-party system)
        self.cx = 0
        self.cy = 0


class Diagram:
    def __init__(self):
        self.rows = []       # list[list[Node]]
        self.row_labels = [] # list[str|None], parallel to self.rows
        self.edges = []      # list[(from_id, to_id, dashed:bool, bidirectional:bool)]
        self._nodes = {}

    def add_row(self, nodes, label=None):
        for n in nodes:
            self._nodes[n.id] = n
        self.rows.append(nodes)
        self.row_labels.append(label)
        return nodes

    def edge(self, a, b, dashed=False, bidir=False, label=None):
        self.edges.append((a, b, dashed, bidir, label))

    def node(self, id_, title, subtitle, color_key, external=False):
        n = Node(id_, title, subtitle, color_key, external)
        self._nodes[id_] = n
        return n

    def render(self):
        max_block_h = 0
        for row in self.rows:
            for n in row:
                block_h = len(n.title_lines) * TITLE_LINE_H + len(n.sub_lines) * SUB_LINE_H
                max_block_h = max(max_block_h, block_h)
        box_h = max_block_h + 48

        row_widths = [len(row) * BOX_W + max(0, len(row) - 1) * COL_GAP for row in self.rows]
        content_w = max(row_widths, default=BOX_W) + 2 * MARGIN
        has_labels = any(self.row_labels)
        gutter = GUTTER_W if has_labels else 0
        canvas_w = content_w + gutter
        canvas_h = MARGIN + len(self.rows) * box_h + max(0, len(self.rows) - 1) * ROW_GAP + MARGIN

        for ri, row in enumerate(self.rows):
            row_w = row_widths[ri]
            start_x = gutter + (content_w - row_w) / 2
            cy = MARGIN + ri * (box_h + ROW_GAP) + box_h / 2
            for ci, n in enumerate(row):
                cx = start_x + ci * (BOX_W + COL_GAP) + BOX_W / 2
                n.cx, n.cy = cx, cy

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w:.0f} {canvas_h:.0f}" '
            f'font-family="\'Inter\',\'IBM Plex Sans\',-apple-system,sans-serif">',
            '<defs>',
            '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
            f'<path d="M0,0 L10,5 L0,10 z" fill="{ARROW_COLOR}"/>',
            '</marker>',
            '<filter id="cardshadow" x="-20%" y="-20%" width="140%" height="140%">',
            '<feDropShadow dx="0" dy="1.5" stdDeviation="2.5" flood-color="#1a1a1a" flood-opacity="0.08"/>',
            '</filter>',
            '</defs>',
            f'<rect x="0" y="0" width="{canvas_w:.0f}" height="{canvas_h:.0f}" fill="#FFFFFF"/>',
        ]

        # edges first (under the cards)
        for a, b, dashed, bidir, label in self.edges:
            na, nb = self._nodes[a], self._nodes[b]
            svg.append(self._edge_path(na, nb, box_h, dashed, bidir, label))

        # left-margin layer labels + spine (only drawn if at least one row has a label)
        if has_labels:
            spine_top = MARGIN
            spine_bottom = canvas_h - MARGIN
            svg.append(f'<line x1="{SPINE_X}" y1="{spine_top:.1f}" x2="{SPINE_X}" y2="{spine_bottom:.1f}" '
                       f'stroke="{SPINE_COLOR}" stroke-width="2.5"/>')

            # vertical double-headed arrow + rotated axis label, spanning the full label stack
            ax = ARROW_COL_W / 2 + 2
            ay1, ay2 = spine_top + 6, spine_bottom - 6
            svg.append(f'<line x1="{ax:.1f}" y1="{ay1:.1f}" x2="{ax:.1f}" y2="{ay2:.1f}" '
                       f'stroke="#1A1A1A" stroke-width="1.5"/>')
            svg.append(f'<polygon points="{ax-5:.1f},{ay1+9:.1f} {ax+5:.1f},{ay1+9:.1f} {ax:.1f},{ay1:.1f}" fill="#1A1A1A"/>')
            svg.append(f'<polygon points="{ax-5:.1f},{ay2-9:.1f} {ax+5:.1f},{ay2-9:.1f} {ax:.1f},{ay2:.1f}" fill="#1A1A1A"/>')
            amid = (ay1 + ay2) / 2
            svg.append(
                f'<text x="{ax:.1f}" y="{amid:.1f}" text-anchor="middle" font-size="11" font-weight="700" '
                f'fill="#1A1A1A" letter-spacing="0.5" transform="rotate(-90 {ax:.1f} {amid:.1f})">'
                f'SYSTEM ORCHESTRATION &amp; KNOWLEDGE FLOW</text>'
            )

            for ri, row in enumerate(self.rows):
                label = self.row_labels[ri]
                if not label:
                    continue
                badge, title, desc = label if isinstance(label, tuple) else (None, label, None)
                row_cy = row[0].cy
                title_lines = _wrap(title, 26, 3)
                desc_lines = _wrap(desc, 30, 2) if desc else []
                content_h = len(title_lines) * 15 + (len(desc_lines) * 12 + 4 if desc_lines else 0)
                lbl_h = max(50, content_h + 22)
                lbl_y = row_cy - lbl_h / 2

                # badge box (L#)
                if badge:
                    svg.append(
                        f'<rect x="{ROWLABEL_BOX_X}" y="{lbl_y:.1f}" width="{ROWLABEL_BADGE_W}" height="{lbl_h}" '
                        f'fill="#FFFFFF" stroke="{ROWLABEL_BORDER}" stroke-width="2"/>'
                    )
                    svg.append(
                        f'<text x="{ROWLABEL_BOX_X + ROWLABEL_BADGE_W/2:.1f}" y="{row_cy+6:.1f}" text-anchor="middle" '
                        f'font-size="17" font-weight="700" fill="#1A1A1A">{esc(badge)}</text>'
                    )
                title_box_x = ROWLABEL_BOX_X + (ROWLABEL_BADGE_W if badge else 0)
                svg.append(
                    f'<rect x="{title_box_x}" y="{lbl_y:.1f}" width="{ROWLABEL_BOX_W}" height="{lbl_h}" '
                    f'fill="#FFFFFF" stroke="{ROWLABEL_BORDER}" stroke-width="2"/>'
                )
                ty = lbl_y + 10 + 10
                for line in title_lines:
                    svg.append(
                        f'<text x="{title_box_x + ROWLABEL_BOX_W/2:.1f}" y="{ty:.1f}" text-anchor="middle" '
                        f'font-size="11.5" font-weight="700" fill="#1A1A1A">{esc(line)}</text>'
                    )
                    ty += 15
                if desc_lines:
                    ty += 3
                    for di, line in enumerate(desc_lines):
                        text = line
                        if di == 0:
                            text = "(" + text
                        if di == len(desc_lines) - 1:
                            text = text + ")"
                        svg.append(
                            f'<text x="{title_box_x + ROWLABEL_BOX_W/2:.1f}" y="{ty:.1f}" text-anchor="middle" '
                            f'font-size="10" fill="#5A6270">{esc(text)}</text>'
                        )
                        ty += 12

                # connector from label box to spine
                svg.append(
                    f'<line x1="{title_box_x + ROWLABEL_BOX_W}" y1="{row_cy:.1f}" x2="{SPINE_X}" y2="{row_cy:.1f}" '
                    f'stroke="{SPINE_COLOR}" stroke-width="1.5" stroke-dasharray="3 3"/>'
                )
                svg.append(f'<circle cx="{SPINE_X}" cy="{row_cy:.1f}" r="4" fill="{SPINE_COLOR}"/>')

        # cards
        for row in self.rows:
            for n in row:
                svg.append(self._card(n, box_h))

        svg.append("</svg>")
        return "\n".join(svg)

    def _edge_path(self, na, nb, box_h, dashed, bidir, label=None):
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        marker_start = ' marker-start="url(#arrow)"' if bidir else ""
        if abs(na.cy - nb.cy) < 1:
            # same row: connect side-to-side instead of bottom-to-top
            if na.cx < nb.cx:
                x1, y1 = na.cx + BOX_W / 2, na.cy
                x2, y2 = nb.cx - BOX_W / 2, nb.cy
            else:
                x1, y1 = na.cx - BOX_W / 2, na.cy
                x2, y2 = nb.cx + BOX_W / 2, nb.cy
            d = f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}"
            label_x, label_y = (x1 + x2) / 2, y1 - 8
        else:
            x1, y1 = na.cx, na.cy + box_h / 2
            x2, y2 = nb.cx, nb.cy - box_h / 2
            if abs(x1 - x2) < 1:
                d = f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}"
                label_x, label_y = x1, (y1 + y2) / 2
            else:
                r = 12
                mid_y = (y1 + y2) / 2
                sign = 1 if x2 > x1 else -1
                d = (
                    f"M {x1:.1f} {y1:.1f} "
                    f"L {x1:.1f} {mid_y - r:.1f} "
                    f"Q {x1:.1f} {mid_y:.1f} {x1 + r * sign:.1f} {mid_y:.1f} "
                    f"L {x2 - r * sign:.1f} {mid_y:.1f} "
                    f"Q {x2:.1f} {mid_y:.1f} {x2:.1f} {mid_y + r:.1f} "
                    f"L {x2:.1f} {y2:.1f}"
                )
                label_x, label_y = (x1 + x2) / 2, mid_y
        path = (
            f'<path d="{d}" fill="none" stroke="{ARROW_COLOR}" stroke-width="1.75"{dash} '
            f'marker-end="url(#arrow)"{marker_start}/>'
        )
        if not label:
            return path
        lw = max(46, len(label) * 6.4 + 16)
        label_svg = (
            f'<g>'
            f'<rect x="{label_x - lw/2:.1f}" y="{label_y - 11:.1f}" width="{lw:.1f}" height="20" rx="9" '
            f'fill="{LABEL_BG}" stroke="{LABEL_BORDER}" stroke-width="1"/>'
            f'<text x="{label_x:.1f}" y="{label_y + 4:.1f}" text-anchor="middle" font-size="10.5" '
            f'font-weight="600" fill="{LABEL_TEXT}">{esc(label)}</text>'
            f'</g>'
        )
        return path + "\n" + label_svg

    def _card(self, n, box_h):
        c = COLORS[n.color_key]
        x = n.cx - BOX_W / 2
        y = n.cy - box_h / 2
        border_dash = ' stroke-dasharray="6 4"' if n.external else ""
        parts = [
            f'<g filter="url(#cardshadow)">',
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{BOX_W}" height="{box_h:.0f}" rx="{CORNER_R}" '
            f'fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.5"{border_dash}/>',
            "</g>",
        ]
        n_title_lines = len(n.title_lines)
        n_sub_lines = len(n.sub_lines)
        block_h = n_title_lines * TITLE_LINE_H + n_sub_lines * SUB_LINE_H
        top = n.cy - block_h / 2
        ty = top + TITLE_LINE_H * 0.78
        for line in n.title_lines:
            parts.append(
                f'<text x="{n.cx:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="{TITLE_SIZE}" '
                f'font-weight="600" fill="{c["title"]}">{esc(line)}</text>'
            )
            ty += TITLE_LINE_H
        sy = top + n_title_lines * TITLE_LINE_H + SUB_LINE_H * 0.72
        for line in n.sub_lines:
            parts.append(
                f'<text x="{n.cx:.1f}" y="{sy:.1f}" text-anchor="middle" font-size="{SUB_SIZE}" '
                f'fill="{c["sub"]}">{esc(line)}</text>'
            )
            sy += SUB_LINE_H
        return "\n".join(parts)
