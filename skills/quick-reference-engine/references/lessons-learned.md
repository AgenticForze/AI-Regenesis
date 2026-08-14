# Lessons Learned

Every item here was found by actually rendering the worked example's diagrams and looking at the output
(`cairosvg` → PNG, visually inspected), not by reading the Python source. All 8 patterns will eventually hit
these if you feed them the wrong shape of input — read this before batch-generating a large set of use cases.

## 1. Fan-out edges pass behind agent cards and create a misleading "which agent owns which action" impression

**Symptom:** in a `blackboard`, `market-based`, or `event-swarm` diagram where the number of actions is
smaller than the number of agents/bidders, some agents visually appear to connect straight down to a
specific action — while others (usually the first and last in the row) appear to dead-end with no downstream
connection at all.

**Cause:** in all three of these patterns, the actions are wired from the controller/auctioneer/bus node
(two rows above), not from individual agents — e.g. `blackboard()`'s edges are `ctrl → agent` (dashed,
"triggers") and, separately, `ctrl → action` (solid), never `agent → action`. When there are fewer actions
than agents, the `ctrl → action` edge's path happens to run vertically through the x-coordinate of whichever
agent card sits at that column position before elbowing over to the action. The line is drawn *behind* that
card (same z-order issue as the deep8 engine's known same-row occlusion bug, but here it's a different-row
pass-through, not a same-row one). Visually confirmed in the SVG path data: a `ctrl → action` edge's vertical
segment (`M 447.0 334.0 L 447.0 452.5 ...`) runs directly through the Transaction Graph Agent card's bounding
box (`x: 322–572, y: 412–517`) in the blackboard worked example, even though that agent has no real
relationship to that specific action in the underlying pattern semantics.

**Fix:** this is a genuine visual-semantics gap in the current renderer, not just a cosmetic nit — a reader
will reasonably infer an agent→action relationship that isn't actually there. Two options until the engine
itself is patched:
- **Prefer `len(actions) == len(agents)`** (or close to it) for these three patterns wherever the real use
  case supports it, so every agent aligns with something below it and the pass-through coincidence doesn't
  read as meaningful.
- **When action count must differ**, say so explicitly in the accompanying markdown text ("all agents feed
  the [controller/bus/auctioneer], which decides the final action(s)") rather than relying on the diagram
  alone to convey that all-agents-to-controller relationship.

## 2. The `title` parameter is accepted by all 8 pattern functions and displayed by none of them

**Symptom:** the diagram renders with no heading at all — just starts directly with the top row of nodes,
even though every function signature takes `title` as its first argument.

**Cause:** `title` is passed into all 8 functions (both Mermaid and SVG versions) but never referenced inside
any function body — confirmed by grep across `svg_patterns.py` and by inspecting the rendered Mermaid text
source, which starts with `flowchart TB` and has no title node. This mirrors the deep8 engine's convention
(diagrams are visual-only; the title belongs in the surrounding document), but it's easy to assume otherwise
here because the parameter exists and looks load-bearing.

**Fix:** always write the use case's title as a markdown heading in the doc that embeds the diagram — don't
expect the `title` argument to produce one. Pass `uc["title"]` for it anyway (costs nothing, keeps the call
site consistent with the build-order call), but don't rely on it.

## 3. Ampersand escaping is correct in this engine — verified, not assumed

**Checked because the deep8 engine had a double-escaping bug** (see that skill's `lessons-learned.md` #1).
Tested directly: a node label with a literal `Risk & Compliance Agent` renders as `Risk &amp; Compliance
Agent` in the raw SVG (single escape, correct) — not `&amp;amp;` (double-escaped) and not a bare unescaped
`&` (which would produce invalid XML). `svg_engine.py`'s `esc()` is shared between this engine and the deep8
engine, so this isn't a coincidence — it's the same fix, already in place. Still worth the 30-second
re-check any time you touch `svg_engine.py`, since a regression here breaks every pattern at once, not just
one.

## General pattern across all of these

Two of these three findings (#1 and #2) would not have been caught by running the code without error —
`blackboard()`, `market_based()`, and `event_swarm()` all execute cleanly and produce valid SVG regardless of
the action/agent count mismatch. **Always render to PNG and visually inspect at least one example of every
pattern you're about to use at scale**, the same discipline the deep8 engine's own lessons file recommends —
this file is proof that following it here caught two real issues in under twenty minutes of testing.
