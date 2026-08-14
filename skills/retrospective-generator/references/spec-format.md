# Spec Format — Retrospective Generator

## The answer dict

One flat dict, keyed by question id (16 total, from `interview_protocol.ALL_QUESTION_IDS`):

```python
answers = {
    "l1_lineage": {"answer": "yes", "detail": "optional free-text grounding"},
    "l1_external_marked": {"answer": "partial", "detail": "..."},
    # ... all 16 question ids required — build_findings() raises AnswerError listing exactly which are
    # missing if you leave any out.
}
```

- `"answer"` — required, must be exactly one of `"yes"`, `"partial"`, `"no"`, `"unknown"`. Anything else
  raises `AnswerError` naming the offending question id and the bad value.
- `"detail"` — optional free text. Not required for the engine to run, but every finding's bullet is more
  useful with it — it's the only thing that makes the output specific to the system being audited instead
  of reading as generic advice. Omit only when the interviewee genuinely has nothing to add.

## Running the interview

`interview_protocol.QUESTIONS` is the source of truth — a dict keyed by layer (`l1`...`l8`), each value a
list of `{"id": ..., "prompt": ...}` dicts. Ask each `prompt` as an actual interview question to the system's
owner/engineer, and record their answer as one of the four enum values plus whatever detail they give you.
Don't paraphrase or infer the enum value from a rambling answer without confirming it with the interviewee —
if you're not sure whether their answer means "yes" or "partial," ask them to pick.

`interview_protocol.question_text(question_id)` looks up a single prompt by id if you need to re-ask or
reference one specific question outside the full interview.

## Generating the report

```python
from retrospective_engine import render_retrospective_markdown

md = render_retrospective_markdown(
    system_name="...",          # required — the real (or, for practice, fictional) system's name
    answers=answers,             # required — see above
    audited_by="...",            # optional
    audit_date="...",            # optional, any string (e.g. "2026-08-12")
)
```

Returns a single markdown string: a per-layer status table, findings split by severity (high = L4/L5/L6 gaps
— the governance/safety-critical layers — plus any `"unknown"` answer on those three layers; medium =
everything else), and a distinct "If we rebuilt this" section with actionable recommendations (see
`lessons-learned.md` #1 for why that section is deliberately *not* a repeat of the findings section).

Lower-level functions, if you need the structured data instead of the rendered markdown:

- `build_findings(answers)` → list of finding dicts (`layer`, `layer_name`, `question_id`, `question`,
  `answer`, `detail`, `severity`), sorted high-severity first.
- `layer_summary(answers)` → list of `(layer_name, status_line)` tuples, L1→L8 order.

## Severity model

`l4` (the gate/threshold), `l5` (execution/audit trail), and `l6` (observability) are the high-severity
layers — a gap here means a bad decision can execute or go unnoticed, not just "the system is a bit rough
around the edges." An `"unknown"` answer on one of these three layers is treated as high severity too, same
as `"no"` — not knowing whether your audit log or gate exists is not meaningfully safer than knowing it
doesn't. Every other layer's gaps are medium severity. This mapping is fixed in
`retrospective_engine.HIGH_SEVERITY_LAYERS` — it's a deliberate editorial choice tied to the framework's own
emphasis (see the framework's L4-L6 role in `deep8-architecture-engine`), not something to tune per-audit
without a good reason to override it.

## Extending the question bank

If you add a 17th (or replace an existing) question, you must also add a matching entry to
`retrospective_engine.RECOMMENDATION_TEMPLATES` keyed by the same question id — `_recommendation_for_finding`
does a plain dict lookup and will raise `KeyError` on any flagged question missing a template. This is
intentional: it forces every question in the bank to have a real, specific recommendation behind it instead
of silently falling back to a generic "fix this" placeholder.
