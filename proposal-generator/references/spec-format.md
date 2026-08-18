# Spec Format — Proposal Generator

## Required arguments to `render_proposal_markdown(...)` / `assemble_proposal_sections(...)`

| Argument | Required | Shape | Notes |
|---|---|---|---|
| `client_name` | yes | str | Used verbatim, multiple times, across the document — see `lessons-learned.md` #3 before embedding parenthetical annotations in it. |
| `uc` | yes | dict | Must have `title`, `problem`, `pattern` (see below). This is the same shape as a `quick-reference-engine` use-case dict — pass a real entry from a vertical pack, or a client's own described problem shaped the same way. |
| `build_order_phases` | yes | list[str], non-empty | Normally `build_order_for(uc)`'s output from the `quick-reference-engine` skill. Raises `ProposalInputError` if empty — this engine won't render a proposal with no build order. |
| `tier_key` | yes | one of `"audit"`, `"workshop"`, `"advisory"`, `"certification"` | See `SERVICE_TIERS` in `proposal_engine.py` for the exact name/description rendered for each. Raises `ProposalInputError` naming the valid options if you pass anything else. |
| `price` | yes | str | **Never defaulted or invented** — pass a real figure or range for this specific engagement (e.g. `"$8,500 flat fee"`, `"$15k-25k depending on scope"`). Raises `ProposalInputError` if omitted. |
| `timeframe` | yes | str | Same rule as `price` — e.g. `"2 weeks from kickoff"`. |
| `deep8_entry` | no | anything truthy, or `None` | Only its presence/absence is checked — pass the actual entry from a `*_deep8_data.py` pack if you have one, or any truthy placeholder if you're just testing the "with Deep 8-Layer" branch. Passing `None` (the default) omits the Deep 8-Layer paragraph and image entirely. |
| `consultant_name` | no | str | Shown in the document's byline if given. |
| `prepared_date` | no | str | Shown in the document's byline if given. |

## `uc` dict's required fields

Only three fields are read by this engine — you don't need the full quick-reference-engine spec shape,
just:

```python
uc = {
    "title": "...",     # used as the document title and in the executive summary (bolded, not lowercased —
                          # see lessons-learned.md #1 for why that matters)
    "problem": "...",   # used verbatim as "The Problem" section's body
    "pattern": "...",   # one of the 8 quick-reference-engine pattern keys — used in "We'd approach this as
                          # a/an {pattern} pattern"
}
```

If you're pulling a real use case from one of the vertical packs (`telecom_data.py` etc.), its dict already
has all three fields plus more that this engine ignores — no need to strip anything out first.

## Diagram file convention

`render_proposal_markdown` embeds `![Architecture diagram](diagram.svg)` and, when `deep8_entry` is given,
`![Deep 8-Layer diagram](deep8_diagram.svg)` — by filename convention, not by taking file paths as
arguments. Before handing the markdown to the `docx` skill (or presenting it as-is), write the real SVGs to
those two filenames alongside the `.md` file:

```python
from svg_patterns import BUILDERS   # quick-reference-engine skill
svg = BUILDERS[uc["pattern"]](...)
open("diagram.svg", "w").write(svg)

from deep8_engine import build_deep8_diagram   # deep8-architecture-engine skill, only if using deep8_entry
open("deep8_diagram.svg", "w").write(build_deep8_diagram(deep8_entry["spec"]))
```

The worked example (`scripts/example_proposal.py`) writes placeholder SVGs at those same two filenames so
the example is fully standalone — swap them for real engine output in actual use.

## Handing off to the `docx` skill

This engine produces markdown content, not a `.docx` file. To turn it into an actual Word document:

1. Generate the markdown with `render_proposal_markdown(...)` and write the two diagram SVGs per the
   convention above.
2. Convert the SVGs to PNG (Word doesn't embed SVG reliably) — `cairosvg.svg2png(...)`, same tool used to
   validate diagrams in the other two engine skills.
3. Hand the markdown text + PNG paths to the `docx` skill's document-creation process (see that skill's
   `SKILL.md` for its own gotchas — table widths, heading levels for a working table of contents, etc.).

This skill deliberately doesn't reimplement `docx` generation itself — that skill already exists and is
good at it; this one's job is producing accurate, well-sequenced proposal *content*.
