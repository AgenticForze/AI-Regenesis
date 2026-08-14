# Lessons Learned

All four items below were found by reading the actual generated `example_proposal.md`, not by reading the
Python source — the code executed cleanly and produced valid markdown on every run, including the broken
versions. This is the same pattern the other two new skills' lessons files describe: valid output and
correct output are not the same thing, and only reading the rendered document catches the gap.

## 1. Lowercasing a use-case title with an acronym in it produces broken-looking English

**Symptom:** the executive summary's first version built its sentence as `f"...approach to
{uc['title'].lower()}."`. For the worked example's title, "Multi-Agent Network Fault RCA & Auto-Remediation",
this rendered as "an AI/agentic approach to multi-agent network fault rca & auto-remediation" — the acronym
RCA reads as a typo once lowercased mid-sentence, in a document meant to go in front of a paying client.

**Fix:** stopped lowercasing the title at all. The sentence now bolds the title as its own clause ("the
following problem: **{title}**") instead of splicing a case-transformed version of it into running prose.
This is a generally safer pattern for any user-supplied title field: don't transform the case of text you
don't control the contents of, restructure the sentence around it instead.

## 2. A section heading and its own body text said the same thing twice, adjacent to each other

**Symptom:** the "Suggested Build Order" section rendered its `##` heading immediately followed by a bolded
`**Suggested build order:**` line, then the numbered phases — the same three words, twice, one line apart.

**Fix:** removed the bolded restatement; the heading already establishes what the list below it is. Same
family of issue as the `retrospective-generator` skill's findings/recommendations duplication (see that
skill's `lessons-learned.md` #1) — different cause here (a leftover label instead of a copy-paste), same
fix philosophy: read the rendered output and cut anything that's saying something the reader was just told.

## 3. Embedding a "(fictional example client)" annotation inside `client_name` repeated it awkwardly

**Symptom:** the worked example's first version set `client_name="Northwind Fiber (fictional example
client)"`. Because `client_name` is echoed verbatim several times across the document (title, executive
summary, twice more in the engagement section), the parenthetical repeated every time — "Northwind Fiber
(fictional example client) is evaluating...get Northwind Fiber (fictional example client) from this
reference design..." reads as noisy and unprofessional, which matters for a document whose whole point is to
look client-ready.

**Fix:** moved the "this is fictional" disclosure to a code comment in the example script instead of into
the data itself. General takeaway for real use: any field that gets echoed multiple times in the rendered
output (`client_name`, `consultant_name`) should carry the client-facing text and nothing else — put caveats,
internal notes, or disclaimers somewhere else, not inline in a field that repeats.

## 4. Wrong article ("a orchestrator-worker") for pattern names starting with a vowel sound

**Symptom:** the "Proposed Architecture" section's first version hardcoded `f"as a **{uc['pattern']}**
pattern"`. Two of the 8 quick-reference-engine pattern keys — `orchestrator-worker` and `event-swarm` —
start with a vowel sound, so this rendered as "a orchestrator-worker pattern," a plain grammar error in
front of a client.

**Fix:** the article is now chosen with a one-line check (`"an" if pattern[0].lower() in "aeiou" else "a"`),
verified directly against all 8 pattern names before shipping — `orchestrator-worker` and `event-swarm` get
"an", the other 6 get "a". This is a narrow, deliberately simple rule (no exceptions for words like "hour"
that start with a consonant letter but a vowel sound) — it's correct for the fixed, known set of 8 pattern
names this engine will ever see, not a general-purpose English grammar solution. If you extend the pattern
set with a 9th name later, sanity-check the article against it the same way.

## General pattern across all of these

Every one of these four is a "the code is correct, the output reads badly" issue — none would show up in a
unit test that only checks the function doesn't raise. Read the rendered proposal end to end, ideally with a
fresh eye, before sending anything this engine produces to an actual client.
