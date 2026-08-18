# -*- coding: utf-8 -*-
"""
Turns a completed interview (answers keyed by question id, from interview_protocol.QUESTIONS) into:
  1. A findings list — one entry per flagged gap, with severity and the interviewee's own detail text.
  2. A per-layer current-state summary table (list of (layer_name, one-line status) tuples).
  3. A markdown retrospective document — in the same "if we rebuilt this" bullet voice as the catalog's own
     `retrospective` fields (see the deep8/quick-reference packs), but grounded in this system's actual
     answers, not fictional.

This is an AUDIT tool, not a generation tool — it never invents system details. Every finding and every
bullet in the output is traceable to a specific answer the interviewee gave. Where an answer is "unknown",
the output says so explicitly rather than guessing.
"""
from interview_protocol import QUESTIONS, LAYER_NAMES, question_text

# Severity by layer — L4/L5/L6 gaps are governance/safety-critical (a bad decision executes or goes
# unnoticed); L1/L2/L3/L7/L8 gaps are operational/quality risks (things degrade slower, are more
# recoverable). This mirrors the framework's own emphasis: the gate, execution audit trail, and
# observability are the layers a real incident review usually traces back to first.
HIGH_SEVERITY_LAYERS = {"l4", "l5", "l6"}

SEVERITY_RANK = {"no": 2, "partial": 1, "unknown": 1, "yes": 0}  # 0 = no finding

# One actionable "what we'd add/fix" recommendation per question, in the same voice as the catalog's own
# retrospective bullets ("Add a confidence-calibration step...", not "Is there a confidence-calibration
# step? — no."). Used only for flagged (non-"yes") answers — see _recommendation_for_finding. Each is a
# generic-but-concrete recommendation; the interviewee's own detail text is appended as grounding context,
# not replaced by it, so the bullet stays specific to their system rather than reading as boilerplate.
RECOMMENDATION_TEMPLATES = {
    "l1_lineage": "Document each data source's freshness/lineage SLA in one place a new engineer (or an "
                  "auditor) can find without asking around.",
    "l1_external_marked": "Explicitly flag every external/third-party data source in the data inventory and "
                           "scope its access separately from internal systems of record.",
    "l2_fallback": "Add a documented fallback/degraded-mode path for when the primary model is unavailable, "
                   "rate-limited, or degraded, instead of letting the system stall silently.",
    "l2_pinned": "Add a regression/eval suite that runs before any production model-version bump, so "
                 "upgrades are a deliberate, verified decision rather than a silent behavior change.",
    "l3_scope": "Document and enforce each agent's tool-access scope at the framework level, so one agent "
                "can't accidentally call a tool meant for another.",
    "l3_circuit_breaker": "Add a circuit-breaker/fallback path for agent call timeouts, errors, or "
                           "malformed output, so failures degrade gracefully instead of hanging or crashing.",
    "l4_threshold": "Replace the implicit/hardcoded routing logic with an explicit, named confidence-risk "
                    "threshold — a policy value, not a buried if-statement.",
    "l4_threshold_reviewable": "Document the threshold's current value and change history somewhere a "
                                "non-engineer (compliance, ops leadership) can review it without reading code.",
    "l5_change_control": "Bring writes to systems of record under the same change-control/rollback "
                          "discipline — including an approval step for high-impact writes — that a "
                          "human-initiated change would require.",
    "l5_audit_log": "Add an execution-level audit log capturing who/what triggered every write and when, "
                    "if one doesn't already cover every write path.",
    "l6_traced": "Extend tracing to capture full input/output/latency/cost per agent call in a queryable "
                 "store, not just the final decision.",
    "l6_alerted": "Add active, real-time alerting on guardrail/policy violations and confidence drift, "
                  "instead of relying on someone noticing after the fact.",
    "l7_visibility": "Give a non-build-team stakeholder (business owner, compliance, or leadership) a "
                      "standing, AI-specific accuracy/outcomes view — not folded into a general team metric.",
    "l7_cadence": "Establish a defined review cadence for that visibility if one doesn't already exist, so "
                  "it isn't only consulted during an incident.",
    "l8_loop_exists": "Build a mechanism that captures confirmed correct/incorrect decisions as labeled "
                       "data and feeds them back into retraining, threshold tuning, or spec updates.",
    "l8_loop_proven": "Prioritize getting the feedback loop to make one real production change end-to-end — "
                       "an unproven loop is a plan, not a capability.",
}


class AnswerError(ValueError):
    pass


def _validate_answers(answers):
    all_ids = {q["id"] for qs in QUESTIONS.values() for q in qs}
    missing = all_ids - set(answers.keys())
    if missing:
        raise AnswerError(f"Missing answers for question id(s): {sorted(missing)}")
    for qid, a in answers.items():
        if qid not in all_ids:
            raise AnswerError(f"Unknown question id in answers: {qid}")
        if "answer" not in a or a["answer"] not in ("yes", "partial", "no", "unknown"):
            raise AnswerError(f"Answer for {qid} must have answer in yes/partial/no/unknown, got: {a}")


