# -*- coding: utf-8 -*-
"""
Deep 8-Layer specs for the 20 BSS/OSS use cases. Each spec drives the diagram, the blueprint table,
the agent stack, and the build order from one source of truth via scripts/deep8_engine.py.
"""

def _ext(id_, title): return {"id": id_, "title": title, "sub": "External Data Store", "external": True}
def _int(id_, title): return {"id": id_, "title": title, "sub": "Internal Data Store"}
def _l2(id_, title, prod=None):
    d = {"id": id_, "title": title, "sub": "L2 · The Brain"}
    if prod: d["prod"] = prod
    return d
def _orch(id_, title): return {"id": id_, "title": title, "sub": "L3 · Orchestration"}
def _w(id_, title): return {"id": id_, "title": title, "sub": "L3 · Specialist"}
def _l4(id_, title): return {"id": id_, "title": title, "sub": "L4 · Governance"}
def _gate(id_, title): return {"id": id_, "title": title, "sub": "Conditional routing"}
def _l5_human(id_, title): return {"id": id_, "title": title, "sub": "Human-in-the-loop", "color": "leadership", "gate_branch": "human"}
def _l5_auto(id_, title): return {"id": id_, "title": title, "sub": "L5 · Tool Registry", "gate_branch": "auto"}
def _l5_plain(id_, title): return {"id": id_, "title": title, "sub": "L5 · Tool Registry"}
def _l5_hold(id_, title): return {"id": id_, "title": title, "sub": "Conditional: policy breach", "color": "obs", "gate_branch": "hold"}
def _l6(id_, title): return {"id": id_, "title": title, "sub": "L6 · Nervous System"}
def _l7(id_, title): return {"id": id_, "title": title, "sub": "L7 · Leadership Portal"}
def _l8(id_, title): return {"id": id_, "title": title, "sub": "L8 · Self-Healing"}


