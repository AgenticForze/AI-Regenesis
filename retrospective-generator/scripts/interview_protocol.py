# -*- coding: utf-8 -*-
"""
The structured interview question bank for auditing an EXISTING (real, already-deployed) agentic/AI system
against the 8-layer Decision Engineering Meta-Architecture — the same L1-L8 taxonomy used by the
deep8-architecture-engine skill, but used here in the audit direction (find gaps in a real system) rather
than the generation direction (design a new one).

Two questions per layer, 16 total. Each question is answered with a 4-value enum (yes/partial/no/unknown)
plus optional free-text detail — NOT open-ended free text alone. This is a deliberate design choice: gap
detection in retrospective_engine.py is a plain rule lookup on the enum value, not text/NLP parsing. Keeping
the structured answer separate from the detail text is what makes the audit's findings reproducible and
testable, instead of depending on how the interviewer happened to phrase the transcript.
"""

LAYER_NAMES = {
    "l1": "L1 · Foundational Data & Infrastructure",
    "l2": "L2 · Agent Intelligence & Models",
    "l3": "L3 · Agentic Core",
    "l4": "L4 · Decision Engineering (the gate/threshold layer)",
    "l5": "L5 · Execution & Interaction",
    "l6": "L6 · End-to-End Observability",
    "l7": "L7 · Leadership Dashboard Layer",
    "l8": "L8 · Feedback & Reinforcement Loops",
}

# Answer enum values, in increasing order of concern.
ANSWER_VALUES = ("yes", "partial", "no", "unknown")

QUESTIONS = {
    "l1": [
        {"id": "l1_lineage", "prompt": "Are the system's data sources (internal systems of record and any "
         "external/third-party feeds) documented, with a known freshness/lineage SLA for each?"},
        {"id": "l1_external_marked", "prompt": "Are external (third-party) data sources explicitly "
         "distinguished from internal systems of record in documentation and access control — not just "
         "treated identically?"},
    ],
    "l2": [
        {"id": "l2_fallback", "prompt": "Is there a documented model-routing/fallback strategy for when the "
         "primary model is unavailable, rate-limited, or degraded?"},
        {"id": "l2_pinned", "prompt": "Is the production model version pinned and change-managed — do you "
         "know exactly which model version is live right now, and is upgrading it a deliberate, tested "
         "decision rather than something that happens silently?"},
    ],
    "l3": [
        {"id": "l3_scope", "prompt": "Is each agent's scope/tool-access documented and enforced, such that "
         "one agent can't accidentally call a tool or take an action meant for a different agent?"},
        {"id": "l3_circuit_breaker", "prompt": "Is there a fallback or circuit-breaker for when an agent "
         "call times out, errors, or returns malformed output?"},
    ],
    "l4": [
        {"id": "l4_threshold", "prompt": "Is there an explicit confidence/risk threshold that routes a "
         "decision to auto-execute vs. human review vs. hold — not an implicit judgment call buried in "
         "code or prompt text?"},
        {"id": "l4_threshold_reviewable", "prompt": "Is that threshold's current value, and the date/reason "
         "it was last changed, documented somewhere a non-engineer could review it?"},
    ],
    "l5": [
        {"id": "l5_change_control", "prompt": "Are the systems of record the agent writes to protected by "
         "the same change-control/rollback discipline a human-initiated change to those systems would "
         "require?"},
        {"id": "l5_audit_log", "prompt": "Is there an execution-level audit log recording who/what "
         "triggered every write, and when?"},
    ],
    "l6": [
        {"id": "l6_traced", "prompt": "Is every agent call traced end-to-end (input, output, latency, "
         "cost) in a queryable store — not just visible in scattered application logs?"},
        {"id": "l6_alerted", "prompt": "Are guardrail/policy violations actively alerted in real time, or "
         "only discoverable after the fact by someone going looking?"},
    ],
    "l7": [
        {"id": "l7_visibility", "prompt": "Does anyone outside the build team (a business owner, "
         "compliance, leadership) have a standing view into the system's real-world accuracy/outcomes?"},
        {"id": "l7_cadence", "prompt": "Is there a defined review cadence (weekly/monthly) for that "
         "visibility, or does it only get looked at during an incident?"},
    ],
    "l8": [
        {"id": "l8_loop_exists", "prompt": "Is there a mechanism that feeds real-world outcomes (confirmed "
         "correct/incorrect decisions) back into improving the system — retraining, threshold tuning, "
         "or prompt/spec updates?"},
        {"id": "l8_loop_proven", "prompt": "Has that feedback loop actually changed something in "
         "production at least once, or does it currently only exist on paper / as an intention?"},
    ],
}

ALL_QUESTION_IDS = [q["id"] for layer_qs in QUESTIONS.values() for q in layer_qs]


def question_text(question_id):
    """Look up a question's prompt text by id, across all layers."""
    for layer_qs in QUESTIONS.values():
        for q in layer_qs:
            if q["id"] == question_id:
                return q["prompt"]
    raise KeyError(f"Unknown question id: {question_id}")
