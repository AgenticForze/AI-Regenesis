# -*- coding: utf-8 -*-
"""
Complete, runnable worked example. Run this directly to confirm your environment is set up correctly:

    cd scripts && python3 example_interview.py

Produces `example_retrospective.md` in the current directory.

The system audited below is FICTIONAL — "Support Ticket Triage Copilot" — invented for this example only,
not a real company or product. Copy this dict's shape as your starting point for a real audit: run the 16
questions in `interview_protocol.QUESTIONS` as an actual interview with the system's owner/engineers, and
fill in real answers.
"""
from retrospective_engine import render_retrospective_markdown

# A plausible mid-maturity system: strong on the "build it" layers (L1-L3), weaker on the "govern it"
# layers (L4-L6) — a common real-world pattern where a system ships and works, but the governance layer
# lags behind because it wasn't part of the original MVP scope.
EXAMPLE_ANSWERS = {
    # L1 — Foundational Data & Infrastructure
    "l1_lineage": {"answer": "yes",
                   "detail": "Zendesk ticket export (internal, hourly batch) and a vendor NLP "
                              "classification API (external, real-time) are both documented in the "
                              "team's onboarding wiki with owner and refresh cadence."},
    "l1_external_marked": {"answer": "yes",
                            "detail": "The vendor NLP API is access-scoped separately and flagged in the "
                                       "data inventory as third-party."},
    # L2 — Agent Intelligence & Models
    "l2_fallback": {"answer": "no",
                    "detail": "If the primary model provider has an outage, ticket triage silently stops "
                               "and tickets queue unclassified — no fallback model or degraded mode."},
    "l2_pinned": {"answer": "partial",
                  "detail": "Model version is pinned in config, but there's no test suite that runs before "
                             "a version bump, so upgrades have gone out without anyone confirming behavior "
                             "didn't shift."},
    # L3 — Agentic Core
    "l3_scope": {"answer": "yes",
                 "detail": "Two agents (Classifier, Router) each have a narrow, documented tool allowlist "
                            "enforced at the framework level, not just by convention."},
    "l3_circuit_breaker": {"answer": "yes",
                            "detail": "A timeout on the classification call routes to a manual-review "
                                       "queue instead of hanging or erroring the ticket."},
    # L4 — Decision Engineering (the gate)
    "l4_threshold": {"answer": "no",
                      "detail": "Auto-routing vs. human review is currently an if-statement with a "
                                 "hardcoded 0.8 confidence cutoff buried in the router agent's code, not a "
                                 "documented policy."},
    "l4_threshold_reviewable": {"answer": "no",
                                 "detail": "Nobody outside the two engineers who wrote it knows that "
                                            "number exists, let alone when it was last changed or why."},
    # L5 — Execution & Interaction
    "l5_change_control": {"answer": "partial",
                           "detail": "Writes to Zendesk (setting ticket priority/team) go through the "
                                      "same API a human agent would use, but there's no additional "
                                      "approval step even for high-priority reclassifications."},
    "l5_audit_log": {"answer": "yes",
                      "detail": "Every write is logged with ticket id, old/new values, and timestamp in a "
                                 "dedicated audit table."},
    # L6 — End-to-End Observability
    "l6_traced": {"answer": "partial",
                  "detail": "Latency and errors are traced in Datadog, but token cost and the model's raw "
                             "output aren't captured anywhere — only the final routing decision is logged."},
    "l6_alerted": {"answer": "no",
                   "detail": "There's no active alerting on classification-confidence drift or a spike in "
                              "manual-review-queue volume — someone has to think to go look."},
    # L7 — Leadership Dashboard Layer
    "l7_visibility": {"answer": "partial",
                       "detail": "Support ops leadership sees a weekly ticket-volume report, but it "
                                  "doesn't break out AI-routed accuracy specifically from the overall "
                                  "team metric."},
    "l7_cadence": {"answer": "yes",
                   "detail": "That weekly report is a standing agenda item in the support ops sync."},
    # L8 — Feedback & Reinforcement Loops
    "l8_loop_exists": {"answer": "no",
                        "detail": "Misrouted tickets that a human corrects aren't captured anywhere as "
                                   "labeled training/eval data — the correction just happens in Zendesk "
                                   "and the signal is lost."},
    "l8_loop_proven": {"answer": "no",
                        "detail": "Follows directly from the above — there's nothing to have proven yet."},
}

if __name__ == "__main__":
    md = render_retrospective_markdown(
        system_name="Support Ticket Triage Copilot (fictional example system)",
        answers=EXAMPLE_ANSWERS,
        audited_by="Example Audit Co.",
        audit_date="2026-08-12",
    )
    with open("example_retrospective.md", "w") as f:
        f.write(md)
    print(f"Retrospective written: {len(md)} chars -> example_retrospective.md")
    print("Open it and read it end-to-end before trusting the pattern for a real audit.")
