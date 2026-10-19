# Diagram spec format

A spec is one JSON object.

## Top level

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `title` | string | yes | Accessible name; becomes the SVG `<title>` and `aria-label` |
| `width`, `height` | number | yes | Canvas size in px (the PNG is rendered at 2×) |
| `zones` | array | no | Background regions with a pill title |
| `nodes` | array | yes | Components |
| `edges` | array | no | Connections |
| `legend` | array | no | Line-style key drawn bottom right |
| `legend_at` | [x, y] | no | Left end of the first legend line |

## Zone

| Key | Default | Meaning |
| --- | --- | --- |
| `x`, `y`, `w`, `h` | — | Rectangle; zones may nest (draw the outer zone first) |
| `title` | — | Text in the pill on the top border |
| `color` | — | Layer token |
| `sub` | none | Italic note in the top-right corner, e.g. "VPC-SC perimeter" |
| `style` | `dash` | `dash` for logical boundaries, `solid` for physical ones such as a region |

## Node

| Key | Default | Meaning |
| --- | --- | --- |
| `id` | — | Unique, kebab-case; used by edges and by the explorer |
| `x`, `y` | — | Top-left corner |
| `w`, `h` | 200, 56 | Size |
| `title` | — | Bold first line |
| `sub` | none | Second line (service name or detail) |
| `icon` | — | Name from `scripts/icons.py` |
| `color` | — | Layer token |

## Edge

Either **anchored**:

| Key | Meaning |
| --- | --- |
| `from`, `to` | `nodeid.side[±offset]` or `[x, y]` |
| `route` | `auto` (default), `hv`, `vh`, `straight` |
| `mid` | x of the vertical run for `hv`; y of the horizontal run for `vh` |
| `via` | list of waypoints (anchors or `[x, y]`) instead of a route |

or **explicit**:

| Key | Meaning |
| --- | --- |
| `points` | list of anchors or `[x, y]`, drawn as straight segments |

Common keys:

| Key | Default | Values |
| --- | --- | --- |
| `style` | `solid` | `solid`, `dash`, `dot` |
| `color` | `ink-2` | `ink-2`, `auto`, `gate`, `risk`, `signal` |
| `arrow` | true | false for joining trunk segments |
| `label` | none | Short text in a pill |
| `at` | longest segment midpoint | `[x, y]` for the label centre |

## Legend item

`{"label": "deny path", "color": "risk", "style": "dash"}`

## Colour tokens

| Token | Light | Dark | Meaning |
| --- | --- | --- | --- |
| `l0` | #5B6B7A | #8FA0AF | Channels, external systems |
| `l1` | #7A4FA3 | #B18BD6 | Edge, identity, content safety |
| `l2` | #1E5AA8 | #7FB0F0 | Orchestration |
| `l3` | #0E7C86 | #5CC3CC | Gateway, network transit |
| `l4` | #2E7D5B | #6CC49A | Model serving |
| `l5` | #8A6D1D | #D2B35A | Knowledge and memory |
| `l6` | #B5541B | #E6905A | Tools and actions |
| `l7` | #4E6A2B | #9CC26A | Data and events |
| `l8` | #A3325A | #E47FA3 | Observability |
| `l9` | #34404C | #9AA8B5 | Security and governance |
| `l10` | #3E5C8A | #8DA9D6 | Platform and MLOps |
| `risk` | #AE2E24 | #F08A80 | Restricted zone, deny, security response |
| `gate` | #B57612 | #E3AE4F | Human approval, backup path |
| `auto` | #2E7D5B | #6CC49A | Pass, verified |
| `signal` | #1E5AA8 | #7FB0F0 | Accent |

## Warnings the renderer checks

- title or subtitle likely to overflow the node
- unknown icon or colour
- overlapping nodes, nodes outside the canvas
- zone title wider than the zone
- an edge segment passing through a node that is not one of its endpoints
- an edge label sitting on a node
