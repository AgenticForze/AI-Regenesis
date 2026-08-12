# -*- coding: utf-8 -*-
"""
Deep 8-Layer specs for the 20 Financial Services use cases. Same spec-driven approach as
bssoss_deep8_data.py — see scripts/deep8_engine.py for the engine these specs feed.
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


FINANCE_SPECS = [

{
 "id": 1, "quick_slug": "aml-transaction-monitoring-sar",
 "quick_title": "AML Transaction Monitoring & SAR Filing",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "AML Case Investigation & SAR Filing Decisioning",
 "intro": ("This deep-8 view keeps the Quick view's strict evidence-citation requirement — every SAR "
           "narrative sentence must cite its source record — as an explicit, non-bypassable L4 policy rather "
           "than a prompting convention, and adds executive visibility into how much investigator time the "
           "system is actually saving."),
 "problem": ("90-95% of AML alerts are false positives, yet each still requires investigator review to avoid "
             "regulatory penalty for a missed suspicious activity. The Quick view's own early prototype "
             "generated a plausible-sounding but unverifiable narrative claim — a hard lesson on where "
             "generative reasoning cannot be trusted without a citation guardrail."),
 "diagram_note": ("The SAR Filing Confidence Gate never bypasses the licensed investigator for an actual "
                   "filing decision — only evidence assembly and narrative drafting are automated. L4's "
                   "citation-grounding guardrail blocks any narrative sentence that isn't traceable to a "
                   "specific source record."),
 "spec": {
   "l1": [_int("int1", "Core Banking Transactions"), _int("int2", "KYC/CDD Records"),
          _ext("ext1", "Sanctions/PEP Lists"), _ext("ext2", "Adverse Media Feeds")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"),
          _l2("kg", "AML Relationship Knowledge Graph", "Neo4j graph database")],
   "l3_orch": _orch("orch", "AML Case Orchestrator Agent"),
   "l3_workers": [_w("w1", "Transaction Pattern Analysis Agent"), _w("w2", "Customer/Entity Risk Profile Agent"),
                  _w("w3", "Adverse Media & Sanctions Screening Agent"), _w("w4", "Network/Relationship Graph Agent")],
   "l4": [_l4("g1", "SAR Narrative Evidence-Citation Policy"), _l4("g2", "Regulatory Filing Guardrail"),
          _l4("g3", "Investigator Sign-off Rule Engine")],
   "gate": _gate("gate", "SAR Filing Confidence Gate"),
   "l5": [_l5_human("human", "Licensed AML Investigator Review"), _l5_auto("a1", "Case Management System Update"),
          _l5_plain("a2", "Regulatory Filing (goAML/FinCEN)"), _l5_hold("hold", "Low-Confidence Hold Queue")],
   "l6": [_l6("m1", "Narrative Citation Monitor"), _l6("m2", "False-Negative Watchdog"), _l6("m3", "Filing Auditor")],
   "l7": [_l7("lead1", "SAR Filing Dashboard"), _l7("lead2", "Investigation Time-Saved Scorecard"), _l7("lead3", "Mule-Network Detection View")],
   "l8": [_l8("s1", "SAR Quality Accuracy Tracker"), _l8("s2", "Ranking-Weight Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("AML investigation", "Transaction Pattern Analysis Agent", "AML Case Orchestrator Agent", 3,
                         "SAR Filing Confidence Gate", "Case Management System Update", "Licensed AML Investigator Review"),
},

{
 "id": 2, "quick_slug": "credit-underwriting-loan-origination",
 "quick_title": "Credit Underwriting & Loan Origination",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Credit Underwriting Decisioning",
 "intro": ("This deep-8 view makes fair-lending disparate-impact testing a co-equal L4 gate from the start — "
           "the Quick view's own retrospective flagged this as a late add-on that should have been a "
           "first-class check on every decision path, not a final checkbox."),
 "problem": ("Underwriting requires synthesizing financial statements, credit bureau data, cash-flow analysis, "
             "and policy compliance under fair-lending regulation. The Quick view found cash-flow analysis "
             "from open banking data dramatically improved thin-file applicant accuracy — but only after "
             "initially over-relying on bureau-only scoring."),
 "diagram_note": ("The Underwriting Decision Confidence Gate routes to Underwriter Review whenever fair-lending "
                   "or policy-exception guardrails flag a concern, keeping the interpretable scorecard model — "
                   "not an LLM — as the actual decision boundary, per the Quick view's own regulatory "
                   "explainability requirement."),
 "spec": {
   "l1": [_int("int1", "Bank Transaction Data (Open Banking)"), _int("int2", "Loan Origination System DB"),
          _ext("ext1", "Credit Bureau Feed")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Applicant Financial Knowledge Graph")],
   "l3_orch": _orch("orch", "Underwriting Orchestrator Agent"),
   "l3_workers": [_w("w1", "Financial Analysis Manager Agent"), _w("w2", "Risk & Compliance Manager Agent"),
                  _w("w3", "Cash-Flow Analysis Agent")],
   "l4": [_l4("g1", "Fair-Lending Disparate-Impact Policy"), _l4("g2", "Policy-Exception Guardrail"), _l4("g3", "Adverse-Action Rule Engine")],
   "gate": _gate("gate", "Underwriting Decision Confidence Gate"),
   "l5": [_l5_human("human", "Underwriter Review"), _l5_auto("a1", "Loan Origination System Decision"),
          _l5_plain("a2", "Adverse Action Notice Generation"), _l5_hold("hold", "Policy Exception Hold Queue")],
   "l6": [_l6("m1", "Fair-Lending Bias Monitor"), _l6("m2", "Approval-Rate Watchdog"), _l6("m3", "Decision Auditor")],
   "l7": [_l7("lead1", "Approval Cycle-Time Dashboard"), _l7("lead2", "Fair-Lending Compliance Scorecard"), _l7("lead3", "Portfolio Risk View")],
   "l8": [_l8("s1", "Underwriting Accuracy Tracker"), _l8("s2", "Scorecard Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("credit underwriting", "Cash-Flow Analysis Agent", "Underwriting Orchestrator Agent", 2,
                         "Underwriting Decision Confidence Gate", "Loan Origination System Decision", "Underwriter Review"),
},

{
 "id": 3, "quick_slug": "algo-trading-strategy-orchestration",
 "quick_title": "Algorithmic Trading Strategy Orchestration",
 "quick_pattern_label": "Market-Based / Auction Agents",
 "title": "Trading Capital Allocation Decisioning",
 "intro": ("This deep-8 view preserves the Quick view's most important design decision — LLM reasoning stays "
           "entirely out of the latency-critical bid/execution loop, used only for offline reporting — and "
           "gives the independent Risk Guardrail absolute veto power from the start, not as advisory-only."),
 "problem": ("Multiple alpha strategies compete for the same risk budget and execution capacity. An early "
             "version routed borderline allocation cases through an LLM and blew the latency SLA; a separate "
             "near-miss saw aggregate strategy exposure briefly exceed firm limits when the risk guardrail was "
             "only advisory rather than a hard veto."),
 "diagram_note": ("The Capital Allocation Confidence Gate governs allocation *decisions*, not live order "
                   "execution — L4's VaR/position-limit policy has absolute veto power over any allocation "
                   "regardless of what the market-based clearing mechanism decided, matching the Quick view's "
                   "hard-learned lesson."),
 "spec": {
   "l1": [_int("int1", "Market Data Feed"), _int("int2", "Position/Portfolio State"), _int("int3", "Risk Limit Configuration")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (offline reporting only)"), _l2("kg", "Strategy Performance Knowledge Graph")],
   "l3_orch": _orch("orch", "Portfolio Risk-Budget Clearing Agent"),
   "l3_workers": [_w("w1", "Momentum Strategy Agent"), _w("w2", "Mean-Reversion Strategy Agent"), _w("w3", "Statistical Arbitrage Strategy Agent")],
   "l4": [_l4("g1", "VaR/Position-Limit Policy (hard veto)"), _l4("g2", "Regime-Detection Guardrail"), _l4("g3", "Compliance Restricted-List Rules")],
   "gate": _gate("gate", "Capital Allocation Confidence Gate"),
   "l5": [_l5_human("human", "Risk Manager Review"), _l5_auto("a1", "Order Management System Submission"),
          _l5_plain("a2", "P&L Attribution Report"), _l5_hold("hold", "Allocation Hold Queue")],
   "l6": [_l6("m1", "Risk Guardrail Monitor"), _l6("m2", "Latency Watchdog"), _l6("m3", "Execution Auditor")],
   "l7": [_l7("lead1", "Firm-Wide P&L Dashboard"), _l7("lead2", "Risk-Budget Utilization Scorecard"), _l7("lead3", "Strategy Performance View")],
   "l8": [_l8("s1", "Allocation Accuracy Tracker"), _l8("s2", "Backtest Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("algorithmic trading", "Momentum Strategy Agent", "Portfolio Risk-Budget Clearing Agent", 2,
                         "Capital Allocation Confidence Gate", "Order Management System Submission", "Risk Manager Review"),
},

{
 "id": 4, "quick_slug": "card-not-present-fraud-detection",
 "quick_title": "Fraud Detection - Card-Not-Present Transactions",
 "quick_pattern_label": "Event-Driven Reactive Swarm",
 "title": "Card-Not-Present Authorization Decisioning",
 "intro": ("This deep-8 view keeps the Quick view's core discipline — the hot authorization path never calls "
           "an LLM, full stop — and tracks declined-legitimate-transaction cost as a co-equal metric to "
           "fraud caught, per the Quick view's own retrospective."),
 "problem": ("Card-not-present fraud decisions must resolve in under 100ms. An early experiment routing "
             "borderline cases through an LLM blew the latency SLA; separately, the system initially "
             "over-indexed on fraud recall without tracking the business cost of declining legitimate "
             "transactions."),
 "diagram_note": ("The Authorization Confidence Gate operates entirely within the real-time scoring path — "
                   "L2's LLM Reasoning Core is explicitly offline-only, used for post-decision case "
                   "investigation, never in the authorization hot path itself."),
 "spec": {
   "l1": [_int("int1", "Real-Time Authorization Stream"), _int("int2", "Feature Store (behavioral baselines)"),
          _ext("ext1", "Card Network Fraud Signals")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (offline case investigation only)"), _l2("kg", "Fraud Pattern Knowledge Graph")],
   "l3_orch": _orch("orch", "Real-Time Scoring Aggregator"),
   "l3_workers": [_w("w1", "Device Fingerprint Agent"), _w("w2", "Velocity/Behavioral Agent"),
                  _w("w3", "Merchant Risk Agent"), _w("w4", "Geolocation Consistency Agent")],
   "l4": [_l4("g1", "Decline-Rate Business-Impact Policy"), _l4("g2", "False-Positive Guardrail"), _l4("g3", "3DS Step-Up Rule Engine")],
   "gate": _gate("gate", "Authorization Confidence Gate"),
   "l5": [_l5_human("human", "Fraud Case Investigator"), _l5_auto("a1", "Approve/Decline Authorization Response"),
          _l5_plain("a2", "3DS Challenge Trigger"), _l5_hold("hold", "Fraud Case Creation Queue")],
   "l6": [_l6("m1", "False-Positive/Negative Monitor"), _l6("m2", "Decline-Rate Watchdog"), _l6("m3", "Scoring Auditor")],
   "l7": [_l7("lead1", "Fraud-Caught Dashboard"), _l7("lead2", "Decline-Rate Business-Impact Scorecard"), _l7("lead3", "Merchant Risk View")],
   "l8": [_l8("s1", "Scoring Accuracy Tracker"), _l8("s2", "Aggregator-Weight Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("card-not-present fraud", "Device Fingerprint Agent", "Real-Time Scoring Aggregator", 3,
                         "Authorization Confidence Gate", "Approve/Decline Authorization Response", "Fraud Case Investigator"),
},

{
 "id": 5, "quick_slug": "customer-onboarding-kyc-finance",
 "quick_title": "Customer Onboarding & KYC (Retail & Business Banking)",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Customer Onboarding & KYC Risk Decisioning",
 "intro": ("This deep-8 view invests early in the beneficial-ownership resolution challenge the Quick view's "
           "own retrospective flagged as harder than expected — international registry resolution gets its "
           "own governed path rather than a single generic worker agent."),
 "problem": ("Digital account opening requires identity verification, sanctions screening, and risk rating in "
             "near real time. The Quick view found beneficial-ownership resolution across international "
             "registries far harder than any other check, and that a slow bureau API could stall the entire "
             "flow without explicit per-agent timeout handling."),
 "diagram_note": ("The Onboarding Risk Confidence Gate routes any CDD risk-matrix ambiguity to EDD Analyst "
                   "Review rather than auto-approving; L4's record-keeping rule engine ensures every decision "
                   "retains its full evidence trail for the 5-7 year regulatory retention window."),
 "spec": {
   "l1": [_int("int1", "Application Form Data"), _ext("ext1", "Government ID/Document Upload"),
          _ext("ext2", "Sanctions/PEP Databases")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Entity Resolution Knowledge Graph")],
   "l3_orch": _orch("orch", "KYC Onboarding Orchestrator Agent"),
   "l3_workers": [_w("w1", "Identity Document Verification Agent"), _w("w2", "Sanctions/PEP Screening Agent"),
                  _w("w3", "Customer Risk Rating Agent"), _w("w4", "Beneficial Ownership Agent")],
   "l4": [_l4("g1", "CDD Risk-Matrix Policy"), _l4("g2", "EDD Escalation Guardrail"), _l4("g3", "Record-Keeping Rule Engine")],
   "gate": _gate("gate", "Onboarding Risk Confidence Gate"),
   "l5": [_l5_human("human", "EDD Analyst Review"), _l5_auto("a1", "Account Opening System Approval"),
          _l5_plain("a2", "Welcome Kit/Rejection Notice"), _l5_hold("hold", "Enhanced Due Diligence Queue")],
   "l6": [_l6("m1", "Onboarding Abandonment Monitor"), _l6("m2", "Screening Latency Watchdog"), _l6("m3", "Decision Auditor")],
   "l7": [_l7("lead1", "Onboarding Conversion Dashboard"), _l7("lead2", "CDD Risk Scorecard"), _l7("lead3", "EDD Volume View")],
   "l8": [_l8("s1", "Risk-Rating Accuracy Tracker"), _l8("s2", "Threshold Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("customer onboarding", "Identity Document Verification Agent", "KYC Onboarding Orchestrator Agent", 3,
                         "Onboarding Risk Confidence Gate", "Account Opening System Approval", "EDD Analyst Review"),
},

{
 "id": 6, "quick_slug": "robo-advisory-portfolio-rebalancing",
 "quick_title": "Wealth Management: Robo-Advisory Portfolio Rebalancing",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Portfolio Rebalancing Decisioning",
 "intro": ("This deep-8 view builds in the household-level (not single-account) wash-sale checking the Quick "
           "view discovered it needed only after an early tax season — a costly gap for a governance layer "
           "to have missed."),
 "problem": ("Automated rebalancing must monitor allocations against tax considerations and fiduciary duty at "
             "scale. Tax-lot optimization that only considers one account misses wash-sale violations across "
             "a client's full household — exactly the gap the Quick view found the hard way."),
 "diagram_note": ("The Rebalance Confidence & Turnover Gate routes any large-turnover or unusual rebalance to "
                   "advisor review; L4's wash-sale compliance policy checks across the full household, not "
                   "just the triggering account, per the Quick view's retrospective."),
 "spec": {
   "l1": [_int("int1", "Custodian Position Feed"), _int("int2", "Client Risk Profile/IPS Data"), _int("int3", "Tax-Lot Records")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Household Tax Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Drift Detection Agent"), _w("w2", "Tax-Impact Analysis Agent"),
                  _w("w3", "Suitability/Risk-Profile Check Agent"), _w("w4", "Trade List Generation Agent")],
   "l4": [_l4("g1", "Wash-Sale Compliance Policy"), _l4("g2", "Turnover-Minimization Guardrail"), _l4("g3", "Fiduciary Documentation Rule Engine")],
   "gate": _gate("gate", "Rebalance Confidence & Turnover Gate"),
   "l5": [_l5_human("human", "Advisor Review (large rebalances)"), _l5_auto("a1", "Trade Execution via OMS"),
          _l5_plain("a2", "Client Notification of Rebalancing"), _l5_hold("hold", "Large-Turnover Hold Queue")],
   "l6": [_l6("m1", "Turnover Monitor"), _l6("m2", "Tax-Impact Watchdog"), _l6("m3", "Trade Auditor")],
   "l7": [_l7("lead1", "AUM Drift Dashboard"), _l7("lead2", "Tax-Alpha Scorecard"), _l7("lead3", "Rebalance Volume View")],
   "l8": [_l8("s1", "Rebalance Accuracy Tracker"), _l8("s2", "Optimization Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("portfolio rebalancing", "Drift Detection Agent", None, 3,
                         "Rebalance Confidence & Turnover Gate", "Trade Execution via OMS", "Advisor Review (large rebalances)"),
},

{
 "id": 7, "quick_slug": "regulatory-compliance-monitoring-reporting",
 "quick_title": "Regulatory Compliance Monitoring & Reg Reporting",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Regulatory Filing Readiness Decisioning",
 "intro": ("This deep-8 view treats regulatory-change monitoring as a first-class L6 component from day one — "
           "the Quick view found new rule versions silently broke report templates before this monitoring "
           "existed."),
 "problem": ("Banks must continuously monitor a patchwork of regulations and file numerous recurring reports. "
             "Data reconciliation exceptions, not report generation itself, were the dominant cause of filing "
             "delays in the Quick view's own experience — and undetected regulatory-text changes silently "
             "broke report templates before change monitoring was added."),
 "diagram_note": ("The Filing Readiness Confidence Gate keeps all financial calculations in deterministic, "
                   "auditable engines — the LLM layer is used only for regulatory-text interpretation and "
                   "change-impact summaries, never for the final numbers, matching the Quick view's explicit "
                   "design principle."),
 "spec": {
   "l1": [_int("int1", "General Ledger/Source Systems"), _int("int2", "Risk-Weighted Asset Data"), _ext("ext1", "Regulatory Rule Updates")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Regulatory Requirement Knowledge Graph")],
   "l3_orch": _orch("orch", "Regulatory Compliance Orchestrator"),
   "l3_workers": [_w("w1", "Capital/Liquidity Reporting Manager Agent"), _w("w2", "Trade/Transaction Reporting Manager Agent"),
                  _w("w3", "Data Reconciliation Agent")],
   "l4": [_l4("g1", "Filing-Deadline Policy"), _l4("g2", "Calculation-Accuracy Guardrail"), _l4("g3", "Regulatory Change-Impact Rule Engine")],
   "gate": _gate("gate", "Filing Readiness Confidence Gate"),
   "l5": [_l5_human("human", "Compliance Officer Review"), _l5_auto("a1", "Regulatory Report Submission"),
          _l5_plain("a2", "Internal Compliance Dashboard"), _l5_hold("hold", "Reconciliation Exception Hold")],
   "l6": [_l6("m1", "Filing Deadline Monitor"), _l6("m2", "Reconciliation Exception Watchdog"), _l6("m3", "Submission Auditor")],
   "l7": [_l7("lead1", "Regulatory Calendar Dashboard"), _l7("lead2", "Filing Accuracy Scorecard"), _l7("lead3", "Cross-Jurisdiction View")],
   "l8": [_l8("s1", "Filing Accuracy Tracker"), _l8("s2", "Rule-Change Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("regulatory reporting", "Data Reconciliation Agent", "Regulatory Compliance Orchestrator", 2,
                         "Filing Readiness Confidence Gate", "Regulatory Report Submission", "Compliance Officer Review"),
},

{
 "id": 8, "quick_slug": "insurance-claims-processing-fraud",
 "quick_title": "Insurance Claims Processing & Fraud Detection",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Insurance Claims Settlement Decisioning",
 "intro": ("This deep-8 view scales auto-settlement dollar caps down for newer, riskier claim types instead "
           "of using one global threshold — the Quick view's own retrospective found a single global cap "
           "overpaid a class of low-frequency, high-severity claims."),
 "problem": ("Claims require damage assessment, coverage verification, fraud screening, and settlement "
             "calculation. Image-based damage assessment needed human adjuster spot-checks for months before "
             "trust was established, and fraud-ring graph analytics caught staged-fraud patterns that "
             "per-claim scoring alone completely missed."),
 "diagram_note": ("The Settlement Confidence & Fraud Gate scales its auto-settlement threshold by claim type "
                   "risk tier rather than one global dollar cap; the fraud-ring pattern-matching in L3 feeds "
                   "directly into the gate alongside the settlement calculation."),
 "spec": {
   "l1": [_int("int1", "Policy Database"), _int("int2", "Claim Photos/Documents"), _ext("ext1", "ISO ClaimSearch Fraud Database")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Claims Fraud-Ring Knowledge Graph")],
   "l3_orch": _orch("orch", "Claims Processing Orchestrator Agent"),
   "l3_workers": [_w("w1", "Policy Coverage Verification Agent"), _w("w2", "Damage Assessment Agent"),
                  _w("w3", "Fraud Indicator Detection Agent"), _w("w4", "Settlement Calculation Agent")],
   "l4": [_l4("g1", "Auto-Settlement Dollar-Cap Policy"), _l4("g2", "Fraud-Ring Guardrail"), _l4("g3", "Claim-Type Risk Rule Engine")],
   "gate": _gate("gate", "Settlement Confidence & Fraud Gate"),
   "l5": [_l5_human("human", "Adjuster Review"), _l5_auto("a1", "Automated Settlement Payment"),
          _l5_plain("a2", "Claimant Settlement Breakdown"), _l5_hold("hold", "Special Investigation Unit Referral")],
   "l6": [_l6("m1", "Settlement Accuracy Monitor"), _l6("m2", "Damage-Estimation Bias Watchdog"), _l6("m3", "Fraud-Ring Auditor")],
   "l7": [_l7("lead1", "Claim Cycle-Time Dashboard"), _l7("lead2", "Settlement Accuracy Scorecard"), _l7("lead3", "Fraud-Caught View")],
   "l8": [_l8("s1", "Settlement Accuracy Tracker"), _l8("s2", "Damage-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("insurance claims", "Policy Coverage Verification Agent", "Claims Processing Orchestrator Agent", 3,
                         "Settlement Confidence & Fraud Gate", "Automated Settlement Payment", "Adjuster Review"),
},

{
 "id": 9, "quick_slug": "contract-loan-document-review",
 "quick_title": "Contract & Loan Document Review (Legal/Credit Agent)",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Contract Risk Review Prioritization Decisioning",
 "intro": ("This deep-8 view keeps the critic agent's independence from the proposer as a hard, non-negotiable "
           "design constraint — the Quick view found that letting the critic see the proposer's flags turned "
           "it into a rubber stamp that missed real gaps."),
 "problem": ("Reviewing loan agreements and commercial contracts for risky clauses is slow, expensive legal "
             "work. A firm-specific precedent library dramatically improved flagging relevance over generic "
             "'market standard' comparisons, and citation-grounding became mandatory after an early draft "
             "included an unverifiable claim."),
 "diagram_note": ("The Review Priority Confidence Gate always routes to a lawyer/credit-officer for final "
                   "sign-off — this system never finalizes a clause position autonomously. L4's "
                   "citation-grounding guardrail requires every flag to cite a specific clause."),
 "spec": {
   "l1": [_int("int1", "Uploaded Contract/Loan Agreement"), _int("int2", "Firm Precedent Clause Library"), _int("int3", "Prior Deal Negotiation History")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Clause Taxonomy Knowledge Graph")],
   "l3_orch": _orch("orch", "Legal Review Prioritization Arbiter Agent"),
   "l3_workers": [_w("w1", "Clause Extraction & Risk-Flagging Agent"), _w("w2", "Adversarial Missed-Risk Critic Agent"),
                  _w("w3", "Precedent Comparison Agent")],
   "l4": [_l4("g1", "Materiality-Ranking Policy"), _l4("g2", "Citation-Grounding Guardrail"), _l4("g3", "Redline Authorization Rule Engine")],
   "gate": _gate("gate", "Review Priority Confidence Gate"),
   "l5": [_l5_human("human", "Lawyer/Credit-Officer Sign-off"), _l5_auto("a1", "Redlined Document Generation"),
          _l5_plain("a2", "Negotiation Position Summary"), _l5_hold("hold", "Ambiguous-Clause Hold Queue")],
   "l6": [_l6("m1", "Missed-Risk Recall Monitor"), _l6("m2", "Citation-Accuracy Watchdog"), _l6("m3", "Redline Auditor")],
   "l7": [_l7("lead1", "Review Turnaround Dashboard"), _l7("lead2", "Risk-Coverage Scorecard"), _l7("lead3", "Precedent Usage View")],
   "l8": [_l8("s1", "Flagging Accuracy Tracker"), _l8("s2", "Precedent-Library Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("contract review", "Clause Extraction & Risk-Flagging Agent", "Legal Review Prioritization Arbiter Agent", 2,
                         "Review Priority Confidence Gate", "Redlined Document Generation", "Lawyer/Credit-Officer Sign-off"),
},

{
 "id": 10, "quick_slug": "fpna-forecasting",
 "quick_title": "Financial Planning & Analysis (FP&A) Forecasting",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Rolling Forecast & Variance Decisioning",
 "intro": ("This deep-8 view grounds every variance narrative in structured price/volume/mix decomposition "
           "before any LLM-generated explanation — the Quick view found finance leadership trusted narratives "
           "far more once they were grounded this way rather than free-form."),
 "problem": ("FP&A teams spend weeks consolidating actuals and building forecasts. The Quick view moved from "
             "quarterly to continuous weekly consolidation and found the value of catching variance early was "
             "clear immediately — but only once variance decomposition was structured, not free-form LLM "
             "explanation."),
 "diagram_note": ("The Forecast Confidence Gate routes any material, unexplained variance to FP&A leadership "
                   "review; L4's variance-decomposition guardrail requires every narrative to be grounded in "
                   "structured price/volume/mix analysis before it reaches L5."),
 "spec": {
   "l1": [_int("int1", "ERP/GL Actuals"), _int("int2", "Business Driver Data"), _ext("ext1", "Macroeconomic Indicators")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Business-Driver Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Actuals Consolidation Agent"), _w("w2", "Driver-Based Forecasting Agent"),
                  _w("w3", "Variance Analysis Agent"), _w("w4", "Scenario/Sensitivity Agent")],
   "l4": [_l4("g1", "Forecast-Confidence-Interval Policy"), _l4("g2", "Variance-Decomposition Guardrail"), _l4("g3", "Board-Reporting Rule Engine")],
   "gate": _gate("gate", "Forecast Confidence Gate"),
   "l5": [_l5_human("human", "FP&A Leadership Review"), _l5_auto("a1", "Board/Leadership Report Package"),
          _l5_plain("a2", "Forecast Update in Planning System"), _l5_hold("hold", "Variance Investigation Hold")],
   "l6": [_l6("m1", "Forecast Accuracy Monitor"), _l6("m2", "Driver-Quality Watchdog"), _l6("m3", "Variance Auditor")],
   "l7": [_l7("lead1", "Rolling Forecast Dashboard"), _l7("lead2", "Forecast Accuracy Scorecard"), _l7("lead3", "Business-Unit Variance View")],
   "l8": [_l8("s1", "Forecast Accuracy Tracker"), _l8("s2", "Driver-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("FP&A forecasting", "Actuals Consolidation Agent", None, 3,
                         "Forecast Confidence Gate", "Board/Leadership Report Package", "FP&A Leadership Review"),
},

{
 "id": 11, "quick_slug": "chargeback-dispute-resolution",
 "quick_title": "Customer Dispute & Chargeback Resolution",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Chargeback Representment Decisioning",
 "intro": ("This deep-8 view prioritizes by win-probability before committing resources to a full "
           "representment package — the Quick view found many early low-probability disputes weren't worth "
           "the operational cost to contest."),
 "problem": ("Chargeback disputes require assembling evidence within tight network deadlines. A missed "
             "deadline is an automatic loss regardless of evidence quality, and the win-probability model "
             "proved essential for prioritizing which disputes were worth contesting at all."),
 "diagram_note": ("The Representment Confidence Gate routes low-win-probability cases to hold rather than "
                   "burning operational effort on a full package; L6's deadline-compliance monitor got "
                   "dedicated redundant alerting given how unforgiving a missed network deadline is."),
 "spec": {
   "l1": [_int("int1", "Transaction Logs"), _int("int2", "Merchant Communication Records"), _ext("ext1", "Card Network Reason-Code Rules")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Chargeback Evidence Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Dispute Intake & Classification Agent"), _w("w2", "Evidence Gathering Agent"),
                  _w("w3", "Win-Probability Assessment Agent"), _w("w4", "Representment Package Generation Agent")],
   "l4": [_l4("g1", "Evidence-Grounding Policy"), _l4("g2", "Deadline-Priority Guardrail"), _l4("g3", "Contest-Threshold Rule Engine")],
   "gate": _gate("gate", "Representment Confidence Gate"),
   "l5": [_l5_human("human", "Chargeback Analyst Review"), _l5_auto("a1", "Network Representment Submission"),
          _l5_plain("a2", "Provisional Credit to Customer"), _l5_hold("hold", "Low-Win-Probability Hold")],
   "l6": [_l6("m1", "Deadline-Compliance Monitor"), _l6("m2", "Win-Rate Watchdog"), _l6("m3", "Submission Auditor")],
   "l7": [_l7("lead1", "Win-Rate Dashboard"), _l7("lead2", "Dollar-Recovery Scorecard"), _l7("lead3", "Reason-Code View")],
   "l8": [_l8("s1", "Win-Probability Accuracy Tracker"), _l8("s2", "Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("chargeback disputes", "Dispute Intake & Classification Agent", None, 3,
                         "Representment Confidence Gate", "Network Representment Submission", "Chargeback Analyst Review"),
},

{
 "id": 12, "quick_slug": "market-risk-var-monitoring",
 "quick_title": "Market Risk Management / VaR Monitoring",
 "quick_pattern_label": "Blackboard / Shared-Memory",
 "title": "Firm-Wide Risk Concentration Decisioning",
 "intro": ("This deep-8 view makes concentration/correlation risk detection a first-class L3 agent from the "
           "start — the Quick view added it only after a near-miss where three desks independently built "
           "correlated exposure that no single desk view caught."),
 "problem": ("Trading desks need a real-time firm-wide view of VaR and limit breaches. Risk factors interact "
             "across desks in non-obvious ways; siloed per-desk views miss firm-wide concentration risk that "
             "only becomes visible when synthesized across all asset classes at once."),
 "diagram_note": ("The Risk Escalation Confidence Gate keeps all VaR/Greeks calculations in established, "
                   "regulator-validated risk engines — the Agentic Core orchestrates and synthesizes, it "
                   "never replaces the validated quantitative models themselves."),
 "spec": {
   "l1": [_int("int1", "Trading Position Feed"), _int("int2", "Market Data Feed"), _int("int3", "Historical Scenario Library")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Cross-Asset Risk Knowledge Graph")],
   "l3_orch": _orch("orch", "Firm-Wide Risk Controller Agent"),
   "l3_workers": [_w("w1", "Equity Risk Agent"), _w("w2", "Fixed Income Risk Agent"),
                  _w("w3", "FX/Commodities Risk Agent"), _w("w4", "Concentration/Correlation Risk Agent")],
   "l4": [_l4("g1", "Firm-Wide Limit Policy (hard veto)"), _l4("g2", "Concentration-Risk Guardrail"), _l4("g3", "Capital-Impact Rule Engine")],
   "gate": _gate("gate", "Risk Escalation Confidence Gate"),
   "l5": [_l5_human("human", "Risk Manager Review"), _l5_auto("a1", "Limit Breach Alert"),
          _l5_plain("a2", "Trading Desk Position Reduction Request"), _l5_hold("hold", "Concentration Investigation Hold")],
   "l6": [_l6("m1", "Limit-Breach Monitor"), _l6("m2", "Cross-Asset Correlation Watchdog"), _l6("m3", "Escalation Auditor")],
   "l7": [_l7("lead1", "Firm-Wide Risk Dashboard"), _l7("lead2", "Capital-at-Risk Scorecard"), _l7("lead3", "Concentration-by-Desk View")],
   "l8": [_l8("s1", "Risk-Model Accuracy Tracker"), _l8("s2", "Scenario-Library Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("market risk", "Equity Risk Agent", "Firm-Wide Risk Controller Agent", 3,
                         "Risk Escalation Confidence Gate", "Limit Breach Alert", "Risk Manager Review"),
},

{
 "id": 13, "quick_slug": "collections-delinquency-management",
 "quick_title": "Collections & Delinquency Management",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Collections Strategy Decisioning",
 "intro": ("This deep-8 view gives the Contact Compliance Agent hard veto power over every outreach action "
           "with no override path except a documented human exception — non-negotiable given the regulatory "
           "risk the Quick view identified from the outset."),
 "problem": ("Effective collections requires tailoring outreach to each borrower's situation while strictly "
             "complying with FDCPA/Reg F contact-frequency rules. Diagnosis-to-offer mapping needs to learn "
             "from actual outcomes, not stay static, and hardship eligibility benefits from proactive income/"
             "employment-change signals, not just reactive payment-history triggers."),
 "diagram_note": ("The Collections Strategy Confidence Gate cannot bypass L4's contact-frequency compliance "
                   "policy under any circumstance — this is the one gate in the whole system with no override "
                   "path besides a documented human exception."),
 "spec": {
   "l1": [_int("int1", "Payment History"), _int("int2", "Customer Communication History"), _ext("ext1", "Credit Bureau Update Feed")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Delinquency Pattern Knowledge Graph")],
   "l3_orch": _orch("orch", "Collections Strategy Orchestrator Agent"),
   "l3_workers": [_w("w1", "Delinquency Cause Diagnosis Agent"), _w("w2", "Contact Compliance Agent (FDCPA/Reg F)"),
                  _w("w3", "Settlement/Payment-Plan Offer Agent")],
   "l4": [_l4("g1", "Contact-Frequency Compliance Policy (hard veto)"), _l4("g2", "Hardship-Program Guardrail"), _l4("g3", "Settlement-Authority Rule Engine")],
   "gate": _gate("gate", "Collections Strategy Confidence Gate"),
   "l5": [_l5_human("human", "Collections Specialist Review"), _l5_auto("a1", "Compliant Outreach Execution"),
          _l5_plain("a2", "Payment Plan Enrollment"), _l5_hold("hold", "Hardship Program Hold Queue")],
   "l6": [_l6("m1", "Complaint-Rate Monitor"), _l6("m2", "Contact-Frequency Watchdog"), _l6("m3", "Recovery Auditor")],
   "l7": [_l7("lead1", "Recovery-Rate Dashboard"), _l7("lead2", "Complaint-Rate Scorecard"), _l7("lead3", "Strategy-Effectiveness View")],
   "l8": [_l8("s1", "Diagnosis Accuracy Tracker"), _l8("s2", "Strategy Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("collections", "Delinquency Cause Diagnosis Agent", "Collections Strategy Orchestrator Agent", 2,
                         "Collections Strategy Confidence Gate", "Compliant Outreach Execution", "Collections Specialist Review"),
},

{
 "id": 14, "quick_slug": "ma-due-diligence",
 "quick_title": "Mergers & Acquisitions Due Diligence",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "M&A Findings Prioritization Decisioning",
 "intro": ("This deep-8 view adds explicit findings de-duplication and materiality-based prioritization from "
           "the start — the Quick view found deal teams valued a prioritized findings list far more than an "
           "exhaustive one, and that cross-workstream overlap needed reconciliation logic the first version "
           "lacked."),
 "problem": ("Due diligence requires reviewing thousands of documents across legal, financial, and commercial "
             "workstreams under deal-timeline pressure. Findings routinely overlapped across workstreams "
             "without a reconciliation process, and confidentiality/access control needed to be "
             "workstream-specific, not deal-team-wide."),
 "diagram_note": ("The Findings Confidence & Materiality Gate consolidates and de-duplicates across all three "
                   "workstream managers before anything reaches the deal team, ranked by materiality rather "
                   "than presented as an undifferentiated list."),
 "spec": {
   "l1": [_int("int1", "Virtual Data Room Documents"), _int("int2", "Deal Risk Register"), _ext("ext1", "Litigation Database (PACER/Westlaw)")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Deal Comparables Knowledge Graph")],
   "l3_orch": _orch("orch", "Due Diligence Orchestrator Agent"),
   "l3_workers": [_w("w1", "Legal Workstream Manager Agent"), _w("w2", "Financial Workstream Manager Agent"),
                  _w("w3", "Commercial/Operational Workstream Manager Agent")],
   "l4": [_l4("g1", "Materiality-Scoring Policy"), _l4("g2", "Confidentiality/Information-Barrier Guardrail"), _l4("g3", "Findings-Deduplication Rule Engine")],
   "gate": _gate("gate", "Findings Confidence & Materiality Gate"),
   "l5": [_l5_human("human", "Deal Team Review"), _l5_auto("a1", "Due Diligence Findings Report"),
          _l5_plain("a2", "Deal Risk Register Update"), _l5_hold("hold", "Red-Flag Escalation Hold")],
   "l6": [_l6("m1", "Finding-Overlap Monitor"), _l6("m2", "Materiality-Calibration Watchdog"), _l6("m3", "Confidentiality Auditor")],
   "l7": [_l7("lead1", "Deal Readiness Dashboard"), _l7("lead2", "Risk-Register Scorecard"), _l7("lead3", "Workstream Progress View")],
   "l8": [_l8("s1", "Findings Accuracy Tracker"), _l8("s2", "Comparables-Library Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("M&A due diligence", "Legal Workstream Manager Agent", "Due Diligence Orchestrator Agent", 2,
                         "Findings Confidence & Materiality Gate", "Due Diligence Findings Report", "Deal Team Review"),
},

{
 "id": 15, "quick_slug": "esg-investment-screening",
 "quick_title": "ESG Investment Screening & Compliance",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "ESG Fund Compliance Screening Decisioning",
 "intro": ("This deep-8 view treats controversy monitoring as a continuous, always-on L3 agent rather than a "
           "static once-a-cycle check — the Quick view found a held company's labor controversy went "
           "undetected for weeks when screening only ran against static data."),
 "problem": ("Asset managers must screen investments against fund-specific ESG mandates that vary by fund. "
             "Fund policy language is often ambiguous, ESG data providers frequently disagree on ratings for "
             "the same company, and greenwashing risk means disclosure language needs conservative, "
             "fact-grounded generation."),
 "diagram_note": ("The Screening Confidence Gate requires Compliance Officer sign-off for any fund-policy "
                   "interpretation before it goes live — ESG policy language is ambiguous enough that getting "
                   "it wrong has real regulatory and reputational consequences, per the Quick view's explicit "
                   "requirement."),
 "spec": {
   "l1": [_int("int1", "Fund Holdings Data"), _int("int2", "Fund Policy/Prospectus Documents"), _ext("ext1", "ESG Ratings Providers")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "ESG Policy Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "ESG Data Aggregation Agent"), _w("w2", "Fund Policy Interpretation Agent"),
                  _w("w3", "Exclusion/Inclusion Screening Agent"), _w("w4", "Controversy Monitoring Agent")],
   "l4": [_l4("g1", "Multi-Provider Disagreement Policy"), _l4("g2", "Greenwashing-Risk Guardrail"), _l4("g3", "Compliance Officer Sign-off Rule Engine")],
   "gate": _gate("gate", "Screening Confidence Gate"),
   "l5": [_l5_human("human", "Compliance Officer Sign-off"), _l5_auto("a1", "Portfolio Compliance Alert"),
          _l5_plain("a2", "Fund Fact Sheet ESG Update"), _l5_hold("hold", "Policy-Ambiguity Hold Queue")],
   "l6": [_l6("m1", "Rating-Disagreement Monitor"), _l6("m2", "Controversy-Detection Watchdog"), _l6("m3", "Screening Auditor")],
   "l7": [_l7("lead1", "ESG Compliance Dashboard"), _l7("lead2", "Fund-Policy Adherence Scorecard"), _l7("lead3", "Controversy Exposure View")],
   "l8": [_l8("s1", "Screening Accuracy Tracker"), _l8("s2", "Policy-Interpretation Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("ESG screening", "ESG Data Aggregation Agent", None, 3,
                         "Screening Confidence Gate", "Portfolio Compliance Alert", "Compliance Officer Sign-off"),
},

{
 "id": 16, "quick_slug": "treasury-cash-liquidity-forecasting",
 "quick_title": "Treasury Cash Management & Liquidity Forecasting",
 "quick_pattern_label": "Orchestrator-Worker (Supervisor fan-out/fan-in)",
 "title": "Treasury Liquidity Action Decisioning",
 "intro": ("This deep-8 view builds segregation of duties into L4 as a hard architectural rule from the "
           "start — no single agent both recommends and executes above threshold — which proved essential "
           "during a vendor API bug that would otherwise have triggered an erroneous cash sweep."),
 "problem": ("Treasury needs near-real-time visibility into cash positions across many accounts, entities, "
             "and currencies. Cash flow forecasting accuracy depends heavily on AP/AR data quality, and "
             "cross-currency netting needed real transfer-cost data per banking corridor that proved more "
             "heterogeneous than initially modeled."),
 "diagram_note": ("The Liquidity Action Confidence Gate enforces segregation of duties as a hard L4 rule: no "
                   "single agent both recommends and executes an investment or sweep action above threshold — "
                   "this caught a vendor API bug during the Quick view's own operation before it caused an "
                   "erroneous sweep."),
 "spec": {
   "l1": [_int("int1", "Bank Account Statements (SWIFT/API)"), _int("int2", "AP/AR Forecast Data"), _ext("ext1", "FX Rate Feeds")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Banking-Relationship Knowledge Graph")],
   "l3_orch": _orch("orch", "Treasury Liquidity Orchestrator Agent"),
   "l3_workers": [_w("w1", "Cash Position Aggregation Agent"), _w("w2", "Cash Flow Forecasting Agent"),
                  _w("w3", "FX Exposure Agent"), _w("w4", "Investment/Sweep Optimization Agent")],
   "l4": [_l4("g1", "Segregation-of-Duties Policy (hard veto)"), _l4("g2", "Investment-Authority Guardrail"), _l4("g3", "Counterparty-Limit Rule Engine")],
   "gate": _gate("gate", "Liquidity Action Confidence Gate"),
   "l5": [_l5_human("human", "Treasurer Approval"), _l5_auto("a1", "Automated Cash Sweep Instruction"),
          _l5_plain("a2", "FX Hedge Recommendation"), _l5_hold("hold", "Large-Transfer Hold Queue")],
   "l6": [_l6("m1", "Forecast-Accuracy Monitor"), _l6("m2", "Data-Quality Watchdog"), _l6("m3", "Sweep Auditor")],
   "l7": [_l7("lead1", "Global Liquidity Dashboard"), _l7("lead2", "Cash-Yield Scorecard"), _l7("lead3", "FX-Exposure View")],
   "l8": [_l8("s1", "Forecast Accuracy Tracker"), _l8("s2", "Forecasting-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("treasury liquidity", "Cash Position Aggregation Agent", "Treasury Liquidity Orchestrator Agent", 3,
                         "Liquidity Action Confidence Gate", "Automated Cash Sweep Instruction", "Treasurer Approval"),
},

{
 "id": 17, "quick_slug": "insider-trading-surveillance",
 "quick_title": "Insider Trading & Market Abuse Surveillance",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Market Abuse Surveillance Decisioning",
 "intro": ("This deep-8 view mirrors the AML use case's proposer/critic independence discipline — the same "
           "design lesson (shared context between proposer and critic causes confirmation bias) applies "
           "equally here, and the severity of a false insider-trading accusation warrants an even stricter "
           "dual-officer review requirement before any regulatory referral."),
 "problem": ("Detecting insider trading requires correlating trading activity with MNPI access and "
             "communications — prone to both false positives and sophisticated evasion. Communications NLP "
             "had high false-positive rates on ordinary business language about the same companies, and given "
             "the severity of false accusations, a single arbiter's determination isn't sufficient for a "
             "regulatory referral."),
 "diagram_note": ("The Surveillance Case Confidence Gate requires the critic agent to remain fully independent "
                   "of the proposer — separate context, no shared framing — and L4's dual-officer review policy "
                   "means even a high-confidence gate outcome still requires two compliance officers before any "
                   "regulatory referral, beyond the agent arbitration alone."),
 "spec": {
   "l1": [_int("int1", "Trading Activity Data"), _int("int2", "MNPI Access Logs"), _int("int3", "Communications Surveillance Data")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Corporate Event Knowledge Graph")],
   "l3_orch": _orch("orch", "Surveillance Case Arbiter Agent"),
   "l3_workers": [_w("w1", "Suspicious Trading Pattern Proposer Agent"), _w("w2", "Alternative Explanation Critic Agent"),
                  _w("w3", "Communications Correlation Agent")],
   "l4": [_l4("g1", "Dual-Officer Review Policy (hard veto)"), _l4("g2", "Evidence-Completeness Guardrail"), _l4("g3", "Regulatory Referral Rule Engine")],
   "gate": _gate("gate", "Surveillance Case Confidence Gate"),
   "l5": [_l5_human("human", "Compliance Officer Case Assignment"), _l5_auto("a1", "Restricted-List Cross-Check"),
          _l5_plain("a2", "Employee Trading Restriction"), _l5_hold("hold", "Regulatory Referral Hold")],
   "l6": [_l6("m1", "Communications False-Positive Monitor"), _l6("m2", "Case-Volume Watchdog"), _l6("m3", "Referral Auditor")],
   "l7": [_l7("lead1", "Surveillance Coverage Dashboard"), _l7("lead2", "Case-Resolution Scorecard"), _l7("lead3", "Restricted-List Compliance View")],
   "l8": [_l8("s1", "Case Accuracy Tracker"), _l8("s2", "NLP-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("insider trading surveillance", "Suspicious Trading Pattern Proposer Agent", "Surveillance Case Arbiter Agent", 2,
                         "Surveillance Case Confidence Gate", "Restricted-List Cross-Check", "Compliance Officer Case Assignment"),
},

{
 "id": 18, "quick_slug": "complaint-handling-regulatory-compliance",
 "quick_title": "Customer Complaint Handling (Regulatory Compliance)",
 "quick_pattern_label": "Hierarchical Multi-Agent (Manager-of-Managers)",
 "title": "Regulatory Complaint Resolution Decisioning",
 "intro": ("This deep-8 view builds vulnerable-customer identification as a conservative, always-routes-to-"
           "human L4 policy from the start — never a fully automated resolution — and elevates systemic-issue "
           "detection to a first-class L6 component, which the Quick view found was the highest-value output "
           "of the entire system despite being originally out of scope."),
 "problem": ("Complaints must be handled within strict regulatory timeframes with consistent categorization "
             "and adequate redress. Vulnerable-customer cases need enhanced care that can never be fully "
             "automated, and patterns across many complaints often point to a systemic product or process bug "
             "worth far more than resolving each complaint individually."),
 "diagram_note": ("The Complaint Routing Confidence Gate routes any vulnerable-customer indicator straight to "
                   "a trained human handler with no auto-resolution path at all — this is deliberately "
                   "conservative given the sensitivity, matching the Quick view's hard requirement from launch."),
 "spec": {
   "l1": [_int("int1", "Omnichannel Complaint Intake"), _int("int2", "Regulatory Complaint Taxonomy"), _ext("ext1", "Regulator Deadline Rules")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Root-Cause Pattern Knowledge Graph")],
   "l3_orch": _orch("orch", "Complaint Handling Orchestrator Agent"),
   "l3_workers": [_w("w1", "Complaint Triage Manager Agent"), _w("w2", "Redress Determination Manager Agent"),
                  _w("w3", "Vulnerable Customer Identification Agent")],
   "l4": [_l4("g1", "Redress-Calculation Determinism Policy (hard veto)"), _l4("g2", "Vulnerable-Customer Guardrail (hard veto)"), _l4("g3", "Deadline-Buffer Rule Engine")],
   "gate": _gate("gate", "Complaint Routing Confidence Gate"),
   "l5": [_l5_human("human", "Trained Complaint Handler"), _l5_auto("a1", "Regulatory Complaint Log Update"),
          _l5_plain("a2", "Root-Cause Systemic Fix Referral"), _l5_hold("hold", "Vulnerable-Customer Hold Queue")],
   "l6": [_l6("m1", "Deadline-Compliance Monitor"), _l6("m2", "Systemic-Issue Watchdog"), _l6("m3", "Redress Auditor")],
   "l7": [_l7("lead1", "Complaint Resolution Dashboard"), _l7("lead2", "Regulatory Deadline Scorecard"), _l7("lead3", "Systemic-Issue View")],
   "l8": [_l8("s1", "Categorization Accuracy Tracker"), _l8("s2", "Taxonomy Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("complaint handling", "Complaint Triage Manager Agent", "Complaint Handling Orchestrator Agent", 2,
                         "Complaint Routing Confidence Gate", "Regulatory Complaint Log Update", "Trained Complaint Handler"),
},

{
 "id": 19, "quick_slug": "trade-settlement-reconciliation",
 "quick_title": "Trade Settlement Reconciliation",
 "quick_pattern_label": "Sequential Pipeline",
 "title": "Trade Settlement Break Resolution Decisioning",
 "intro": ("This deep-8 view prioritizes by deadline proximity from the start — the Quick view found "
           "deadline-aware triage had the single biggest impact on reducing settlement fails, more than any "
           "improvement to matching sophistication itself."),
 "problem": ("Post-trade settlement requires matching trade details before T+1/T+2 deadlines. Static data "
             "quality (incorrect settlement instructions on file), not trade-booking errors, turned out to be "
             "the bigger root cause of breaks — and corporate-action-driven breaks needed dedicated "
             "calendar-aware handling, not generic quantity-mismatch treatment."),
 "diagram_note": ("The Settlement Confidence Gate prioritizes by proximity to the settlement deadline, not "
                   "arrival order — this single change had the biggest measured impact on reducing settlement "
                   "fails in the Quick view's own experience."),
 "spec": {
   "l1": [_int("int1", "Internal Trade Booking Records"), _ext("ext1", "Counterparty/Custodian Confirmations"), _int("int2", "Static Data/SSI Records")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Break-Pattern Knowledge Graph")],
   "l3_orch": None,
   "l3_workers": [_w("w1", "Trade Matching Agent"), _w("w2", "Break Classification Agent"),
                  _w("w3", "Root-Cause Investigation Agent"), _w("w4", "Auto-Resolution Agent")],
   "l4": [_l4("g1", "Auto-Resolution Scope Policy"), _l4("g2", "Deadline-Prioritization Guardrail"), _l4("g3", "Static-Data Accuracy Rule Engine")],
   "gate": _gate("gate", "Settlement Confidence Gate"),
   "l5": [_l5_human("human", "Operations Team Escalation"), _l5_auto("a1", "Settlement Confirmation"),
          _l5_plain("a2", "Custodian Instruction Correction"), _l5_hold("hold", "Near-Deadline Hold Queue")],
   "l6": [_l6("m1", "Settlement-Fail Monitor"), _l6("m2", "Static-Data-Quality Watchdog"), _l6("m3", "Resolution Auditor")],
   "l7": [_l7("lead1", "Settlement Fail-Rate Dashboard"), _l7("lead2", "Break-Aging Scorecard"), _l7("lead3", "Root-Cause-by-Type View")],
   "l8": [_l8("s1", "Break-Resolution Accuracy Tracker"), _l8("s2", "Classification Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("trade settlement", "Trade Matching Agent", None, 3,
                         "Settlement Confidence Gate", "Settlement Confirmation", "Operations Team Escalation"),
},

{
 "id": 20, "quick_slug": "personalized-financial-advisory-nba",
 "quick_title": "Personalized Financial Advisory & Next-Best-Action",
 "quick_pattern_label": "Debate-Critique-Arbiter (Reflective Loop)",
 "title": "Next-Best-Action Recommendation Decisioning",
 "intro": ("This deep-8 view makes the minimum customer-wellbeing-benefit threshold a hard L4 policy the "
           "arbiter cannot override for revenue reasons — the direct lesson carried over from watching purely "
           "revenue-optimized recommenders erode long-term customer trust."),
 "problem": ("Proactive financial recommendations must balance business value against genuine customer "
             "benefit. Without outcome tracking, there's no way to prove the wellbeing critic actually "
             "improves customer outcomes rather than just suppressing profitable offers, and life-event "
             "detection needs careful pacing to avoid feeling surveillance-like."),
 "diagram_note": ("The Recommendation Confidence Gate enforces a hard minimum wellbeing-benefit threshold in "
                   "L4 that the arbiter cannot override for revenue reasons — this is the single non-negotiable "
                   "rule carried directly from the retrospective's core lesson."),
 "spec": {
   "l1": [_int("int1", "Account & Transaction History"), _int("int2", "Product Catalog & Pricing"), _int("int3", "Life-Event Signal Data")],
   "l2": [_l2("gw", "AI Gateway"), _l2("llm", "LLM Reasoning Core (Claude)"), _l2("kg", "Household Financial Knowledge Graph")],
   "l3_orch": _orch("orch", "Next-Best-Action Arbiter Agent"),
   "l3_workers": [_w("w1", "Revenue-Optimized Product Recommendation Agent"), _w("w2", "Customer Financial Wellbeing Critic Agent"),
                  _w("w3", "Life-Event Detection Agent")],
   "l4": [_l4("g1", "Minimum-Wellbeing-Benefit Policy (hard veto)"), _l4("g2", "Suitability-Documentation Guardrail"), _l4("g3", "Advisor-Escalation Rule Engine")],
   "gate": _gate("gate", "Recommendation Confidence Gate"),
   "l5": [_l5_human("human", "Advisor Outreach"), _l5_auto("a1", "In-App Personalized Recommendation"),
          _l5_plain("a2", "Recommendation Outcome Tracking"), _l5_hold("hold", "Complex-Case Hold Queue")],
   "l6": [_l6("m1", "Wellbeing-Benefit Monitor"), _l6("m2", "Recommendation-Trust Watchdog"), _l6("m3", "Outcome Auditor")],
   "l7": [_l7("lead1", "Customer Financial Outcomes Dashboard"), _l7("lead2", "Revenue-vs-Wellbeing Scorecard"), _l7("lead3", "Life-Event Response View")],
   "l8": [_l8("s1", "Recommendation Accuracy Tracker"), _l8("s2", "Uplift-Model Retraining Trigger"), _l8("s3", "Policy Memory Updater")],
 },
 "build_order_params": ("personalized advisory", "Revenue-Optimized Product Recommendation Agent", "Next-Best-Action Arbiter Agent", 2,
                         "Recommendation Confidence Gate", "In-App Personalized Recommendation", "Advisor Outreach"),
},

]
