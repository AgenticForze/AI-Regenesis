# -*- coding: utf-8 -*-
"""
Standalone reference-blueprint table renderer, extracted from the Deep 8-Layer catalog build.
Renders the two-column-style manuscript blueprint: left = reference model (layer badge, title,
manuscript description), right = this use case's specific architecture/solution + tools, split into
two sub-columns. Ordered L8 -> L1 to match the manuscript's own presentation.
"""
from svg_engine import COLORS, esc


def blueprint_table(rows):
    """
    Two-column-style blueprint table: left side is the reference model (layer badge, title, manuscript
    description); right side is split into this use case's architecture/solution for that layer and the
    tools/technologies used. Ordered L8 -> L1 to match the manuscript's own table presentation (top of the
    stack first). This is a plain table renderer, not the node/edge Diagram engine — rows stack vertically
    with three text columns of independently-wrapped, variable-height content.
    """
    import textwrap as _tw
    COL1_W, COL2_W, COL3_W = 400, 520, 420
    PAD = 16
    LINE_H = 17
    TITLE_LINE_H = 21
    HEADER_H = 50
    CANVAS_W = COL1_W + COL2_W + COL3_W

    def wrap(text, width):
        return _tw.wrap(text, width=width, break_long_words=False)

    processed = []
    for r in rows:
        title_lines = wrap(r["title"], 22)
        desc_lines = wrap(r["desc"], 38)
        sol_lines = wrap(r["solution"], 60)
        tools_lines = wrap(r["tools"], 44)
        col1_h = len(title_lines) * TITLE_LINE_H + 6 + len(desc_lines) * LINE_H
        col2_h = len(sol_lines) * LINE_H
        col3_h = len(tools_lines) * LINE_H
        row_h = max(col1_h, col2_h, col3_h, 70) + 2 * PAD
        processed.append((r, title_lines, desc_lines, sol_lines, tools_lines, row_h))

    canvas_h = HEADER_H + sum(p[-1] for p in processed) + 2

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {canvas_h:.0f}" '
        f'font-family="\'Inter\',\'IBM Plex Sans\',-apple-system,sans-serif">',
        f'<rect width="{CANVAS_W}" height="{canvas_h:.0f}" fill="#FFFFFF"/>',
        f'<rect x="0" y="0" width="{CANVAS_W}" height="{HEADER_H}" fill="#F4F5F7"/>',
    ]
    headers = [
        ("Reference Blueprint (Manuscript Model)", COL1_W / 2),
        ("Use Case Blueprint — Architecture & Solution", COL1_W + COL2_W / 2),
        ("Tools & Technologies", COL1_W + COL2_W + COL3_W / 2),
    ]
    for label, cx in headers:
        svg.append(
            f'<text x="{cx:.1f}" y="{HEADER_H/2+5:.1f}" text-anchor="middle" font-size="13" '
            f'font-weight="700" fill="#333B4A">{esc(label)}</text>'
        )
    svg.append(f'<line x1="0" y1="{HEADER_H}" x2="{CANVAS_W}" y2="{HEADER_H}" stroke="#D8DCE2" stroke-width="1.5"/>')
    svg.append(f'<line x1="{COL1_W}" y1="0" x2="{COL1_W}" y2="{canvas_h:.0f}" stroke="#E2E5EA" stroke-width="1"/>')
    svg.append(f'<line x1="{COL1_W+COL2_W}" y1="0" x2="{COL1_W+COL2_W}" y2="{canvas_h:.0f}" stroke="#E2E5EA" stroke-width="1"/>')

    y = HEADER_H
    for i, (r, title_lines, desc_lines, sol_lines, tools_lines, row_h) in enumerate(processed):
        c = COLORS[r["color"]]
        row_bg = "#FBFBFA" if i % 2 else "#FFFFFF"
        svg.append(f'<rect x="0" y="{y:.1f}" width="{CANVAS_W}" height="{row_h:.1f}" fill="{row_bg}"/>')
        svg.append(f'<rect x="0" y="{y:.1f}" width="5" height="{row_h:.1f}" fill="{c["stroke"]}"/>')

        badge_cx, badge_cy = 38, y + 30
        svg.append(f'<circle cx="{badge_cx}" cy="{badge_cy:.1f}" r="18" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.5"/>')
        svg.append(
            f'<text x="{badge_cx}" y="{badge_cy+5:.1f}" text-anchor="middle" font-size="13.5" '
            f'font-weight="700" fill="{c["title"]}">{r["layer"]}</text>'
        )

        tx, ty = badge_cx + 30, y + 26
        for line in title_lines:
            svg.append(
                f'<text x="{tx}" y="{ty:.1f}" font-size="14.5" font-weight="700" fill="{c["title"]}">{esc(line)}</text>'
            )
            ty += TITLE_LINE_H
        dy = ty + 5
        for line in desc_lines:
            svg.append(f'<text x="20" y="{dy:.1f}" font-size="11.5" fill="#6B7280">{esc(line)}</text>')
            dy += LINE_H

        sx, sy = COL1_W + 18, y + PAD + 12
        for line in sol_lines:
            svg.append(f'<text x="{sx}" y="{sy:.1f}" font-size="12" fill="#374151">{esc(line)}</text>')
            sy += LINE_H

        tx3, ty3 = COL1_W + COL2_W + 18, y + PAD + 12
        for line in tools_lines:
            svg.append(
                f'<text x="{tx3}" y="{ty3:.1f}" font-size="11.5" font-family="\'IBM Plex Mono\',monospace" '
                f'fill="#3E6D93">{esc(line)}</text>'
            )
            ty3 += LINE_H

        y += row_h
        svg.append(f'<line x1="0" y1="{y:.1f}" x2="{CANVAS_W}" y2="{y:.1f}" stroke="#EDEEF1" stroke-width="1"/>')

    svg.append("</svg>")
    return "\n".join(svg)