BSSOSS_SPECS = [

{
 "id": 1, "quick_slug": "order-to-activation-orchestration",
 "quick_title": "Order-to-Activation Orchestration",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Order-to-Activation Fulfillment Decisioning",
 "intro": ("This deep-8 view takes the order-to-activation pipeline beyond task execution into a governed, "
           "observable, self-improving decision system — a fulfillment engine that knows when to auto-execute, "
           "when to ask a human, and when to hold and escalate, with executive-level cost/cycle-time visibility."),
 "problem": ("A single customer order fans out into dozens of downstream tasks across CRM, catalog, provisioning, "
             "and billing. Static workflow engines break silently on unexpected product combinations, leaving "
             "orders stuck in fallout queues for days with no governance layer, no executive visibility into what "
             "automation is actually saving, and no feedback loop that gets better at handling edge cases over time."),
 "diagram_note": ("The Fulfillment Confidence & Risk Gate branches three ways — clean orders auto-execute, "
                   "ambiguous or high-value orders go to Order Ops, and policy-breaching orders hold. L8 closes "
                   "the loop by comparing predicted fulfillment outcomes against what actually shipped."),
 "spec": {
   "l1": [_ext("ext1", "Partner/Vendor Order API"), _int("int1", "Order Management System DB"),
          _int("int2", "Product Catalog DB"), _int("int3", "Network Provisioning Logs")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"),
          _l2("kg", "Order/Catalog Knowledge Graph", "Neo4j graph database")],
   "l3_orch": _orch("orch", "Order Orchestration Agent"),
   "l3_workers": [_w("w1", "Order Validation Agent"), _w("w2", "Product-to-Service Mapping Agent"),
                  _w("w3", "Provisioning Sequencing Agent"), _w("w4", "Activation Confirmation Agent")],
   "l4": [_l4("g1", "Catalog Compliance Policy Engine"), _l4("g2", "Fallout Risk Guardrail"),
          _l4("g3", "Change-Management Rule Engine")],
   "gate": _gate("gate", "Fulfillment Confidence & Risk Gate"),
   "l5": [_l5_human("human", "Order Ops Approval"), _l5_auto("a1", "Billing Activation API"),
          _l5_plain("a2", "Network Provisioning API"), _l5_plain("a3", "Customer Notification Gateway"),
          _l5_hold("hold", "Fallout Hold Queue")],
   "l6": [_l6("m1", "Fallout Recurrence Monitor"), _l6("m2", "Data Quality Watchdog"), _l6("m3", "Provisioning Auditor")],
   "l7": [_l7("lead1", "Order Cycle-Time Dashboard"), _l7("lead2", "Fallout Cost Scorecard"), _l7("lead3", "Automation Coverage View")],
   "l8": [_l8("s1", "Fulfillment Accuracy Tracker"), _l8("s2", "Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("order fulfillment", "Order Validation Agent", "Order Orchestration Agent", 3,
                         "Fulfillment Confidence & Risk Gate", "Billing Activation API", "Order Ops Approval"),
},

{
 "id": 2, "quick_slug": "product-catalog-offer-management",
 "quick_title": "Product Catalog & Offer Management Automation",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Product Catalog & Offer Launch Decisioning",
 "intro": ("This deep-8 view treats every catalog/offer launch as a governed decision, not just a publish "
           "action — with margin and legal guardrails before launch, drift detection after launch, and a "
           "feedback loop that improves the rules over time, not just faster publishing."),
 "problem": ("Launching a bundled offer requires coordinating pricing, eligibility, and technical service specs "
             "across a sprawling catalog. Commercial teams call this the biggest speed-to-market bottleneck, but "
             "speed without governance risks margin-eroding offers and API-breaking catalog changes with no "
             "executive visibility into either."),
 "diagram_note": ("The Offer Launch Readiness Gate branches into auto-publish for validated low-risk offers, "
                   "Commercial Sign-off for anything touching margin, and a hold queue for anything failing "
                   "the test-order validation run."),
 "spec": {
   "l1": [_int("int1", "Product Catalog DB (TMF620)"), _int("int2", "Pricing/Discount Rules DB"),
          _int("int3", "Channel Content Store")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Offer/Product Knowledge Graph")],
   "l3_orch": _orch("orch", "Catalog Publication Orchestrator"),
   "l3_workers": [_w("w1", "Commercial Offer Manager Agent"), _w("w2", "Technical Specification Manager Agent"),
                  _w("w3", "Pricing Validation Agent")],
   "l4": [_l4("g1", "Margin Floor Policy Engine"), _l4("g2", "Discount Stacking Guardrail"), _l4("g3", "Legal Review Rule Engine")],
   "gate": _gate("gate", "Offer Launch Readiness Gate"),
   "l5": [_l5_human("human", "Commercial Sign-off"), _l5_auto("a1", "Catalog Publish API (TMF620)"),
          _l5_plain("a2", "Channel CMS Update"), _l5_plain("a3", "Test-Order Validation Run"),
          _l5_hold("hold", "Launch Hold Queue")],
   "l6": [_l6("m1", "Post-Launch Fallout-Rate Monitor"), _l6("m2", "Pricing Drift Watchdog"), _l6("m3", "API Contract Drift Detector")],
   "l7": [_l7("lead1", "Speed-to-Market Dashboard"), _l7("lead2", "Margin Compliance Scorecard"), _l7("lead3", "Offer Adoption View")],
   "l8": [_l8("s1", "Offer Performance Tracker"), _l8("s2", "Catalog-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("product catalog", "Commercial Offer Manager Agent", "Catalog Publication Orchestrator", 2,
                         "Offer Launch Readiness Gate", "Catalog Publish API (TMF620)", "Commercial Sign-off"),
},

{
 "id": 3, "quick_slug": "revenue-assurance-leakage-detection",
 "quick_title": "Revenue Assurance & Leakage Detection",
 "quick_pattern_label": "Blackboard / Shared-Memory",
 "title": "Revenue Leakage Detection & Recovery Decisioning",
 "intro": ("This deep-8 view turns leakage detection from a reporting exercise into a governed recovery "
           "decision system — auto-correcting only what's high-confidence, routing the rest to finance, and "
           "tracking recovered-vs-at-risk revenue for leadership."),
 "problem": ("Revenue leakage typically runs 1-3% of telecom revenue and is scattered across mediation, rating, "
             "billing, and provisioning systems. Detection alone doesn't recover a dollar — without correction "
             "authorization guardrails and materiality-based prioritization, leakage findings pile up faster than "
             "finance can act on them."),
 "diagram_note": ("The Leakage Confidence & Materiality Gate separates auto-correctable leakage from cases "
                   "needing finance review, and holds low-confidence findings rather than risking a wrong "
                   "correction in the other direction."),
 "spec": {
   "l1": [_int("int1", "Mediation Platform Feed"), _int("int2", "Rating Engine Logs"),
          _int("int3", "Billing System Records"), _int("int4", "Provisioning/Inventory Feed")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Revenue Assurance Knowledge Graph")],
   "l3_orch": _orch("orch", "Revenue Assurance Controller Agent"),
   "l3_workers": [_w("w1", "Usage-to-Billing Reconciliation Agent"), _w("w2", "Discount Misapplication Agent"),
                  _w("w3", "Un-activated Service Agent"), _w("w4", "Rating Config Drift Agent")],
   "l4": [_l4("g1", "Correction Authorization Policy"), _l4("g2", "Minimum-Evidence Guardrail"), _l4("g3", "Finance Sign-off Rule Engine")],
   "gate": _gate("gate", "Leakage Confidence & Materiality Gate"),
   "l5": [_l5_human("human", "Finance Review Queue"), _l5_auto("a1", "Automated Re-billing Trigger"),
          _l5_plain("a2", "Systemic Root-Cause Ticket"), _l5_hold("hold", "Low-Confidence Hold Queue")],
   "l6": [_l6("m1", "Leakage Recurrence Monitor"), _l6("m2", "Data Quality Watchdog"), _l6("m3", "Correction Auditor")],
   "l7": [_l7("lead1", "Recovered Revenue Dashboard"), _l7("lead2", "At-Risk Revenue Scorecard"), _l7("lead3", "Leakage-by-Root-Cause View")],
   "l8": [_l8("s1", "Leakage Detection Accuracy Tracker"), _l8("s2", "Detection-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("revenue assurance", "Usage-to-Billing Reconciliation Agent", "Revenue Assurance Controller Agent", 3,
                         "Leakage Confidence & Materiality Gate", "Automated Re-billing Trigger", "Finance Review Queue"),
},

{
 "id": 4, "quick_slug": "order-fallout-detection-recovery",
 "quick_title": "Order Fallout Detection & Auto-Recovery",
 "quick_pattern_label": "Event-Driven Reactive Swarm",
 "title": "Order Fallout Recovery Decisioning",
 "intro": ("This deep-8 view adds governance and accountability around fallout auto-correction — the reactive "
           "swarm from the Quick view still catches events in real time, but every correction now passes through "
           "a risk gate and gets tracked for accuracy over time."),
 "problem": ("Orders that stall mid-fulfillment pile up in manual work queues. Most fallout falls into recurring "
             "patterns a swarm can resolve instantly, but auto-correction without guardrails risks masking "
             "systemic bugs behind an ever-retrying agent, and without accuracy tracking nobody knows if the "
             "auto-fixes are actually still working six months later."),
 "diagram_note": ("The Fallout Confidence & Novelty Gate routes recognized patterns to auto-correction, "
                   "genuinely novel fallout to a specialist, and anything failing policy checks to escalation "
                   "hold — with L8 tracking whether each pattern's fix accuracy is holding up over time."),
 "spec": {
   "l1": [_int("int1", "Order State Event Stream"), _int("int2", "Historical Fallout Case Archive"),
          _int("int3", "Catalog Version History")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Fallout Pattern Knowledge Graph")],
   "l3_orch": _orch("orch", "Fallout Triage Orchestrator"),
   "l3_workers": [_w("w1", "Timeout/Retry Agent"), _w("w2", "Data Mismatch Detection Agent"),
                  _w("w3", "Duplicate Order Detection Agent"), _w("w4", "Novel Fallout Escalation Agent")],
   "l4": [_l4("g1", "Retry-Limit Policy Engine"), _l4("g2", "Blast-Radius Guardrail"), _l4("g3", "Correction Authorization Rules")],
   "gate": _gate("gate", "Fallout Confidence & Novelty Gate"),
   "l5": [_l5_human("human", "Order Ops Specialist Queue"), _l5_auto("a1", "Automated Order Correction"),
          _l5_plain("a2", "Fallout Queue Update"), _l5_hold("hold", "Escalation Hold Queue")],
   "l6": [_l6("m1", "Auto-Resolution Accuracy Monitor"), _l6("m2", "Retry-Storm Watchdog"), _l6("m3", "Correction Auditor")],
   "l7": [_l7("lead1", "Fallout Rate Dashboard"), _l7("lead2", "Auto-Resolution Coverage Scorecard"), _l7("lead3", "Cost-Avoidance View")],
   "l8": [_l8("s1", "Fallout Pattern Accuracy Tracker"), _l8("s2", "Pattern-Library Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("order fallout", "Timeout/Retry Agent", "Fallout Triage Orchestrator", 3,
                         "Fallout Confidence & Novelty Gate", "Automated Order Correction", "Order Ops Specialist Queue"),
},

{
 "id": 5, "quick_slug": "network-inventory-discovery-reconciliation",
 "quick_title": "Network Inventory Discovery & Reconciliation",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Network Inventory Reconciliation Decisioning",
 "intro": ("This deep-8 view wraps inventory discovery in explicit blast-radius governance — bulk corrections "
           "always require sign-off, individual low-risk corrections can auto-execute, and leadership gets a "
           "direct view of inventory accuracy trends, not just a one-time cleanup report."),
 "problem": ("OSS inventory drifts out of sync with the physical network over time, cascading into failed "
             "provisioning and wasted truck-rolls. Auto-correcting inventory discrepancies without a bulk-change "
             "approval gate risks deleting legitimately-planned-but-not-yet-installed equipment records, as "
             "happened in the Quick Reference version's own retrospective."),
 "diagram_note": ("The Reconciliation Confidence & Impact Gate keeps bulk/high-volume corrections behind human "
                   "approval by design — this mirrors the Quick view's own hard-learned lesson about auto-"
                   "correction risk, now made an explicit, permanent architectural gate rather than a policy note."),
 "spec": {
   "l1": [_int("int1", "EMS/NMS Live Network State"), _int("int2", "OSS Inventory System of Record"),
          _int("int3", "Field Technician Close-out Reports")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Network Topology Knowledge Graph", "Neo4j")],
   "l3_orch": _orch("orch", "Inventory Reconciliation Orchestrator"),
   "l3_workers": [_w("w1", "Physical Layer Discovery Agent"), _w("w2", "Logical/Service Layer Discovery Agent"),
                  _w("w3", "Ghost Record Detection Agent"), _w("w4", "Discrepancy Impact Agent")],
   "l4": [_l4("g1", "Bulk-Correction Approval Policy"), _l4("g2", "Blast-Radius Guardrail"), _l4("g3", "Correction Authorization Rules")],
   "gate": _gate("gate", "Reconciliation Confidence & Impact Gate"),
   "l5": [_l5_human("human", "Inventory Manager Approval"), _l5_auto("a1", "Inventory Auto-Correction API"),
          _l5_plain("a2", "Field Audit Work Order"), _l5_hold("hold", "Reconciliation Hold Queue")],
   "l6": [_l6("m1", "Inventory Accuracy Monitor"), _l6("m2", "Discovery Sweep Watchdog"), _l6("m3", "Correction Auditor")],
   "l7": [_l7("lead1", "Inventory Accuracy Dashboard"), _l7("lead2", "Reconciliation Cost Scorecard"), _l7("lead3", "Domain Coverage View")],
   "l8": [_l8("s1", "Reconciliation Accuracy Tracker"), _l8("s2", "Sweep-Cadence Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("network inventory", "Physical Layer Discovery Agent", "Inventory Reconciliation Orchestrator", 3,
                         "Reconciliation Confidence & Impact Gate", "Inventory Auto-Correction API", "Inventory Manager Approval"),
},

{
 "id": 6, "quick_slug": "mediation-cdr-xdr-processing",
 "quick_title": "Mediation & CDR/xDR Processing Pipeline",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Mediation & Rating-Feed Integrity Decisioning",
 "intro": ("This deep-8 view treats mediation as more than a data pipeline — every record's path to the rating "
           "engine now passes through explicit data-quality governance, with drift detection catching vendor "
           "format changes before they silently corrupt a billing cycle."),
 "problem": ("Mediation ingests billions of records from heterogeneous network elements. Format drift from "
             "vendor firmware updates causes downstream rating errors that go undetected for entire billing "
             "cycles — the Quick Reference retrospective specifically flags this as the most costly gap in the "
             "original design."),
 "diagram_note": ("The Record Confidence & Exception Gate routes clean records straight to the rating engine, "
                   "ambiguous records to mediation ops, and records failing quality thresholds to an exception "
                   "queue — with L6's vendor-drift auditor specifically designed to catch the class of failure "
                   "that went undetected in the original design."),
 "spec": {
   "l1": [_int("int1", "Raw Network Element Feed"), _int("int2", "Vendor Format Spec Archive"),
          _int("int3", "Customer/Service Context Store")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Vendor Format Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Record Ingestion & Format Detection Agent"), _w("w2", "Data Quality Validation Agent"),
                  _w("w3", "Correlation & De-duplication Agent"), _w("w4", "Normalization & Enrichment Agent")],
   "l4": [_l4("g1", "Data-Quality Threshold Policy"), _l4("g2", "Vendor-Format Compatibility Guardrail"), _l4("g3", "Correction Authorization Rules")],
   "gate": _gate("gate", "Record Confidence & Exception Gate"),
   "l5": [_l5_human("human", "Mediation Ops Review"), _l5_auto("a1", "Rating Engine Feed"),
          _l5_plain("a2", "Vendor Format-Change Alert"), _l5_hold("hold", "Exception Queue")],
   "l6": [_l6("m1", "Record-Loss Monitor"), _l6("m2", "Data-Quality Watchdog"), _l6("m3", "Vendor Drift Auditor")],
   "l7": [_l7("lead1", "Mediation Throughput Dashboard"), _l7("lead2", "Data-Quality Scorecard"), _l7("lead3", "Billing-Accuracy Impact View")],
   "l8": [_l8("s1", "Mediation Accuracy Tracker"), _l8("s2", "Parser Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("mediation", "Record Ingestion & Format Detection Agent", None, 3,
                         "Record Confidence & Exception Gate", "Rating Engine Feed", "Mediation Ops Review"),
},

{
 "id": 7, "quick_slug": "charging-rating-anomaly-detection",
 "quick_title": "Charging & Rating Engine Anomaly Detection",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Rating Anomaly Correction Decisioning",
 "intro": ("This deep-8 view keeps the proposer/critic reflective loop from the Quick view but wraps it in "
           "explicit dollar-limit governance and executive revenue-recovery reporting — the debate happens "
           "inside L3, but nothing gets corrected without passing L4's guardrails."),
 "problem": ("Real-time charging engines occasionally under- or over-charge due to configuration errors or "
             "edge-case usage patterns. Auto-correction without a dollar-amount ceiling risks compounding small "
             "per-event errors into material revenue impact at scale — exactly what the Quick view's "
             "retrospective flagged after tightening its own threshold."),
 "diagram_note": ("The Rating Anomaly Confidence Gate keeps auto-correction scoped to small, high-confidence, "
                   "policy-bounded cases; anything larger routes to Revenue Assurance for human review before "
                   "a customer sees a corrected charge."),
 "spec": {
   "l1": [_int("int1", "Real-Time Charging Records"), _int("int2", "Rate Plan & Promo Configuration"),
          _int("int3", "Historical Rating Baseline")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Rate-Plan Knowledge Graph")],
   "l3_orch": _orch("orch", "Rating Anomaly Arbiter Agent"),
   "l3_workers": [_w("w1", "Rating Anomaly Proposer Agent"), _w("w2", "Legitimate Rating Explanation Critic Agent"),
                  _w("w3", "Configuration Drift Cross-Check Agent")],
   "l4": [_l4("g1", "Auto-Correction Dollar-Limit Policy"), _l4("g2", "Customer-Impact Guardrail"), _l4("g3", "Correction Authorization Rules")],
   "gate": _gate("gate", "Rating Anomaly Confidence Gate"),
   "l5": [_l5_human("human", "Revenue Assurance Review"), _l5_auto("a1", "Correction Execution API"),
          _l5_plain("a2", "Customer Credit Notification"), _l5_hold("hold", "Rating Case Hold Queue")],
   "l6": [_l6("m1", "Rating-Accuracy Monitor"), _l6("m2", "False-Positive Watchdog"), _l6("m3", "Correction Auditor")],
   "l7": [_l7("lead1", "Rating Accuracy Dashboard"), _l7("lead2", "Revenue-Recovery Scorecard"), _l7("lead3", "Customer-Credit Impact View")],
   "l8": [_l8("s1", "Rating Anomaly Accuracy Tracker"), _l8("s2", "Threshold Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("charging/rating", "Rating Anomaly Proposer Agent", "Rating Anomaly Arbiter Agent", 2,
                         "Rating Anomaly Confidence Gate", "Correction Execution API", "Revenue Assurance Review"),
},

{
 "id": 8, "quick_slug": "customer-360-master-data-unification",
 "quick_title": "Customer 360 / Master Data Unification",
 "quick_pattern_label": "Blackboard / Shared-Memory",
 "title": "Customer Identity Resolution Decisioning",
 "intro": ("This deep-8 view makes the Quick view's 'most restrictive wins' consent rule an explicit, "
           "non-bypassable L4 policy, and adds a materiality-tiered review path for genuinely ambiguous "
           "identity conflicts rather than forcing every conflict through the same resolution path."),
 "problem": ("Customer data is fragmented across CRM, billing, provisioning, loyalty, and support systems. "
             "Identity-resolution false-merges are far more damaging than false-splits, and consent conflicts "
             "resolved in favor of marketing reach — even briefly — create real compliance exposure."),
 "diagram_note": ("The Profile Confidence & Conflict Gate routes high-confidence matches to automatic sync, "
                   "genuinely ambiguous conflicts to a data steward, and low-confidence matches to hold — with "
                   "the consent/preference guardrail in L4 hard-coded to the most-restrictive-wins rule, no "
                   "override path."),
 "spec": {
   "l1": [_int("int1", "CRM/Billing/Provisioning Feeds"), _int("int2", "Loyalty & Support System Feeds"),
          _int("int3", "Consent & Preference Store")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Customer Identity Knowledge Graph")],
   "l3_orch": _orch("orch", "Customer 360 Synthesis Controller Agent"),
   "l3_workers": [_w("w1", "Identity Resolution Agent"), _w("w2", "Contact/Address Conflict Resolution Agent"),
                  _w("w3", "Product/Service Holdings Agent"), _w("w4", "Preference & Consent Agent")],
   "l4": [_l4("g1", "Most-Restrictive-Consent Policy"), _l4("g2", "Identity-Match Confidence Guardrail"), _l4("g3", "Data Steward Rule Engine")],
   "gate": _gate("gate", "Profile Confidence & Conflict Gate"),
   "l5": [_l5_human("human", "Data Steward Review"), _l5_auto("a1", "Unified Profile API Sync"),
          _l5_plain("a2", "Downstream System Sync"), _l5_hold("hold", "Conflict Hold Queue")],
   "l6": [_l6("m1", "Profile Drift Monitor"), _l6("m2", "Match-Quality Watchdog"), _l6("m3", "Sync Auditor")],
   "l7": [_l7("lead1", "Profile Completeness Dashboard"), _l7("lead2", "Data-Quality Scorecard"), _l7("lead3", "Downstream Adoption View")],
   "l8": [_l8("s1", "Match Accuracy Tracker"), _l8("s2", "Resolution-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("customer identity", "Identity Resolution Agent", "Customer 360 Synthesis Controller Agent", 3,
                         "Profile Confidence & Conflict Gate", "Unified Profile API Sync", "Data Steward Review"),
},

{
 "id": 9, "quick_slug": "subscription-lifecycle-entitlement",
 "quick_title": "Subscription Lifecycle & Entitlement Management",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Subscription Entitlement Accuracy Decisioning",
 "intro": ("This deep-8 view adds the entitlement-drift monitoring the Quick view's own retrospective wished "
           "it had built first — proactive drift detection is now a first-class L6 component, not an "
           "afterthought discovered through customer complaints."),
 "problem": ("Bundled subscriptions (streaming, cloud storage, device insurance) must stay perfectly "
             "synchronized between entitlement state and billing state across upgrades, downgrades, and partner "
             "integrations of wildly varying reliability. Drift between what a customer is billed for and what "
             "they actually have access to erodes trust silently until a complaint surfaces it."),
 "diagram_note": ("The Entitlement Change Confidence Gate separates routine plan changes (auto-execute) from "
                   "partner-API-dependent changes needing billing ops review, given how unreliable partner APIs "
                   "proved to be in the Quick view's own build history."),
 "spec": {
   "l1": [_int("int1", "Entitlement Management System"), _int("int2", "Billing State Feed"),
          _ext("ext1", "Partner Platform APIs")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Entitlement Knowledge Graph")],
   "l3_orch": _orch("orch", "Subscription Lifecycle Orchestrator"),
   "l3_workers": [_w("w1", "Internal Product Entitlement Manager Agent"), _w("w2", "Third-Party Partner Entitlement Manager Agent"),
                  _w("w3", "Plan Change Entitlement Agent")],
   "l4": [_l4("g1", "Proration Rule Engine"), _l4("g2", "Grandfathering Policy Guardrail"), _l4("g3", "Partner SLA Rule Engine")],
   "gate": _gate("gate", "Entitlement Change Confidence Gate"),
   "l5": [_l5_human("human", "Billing Ops Review"), _l5_auto("a1", "Entitlement System Update"),
          _l5_plain("a2", "Partner Provisioning Call"), _l5_hold("hold", "Entitlement Drift Hold Queue")],
   "l6": [_l6("m1", "Entitlement Drift Monitor"), _l6("m2", "Partner API Reliability Watchdog"), _l6("m3", "Reconciliation Auditor")],
   "l7": [_l7("lead1", "Entitlement Accuracy Dashboard"), _l7("lead2", "Partner Settlement Scorecard"), _l7("lead3", "Drift-by-Partner View")],
   "l8": [_l8("s1", "Entitlement Accuracy Tracker"), _l8("s2", "Reconciliation Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("subscription entitlements", "Internal Product Entitlement Manager Agent", "Subscription Lifecycle Orchestrator", 2,
                         "Entitlement Change Confidence Gate", "Entitlement System Update", "Billing Ops Review"),
},

{
 "id": 10, "quick_slug": "number-portability-orchestration",
 "quick_title": "Number Portability Orchestration",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Number Portability Execution Decisioning",
 "intro": ("This deep-8 view keeps the Quick view's deliberately rigid, rules-driven sequencing — the "
           "regulatory and service-continuity stakes are too high for adaptive flexibility — while adding the "
           "governance and observability layers that were previously implicit in the pipeline's discipline."),
 "problem": ("Porting a number between operators involves a strict, regulator-defined sequence with tight SLA "
             "windows. A mis-sequenced or rolled-back port disrupts real customer service; the Quick view's own "
             "retrospective flags rollback handling as originally under-invested relative to the forward path."),
 "diagram_note": ("The Port Execution Readiness Gate is deliberately conservative — this is the one deep-8 view "
                   "where the hold path is not a fallback but a first-class, equally-engineered option, matching "
                   "the Quick view's explicit design principle that rollback deserves the same rigor as the "
                   "forward path."),
 "spec": {
   "l1": [_ext("ext1", "Number Portability Registry (NPAC-style)"), _int("int1", "Switch/HLR-HSS State"),
          _int("int2", "Regulatory Rules Archive")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Porting Rules Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Port Request Validation Agent"), _w("w2", "Donor Operator Confirmation Agent"),
                  _w("w3", "NPDB Update Agent"), _w("w4", "Network Cutover Sequencing Agent")],
   "l4": [_l4("g1", "Regulatory Eligibility Rule Engine"), _l4("g2", "SLA-Deadline Guardrail"), _l4("g3", "Rollback Authorization Policy")],
   "gate": _gate("gate", "Port Execution Readiness Gate"),
   "l5": [_l5_human("human", "Porting Ops Review"), _l5_auto("a1", "NPDB/Central Registry Update"),
          _l5_plain("a2", "Network Switch Cutover Execution"), _l5_hold("hold", "Rollback Hold Queue")],
   "l6": [_l6("m1", "SLA-Deadline Monitor"), _l6("m2", "Cutover Success Watchdog"), _l6("m3", "Rollback Auditor")],
   "l7": [_l7("lead1", "Port Cycle-Time Dashboard"), _l7("lead2", "SLA Compliance Scorecard"), _l7("lead3", "Rollback Rate View")],
   "l8": [_l8("s1", "Port Success Accuracy Tracker"), _l8("s2", "Timing-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("number portability", "Port Request Validation Agent", None, 3,
                         "Port Execution Readiness Gate", "NPDB/Central Registry Update", "Porting Ops Review"),
},

{
 "id": 11, "quick_slug": "wholesale-partner-interconnect-onboarding",
 "quick_title": "Wholesale/Partner Interconnect Onboarding",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Partner Interconnect Onboarding Decisioning",
 "intro": ("This deep-8 view turns partner onboarding into a governed go-live decision with a single readiness "
           "gate — instead of a project-managed checklist, commercial and security sign-off are explicit, "
           "auditable gate conditions."),
 "problem": ("Onboarding a wholesale partner requires coordinating commercial, technical, billing, and security "
             "workstreams. The Quick view's own retrospective notes several onboardings passed every individual "
             "workstream check but failed on first real traffic — a governance gap this deep-8 view closes with "
             "an explicit test-traffic validation step before go-live."),
 "diagram_note": ("The Go-Live Readiness Gate requires both commercial and security sign-off before any "
                   "interconnect provisioning executes — the two approval paths from the Quick view's human "
                   "gate are now explicit, separately-tracked conditions."),
 "spec": {
   "l1": [_int("int1", "Signed Interconnect Agreement"), _int("int2", "Partner Technical Spec Docs"),
          _ext("ext1", "Security Questionnaire Responses")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Interconnect Knowledge Graph")],
   "l3_orch": _orch("orch", "Partner Onboarding Orchestrator"),
   "l3_workers": [_w("w1", "Contract Terms Configuration Agent"), _w("w2", "Technical Interconnection Setup Agent"),
                  _w("w3", "Billing/Settlement Configuration Agent"), _w("w4", "Security & Compliance Verification Agent")],
   "l4": [_l4("g1", "Rate-Card Approval Policy"), _l4("g2", "Security Baseline Guardrail"), _l4("g3", "Commercial Sign-off Rule Engine")],
   "gate": _gate("gate", "Go-Live Readiness Gate"),
   "l5": [_l5_human("human", "Commercial & Security Sign-off"), _l5_auto("a1", "Interconnect Provisioning Execution"),
          _l5_plain("a2", "Settlement System Configuration"), _l5_hold("hold", "Onboarding Hold Queue")],
   "l6": [_l6("m1", "Test-Traffic Monitor"), _l6("m2", "Configuration Drift Watchdog"), _l6("m3", "Go-Live Auditor")],
   "l7": [_l7("lead1", "Onboarding Cycle-Time Dashboard"), _l7("lead2", "Partner Revenue Scorecard"), _l7("lead3", "Security Posture View")],
   "l8": [_l8("s1", "Onboarding Accuracy Tracker"), _l8("s2", "Checklist Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("partner onboarding", "Contract Terms Configuration Agent", "Partner Onboarding Orchestrator", 3,
                         "Go-Live Readiness Gate", "Interconnect Provisioning Execution", "Commercial & Security Sign-off"),
},

{
 "id": 12, "quick_slug": "service-catalog-network-activation-mapping",
 "quick_title": "Service Catalog-to-Network Activation Mapping (TMF Open APIs)",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Catalog-to-Network Mapping Decisioning",
 "intro": ("This deep-8 view elevates API contract drift detection — the Quick view's highest-value addition "
           "found in hindsight — to a first-class, always-on L6 component rather than something built after "
           "production mapping failures had already occurred."),
 "problem": ("Translating a commercial catalog entry into the correct OSS API call sequence requires deep, "
             "often tribal-knowledge mapping logic that breaks whenever the catalog or an underlying vendor API "
             "changes. Undetected vendor API changes were, by the Quick view's own account, the dominant cause "
             "of production mapping failures."),
 "diagram_note": ("The Mapping Confidence & Drift Gate routes stable, previously-validated mappings to "
                   "auto-execution, and anything touching a recently-changed API contract to engineer review "
                   "before it can reach production."),
 "spec": {
   "l1": [_int("int1", "Product Catalog (TMF620)"), _int("int2", "OSS API Contract Specs"),
          _int("int3", "Network Domain Inventory")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Catalog-to-Network Mapping Graph")],
   "l3_orch": _orch("orch", "Catalog-to-Network Mapping Orchestrator"),
   "l3_workers": [_w("w1", "Access Network Domain Mapping Agent"), _w("w2", "Core Network Domain Mapping Agent"),
                  _w("w3", "Mapping Validation Agent")],
   "l4": [_l4("g1", "API Contract Compatibility Policy"), _l4("g2", "Engineer Review Guardrail"), _l4("g3", "Mapping Change Authorization Rules")],
   "gate": _gate("gate", "Mapping Confidence & Drift Gate"),
   "l5": [_l5_human("human", "Engineer Review"), _l5_auto("a1", "TMF641 Service Order Execution"),
          _l5_plain("a2", "Regression Test Suite Run"), _l5_hold("hold", "Mapping Change Hold Queue")],
   "l6": [_l6("m1", "API Contract Drift Monitor"), _l6("m2", "Mapping Success Watchdog"), _l6("m3", "Change Auditor")],
   "l7": [_l7("lead1", "Mapping Success-Rate Dashboard"), _l7("lead2", "Domain Coverage Scorecard"), _l7("lead3", "Drift Incident View")],
   "l8": [_l8("s1", "Mapping Accuracy Tracker"), _l8("s2", "Mapping-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("catalog-to-network mapping", "Access Network Domain Mapping Agent", "Catalog-to-Network Mapping Orchestrator", 2,
                         "Mapping Confidence & Drift Gate", "TMF641 Service Order Execution", "Engineer Review"),
},

{
 "id": 13, "quick_slug": "trouble-ticket-cross-domain-assurance",
 "quick_title": "Trouble Ticket Management & Cross-Domain Assurance (OSS)",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Cross-Domain Trouble Ticket Decisioning",
 "intro": ("This deep-8 view makes explicit customer consent for any device-affecting auto-resolution — the "
           "hard lesson from the Quick view's early remote-reboot-during-a-call incident is now a permanent, "
           "non-bypassable L4 policy."),
 "problem": ("Trouble tickets often bounce between teams before landing correctly, since cross-domain diagnosis "
             "(access, transport, core, or CPE) needs to happen before the right team can even start fixing it. "
             "Auto-resolution without explicit customer consent risks disrupting active service, as the Quick "
             "view's own early version discovered."),
 "diagram_note": ("The Diagnosis Confidence Gate separates auto-resolvable symptoms from ambiguous ones needing "
                   "a specialist; any auto-resolution action that touches customer equipment requires the "
                   "explicit consent flag set in L4 before L5 can execute it."),
 "spec": {
   "l1": [_int("int1", "Customer-Reported Symptom Data"), _int("int2", "Real-Time Alarm/PM Data"),
          _int("int3", "Historical Ticket Resolution Archive")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Symptom-to-Domain Knowledge Graph")],
   "l3_orch": _orch("orch", "Trouble Ticket Triage Orchestrator"),
   "l3_workers": [_w("w1", "Access Domain Diagnostic Agent"), _w("w2", "Transport Domain Diagnostic Agent"),
                  _w("w3", "Core Domain Diagnostic Agent"), _w("w4", "CPE Diagnostic Agent")],
   "l4": [_l4("g1", "Auto-Resolution Consent Policy"), _l4("g2", "Diagnostic Confidence Guardrail"), _l4("g3", "Correct-Team Routing Rules")],
   "gate": _gate("gate", "Diagnosis Confidence Gate"),
   "l5": [_l5_human("human", "Order Ops Specialist"), _l5_auto("a1", "Correct Team Ticket Assignment"),
          _l5_plain("a2", "Remote CPE Reboot (with consent)"), _l5_hold("hold", "Novel-Symptom Hold Queue")],
   "l6": [_l6("m1", "First-Time-Right Monitor"), _l6("m2", "Diagnostic Accuracy Watchdog"), _l6("m3", "Resolution Auditor")],
   "l7": [_l7("lead1", "MTTR Dashboard"), _l7("lead2", "First-Time-Right Scorecard"), _l7("lead3", "Domain Accuracy View")],
   "l8": [_l8("s1", "Diagnosis Accuracy Tracker"), _l8("s2", "Symptom-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("trouble ticket triage", "Access Domain Diagnostic Agent", "Trouble Ticket Triage Orchestrator", 3,
                         "Diagnosis Confidence Gate", "Correct Team Ticket Assignment", "Order Ops Specialist"),
},

{
 "id": 14, "quick_slug": "digital-bss-oss-migration-reconciliation",
 "quick_title": "Digital BSS/OSS Migration & Data Reconciliation",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "BSS/OSS Migration Cutover Decisioning",
 "intro": ("This deep-8 view makes deep-diff sampling — the Quick view's own highest-value validation "
           "technique, discovered mid-program — the default validation method from day one, not an optional "
           "extra check added after count-based validation missed systematic errors."),
 "problem": ("Migrating to a modern BSS/OSS platform requires moving millions of records without service "
             "disruption. Aggregate-count validation alone misses systematic errors that a sampled deep-diff "
             "catches — a lesson the Quick view learned only after shipping several waves on count-only checks."),
 "diagram_note": ("The Cutover Readiness Gate requires deep-diff-sampled validation, not just count-matching, "
                   "before any wave can proceed to production load — with an equally-engineered rollback path "
                   "for any wave that fails."),
 "spec": {
   "l1": [_int("int1", "Legacy BSS/OSS Database"), _int("int2", "New Platform Schema Spec"), _int("int3", "Migration Wave Plan")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Legacy-to-New Mapping Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Legacy Data Extraction & Profiling Agent"), _w("w2", "Transformation Mapping Agent"),
                  _w("w3", "Migration Validation Agent"), _w("w4", "Discrepancy Investigation Agent")],
   "l4": [_l4("g1", "Data-Quality Threshold Policy"), _l4("g2", "Rollback Authorization Guardrail"), _l4("g3", "Cutover Sign-off Rules")],
   "gate": _gate("gate", "Cutover Readiness Gate"),
   "l5": [_l5_human("human", "Program Management Office Review"), _l5_auto("a1", "New Platform Data Load"),
          _l5_plain("a2", "Migration Discrepancy Report"), _l5_hold("hold", "Wave Rollback Hold")],
   "l6": [_l6("m1", "Wave Health Monitor"), _l6("m2", "Deep-Diff Sample Watchdog"), _l6("m3", "Rollback Auditor")],
   "l7": [_l7("lead1", "Migration Progress Dashboard"), _l7("lead2", "Data-Quality Scorecard"), _l7("lead3", "Wave-by-Wave View")],
   "l8": [_l8("s1", "Migration Accuracy Tracker"), _l8("s2", "Mapping-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("BSS/OSS migration", "Legacy Data Extraction & Profiling Agent", None, 3,
                         "Cutover Readiness Gate", "New Platform Data Load", "Program Management Office Review"),
},

{
 "id": 15, "quick_slug": "promotions-campaign-configuration-engine",
 "quick_title": "Promotions & Campaign Configuration Engine",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Promotion Launch Risk Decisioning",
 "intro": ("This deep-8 view makes post-launch monitoring mandatory, not optional — the Quick view's own "
           "retrospective found real gaming patterns only emerged after launch, no matter how thorough the "
           "pre-launch simulation."),
 "problem": ("Poorly modeled promotions can be gamed or cannibalize existing revenue. Pre-launch Monte Carlo "
             "simulation catches most risks, but the Quick view's own experience shows some gaming patterns "
             "only surface in real redemption data — making post-launch monitoring a governance requirement, "
             "not a nice-to-have."),
 "diagram_note": ("The Promotion Launch Confidence Gate requires Finance sign-off for anything with material "
                   "margin exposure; L6's redemption-pattern monitor is mandatory for every launch, matching "
                   "the retrospective's finding that pre-launch simulation alone is never sufficient."),
 "spec": {
   "l1": [_int("int1", "Active Promotion Catalog"), _int("int2", "Historical Promotion Performance Data"),
          _int("int3", "Margin/Cost Model")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Promotion Interaction Knowledge Graph")],
   "l3_orch": _orch("orch", "Promotion Launch Arbiter Agent"),
   "l3_workers": [_w("w1", "Promotion Design Proposer Agent"), _w("w2", "Gaming & Cannibalization Critic Agent"),
                  _w("w3", "Promotion Interaction Agent")],
   "l4": [_l4("g1", "Margin-Impact Policy"), _l4("g2", "Gaming-Risk Guardrail"), _l4("g3", "Finance Sign-off Rule Engine")],
   "gate": _gate("gate", "Promotion Launch Confidence Gate"),
   "l5": [_l5_human("human", "Finance Sign-off"), _l5_auto("a1", "Product Catalog Promotion Publish"),
          _l5_plain("a2", "Marketing Campaign Launch"), _l5_hold("hold", "Launch Hold Queue")],
   "l6": [_l6("m1", "Redemption-Pattern Monitor"), _l6("m2", "Gaming-Behavior Watchdog"), _l6("m3", "Stacking Auditor")],
   "l7": [_l7("lead1", "Promotion ROI Dashboard"), _l7("lead2", "Margin Impact Scorecard"), _l7("lead3", "Adoption View")],
   "l8": [_l8("s1", "Promotion Outcome Accuracy Tracker"), _l8("s2", "Simulation Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("promotions", "Promotion Design Proposer Agent", "Promotion Launch Arbiter Agent", 2,
                         "Promotion Launch Confidence Gate", "Product Catalog Promotion Publish", "Finance Sign-off"),
},

{
 "id": 16, "quick_slug": "dunning-collections-automation",
 "quick_title": "Dunning & Prepaid/Postpaid Collections Automation",
 "quick_pattern_label": "Human-in-the-Loop Escalation Chain",
 "title": "Collections Risk & Hardship Decisioning",
 "intro": ("This deep-8 view keeps the Quick view's non-negotiable rule — the risk gate can never be "
           "overridden for automated suspension — as an explicit L4 policy rather than an implicit design "
           "choice, and adds household-level (not per-line) value assessment as a first-class guardrail."),
 "problem": ("Collections must run at scale while escalating hardship, dispute, or high-value cases to a "
             "human. The Quick view's own retrospective flags two near-misses: suspending a customer with an "
             "active billing dispute, and nearly suspending a high-value multi-line household over one small "
             "overdue line."),
 "diagram_note": ("The Hardship/Dispute/High-Value Risk Gate blocks automated restriction for any flagged case "
                   "by design — this gate has no override path, matching the Quick view's explicit requirement "
                   "that this be non-negotiable from launch."),
 "spec": {
   "l1": [_int("int1", "Billing Payment Status Feed"), _int("int2", "Customer Value (CLV) Data"),
          _int("int3", "Hardship Program Rules")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Collections Risk Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Payment Reminder Agent"), _w("w2", "Grace Period & Partial Payment Agent"),
                  _w("w3", "Service Restriction Agent")],
   "l4": [_l4("g1", "Contact-Frequency Compliance Policy (Reg F)"), _l4("g2", "Hardship-Indicator Guardrail"), _l4("g3", "Dispute-Hold Rule Engine")],
   "gate": _gate("gate", "Hardship/Dispute/High-Value Risk Gate"),
   "l5": [_l5_human("human", "Collections Specialist"), _l5_auto("a1", "Automated Reminder/Restriction Execution"),
          _l5_plain("a2", "Customer Continuity Adjustment"), _l5_hold("hold", "Hardship Program Enrollment Queue")],
   "l6": [_l6("m1", "Restriction/Complaint Monitor"), _l6("m2", "Contact-Frequency Watchdog"), _l6("m3", "Suspension Auditor")],
   "l7": [_l7("lead1", "Recovery-Rate Dashboard"), _l7("lead2", "Complaint-Rate Scorecard"), _l7("lead3", "Hardship Enrollment View")],
   "l8": [_l8("s1", "Risk-Gate Accuracy Tracker"), _l8("s2", "Escalation-Rule Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("collections", "Payment Reminder Agent", None, 2,
                         "Hardship/Dispute/High-Value Risk Gate", "Automated Reminder/Restriction Execution", "Collections Specialist"),
},

{
 "id": 17, "quick_slug": "api-gateway-tmf-governance",
 "quick_title": "API Gateway & TMF Open API Orchestration Governance",
 "quick_pattern_label": "Event-Driven Reactive Swarm",
 "title": "API Governance & Abuse Response Decisioning",
 "intro": ("This deep-8 view adds a conservative-by-default throttling guardrail after the Quick view's own "
           "near-miss — an early false positive throttled a legitimate high-volume partner during a peak "
           "traffic event."),
 "problem": ("As operators expose more Open APIs, misuse, quota abuse, and contract-breaking changes need "
             "real-time detection at scale. Automated throttling without conservative guardrails risks blocking "
             "legitimate high-volume partners at exactly the moment — peak traffic — when the cost of a false "
             "positive is highest."),
 "diagram_note": ("The Abuse/Drift Confidence Gate requires sustained abuse signal, not a single spike, before "
                   "auto-throttling — and routes anything ambiguous to the platform team rather than risking "
                   "another peak-traffic false positive."),
 "spec": {
   "l1": [_int("int1", "API Gateway Traffic Logs"), _int("int2", "Published OpenAPI/TMF Specs"),
          _ext("ext1", "Consumer/Partner Registry")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "API Contract Knowledge Graph")],
   "l3_orch": _orch("orch", "API Governance Orchestrator"),
   "l3_workers": [_w("w1", "Rate Limit/Quota Abuse Agent"), _w("w2", "Contract Compliance Agent"),
                  _w("w3", "Latency/Error-Rate Degradation Agent"), _w("w4", "Deprecated Version Usage Agent")],
   "l4": [_l4("g1", "Throttling Authorization Policy"), _l4("g2", "False-Positive Guardrail"), _l4("g3", "Consumer Communication Rules")],
   "gate": _gate("gate", "Abuse/Drift Confidence Gate"),
   "l5": [_l5_human("human", "Platform Team Review"), _l5_auto("a1", "Automated Throttling/Block"),
          _l5_plain("a2", "Consumer Portal Notification"), _l5_hold("hold", "Investigation Hold Queue")],
   "l6": [_l6("m1", "API Health Monitor"), _l6("m2", "Contract Drift Watchdog"), _l6("m3", "Throttling Auditor")],
   "l7": [_l7("lead1", "API Health Dashboard"), _l7("lead2", "Consumer Compliance Scorecard"), _l7("lead3", "Deprecation Migration View")],
   "l8": [_l8("s1", "Governance Accuracy Tracker"), _l8("s2", "Threshold Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("API governance", "Rate Limit/Quota Abuse Agent", "API Governance Orchestrator", 3,
                         "Abuse/Drift Confidence Gate", "Automated Throttling/Block", "Platform Team Review"),
},

{
 "id": 18, "quick_slug": "credit-limit-fraud-threshold-management",
 "quick_title": "Credit Limit & Fraud Threshold Management (BSS)",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Credit & Fraud Threshold Decisioning",
 "intro": ("This deep-8 view tracks customer friction (unnecessary restrictions) as a co-equal metric to "
           "bad-debt prevention from day one — the Quick view's own retrospective found it over-indexed on "
           "risk-prevention in v1, generating avoidable complaints from legitimate roaming customers."),
 "problem": ("Dynamic credit limits and fraud thresholds must balance bad-debt exposure against not restricting "
             "legitimate high-usage customers. Static, per-line thresholds misread family-plan usage sharing as "
             "anomalous, and no proactive warning before restriction meant customers were caught off guard."),
 "diagram_note": ("The Threshold Adjustment Confidence Gate always routes through the proactive spend-cap "
                   "notification before any restriction — a hard requirement carried over from the Quick view's "
                   "finding that a warning-then-restrict flow generated far fewer complaints than a hard cutoff."),
 "spec": {
   "l1": [_int("int1", "Customer Payment/Credit History"), _int("int2", "Real-Time Usage Data"),
          _int("int3", "Historical Bad-Debt Outcomes")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Usage-Pattern Knowledge Graph")],
   "l3_orch": _orch("orch", "Threshold Policy Arbiter Agent"),
   "l3_workers": [_w("w1", "Threshold Tightening Proposer Agent"), _w("w2", "Legitimate Usage Pattern Critic Agent"),
                  _w("w3", "Bad-Debt Outcome Feedback Agent")],
   "l4": [_l4("g1", "Friction-Cost Policy"), _l4("g2", "Household-Usage Guardrail"), _l4("g3", "Notification Rule Engine")],
   "gate": _gate("gate", "Threshold Adjustment Confidence Gate"),
   "l5": [_l5_human("human", "Risk Ops Review"), _l5_auto("a1", "Dynamic Credit Limit Adjustment"),
          _l5_plain("a2", "Real-Time Spend Cap Alert"), _l5_hold("hold", "Threshold Hold Queue")],
   "l6": [_l6("m1", "Bad-Debt Monitor"), _l6("m2", "Friction-Rate Watchdog"), _l6("m3", "Adjustment Auditor")],
   "l7": [_l7("lead1", "Bad-Debt-Prevented Dashboard"), _l7("lead2", "Customer-Friction Scorecard"), _l7("lead3", "Threshold-by-Segment View")],
   "l8": [_l8("s1", "Threshold Accuracy Tracker"), _l8("s2", "Risk-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("credit/fraud thresholds", "Threshold Tightening Proposer Agent", "Threshold Policy Arbiter Agent", 2,
                         "Threshold Adjustment Confidence Gate", "Dynamic Credit Limit Adjustment", "Risk Ops Review"),
},

{
 "id": 19, "quick_slug": "partner-revenue-share-settlement",
 "quick_title": "Partner Revenue Share & Settlement Automation",
 "quick_pattern_label": "Market-Based / Auction Agents",
 "title": "Partner Settlement Transparency Decisioning",
 "intro": ("This deep-8 view makes the partner-facing calculation transparency portal — the Quick view's own "
           "single highest-leverage addition — an explicit L5 component from the start, not a later retrofit "
           "after dispute volume proved the point."),
 "problem": ("Revenue-share settlement across partners involves complex, often-disputed calculations. The "
             "Quick view found that dispute volume dropped more from calculation transparency than from any "
             "improvement in calculation accuracy itself — most disputes turned out to be cycle-boundary timing "
             "issues, not real disagreements."),
 "diagram_note": ("The Settlement Confidence & Dispute Gate auto-clears settlements within each partner's "
                   "contract-specific tolerance; anything outside it routes to Finance mediation with the same "
                   "transparent calculation trail the partner already sees in their portal."),
 "spec": {
   "l1": [_int("int1", "Usage/Revenue Attribution Data"), _int("int2", "Partner Contract Terms"),
          _ext("ext1", "Partner Settlement Statements")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Partner Contract Knowledge Graph")],
   "l3_orch": _orch("orch", "Revenue Share Clearing Agent"),
   "l3_workers": [_w("w1", "Partner Settlement Claim Agent"), _w("w2", "Internal Revenue Attribution Agent"),
                  _w("w3", "Contract Terms Interpretation Agent")],
   "l4": [_l4("g1", "Dispute-Tolerance Policy"), _l4("g2", "Calculation Transparency Guardrail"), _l4("g3", "Settlement Authorization Rules")],
   "gate": _gate("gate", "Settlement Confidence & Dispute Gate"),
   "l5": [_l5_human("human", "Finance Mediation Review"), _l5_auto("a1", "Automated Partner Payment"),
          _l5_plain("a2", "Settlement Statement Generation"), _l5_hold("hold", "Dispute Case Hold Queue")],
   "l6": [_l6("m1", "Settlement Accuracy Monitor"), _l6("m2", "Cycle-Boundary Watchdog"), _l6("m3", "Payment Auditor")],
   "l7": [_l7("lead1", "Settlement Cycle-Time Dashboard"), _l7("lead2", "Dispute-Rate Scorecard"), _l7("lead3", "Partner Revenue View")],
   "l8": [_l8("s1", "Settlement Accuracy Tracker"), _l8("s2", "Contract-Parsing Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("partner settlement", "Partner Settlement Claim Agent", "Revenue Share Clearing Agent", 2,
                         "Settlement Confidence & Dispute Gate", "Automated Partner Payment", "Finance Mediation Review"),
},

{
 "id": 20, "quick_slug": "legacy-system-decommissioning-archival",
 "quick_title": "Legacy System Decommissioning & Data Archival",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Legacy System Decommissioning Decisioning",
 "intro": ("This deep-8 view extends the zero-traffic validation window the Quick view's retrospective wished "
           "it had built longer — an early decommissioning shut down a system that still received a rare "
           "monthly batch job, missed by a shorter initial window."),
 "problem": ("Decommissioning a legacy BSS/OSS system requires exhaustively mapping every remaining dependency, "
             "which documentation and interviews consistently miss. Empirical, traffic-based discovery finds "
             "integrations no other method surfaces — but only if the validation window is long enough to catch "
             "infrequent (monthly, quarterly) batch dependencies."),
 "diagram_note": ("The Shutdown Readiness Gate requires a validated zero-traffic window before any shutdown "
                   "executes, and the Program Sponsor Approval branch is mandatory regardless of confidence "
                   "level — this decision is irreversible enough that it never fully auto-executes."),
 "spec": {
   "l1": [_int("int1", "Network Traffic to Legacy System"), _int("int2", "Batch Job Scheduler Logs"),
          _int("int3", "Regulatory Retention Requirements")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "System Dependency Knowledge Graph")],
   "l3_orch": _orch("orch", "Decommissioning Orchestrator Agent"),
   "l3_workers": [_w("w1", "Dependency Discovery Agent"), _w("w2", "Data Archival & Retention Compliance Agent"),
                  _w("w3", "Downstream Consumer Notification Agent"), _w("w4", "Cutover Validation Agent")],
   "l4": [_l4("g1", "Retention-Period Compliance Policy"), _l4("g2", "Zero-Traffic Validation Guardrail"), _l4("g3", "Shutdown Authorization Rules")],
   "gate": _gate("gate", "Shutdown Readiness Gate"),
   "l5": [_l5_human("human", "Program Sponsor Approval"), _l5_auto("a1", "Final Data Archive Execution"),
          _l5_plain("a2", "Stakeholder Notification"), _l5_hold("hold", "Shutdown Hold Queue")],
   "l6": [_l6("m1", "Residual-Traffic Monitor"), _l6("m2", "Dependency-Discovery Watchdog"), _l6("m3", "Archival Auditor")],
   "l7": [_l7("lead1", "Decommissioning Progress Dashboard"), _l7("lead2", "Cost-Avoidance Scorecard"), _l7("lead3", "Compliance View")],
   "l8": [_l8("s1", "Dependency-Discovery Accuracy Tracker"), _l8("s2", "Discovery-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("legacy decommissioning", "Dependency Discovery Agent", "Decommissioning Orchestrator Agent", 3,
                         "Shutdown Readiness Gate", "Final Data Archive Execution", "Program Sponsor Approval"),
},

]
