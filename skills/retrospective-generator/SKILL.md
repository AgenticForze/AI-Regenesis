---
name: retrospective-generator
description: Audits an EXISTING, already-deployed AI/agentic system (not a catalog use case, not a new design) via a structured 16-question interview covering the 8-layer Decision Engineering Meta-Architecture (L1 Foundational Data through L8 Feedback & Reinforcement Loops), and produces a governance-style markdown report — a per-layer current-state table, severity-ranked findings, and an actionable "If we rebuilt this" recommendation section. Use whenever asked to audit, review, assess, or write a retrospective/gap-report for a real production or already-built AI/agentic system, run an "architecture audit," evaluate an existing system against the 8-layer framework, or interview a team about an AI system's governance/observability/data maturity. Distinct from deep8-architecture-engine (designs a NEW use case's architecture) and quick-reference-engine (designs a NEW use case's pattern diagram) — this skill is audit-only and never invents details about a system it wasn't told about.
---

# Retrospective Generator

An audit tool, not a generation tool. Interviews someone about a real system they already built and run, and
turns their answers into a governance-style report — the automated version of the "Architecture Audit"
service (run a client's existing AI system through the framework, deliver a gap report). Never invents system
details: every finding and every recommendation in the output traces back to a specific answer the
interviewee gave, and an answer of `"unknown"` shows up as "could not be confirmed" in the output, not as a
guess.

## What it produces

One markdown document with three sections, from one 16-question interview:

1. **Current state, by layer** — an 8-row table (L1→L8), each row a one-line status derived purely from that
   layer's two answers (`Solid` / `Partial coverage` / `Gap(s) found` / `Undetermined`).
2. **Findings** — every flagged (non-"yes") answer, split into high-severity (L4 gate, L5 execution/audit,
   L6 observability — the governance/safety-critical layers) and medium-severity, each bullet stating what
   was asked, what was answered, and the interviewee's own grounding detail.
3. **"If we rebuilt this"** — one actionable recommendation per finding, in the same voice as the catalog's
   own retrospective bullets ("Add a documented fallback path...", not a restated question). Deliberately a
   *different* rendering of each finding, not a repeat of section 2 — see `references/lessons-learned.md` #1
   for why that distinction mattered enough to fix.

## Quick start

```python
import sys; sys.path.insert(0, "scripts")
from interview_protocol import QUESTIONS, ALL_QUESTION_IDS, question_text
from retrospective_engine import render_retrospective_markdown

# Run the interview: ask every prompt in QUESTIONS (grouped by layer l1..l8) to the system's
# owner/engineer, and record a 4-value enum answer + optional free-text detail for each.
answers = {
    "l1_lineage": {"answer": "yes", "detail": "..."},
    # ... all 16 question ids, see references/spec-format.md for the full list and the enum values
}

report_md = render_retrospective_markdown(
    system_name="Their System's Real Name",
    answers=answers,
    audited_by="Your name/firm",   # optional
    audit_date="2026-08-12",        # optional
)
```

Write `report_md` to a `.md` file and present it — don't inline the whole report into chat prose for a real
audit; it's meant to be a standalone deliverable.

**All 16 questions are required.** `render_retrospective_markdown` (via `build_findings`) raises
`AnswerError` listing exactly which question ids are missing, or which one has an invalid enum value — it
won't silently skip an unanswered question. Run the whole interview before generating the report, not a
partial one.

## Running a real interview — practical notes

- Ask the `prompt` text verbatim or close to it — the questions were written to be answerable with the
  4-value enum without much interpretation. If the interviewee's answer is genuinely ambiguous between two
  enum values, ask them to pick rather than inferring it yourself.
- Prefer an interviewee who didn't build the system, or has no stake in it looking good, if that's an option
  — see `references/lessons-learned.md` #3. An all-`"yes"` report is worth a second, more skeptical pass
  before treating it as clean; the rendered report says so explicitly in that case.
- The `"detail"` field is optional per the engine, but skipping it consistently produces a much less useful
  report — the detail text is what makes a finding specific to *this* system instead of reading as generic
  audit boilerplate copied from the question bank.

## Reference files

- `references/spec-format.md` — the answer dict shape, how to run the interview, the severity model
  (`l4`/`l5`/`l6` = high severity, including on `"unknown"` answers), and what's required if you extend the
  question bank.
- `references/lessons-learned.md` — the findings/recommendations duplication bug (fixed, not just noted),
  the "unknown" severity design decision, and a process-level (not code-level) honesty caveat — read before
  extending this engine or running a real audit with it.
- `scripts/interview_protocol.py` — the 16-question bank (`QUESTIONS`, 2 per layer), `LAYER_NAMES`, and
  `question_text(question_id)`.
- `scripts/retrospective_engine.py` — `build_findings(answers)`, `layer_summary(answers)`,
  `render_retrospective_markdown(...)`, and `RECOMMENDATION_TEMPLATES` (one actionable recommendation per
  question id — required if you add a question).
- `scripts/example_interview.py` — one complete, runnable worked example against a fictional system (run it
  directly to produce a sample report and confirm your environment is set up correctly before running a real
  interview).
