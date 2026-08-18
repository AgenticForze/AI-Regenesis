# Lessons Learned

## 1. The findings section and the recommendation section said the exact same thing, word for word

**Symptom:** the first working version of this engine rendered the "Findings" section and the "If we
rebuilt this" section as identical bullet lists — same question text, same "— currently no" phrasing, same
detail text, twice in one document. Caught by reading the actual generated `example_retrospective.md` end
to end, not by running the code (it executed fine and produced valid markdown both times).

**Cause:** `_bullet_for_finding()` was the only bullet-rendering function, and both sections called it. It
restates the interview question and the answer — factually correct, but not the same thing as a
recommendation, and rendering it twice added length without adding information.

**Fix:** split into two functions. `_bullet_for_finding()` (descriptive — what was asked, what was
answered, findings section only) and `_recommendation_for_finding()` (prescriptive — what to actually do
about it, backed by a hand-written `RECOMMENDATION_TEMPLATES` entry per question id, retrospective section
only). This also fixed a voice problem: the catalog's own retrospective bullets ("Add a
confidence-calibration step...") are action-oriented, and a restated interview question never reads that
way no matter how it's punctuated.

**If you extend the question bank:** add a matching `RECOMMENDATION_TEMPLATES` entry for every new question
id — the lookup is a plain dict access with no fallback, so a missing template raises `KeyError` at render
time (verified directly: adding a question without a template and rendering raises `KeyError` naming the
missing id) rather than silently falling back to generic text. This is deliberate — a silent fallback would
let a low-effort question slip through undetected.

## 2. "Unknown" needs to be its own severity path, not folded into "no"

**Symptom, caught during design, not after a bug:** an early version of the severity logic mapped `"unknown"`
to the same rank as `"partial"` uniformly across all layers, meaning "we didn't ask" and "we asked and it's
half-there" looked identical in the output.

**Why that's wrong specifically for L4/L5/L6:** not knowing whether your gate threshold is documented, or
whether writes are audit-logged, or whether guardrail violations are alerted, is a worse epistemic position
for a governance audit than knowing it's partially there — an "unknown" here usually means the interviewee
couldn't point to evidence, which is itself the finding. `build_findings()` explicitly upgrades `"unknown"`
answers on `l4`/`l5`/`l6` to `"high"` severity, matching `"no"`, rather than leaving it at the generic
`"partial"`-equivalent rank. Confirmed this fires correctly with a direct test (an `"unknown"` answer on
`l6_traced` produces a high-severity finding, not medium).

## 3. Don't let the interview format substitute for interviewee honesty — this is a process risk, not a code bug

The engine can only be as accurate as the answers it's given. A rushed or defensive interviewee answering
"yes" to avoid a longer conversation produces a clean-looking report that isn't a true audit. There's no code
fix for this — it's a process note: **run the interview with someone who didn't build the system, or who has
no stake in the outcome looking good**, and treat an all-"yes" result (see the "no findings" path in
`render_retrospective_markdown`, which explicitly flags this) with a second, more skeptical pass rather than
taking it at face value. This mirrors a real failure mode of any self-reported audit, not something specific
to this tool.

## General pattern across all of these

Two of these three items (#1, and the design decision behind #2) were only visible by reading the actual
rendered document end to end — #1 in particular executed without any exception on both runs and still
produced a materially worse deliverable. Read the generated markdown yourself before treating an audit as
done, the same discipline the other two engines' lessons files recommend for their SVG output.
