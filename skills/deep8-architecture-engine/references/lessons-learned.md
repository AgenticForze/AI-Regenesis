# Lessons Learned

Every item here is a real bug that was hit and fixed while building and validating this engine across 22
use cases, not a hypothetical. Read this before extending `deep8_engine.py` or `svg_engine.py` — several of
these will reappear if the underlying design decision gets undone.

## 1. Double-escaped ampersands

**Symptom:** node titles rendered as literal `Billing &amp; Usage (CDR) DB` instead of `Billing & Usage
(CDR) DB`.

**Cause:** a hardcoded label constant was written with `&amp;` already in the Python string, and then the
renderer's own `esc()` function escaped the `&` a second time.

**Fix:** always write plain `&` in spec strings. `esc()` (in `svg_engine.py`) handles escaping exactly once,
at render time. Never pre-escape anything going into a spec.

## 2. A duplicate edge garbling two labels together

**Symptom:** two condition labels on adjacent edges rendered as overlapping, unreadable text (looked like
`...out ...rain` — two labels' characters interleaved).

**Cause:** the same edge (`gate → hold`) was added twice — once in a "conditional branches" block, once again
in a later "L5 → L6 telemetry" block that wasn't checked against edges already added.

**Fix:** `deep8_engine.py`'s edge-generation logic is centralized and each edge type is added exactly once,
in one place. If you're hand-adding edges outside the generic engine, grep for the same `(from_id, to_id)`
pair before adding a new one.

## 3. Condition labels overlapping when gate-branch targets are adjacent

**Symptom:** `"medium confidence"` and `"high confidence"` labels rendered on top of each other when their
target nodes (`human` and `auto`) were in neighboring columns.

**Cause:** a label's position is the midpoint between the gate node (fixed, centered) and its target. If two
targets are close together in the row, their midpoints are close together too, regardless of how short the
label text is.

**Fix:** spread the three `gate_branch` targets across the `l5` row — `human` at one end, `hold` at the other,
everything else in between. See `references/spec-format.md`'s "The gate and its branches" section for the
exact ordering convention. This is a *layout* fix, not a text-shortening fix — shortening the labels alone
was tried first and still collided.

## 4. A same-row edge rendering its label — and itself — invisibly behind a card

**Symptom:** an "approved" label between `human` and an `auto`-branch action item vanished entirely, and a
small stray double-arrow artifact appeared in an unrelated gap between two other cards.

**Cause:** the edge's two endpoints weren't in adjacent columns — there was a card *between* them. The
same-row connector draws a straight line between the two endpoints' edges, which passes directly through
(behind) the intervening card. The line segment inside that card's bounding box is invisible (occluded); the
label, positioned at the path's midpoint, landed exactly inside that occluded region too.

**Fix:** don't add same-row edges between non-adjacent columns. If the relationship is worth showing, route it
through an adjacent-row connection instead, or drop the edge if it's not essential to the diagram's story (this
specific edge — "human approval leads to execution" — was dropped entirely in favor of a cleaner
`human → observability` edge, since the *human's* action already implies downstream execution and didn't need
its own explicit arrow).

## 5. Long-distance edges with labels landing inside unrelated rows

**Symptom:** the L8-closes-the-loop-back-into-memory edges (spanning 6+ rows) had labels that rendered
partially hidden behind cards in the middle rows, showing fragments like `mem` and `emc`.

**Cause:** a label's position is always the midpoint of the full path, regardless of how many rows the path
crosses. A 6-row jump's midpoint lands in row 3, not near either endpoint.

**Fix:** don't label edges that span more than 2-3 rows. Unlabeled dashed lines spanning many rows render fine
— they're mostly occluded by cards along the path and read as a faint background connection, which is exactly
right for a "closes the loop, eventually" relationship. This is why `generic_build_order`'s L8→memory edges are
always unlabeled in the shipped engine.

## 6. A redundant edge pair that looked like a messy "bus line"

**Symptom:** a blackboard-pattern diagram had both `controller → agent` (dashed trigger) and
`agent → store` (bidirectional read/write) edges for every agent, creating a dense tangle of overlapping
dashed lines across the whole agent row.

**Cause:** both edges were genuinely accurate to the blackboard pattern's semantics, but drawing both for every
agent added visual noise without adding information a reader would actually use — the controller-mediated
relationship already implies the store read/write.

**Fix:** for patterns with genuinely redundant relationships, pick the single edge that tells the story best
and drop the other, even if the dropped one is technically also true. Readability beat exhaustiveness here.

## 7. A hardcoded domain string

**Symptom:** every generated markdown doc showed `**Domain:** Telecommunications`, including doc for BSS/OSS
and (eventually) Finance use cases.

**Cause:** the markdown-rendering function was originally written for two Telecom pilots only, and the domain
name was typed as a literal string instead of a parameter.

**Fix:** always derive domain (and anything else that varies per use case) from the actual data being
processed, never from a value that happened to be correct for the first N examples. This is a general lesson
beyond this specific skill: when a function is first built against a narrow set of examples, audit every
literal string in it before reusing the function at scale.

## 8. A "Purpose" column that just repeated the layer tag

**Symptom:** the agent stack table's Purpose column showed values like `"L2 · The Brain"` — technically not
wrong, but not a purpose description either, just the subtitle field repeated verbatim.

**Cause:** the fallback for a missing explicit `purpose` field defaulted to the item's `sub` field, which is a
short category tag, not a sentence.

**Fix:** `deep8_engine.py`'s `_default_purpose()` generates a real (if generic) templated sentence per layer
when `purpose` isn't explicitly set (e.g. `"Provides {title}'s reasoning/knowledge capability to the Agentic
Core."`), instead of falling back to a non-sentence field. Still worth overriding with genuinely bespoke text
for the items that matter most — see `references/spec-format.md`'s note on this.

## General pattern across all of these

Every one of these was caught by **actually rendering the SVG and looking at it** (or reading the generated
markdown output), not by reading the Python code. The code executed without exceptions in every single case —
none of these were crashes. Always render to PNG (`cairosvg`) and visually inspect, or at minimum read the
generated markdown text end-to-end, before considering a batch of generated content done. This is the single
highest-leverage habit for using this engine reliably.