def build_findings(answers):
    """
    answers: dict[question_id] -> {"answer": "yes"|"partial"|"no"|"unknown", "detail": str (optional)}
    Returns: list of finding dicts, sorted highest-severity first, each with:
        layer, layer_name, question_id, question, answer, detail, severity ("high"|"medium")
    """
    _validate_answers(answers)
    findings = []
    for layer, qs in QUESTIONS.items():
        for q in qs:
            qid = q["id"]
            a = answers[qid]
            rank = SEVERITY_RANK[a["answer"]]
            if rank == 0:
                continue
            severity = "high" if (layer in HIGH_SEVERITY_LAYERS and rank >= 1) else "medium"
            # An "unknown" on a high-severity layer is itself worth flagging as high — not knowing
            # whether your gate/audit-log/observability exists is not meaningfully safer than knowing
            # it doesn't.
            if layer in HIGH_SEVERITY_LAYERS and a["answer"] == "unknown":
                severity = "high"
            findings.append({
                "layer": layer,
                "layer_name": LAYER_NAMES[layer],
                "question_id": qid,
                "question": q["prompt"],
                "answer": a["answer"],
                "detail": a.get("detail", "").strip(),
                "severity": severity,
            })
    findings.sort(key=lambda f: (0 if f["severity"] == "high" else 1, f["layer"]))
    return findings


def layer_summary(answers):
    """
    Returns list of (layer_name, status_line) tuples, one per layer, in L1->L8 order.
    status_line is a short plain-English rollup: "Solid", "Partial coverage", "Gap(s) found", or
    "Undetermined" — derived purely from the answer enum, not a judgment call made in this function.
    """
    _validate_answers(answers)
    out = []
    for layer, qs in QUESTIONS.items():
        vals = [answers[q["id"]]["answer"] for q in qs]
        if all(v == "yes" for v in vals):
            status = "Solid — both audit questions answered yes."
        elif "no" in vals:
            status = "Gap(s) found — see findings below."
        elif "unknown" in vals:
            status = "Undetermined — at least one question couldn't be answered during the interview."
        else:
            status = "Partial coverage — see findings below."
        out.append((LAYER_NAMES[layer], status))
    return out


def _bullet_for_finding(f):
    """
    One markdown bullet per finding, for the FINDINGS section — factual, states what was asked and what was
    answered, grounded in the interviewee's own detail text when they gave one. This section documents the
    current state; it deliberately does not prescribe a fix (that's _recommendation_for_finding's job) so
    the two sections don't end up saying the same thing twice.
    """
    layer_short = f["layer_name"].split(" · ")[1]
    if f["answer"] == "no":
        base = f"**{layer_short}:** {f['question']} — currently no."
    elif f["answer"] == "partial":
        base = f"**{layer_short}:** {f['question']} — currently partial."
    else:  # unknown
        base = f"**{layer_short}:** {f['question']} — could not be confirmed during this audit."
    if f["detail"]:
        base += f" {f['detail']}"
    return base


def _recommendation_for_finding(f):
    """
    One markdown bullet per finding, for the "If we rebuilt this" section — an actionable recommendation
    (what to add/fix), in the catalog's own retrospective voice, not a restated question. Distinct from
    _bullet_for_finding on purpose: this is prescriptive, that one is descriptive.
    """
    layer_short = f["layer_name"].split(" · ")[1]
    rec = RECOMMENDATION_TEMPLATES[f["question_id"]]
    base = f"**{layer_short}:** {rec}"
    if f["detail"]:
        base += f" (Current state: {f['detail']})"
    return base


def render_retrospective_markdown(system_name, answers, audited_by=None, audit_date=None):
    """
    Full markdown document: title, per-layer summary table, findings by severity, and an
    "If we rebuilt this" bullet section — the artifact this skill exists to produce.
    """
    findings = build_findings(answers)
    summary = layer_summary(answers)

    lines = [f"# Architecture Audit & Retrospective — {system_name}", ""]
    meta_bits = []
    if audited_by:
        meta_bits.append(f"Audited by: {audited_by}")
    if audit_date:
        meta_bits.append(f"Date: {audit_date}")
    if meta_bits:
        lines.append("*" + " · ".join(meta_bits) + "*")
        lines.append("")

    lines.append("## Current state, by layer")
    lines.append("")
    lines.append("| Layer | Status |")
    lines.append("|---|---|")
    for layer_name, status in summary:
        lines.append(f"| {layer_name} | {status} |")
    lines.append("")

    high = [f for f in findings if f["severity"] == "high"]
    medium = [f for f in findings if f["severity"] == "medium"]

    if not findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("No gaps flagged — every audit question was answered **yes**. Worth a second, more "
                      "skeptical pass before taking that at face value (see `references/lessons-learned.md` "
                      "on interview-answer honesty), but nothing in this interview surfaced a concrete gap.")
        lines.append("")
    else:
        if high:
            lines.append("## High-severity findings (governance/safety-critical layers)")
            lines.append("")
            for f in high:
                lines.append(f"- {_bullet_for_finding(f)}")
            lines.append("")
        if medium:
            lines.append("## Medium-severity findings")
            lines.append("")
            for f in medium:
                lines.append(f"- {_bullet_for_finding(f)}")
            lines.append("")

    lines.append('## "If we rebuilt this" — what we\'d improve')
    lines.append("")
    if not findings:
        lines.append("Nothing to add beyond the note above — no gaps were surfaced by this interview.")
    else:
        for f in findings:
            lines.append(f"- {_recommendation_for_finding(f)}")
    lines.append("")

    return "\n".join(lines)
