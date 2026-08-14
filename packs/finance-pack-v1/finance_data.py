# -*- coding: utf-8 -*-
FINANCE = [
{
 "id": 1, "slug": "aml-transaction-monitoring-sar",
 "title": "AML Transaction Monitoring & SAR Filing",
 "pattern": "orchestrator-worker",
 "problem": (
   "Banks generate thousands of AML alerts daily from rules-based monitoring, of which 90-95% are false "
   "positives, yet each still requires investigator review to avoid regulatory penalty for missed suspicious "
   "activity. Investigators spend hours per alert gathering evidence across systems before deciding whether to "
   "file a Suspicious Activity Report (SAR). An agent team can pre-investigate every alert, assembling evidence "
   "and a draft narrative, so human investigators focus on judgment rather than data-gathering."
 ),
 "orchestrator": "AML Case Orchestrator Agent",
 "workers": ["Transaction Pattern Analysis Agent", "Customer/Entity Risk Profile Agent", "Adverse Media & Sanctions Screening Agent",
             "Network/Relationship Graph Agent", "Prior SAR/Case History Agent"],
 "data_sources": ["Core Banking Transactions", "KYC/CDD Records", "Sanctions/PEP Lists", "Adverse Media Feeds", "Prior Case Files"],
 "actions": ["SAR Draft for Investigator Review", "Case Management System Update", "Regulatory Filing (goAML/FinCEN)"],
 "human_gate": "Licensed AML Investigator Final Determination & Sign-off",
 "agents_table": [
   ("AML Case Orchestrator", "Fans out an alert to evidence-gathering agents, aggregates findings into a case file with a preliminary risk rating"),
   ("Transaction Pattern Analysis Agent", "Detects structuring, layering, and velocity patterns in the alerted account's transaction history"),
   ("Customer/Entity Risk Profile Agent", "Assesses whether behavior deviates from the customer's declared occupation/expected activity"),
   ("Adverse Media & Sanctions Screening Agent", "Screens involved parties against sanctions, PEP, and adverse media"),
   ("Network/Relationship Graph Agent", "Maps connections to other flagged accounts/entities to detect mule networks"),
   ("SAR Narrative Drafting Agent", "Synthesizes all evidence into a structured, regulator-ready draft narrative"),
 ],
 "tech_table": [
   ("Transaction monitoring", "Existing AML rules engine (Actimize/SAS AML) as the alert source"),
   ("Agent orchestration", "LangGraph supervisor with strict tool-use audit logging (regulatory requirement)"),
   ("Graph analytics", "Neo4j for entity-relationship/mule-network detection"),
   ("Screening", "Sanctions/PEP/adverse-media API (Refinitiv World-Check, Dow Jones)"),
   ("Narrative generation", "Claude grounded strictly in retrieved evidence with citation of source records"),
   ("Case management", "Actimize/NICE Case Manager integration"),
   ("Regulatory filing", "FinCEN BSA E-Filing / goAML XML schema generation"),
   ("Model governance", "Full explainability + human-override logging for regulatory exam readiness"),
 ],
 "retrospective": [
   "Every generated narrative sentence is required to cite its source transaction/record — this was added after an early draft included a plausible-sounding but unverifiable claim.",
   "Would build the network/relationship graph agent earlier; it caught mule-network patterns that individual per-account agents missed entirely in the first version.",
   "Investigators wanted a 'confidence + missing evidence' summary, not just a narrative, so they know what to double-check — added after investigator feedback.",
   "Regulatory audit requirements meant every agent tool call needed immutable logging from day one; retrofitting this after a pilot was costly.",
 ],
},
{
 "id": 2, "slug": "credit-underwriting-loan-origination",
 "title": "Credit Underwriting & Loan Origination",
 "pattern": "hierarchical",
 "problem": (
   "Small-business and consumer loan underwriting requires synthesizing financial statements, credit bureau data, "
   "bank transaction cash-flow analysis, collateral valuation, and policy compliance — traditionally a multi-day, "
   "multi-department process. A hierarchical agent system can compress this into hours while preserving auditable, "
   "explainable decisions required under fair-lending regulation."
 ),
 "top": "Underwriting Orchestrator Agent",
 "mid_layer": ["Financial Analysis Manager Agent", "Risk & Compliance Manager Agent"],
 "leaves_by_mid": [
   ["Financial Statement Spreading Agent", "Cash-Flow Analysis Agent", "Collateral Valuation Agent"],
   ["Credit Bureau & Score Agent", "Fair-Lending Compliance Agent", "Policy Exception Agent"],
 ],
 "actions": ["Loan Origination System Decision", "Adverse Action Notice Generation", "Underwriter Review Queue"],
 "agents_table": [
   ("Underwriting Orchestrator", "Coordinates financial and risk/compliance managers, produces the final decision package"),
   ("Financial Analysis Manager", "Oversees financial-statement, cash-flow, and collateral sub-agents"),
   ("Risk & Compliance Manager", "Oversees credit-score and fair-lending compliance sub-agents"),
   ("Financial Statement Spreading Agent", "Extracts and normalizes figures from uploaded financial statements/tax returns"),
   ("Cash-Flow Analysis Agent", "Analyzes bank transaction data (via open banking) for real cash-flow-based ability to repay"),
   ("Fair-Lending Compliance Agent", "Checks the decision for disparate-impact risk against protected classes before finalization"),
 ],
 "tech_table": [
   ("Document extraction", "OCR + LLM extraction of financial statements/tax docs (docx/pdf skill patterns)"),
   ("Cash-flow analysis", "Open banking API (Plaid) + transaction categorization ML model"),
   ("Credit bureau integration", "Experian/Equifax/TransUnion API"),
   ("Agent orchestration", "Hierarchical LangGraph with domain-manager sub-graphs"),
   ("Fair-lending testing", "Statistical disparate-impact testing (adverse impact ratio) as an automated gate"),
   ("Decisioning", "Explainable scorecard model (regulatory-preferred over black-box) combined with agent-gathered evidence"),
   ("LOS integration", "Encompass/nCino loan origination system API"),
   ("Compliance documentation", "Auto-generated adverse action notices citing specific reasons (Reg B compliant)"),
 ],
 "retrospective": [
   "Fair-lending compliance agent was added as a late gate in v1; would make it a co-equal manager reviewing every decision path from the start, not a final checkbox.",
   "Cash-flow analysis dramatically improved thin-file applicant approval accuracy — would prioritize open banking integration earlier over bureau-only scoring.",
   "Explainability requirements meant we had to avoid pure LLM-based final scoring; kept the decision boundary in a traditional interpretable model with agents feeding it features.",
   "Would add a policy-exception agent with clear escalation rather than allowing any single sub-agent to silently apply an exception.",
 ],
},
{
 "id": 3, "slug": "algo-trading-strategy-orchestration",
 "title": "Algorithmic Trading Strategy Orchestration",
 "pattern": "market-based",
 "problem": (
   "A multi-strategy trading desk runs several independent alpha strategies (momentum, mean-reversion, stat-arb) "
   "that compete for the same risk budget and execution capacity. Coordinating capital allocation and execution "
   "priority manually under changing market conditions is slow. A market-based internal architecture lets each "
   "strategy 'bid' for capital and execution priority against a risk-aware clearing mechanism."
 ),
 "auctioneer": "Portfolio Risk-Budget Clearing Agent",
 "bidders": ["Momentum Strategy Agent", "Mean-Reversion Strategy Agent", "Statistical Arbitrage Strategy Agent", "Market-Making Strategy Agent"],
 "actions": ["Order Management System (OMS) Submission", "Risk Limit Enforcement", "P&L Attribution Report"],
 "agents_table": [
   ("Portfolio Risk-Budget Clearing Agent", "Allocates the firm's risk budget (VaR limits) across strategies based on their bids and recent performance"),
   ("Momentum Strategy Agent", "Bids for capital proportional to signal strength and current market regime fit"),
   ("Mean-Reversion Strategy Agent", "Bids for capital based on detected dislocations and expected reversion timeline"),
   ("Statistical Arbitrage Strategy Agent", "Bids based on pair/basket cointegration signal confidence"),
   ("Execution Agent", "Executes allocated orders via smart order routing, minimizing market impact across strategies"),
   ("Risk Guardrail Agent", "Enforces hard VaR/position limits independent of strategy bidding, can veto any allocation"),
 ],
 "tech_table": [
   ("Strategy signal generation", "Existing quant research pipeline (Python/pandas, proprietary factor models)"),
   ("Market-based allocation", "Internal auction mechanism with risk-adjusted bid weighting"),
   ("Execution", "Smart order router (SOR) with FIX protocol connectivity"),
   ("Risk management", "Real-time VaR engine (e.g., Axioma/MSCI RiskMetrics) as an independent veto layer"),
   ("Orchestration", "Low-latency event-driven agent framework (not LLM-in-the-loop for execution-critical paths)"),
   ("LLM usage", "Claude used offline for strategy performance narrative/attribution reports, not live order decisions"),
   ("Backtesting", "Vectorized backtest engine validating allocation policy changes before production"),
   ("Compliance", "Pre-trade compliance checks (restricted list, position limits) as a hard gate before OMS submission"),
 ],
 "retrospective": [
   "Kept LLM reasoning entirely out of the latency-critical bid/execution loop after early testing showed unacceptable tail latency; LLMs are used only for post-trade analysis and reporting.",
   "Would give the Risk Guardrail Agent absolute veto power from day one rather than advisory-only, after a v1 near-miss where aggregate strategy exposure briefly exceeded firm limits.",
   "Add regime-detection as an explicit shared signal so strategy agents don't all bid aggressively into the same unfavorable regime simultaneously.",
   "Auction re-clearing frequency needed careful tuning — too frequent caused excessive turnover/costs, too infrequent caused stale allocations in fast markets.",
 ],
},
{
 "id": 4, "slug": "card-not-present-fraud-detection",
 "title": "Fraud Detection - Card-Not-Present Transactions",
 "pattern": "event-swarm",
 "problem": (
   "Card-not-present (e-commerce) fraud requires a decision within ~100ms at authorization time, evaluating "
   "device fingerprint, velocity, merchant risk, and behavioral signals simultaneously. A reactive swarm of "
   "specialized micro-agents subscribed to the transaction event stream can each contribute a fast partial signal "
   "that a real-time scorer combines, without the latency cost of a single monolithic model."
 ),
 "bus_name": "Real-Time Authorization Event Bus",
 "agents": ["Device Fingerprint Agent", "Velocity/Behavioral Agent", "Merchant Risk Agent", "Geolocation Consistency Agent",
            "Known Fraud-Pattern Match Agent"],
 "actions": ["Approve/Decline Authorization Response", "Step-up 3DS Challenge Trigger", "Fraud Case Creation for Confirmed Fraud"],
 "agents_table": [
   ("Real-Time Scoring Aggregator", "Combines all agent signals within the authorization time budget into a single risk score"),
   ("Device Fingerprint Agent", "Evaluates device/browser fingerprint reputation and consistency with account history"),
   ("Velocity/Behavioral Agent", "Checks transaction velocity and behavioral deviation from the cardholder's baseline"),
   ("Merchant Risk Agent", "Scores merchant category/reputation risk, including known fraud-prone merchants"),
   ("Geolocation Consistency Agent", "Flags impossible-travel or geo-IP/billing-address mismatches"),
   ("Known Fraud-Pattern Match Agent", "Matches against real-time-updated fraud signatures from the card network"),
 ],
 "tech_table": [
   ("Event streaming", "Kafka with sub-10ms consumer group processing"),
   ("Agent runtime", "In-memory feature-serving microservices (not LLM-based for the hot path — latency-critical)"),
   ("Feature store", "Real-time feature store (Feast/Tecton) for behavioral baselines"),
   ("Aggregation model", "Gradient-boosted ensemble combining agent signals, trained on labeled fraud outcomes"),
   ("3DS orchestration", "EMVCo 3-D Secure step-up integration"),
   ("Network intelligence", "Visa/Mastercard real-time fraud signal feeds"),
   ("Offline LLM layer", "Claude used asynchronously for case investigation and fraud-pattern narrative generation post-decision"),
   ("Monitoring", "Real-time false-positive/false-negative dashboard with decline-rate business impact tracking"),
 ],
 "retrospective": [
   "Confirmed the hot-path decision must stay in low-latency ML/rules, not LLM calls — an early experiment routing borderline cases through an LLM blew the latency SLA.",
   "Would add explicit false-positive cost tracking (declined legitimate transactions) as a KPI with equal weight to fraud-catch rate from the start.",
   "Add a feedback loop from confirmed-fraud/confirmed-legitimate chargebacks to continuously recalibrate each agent's weight in the aggregator.",
   "Geolocation agent needed VPN/proxy-awareness tuning — over-flagged legitimate VPN users initially, requiring a more nuanced risk tiering instead of a binary flag.",
 ],
},
{
 "id": 5, "slug": "customer-onboarding-kyc-finance",
 "title": "Customer Onboarding & KYC (Retail & Business Banking)",
 "pattern": "orchestrator-worker",
 "problem": (
   "Digital account opening abandons at high rates when identity verification, sanctions screening, and risk "
   "rating steps are sequential and slow. Banks need a parallelized, auditable KYC agent team that completes "
   "onboarding checks in near real time while meeting CDD/EDD regulatory requirements."
 ),
 "orchestrator": "KYC Onboarding Orchestrator Agent",
 "workers": ["Identity Document Verification Agent", "Sanctions/PEP Screening Agent", "Beneficial Ownership Agent (for business accounts)",
             "Customer Risk Rating Agent", "Source of Funds Agent"],
 "data_sources": ["Government ID/Document Upload", "Sanctions/PEP Databases", "Business Registry Data", "Application Form Data"],
 "actions": ["Account Opening System Approval", "Enhanced Due Diligence (EDD) Queue", "Welcome Kit / Rejection Notice"],
 "human_gate": "EDD Analyst Review for High-Risk Customers",
 "agents_table": [
   ("KYC Onboarding Orchestrator", "Runs verification agents in parallel and produces a risk-rated onboarding decision"),
   ("Identity Document Verification Agent", "Validates ID authenticity and performs liveness/facial-match check"),
   ("Sanctions/PEP Screening Agent", "Screens applicant (and beneficial owners for business accounts) against sanctions/PEP lists"),
   ("Beneficial Ownership Agent", "For business accounts, resolves the ultimate beneficial ownership structure from registry filings"),
   ("Customer Risk Rating Agent", "Computes a CDD risk rating from geography, product, and screening results"),
   ("Source of Funds Agent", "For higher-risk applicants, gathers and validates declared source-of-funds documentation"),
 ],
 "tech_table": [
   ("Identity verification", "Onfido/Jumio document + biometric verification API"),
   ("Sanctions screening", "Refinitiv World-Check / Dow Jones Risk & Compliance API"),
   ("Beneficial ownership", "Business registry APIs (OpenCorporates, national registries) + LLM entity-resolution"),
   ("Orchestration", "LangGraph supervisor with parallel tool calls and per-agent timeout/fallback"),
   ("Risk rating", "Rules-based CDD risk matrix combined with agent-gathered evidence"),
   ("Case management", "Integration with AML case management system for EDD queue"),
   ("Core banking integration", "Account opening API (Temenos/Mambu)"),
   ("Audit/compliance", "Full evidence trail retained per regulatory record-keeping requirements (5-7 years)"),
 ],
 "retrospective": [
   "Beneficial ownership resolution across international registries was far harder than expected; would budget significantly more time for this sub-agent and expect more human fallback initially.",
   "Would define hard timeout/fallback behavior for each verification agent from day one — a slow sanctions-screening API stalled the entire flow in early testing.",
   "Add a plain-language 'what's missing / what's next' customer-facing status message generated per abandonment point to reduce drop-off.",
   "Risk-rating thresholds needed periodic recalibration against actual EDD outcomes; built this feedback loop only after the first regulatory exam recommendation.",
 ],
},
{
 "id": 6, "slug": "robo-advisory-portfolio-rebalancing",
 "title": "Wealth Management: Robo-Advisory Portfolio Rebalancing",
 "pattern": "pipeline",
 "problem": (
   "Automated investment advisory platforms need to continuously monitor client portfolios against target "
   "allocations, tax considerations, and changing risk profiles, then execute rebalancing trades — all while "
   "meeting fiduciary duty and suitability documentation requirements. A pipeline of specialized agents keeps "
   "this both scalable and auditable across millions of accounts."
 ),
 "stages": ["Drift Detection Agent", "Tax-Impact Analysis Agent", "Suitability/Risk-Profile Check Agent",
            "Trade List Generation Agent", "Client Communication Agent"],
 "actions": ["Trade Execution via OMS", "Client Notification of Rebalancing", "Compliance Record Filing"],
 "agents_table": [
   ("Drift Detection Agent", "Scans all client portfolios daily for allocation drift beyond configured bands"),
   ("Tax-Impact Analysis Agent", "Computes tax-loss harvesting opportunities and capital-gains impact of proposed trades"),
   ("Suitability/Risk-Profile Check Agent", "Confirms the rebalancing target still matches the client's current risk profile/goals"),
   ("Trade List Generation Agent", "Produces the minimal-turnover trade list to restore target allocation"),
   ("Client Communication Agent", "Generates a plain-language explanation of why and what is being rebalanced"),
 ],
 "tech_table": [
   ("Portfolio monitoring", "Daily batch job over custodian position feeds (Schwab/Fidelity API)"),
   ("Tax optimization", "Tax-lot-level optimization engine for loss-harvesting and wash-sale avoidance"),
   ("Suitability check", "Rules engine cross-referencing latest risk-questionnaire/IPS data"),
   ("Trade generation", "Portfolio optimization (mean-variance / risk-parity) with turnover minimization constraint"),
   ("Orchestration", "Airflow/Temporal daily pipeline processing accounts in batches"),
   ("Communication", "Claude generating client-facing rebalancing explanations from structured trade rationale"),
   ("Execution", "OMS/custodian trading API integration"),
   ("Compliance", "Fiduciary-duty documentation auto-filed per trade batch (Form ADV / suitability records)"),
 ],
 "retrospective": [
   "Would add an explicit human-advisor review step for large or unusual rebalances (e.g., >$X or >Y% turnover) rather than full automation for every account tier.",
   "Tax-impact analysis needed wash-sale rules across the client's entire household (not just one account) — a costly gap discovered after early tax season.",
   "Client communication drafts initially felt robotic; iterated with real advisors to make explanations feel personalized, not templated.",
   "Would build a dry-run/simulation mode into the pipeline from the start so compliance could validate trade-list logic against edge cases before go-live.",
 ],
},
{
 "id": 7, "slug": "regulatory-compliance-monitoring-reporting",
 "title": "Regulatory Compliance Monitoring & Reg Reporting",
 "pattern": "hierarchical",
 "problem": (
   "Banks must continuously monitor for compliance with a growing patchwork of regulations (Basel III/IV, "
   "Dodd-Frank, MiFID II, local reporting) and file numerous recurring regulatory reports. Manual tracking of "
   "which rules apply to which business lines, and reconciling data across systems for each report, is a major "
   "operational burden and source of regulatory findings."
 ),
 "top": "Regulatory Compliance Orchestrator",
 "mid_layer": ["Capital/Liquidity Reporting Manager Agent", "Trade/Transaction Reporting Manager Agent"],
 "leaves_by_mid": [
   ["Basel Capital Ratio Calculation Agent", "LCR/NSFR Liquidity Agent", "Data Reconciliation Agent"],
   ["MiFID II Transaction Reporting Agent", "Trade Reporting Exception Agent"],
 ],
 "actions": ["Regulatory Report Submission", "Internal Compliance Dashboard", "Breach/Exception Escalation"],
 "agents_table": [
   ("Regulatory Compliance Orchestrator", "Tracks the full regulatory calendar and coordinates domain managers to meet filing deadlines"),
   ("Capital/Liquidity Reporting Manager", "Oversees capital ratio and liquidity coverage sub-agents"),
   ("Trade/Transaction Reporting Manager", "Oversees transaction-reporting sub-agents across jurisdictions"),
   ("Basel Capital Ratio Calculation Agent", "Computes CET1/Tier 1/Total capital ratios from risk-weighted asset data"),
   ("Data Reconciliation Agent", "Reconciles source-system data against the general ledger before report generation"),
   ("MiFID II Transaction Reporting Agent", "Generates and validates transaction reports against ESMA schema requirements"),
 ],
 "tech_table": [
   ("Regulatory calendar", "Rules-driven calendar engine tracking jurisdiction-specific filing deadlines"),
   ("Data reconciliation", "Automated GL-to-source reconciliation with exception flagging"),
   ("Calculation engines", "Purpose-built regulatory capital calculation engines (Moody's/Wolters Kluwer OneSumX)"),
   ("Report generation", "XBRL/XML schema generation per regulator (EBA, FCA, ESMA formats)"),
   ("Orchestration", "Hierarchical LangGraph tracking report state machines per filing"),
   ("LLM usage", "Claude for regulatory-text change monitoring/impact-summary, not final calculations"),
   ("Validation", "Automated schema + business-rule validation before submission"),
   ("Audit", "Full lineage from source transaction to final regulatory report field"),
 ],
 "retrospective": [
   "Kept all financial calculations in deterministic, auditable engines — LLM agents are used only for regulatory-text interpretation and change-impact summaries, never final numbers.",
   "Would build the regulatory-change monitoring agent first; new rule versions silently broke report templates in v1 before this was added.",
   "Data reconciliation exceptions were the dominant cause of filing delays; would invest more heavily here relative to report-generation automation.",
   "Cross-jurisdiction rule conflicts (same transaction reportable differently in two regimes) needed a dedicated conflict-resolution sub-agent, added after a near-miss on a filing.",
 ],
},
{
 "id": 8, "slug": "insurance-claims-processing-fraud",
 "title": "Insurance Claims Processing & Fraud Detection",
 "pattern": "orchestrator-worker",
 "problem": (
   "Insurance claims (auto, property, health) require damage assessment, policy coverage verification, fraud "
   "screening, and settlement calculation — currently siloed steps causing multi-week claim cycles and "
   "inconsistent fraud detection. An agent team can triage and settle straightforward claims automatically while "
   "flagging complex or suspicious claims for adjusters."
 ),
 "orchestrator": "Claims Processing Orchestrator Agent",
 "workers": ["Policy Coverage Verification Agent", "Damage Assessment Agent (image/document analysis)",
             "Fraud Indicator Detection Agent", "Settlement Calculation Agent"],
 "data_sources": ["Policy Database", "Claim Photos/Documents", "Historical Claims Data", "External Fraud Databases (ISO ClaimSearch)"],
 "actions": ["Automated Settlement Payment", "Adjuster Assignment for Complex Claims", "Special Investigation Unit (SIU) Referral"],
 "human_gate": "Adjuster Review for Claims Above Auto-Settlement Threshold or Fraud Flag",
 "agents_table": [
   ("Claims Processing Orchestrator", "Routes the claim through verification/assessment/fraud agents and decides auto-settle vs. adjuster review"),
   ("Policy Coverage Verification Agent", "Confirms the claim falls within active policy coverage, limits, and exclusions"),
   ("Damage Assessment Agent", "Analyzes submitted photos/videos and repair estimates to assess damage severity and cost"),
   ("Fraud Indicator Detection Agent", "Screens for staged-accident patterns, claim-timing anomalies, and cross-references SIU watchlists"),
   ("Settlement Calculation Agent", "Computes the settlement amount per policy terms, deductibles, and depreciation schedules"),
 ],
 "tech_table": [
   ("Image analysis", "Computer vision model for vehicle/property damage severity estimation"),
   ("Document extraction", "OCR + LLM extraction from repair estimates and medical bills"),
   ("Fraud detection", "Graph analytics (Neo4j) linking claimants, repair shops, and prior claims for staged-fraud rings"),
   ("Policy engine", "Rules engine checking coverage/exclusions against policy documents"),
   ("Orchestration", "LangGraph supervisor with auto-settle threshold logic"),
   ("External data", "ISO ClaimSearch / LexisNexis fraud database integration"),
   ("Payment", "Direct settlement payment via claims payment processor"),
   ("Case management", "Guidewire ClaimCenter integration"),
 ],
 "retrospective": [
   "Image-based damage assessment needed human adjuster spot-checks for the first several months to build trust and catch systematic estimation biases before full automation.",
   "Would add explicit auto-settlement dollar caps that scale down for newer/riskier claim types rather than one global threshold — an early miscalibration overpaid a class of low-frequency high-severity claims.",
   "Fraud graph analytics caught ring-based fraud that per-claim fraud scoring missed entirely — would prioritize building this earlier.",
   "Claimants found black-box settlement calculations frustrating; added a plain-language settlement-breakdown explanation, which reduced disputes noticeably.",
 ],
},
{
 "id": 9, "slug": "contract-loan-document-review",
 "title": "Contract & Loan Document Review (Legal/Credit Agent)",
 "pattern": "debate-critique",
 "problem": (
   "Reviewing loan agreements, ISDA/credit agreements, and commercial contracts for risky clauses, missing "
   "covenants, or deviations from standard playbooks is slow, expensive legal/credit-risk work. A "
   "proposer/critic agent pair — one extracting and flagging issues, one adversarially checking for missed risks "
   "or over-flagged non-issues — improves both coverage and precision before a human lawyer's final review."
 ),
 "proposer": "Clause Extraction & Risk-Flagging Agent",
 "critic": "Adversarial Missed-Risk Critic Agent",
 "arbiter": "Legal Review Prioritization Arbiter Agent",
 "refs": ["Uploaded Contract/Loan Agreement", "Standard Playbook/Precedent Clause Library", "Prior Deal Negotiation History"],
 "actions": ["Redlined Document with Flagged Clauses", "Lawyer/Credit-Officer Review Queue", "Negotiation Position Summary"],
 "agents_table": [
   ("Clause Extraction & Risk-Flagging Agent", "Extracts key clauses (covenants, MAC clauses, indemnities) and flags deviations from the standard playbook"),
   ("Adversarial Missed-Risk Critic Agent", "Independently re-reads the document looking specifically for risks the proposer may have missed"),
   ("Legal Review Prioritization Arbiter Agent", "Combines both agents' findings into a prioritized issues list for the human reviewer"),
   ("Precedent Comparison Agent", "Compares clause language against a library of the firm's prior negotiated precedents"),
   ("Redline Generation Agent", "Produces a suggested redline with rationale for each proposed change"),
 ],
 "tech_table": [
   ("Document parsing", "docx/pdf skill-based extraction preserving clause structure and cross-references"),
   ("Clause extraction", "Claude with legal-domain prompting + structured clause taxonomy output"),
   ("Adversarial critique", "Second independent Claude pass with an explicit 'find what was missed' objective and no visibility into the first pass's flags"),
   ("Precedent matching", "Vector search (pgvector) over the firm's precedent clause library"),
   ("Arbitration", "Rule-based prioritization (materiality x deviation-from-standard) combining both agents' outputs"),
   ("Redlining", "Document generation preserving Word track-changes format (docx skill)"),
   ("Workflow", "Integration with contract lifecycle management (CLM) platform (Ironclad/Icertis)"),
   ("Human review", "Lawyer/credit-officer sign-off required before any clause position is finalized"),
 ],
 "retrospective": [
   "The critic's independence (no visibility into the proposer's flags) was essential — an early version where the critic saw the proposer's output just rubber-stamped it, missing real gaps.",
   "Would build the precedent library integration first; generic 'market standard' flagging without firm-specific precedent context produced too many irrelevant flags initially.",
   "Legal reviewers strongly preferred seeing *why* something was flagged with a specific clause citation, not just a risk label — made citation-grounding mandatory.",
   "Contract structure variance (different templates per deal type) broke naive clause extraction; would invest in more robust document-structure parsing earlier.",
 ],
},
{
 "id": 10, "slug": "fpna-forecasting",
 "title": "Financial Planning & Analysis (FP&A) Forecasting",
 "pattern": "pipeline",
 "problem": (
   "Corporate FP&A teams spend weeks each quarter consolidating actuals across business units, building "
   "forecasts, and preparing variance-explanation narratives for leadership. Manual Excel-based consolidation is "
   "error-prone and slow to adapt when business drivers change mid-quarter. An automated pipeline can consolidate, "
   "forecast, and narrate variances continuously rather than only at quarter-end."
 ),
 "stages": ["Actuals Consolidation Agent", "Driver-Based Forecasting Agent", "Variance Analysis Agent",
            "Scenario/Sensitivity Agent", "Executive Narrative Generation Agent"],
 "actions": ["Board/Leadership Report Package", "Forecast Update in Planning System", "Budget Variance Alert"],
 "agents_table": [
   ("Actuals Consolidation Agent", "Pulls and consolidates actuals from ERP/GL across business units into a unified structure"),
   ("Driver-Based Forecasting Agent", "Updates rolling forecasts using business drivers (headcount, pipeline, macro indicators)"),
   ("Variance Analysis Agent", "Identifies and explains material variances between forecast and actuals per line item"),
   ("Scenario/Sensitivity Agent", "Generates upside/downside scenarios based on key driver sensitivity"),
   ("Executive Narrative Generation Agent", "Drafts the leadership-ready summary connecting numbers to business explanations"),
 ],
 "tech_table": [
   ("Data consolidation", "ERP integration (SAP/Oracle) + data warehouse (Snowflake) consolidation layer"),
   ("Forecasting", "Driver-based forecasting models (statistical + ML ensemble) per P&L line"),
   ("Variance analysis", "Automated variance decomposition (price/volume/mix analysis)"),
   ("Scenario modeling", "Monte Carlo sensitivity analysis on key driver assumptions"),
   ("Orchestration", "dbt + Airflow pipeline with agent-based narrative steps"),
   ("Narrative generation", "Claude generating variance explanations grounded in the decomposition output"),
   ("Reporting", "Automated board-deck generation (pptx skill) from templated slide structure"),
   ("Planning system", "Integration with Anaplan/Adaptive Insights for forecast updates"),
 ],
 "retrospective": [
   "Variance narratives were much more trusted by finance leadership once grounded in structured decomposition (price/volume/mix) rather than free-form LLM explanation — added this structure after early skepticism.",
   "Would move from quarterly to continuous (weekly) consolidation cadence from the start; the value of catching variance early was clear immediately after launch.",
   "Add business-unit-level self-service query agent so FP&A isn't the bottleneck for every ad hoc leadership question.",
   "Driver-based forecast accuracy varied a lot by business unit maturity; would set differentiated confidence-interval reporting per unit rather than a uniform point forecast.",
 ],
},
{
 "id": 11, "slug": "chargeback-dispute-resolution",
 "title": "Customer Dispute & Chargeback Resolution",
 "pattern": "pipeline",
 "problem": (
   "Card chargeback disputes require gathering transaction evidence, matching against network reason codes, and "
   "assembling representment packages within tight network deadlines (often 7-20 days). Manual handling scales "
   "poorly with dispute volume and banks often miss deadlines or under-invest in winnable disputes."
 ),
 "stages": ["Dispute Intake & Reason-Code Classification Agent", "Evidence Gathering Agent", "Win-Probability Assessment Agent",
            "Representment Package Generation Agent", "Deadline & Submission Tracking Agent"],
 "actions": ["Network Representment Submission (Visa/Mastercard)", "Provisional Credit to Customer", "Merchant Liability Notification"],
 "agents_table": [
   ("Dispute Intake & Classification Agent", "Classifies the dispute reason code and applicable network rules"),
   ("Evidence Gathering Agent", "Assembles transaction logs, AVS/CVV match results, delivery confirmation, and prior correspondence"),
   ("Win-Probability Assessment Agent", "Estimates likelihood of winning representment based on evidence strength and historical outcomes"),
   ("Representment Package Generation Agent", "Assembles a network-compliant evidence package for cases worth contesting"),
   ("Deadline & Submission Tracking Agent", "Tracks network-specific deadlines and ensures timely submission"),
 ],
 "tech_table": [
   ("Reason-code classification", "Rules engine mapping to Visa/Mastercard reason-code taxonomies"),
   ("Evidence gathering", "Tool-calling agent across transaction, fraud-screening, and merchant-communication systems"),
   ("Win-probability model", "Classifier trained on historical representment outcomes by reason code and evidence type"),
   ("Package generation", "Automated compilation into network-required format (Visa VROL/Mastercom)"),
   ("Orchestration", "Temporal workflow with deadline-based SLA tracking and alerts"),
   ("LLM usage", "Claude drafting the cover narrative summarizing evidence, grounded in gathered documents"),
   ("Case management", "Chargeback management platform integration (Verifi/Ethoca)"),
   ("Analytics", "Win-rate and dollar-recovery dashboard by reason code and merchant"),
 ],
 "retrospective": [
   "Would add the win-probability agent before building full package-generation automation — many early low-probability disputes weren't worth the operational cost to contest.",
   "Deadline tracking needed to be the most bulletproof part of the system; a missed deadline is an automatic loss regardless of evidence quality, so this got dedicated redundant alerting.",
   "Evidence quality varied a lot by merchant integration; would invest earlier in standardizing merchant-side evidence submission (delivery confirmation, etc.).",
   "Cover narrative drafts occasionally over-claimed certainty; added strict grounding requirements so claims map 1:1 to attached evidence documents.",
 ],
},
{
 "id": 12, "slug": "market-risk-var-monitoring",
 "title": "Market Risk Management / VaR Monitoring",
 "pattern": "blackboard",
 "problem": (
   "Trading desks and risk management need a real-time, firm-wide view of Value-at-Risk, stress-test exposure, "
   "and limit breaches across asset classes. Risk factors interact in non-obvious ways across desks, and siloed "
   "per-desk risk views miss firm-wide concentration risk. A blackboard architecture lets per-asset-class risk "
   "agents post findings that a controller synthesizes into a firm-wide risk picture."
 ),
 "controller": "Firm-Wide Risk Controller Agent",
 "store_name": "Risk Blackboard (positions, sensitivities, limit status)",
 "agents": ["Equity Risk Agent", "Fixed Income Risk Agent", "FX/Commodities Risk Agent", "Derivatives Greeks Agent",
            "Concentration/Correlation Risk Agent"],
 "actions": ["Limit Breach Alert to Risk Manager", "Trading Desk Position Reduction Request", "Regulatory Capital Impact Report"],
 "agents_table": [
   ("Firm-Wide Risk Controller Agent", "Monitors the blackboard for limit breaches and synthesizes cross-asset-class risk concentration"),
   ("Equity Risk Agent", "Computes equity VaR and factor exposures (beta, sector, style) and posts to the blackboard"),
   ("Fixed Income Risk Agent", "Computes duration, convexity, and credit-spread risk for the bond book"),
   ("FX/Commodities Risk Agent", "Computes currency and commodity exposure and posts hedging-need signals"),
   ("Derivatives Greeks Agent", "Aggregates delta/gamma/vega across the derivatives book"),
   ("Concentration/Correlation Risk Agent", "Watches the blackboard for correlated exposures across asset classes that individually look fine but combine into concentration risk"),
 ],
 "tech_table": [
   ("Risk calculation", "Existing risk engines (MSCI RiskMetrics/Axioma) as per-asset-class calculators"),
   ("Blackboard store", "Low-latency in-memory grid (Redis/Apache Ignite) for shared position/risk state"),
   ("Controller reasoning", "Claude synthesizing structured blackboard entries into a firm-wide risk narrative for the risk committee"),
   ("Stress testing", "Historical and hypothetical scenario engine run against the consolidated position blackboard"),
   ("Alerting", "Real-time limit-breach alerting to risk managers and desk heads"),
   ("Regulatory reporting", "Feed into capital calculation (linked to Use Case 7's Basel agents)"),
   ("Audit", "Full snapshot history of the blackboard for regulatory exam reconstruction"),
   ("Dashboard", "Real-time firm-wide risk dashboard for CRO and risk committee"),
 ],
 "retrospective": [
   "Kept all VaR/Greeks calculations in established, regulator-validated risk engines — agents orchestrate and synthesize, they do not replace validated quantitative models.",
   "Would add the concentration/correlation agent from day one; it was added after a near-miss where three desks independently built correlated exposure that no single desk view caught.",
   "Blackboard update latency across asset classes needed careful synchronization — stale FX data briefly caused a false concentration alert in early testing.",
   "Risk committee wanted the controller's narrative to explicitly cite which underlying positions drove a concentration finding, not just a summary conclusion.",
 ],
},
{
 "id": 13, "slug": "collections-delinquency-management",
 "title": "Collections & Delinquency Management",
 "pattern": "orchestrator-worker",
 "problem": (
   "Effective collections requires tailoring contact strategy, timing, and settlement offers to each delinquent "
   "borrower's specific situation (hardship vs. simple oversight vs. unwillingness to pay) while strictly "
   "complying with FDCPA/Reg F contact-frequency and disclosure rules. Blanket collection scripts recover less "
   "and generate more complaints than a diagnosed, compliant, personalized approach."
 ),
 "orchestrator": "Collections Strategy Orchestrator Agent",
 "workers": ["Delinquency Cause Diagnosis Agent", "Contact Compliance Agent (FDCPA/Reg F)", "Settlement/Payment-Plan Offer Agent",
             "Hardship Program Eligibility Agent"],
 "data_sources": ["Payment History", "Customer Communication History", "Hardship Program Rules", "Credit Bureau Update Feed"],
 "actions": ["Compliant Outreach (Call/SMS/Letter)", "Payment Plan Enrollment", "Hardship Program Enrollment"],
 "human_gate": "Collections Specialist Review for Complex Hardship Cases",
 "agents_table": [
   ("Collections Strategy Orchestrator", "Diagnoses the delinquency situation and selects a compliant, tailored outreach and offer strategy"),
   ("Delinquency Cause Diagnosis Agent", "Infers likely cause (hardship, dispute, oversight) from payment pattern and any prior communication"),
   ("Contact Compliance Agent", "Enforces Reg F contact-frequency limits and required disclosures before any outreach is sent"),
   ("Settlement/Payment-Plan Offer Agent", "Generates an appropriate settlement or payment plan offer within approved policy bands"),
   ("Hardship Program Eligibility Agent", "Checks eligibility for hardship programs (forbearance, rate reduction) and initiates enrollment"),
 ],
 "tech_table": [
   ("Diagnosis reasoning", "Claude classifying delinquency cause from structured payment history + communication transcripts"),
   ("Compliance engine", "Rules engine encoding Reg F/FDCPA contact-frequency and disclosure requirements as hard gates"),
   ("Offer optimization", "Policy-constrained settlement optimization balancing recovery rate and compliance risk"),
   ("Orchestration", "LangGraph supervisor with compliance agent as a mandatory pre-send gate"),
   ("Outreach channels", "Dialer/SMS/mail integration with consent and opt-out tracking"),
   ("Hardship processing", "Integration with servicing system for program enrollment"),
   ("Credit bureau reporting", "Automated accurate/timely furnishing per FCRA requirements"),
   ("Monitoring", "Complaint-rate and recovery-rate dashboard segmented by strategy"),
 ],
 "retrospective": [
   "The Contact Compliance Agent has hard veto power over every outreach action, with no override path except through a documented human exception — this was non-negotiable given regulatory risk.",
   "Would add outcome-based strategy refinement earlier; v1 used static diagnosis-to-offer mapping rather than learning which offers actually worked for which diagnosed cause.",
   "Hardship eligibility checks needed broader data (beyond payment history) — would integrate income/employment-change signals earlier to catch hardship cases proactively rather than reactively.",
   "Complaint-driver analysis after launch showed most complaints came from contact-frequency edge cases across multiple accounts held by the same customer; added cross-account contact-frequency aggregation.",
 ],
},
{
 "id": 14, "slug": "ma-due-diligence",
 "title": "Mergers & Acquisitions Due Diligence",
 "pattern": "hierarchical",
 "problem": (
   "M&A due diligence requires reviewing thousands of contracts, financial records, and disclosures across "
   "legal, financial, and operational workstreams within a compressed deal timeline. Deal teams (bankers, "
   "lawyers, consultants) spend enormous hours on document review that a hierarchical agent team can accelerate "
   "while flagging deal-relevant risks for senior dealmakers."
 ),
 "top": "Due Diligence Orchestrator Agent",
 "mid_layer": ["Legal Workstream Manager Agent", "Financial Workstream Manager Agent", "Commercial/Operational Workstream Manager Agent"],
 "leaves_by_mid": [
   ["Material Contract Review Agent", "Litigation & Liability Search Agent", "IP/Regulatory Compliance Agent"],
   ["Financial Statement Quality-of-Earnings Agent", "Debt/Covenant Review Agent"],
   ["Customer Concentration Analysis Agent", "Key-Person/Change-of-Control Risk Agent"],
 ],
 "actions": ["Due Diligence Findings Report", "Deal Risk Register Update", "Red-Flag Escalation to Deal Lead"],
 "agents_table": [
   ("Due Diligence Orchestrator", "Coordinates the three workstream managers and consolidates findings into a unified risk register"),
   ("Legal Workstream Manager", "Oversees contract, litigation, and IP/regulatory sub-agents"),
   ("Financial Workstream Manager", "Oversees quality-of-earnings and debt/covenant sub-agents"),
   ("Material Contract Review Agent", "Reviews key contracts for change-of-control clauses, assignment restrictions, and unusual terms"),
   ("Financial Statement Quality-of-Earnings Agent", "Identifies one-time items, revenue recognition issues, and normalized EBITDA adjustments"),
   ("Customer Concentration Analysis Agent", "Quantifies revenue concentration and contract-renewal risk among top customers"),
 ],
 "tech_table": [
   ("Document ingestion", "Virtual data room (VDR) integration with bulk document extraction (docx/pdf skills)"),
   ("Contract analysis", "Claude with clause-taxonomy extraction, similar to Use Case 9's contract review agent"),
   ("Financial analysis", "Structured financial data extraction + quality-of-earnings adjustment modeling"),
   ("Orchestration", "Hierarchical LangGraph processing documents in parallel across workstreams"),
   ("Risk register", "Structured findings database with severity/materiality tagging"),
   ("Litigation search", "Legal database API (PACER, Westlaw) integration for litigation history"),
   ("Reporting", "Auto-generated due diligence report (docx/pptx skills) for deal committee"),
   ("Security", "Strict access controls and data-room-level audit logging given deal confidentiality"),
 ],
 "retrospective": [
   "Would build the risk-register consolidation and de-duplication logic earlier; findings initially overlapped heavily across workstreams (e.g., a contract flagged by both legal and commercial agents) without a clear reconciliation process.",
   "Deal teams valued materiality-ranked findings far more than exhaustive findings lists — added explicit materiality scoring after initial report was seen as overwhelming.",
   "Confidentiality/access control needed to be workstream-specific (not all deal team members should see all findings) — retrofitted this after an internal information-barrier concern.",
   "Quality-of-earnings analysis benefited enormously from historical deal comparables as few-shot grounding — would build this comparables library from the start.",
 ],
},
{
 "id": 15, "slug": "esg-investment-screening",
 "title": "ESG Investment Screening & Compliance",
 "pattern": "pipeline",
 "problem": (
   "Asset managers must screen potential investments against ESG mandates, exclusionary criteria, and disclosure "
   "regulations (SFDR, SEC climate rules) that vary by fund. Manually cross-referencing company ESG data against "
   "each fund's specific policy is slow and inconsistent across analysts. A pipeline agent can screen the entire "
   "investable universe against every fund's specific ESG policy continuously."
 ),
 "stages": ["ESG Data Aggregation Agent", "Fund Policy Interpretation Agent", "Exclusion/Inclusion Screening Agent",
            "Controversy Monitoring Agent", "Disclosure Report Generation Agent"],
 "actions": ["Portfolio Compliance Alert", "Fund Fact Sheet ESG Section Update", "Regulatory ESG Disclosure Filing"],
 "agents_table": [
   ("ESG Data Aggregation Agent", "Consolidates ESG ratings/data from multiple providers (MSCI, Sustainalytics, company disclosures)"),
   ("Fund Policy Interpretation Agent", "Extracts each fund's specific exclusionary and inclusionary ESG criteria from its prospectus/policy documents"),
   ("Exclusion/Inclusion Screening Agent", "Screens holdings and candidate investments against each fund's specific policy"),
   ("Controversy Monitoring Agent", "Continuously monitors for new ESG controversies (labor violations, environmental incidents) affecting held companies"),
   ("Disclosure Report Generation Agent", "Generates SFDR/SEC-compliant ESG disclosure reports per fund"),
 ],
 "tech_table": [
   ("ESG data", "MSCI ESG / Sustainalytics / Bloomberg ESG data feeds"),
   ("Policy extraction", "Claude + RAG over fund prospectus and ESG policy documents"),
   ("Screening logic", "Rules engine applying fund-specific inclusion/exclusion criteria"),
   ("Controversy monitoring", "News/controversy feed monitoring (RepRisk) with real-time alerting"),
   ("Orchestration", "Airflow pipeline running daily screening across the full fund lineup"),
   ("Disclosure generation", "Automated SFDR Annex/SEC climate-disclosure report generation (docx/pdf skills)"),
   ("Portfolio integration", "Integration with portfolio management system (Aladdin/Charles River) for compliance blocking"),
   ("Audit", "Full traceability from fund policy clause to screening decision for regulatory examination"),
 ],
 "retrospective": [
   "Fund policy interpretation needed compliance officer sign-off per fund before automation went live — ESG policy language is often ambiguous and getting it wrong has regulatory and reputational consequences.",
   "Would add the controversy monitoring agent earlier; a held company's labor controversy went undetected for weeks in the initial rollout because screening only ran against static data.",
   "Different ESG data providers frequently disagreed on ratings for the same company — added an explicit multi-provider disagreement flag rather than silently picking one source.",
   "Greenwashing risk meant disclosure report language needed careful, conservative grounding — added strict fact-citation requirements after internal legal review.",
 ],
},
{
 "id": 16, "slug": "treasury-cash-liquidity-forecasting",
 "title": "Treasury Cash Management & Liquidity Forecasting",
 "pattern": "orchestrator-worker",
 "problem": (
   "Corporate and bank treasury functions need accurate, near-real-time visibility into cash positions across "
   "many accounts/entities/currencies to optimize liquidity, meet regulatory liquidity ratios, and avoid costly "
   "overdrafts or idle cash. Manual consolidation across banking relationships and business units introduces lag "
   "and error into decisions that need to happen same-day."
 ),
 "orchestrator": "Treasury Liquidity Orchestrator Agent",
 "workers": ["Cash Position Aggregation Agent", "Cash Flow Forecasting Agent", "FX Exposure Agent",
             "Intercompany Netting Agent", "Investment/Sweep Optimization Agent"],
 "data_sources": ["Bank Account Statements (SWIFT/API feeds)", "AP/AR Forecast Data", "FX Rate Feeds", "Intercompany Loan Ledger"],
 "actions": ["Automated Cash Sweep/Investment Instruction", "FX Hedge Recommendation", "Liquidity Risk Dashboard"],
 "human_gate": "Treasurer Approval for Investment/Hedge Actions Above Threshold",
 "agents_table": [
   ("Treasury Liquidity Orchestrator", "Consolidates all agent outputs into a single global cash position and optimal-use recommendation"),
   ("Cash Position Aggregation Agent", "Pulls real-time balances across all bank accounts/entities/currencies via SWIFT/API"),
   ("Cash Flow Forecasting Agent", "Forecasts near-term inflows/outflows from AP/AR pipelines and known obligations"),
   ("FX Exposure Agent", "Calculates net FX exposure across entities and flags hedging needs"),
   ("Intercompany Netting Agent", "Optimizes intercompany settlement to minimize cross-border transfer costs and FX conversions"),
   ("Investment/Sweep Optimization Agent", "Recommends optimal allocation of excess cash across sweep accounts/short-term investments"),
 ],
 "tech_table": [
   ("Bank connectivity", "SWIFT MT/MX and bank API aggregation (via a TMS like Kyriba/GTreasury)"),
   ("Forecasting", "ML-based cash flow forecasting incorporating AP/AR system data"),
   ("FX management", "Real-time FX rate feeds + exposure netting calculation"),
   ("Orchestration", "LangGraph supervisor combining position, forecast, and optimization agents"),
   ("Optimization", "Linear programming for optimal cash allocation across sweep/investment vehicles"),
   ("Execution", "Automated payment/investment instruction generation with bank API execution"),
   ("Compliance", "Segregation-of-duties enforcement — no single agent both recommends and executes above threshold"),
   ("Dashboard", "Real-time global liquidity position dashboard for treasury team"),
 ],
 "retrospective": [
   "Segregation of duties (recommend vs. execute, with independent approval) was built in from the start given the direct financial-movement risk — this proved essential during a vendor API bug that would have caused an erroneous sweep.",
   "Cash flow forecasting accuracy was heavily dependent on AP/AR system data quality; would invest in data-quality validation agents earlier rather than assuming clean upstream data.",
   "Would add scenario stress-testing (e.g., a major customer payment delay) to the forecasting agent from the start, not just point forecasts.",
   "Cross-currency netting optimization needed real transfer-cost data per banking corridor, which was more heterogeneous than initially modeled — required significant refinement post-launch.",
 ],
},
{
 "id": 17, "slug": "insider-trading-surveillance",
 "title": "Insider Trading & Market Abuse Surveillance",
 "pattern": "debate-critique",
 "problem": (
   "Detecting insider trading and market manipulation requires correlating trading activity with material "
   "non-public information (MNPI) access, communications, and timing — a task prone to both false positives "
   "(coincidental profitable trades) and false negatives (sophisticated evasion). A proposer/critic pair "
   "improves the precision of surveillance alerts before they reach compliance officers, who face significant "
   "regulatory scrutiny on both over- and under-reporting."
 ),
 "proposer": "Suspicious Trading Pattern Proposer Agent",
 "critic": "Alternative Explanation Critic Agent",
 "arbiter": "Surveillance Case Arbiter Agent",
 "refs": ["Trading Activity Data", "MNPI Access Logs (deal rooms, restricted lists)", "Communications Surveillance (email/chat)",
          "Corporate Event Calendar (earnings, M&A announcements)"],
 "actions": ["Compliance Officer Case Assignment", "Regulatory Referral (SEC/FCA)", "Employee Trading Restriction"],
 "agents_table": [
   ("Suspicious Trading Pattern Proposer Agent", "Flags trades with unusual timing/size relative to subsequent material announcements and the trader's MNPI access"),
   ("Alternative Explanation Critic Agent", "Searches for legitimate explanations (scheduled trading plan, sector-wide movement, pre-existing position)"),
   ("Surveillance Case Arbiter Agent", "Weighs both agents' findings into a final case priority and evidence summary for compliance"),
   ("Communications Correlation Agent", "Searches surveilled communications for contemporaneous discussion of the relevant MNPI"),
   ("Restricted List Cross-Reference Agent", "Checks whether the trader/entity was on a restricted or watch list at the time of trading"),
 ],
 "tech_table": [
   ("Trade surveillance", "Existing trade surveillance platform (Nasdaq SMARTS/ACA) as the alert and data source"),
   ("MNPI access logs", "Deal-room and restricted-list access logging integrated into the analysis"),
   ("Communications surveillance", "Email/chat surveillance platform (Behavox/Theta Lake) with NLP-based topic detection"),
   ("Proposer/critic reasoning", "Two independent Claude passes with opposing objectives, similar in design to Use Case 7 (telecom fraud)"),
   ("Arbitration", "Structured evidence-weighting model, human-calibrated against historical confirmed cases"),
   ("Case management", "Compliance case management system integration"),
   ("Regulatory filing", "Automated SAR/STOR (Suspicious Transaction and Order Report) drafting for confirmed cases"),
   ("Audit", "Full evidentiary chain retained given the severity of insider-trading allegations"),
 ],
 "retrospective": [
   "Kept the critic agent fully independent of the proposer's reasoning (separate context, no shared framing) — this design choice, carried over from the telecom fraud use case, was equally critical here to avoid confirmation bias.",
   "Communications NLP had high false-positive rates on ordinary business language about the same companies; would invest more in contextual disambiguation before broad rollout.",
   "Compliance officers wanted the arbiter to explicitly state what evidence was *not* found (e.g., no communications correlation) alongside what was, to support both escalation and clearance decisions.",
   "Given the severity of false accusations, added a mandatory dual-compliance-officer review before any regulatory referral, beyond just the agent arbitration.",
 ],
},
{
 "id": 18, "slug": "complaint-handling-regulatory-compliance",
 "title": "Customer Complaint Handling (Regulatory Compliance)",
 "pattern": "hierarchical",
 "problem": (
   "Financial institutions must handle customer complaints within strict regulatory timeframes (e.g., CFPB, FCA "
   "8-week rules) with proper categorization, root-cause tracking, and redress calculation, or face fines and "
   "consent orders. Manual complaint handling struggles with consistent categorization and timely, adequate "
   "redress determination across high volumes."
 ),
 "top": "Complaint Handling Orchestrator Agent",
 "mid_layer": ["Complaint Triage Manager Agent", "Redress Determination Manager Agent"],
 "leaves_by_mid": [
   ["Complaint Categorization Agent", "Regulatory Deadline Tracking Agent", "Vulnerable Customer Identification Agent"],
   ["Root-Cause Investigation Agent", "Redress Calculation Agent"],
 ],
 "actions": ["Customer Redress Payment", "Regulatory Complaint Log Update", "Root-Cause Systemic Fix Referral"],
 "agents_table": [
   ("Complaint Handling Orchestrator", "Routes each complaint through triage and redress workstreams, tracking regulatory deadlines end-to-end"),
   ("Complaint Triage Manager", "Oversees categorization, deadline-tracking, and vulnerable-customer sub-agents"),
   ("Redress Determination Manager", "Oversees root-cause investigation and redress-calculation sub-agents"),
   ("Complaint Categorization Agent", "Classifies the complaint per regulatory taxonomy (e.g., FCA's complaint categories)"),
   ("Vulnerable Customer Identification Agent", "Flags indicators of customer vulnerability requiring enhanced care per regulatory guidance"),
   ("Redress Calculation Agent", "Computes fair redress (refund, compensation, corrective action) per the root cause and regulatory guidance"),
 ],
 "tech_table": [
   ("Complaint intake", "Omnichannel intake (call, email, letter, app) normalized into a case management system"),
   ("Categorization", "LLM classifier grounded in the regulator's official complaint taxonomy"),
   ("Deadline tracking", "Rules engine encoding jurisdiction-specific regulatory response deadlines"),
   ("Vulnerability detection", "Careful, conservative classifier flagging vulnerability indicators for enhanced-care routing to trained staff"),
   ("Root-cause investigation", "Tool-calling agent gathering evidence across relevant systems (similar pattern to Use Case 10, telecom billing disputes)"),
   ("Redress calculation", "Deterministic rules engine, not LLM-generated, for financial redress accuracy"),
   ("Orchestration", "Hierarchical LangGraph with hard SLA-deadline alerting"),
   ("Regulatory reporting", "Automated complaint-log submission per regulator format"),
 ],
 "retrospective": [
   "Vulnerable-customer identification was deliberately built conservative (flag more, not less) and always routes to a trained human, never a fully automated resolution — given the sensitivity, this was a hard requirement from the start.",
   "Would add a systemic-issue detection agent earlier (patterns across many complaints pointing to a product/process bug) — this was originally out of scope but proved to be the highest-value output for the business.",
   "Kept redress calculation in deterministic rules engines after seeing the billing-dispute lesson (Telecom Use Case 10) about not trusting generative math for financial amounts.",
   "Regulatory deadline tracking needed buffer time built in for human review steps, not just the raw regulatory deadline — an early near-miss on an 8-week case prompted this change.",
 ],
},
{
 "id": 19, "slug": "trade-settlement-reconciliation",
 "title": "Trade Settlement Reconciliation",
 "pattern": "pipeline",
 "problem": (
   "Post-trade settlement requires matching trade details across counterparties, custodians, and internal books "
   "before T+1/T+2 settlement deadlines. Breaks (mismatches) require rapid investigation to avoid settlement "
   "failures, which carry financial and regulatory penalties. An automated pipeline can triage and resolve the "
   "majority of routine breaks well within settlement windows."
 ),
 "stages": ["Trade Matching Agent", "Break Classification Agent", "Root-Cause Investigation Agent",
            "Auto-Resolution Agent", "Settlement Confirmation Agent"],
 "actions": ["Custodian/Counterparty Instruction Correction", "Settlement Confirmation", "Operations Team Escalation for Unresolved Breaks"],
 "agents_table": [
   ("Trade Matching Agent", "Matches internal trade records against counterparty/custodian confirmations across key fields"),
   ("Break Classification Agent", "Classifies mismatches by type (price, quantity, settlement date, static data) and severity"),
   ("Root-Cause Investigation Agent", "Traces the break back to its source (trade booking error, static data mismatch, corporate action)"),
   ("Auto-Resolution Agent", "Resolves well-understood break types automatically per pre-approved resolution rules"),
   ("Settlement Confirmation Agent", "Confirms final settlement instructions once the break is resolved"),
 ],
 "tech_table": [
   ("Trade matching", "Automated matching engine (similar to DTCC CTM) comparing trade legs across parties"),
   ("Break classification", "Rules + ML classifier trained on historical break categories"),
   ("Root-cause investigation", "Tool-calling agent querying trade booking, static data, and corporate-action systems"),
   ("Auto-resolution", "Deterministic resolution rules for known break types (e.g., standard settlement instruction updates)"),
   ("Orchestration", "Temporal workflow with T+1/T+2 deadline-aware prioritization"),
   ("LLM usage", "Claude for root-cause narrative and unresolved-break escalation summaries"),
   ("Settlement integration", "SWIFT messaging (MT54x series) for instruction confirmation"),
   ("Monitoring", "Break-aging dashboard prioritizing near-deadline unresolved breaks"),
 ],
 "retrospective": [
   "Would prioritize the deadline-aware triage logic (which breaks are closest to failing settlement) from day one rather than processing breaks in arrival order — this had the single biggest impact on reducing settlement fails.",
   "Auto-resolution rules were kept narrow and conservative initially (only the most common, lowest-risk break types); expanded gradually as confidence built, rather than attempting broad auto-resolution from launch.",
   "Static data quality (incorrect settlement instructions on file) was a bigger root cause than trade-booking errors — would invest more in static-data-quality agents relative to trade-matching sophistication.",
   "Corporate-action-driven breaks (dividends, splits) needed a dedicated sub-agent with calendar awareness — initially handled poorly as generic 'quantity mismatch' breaks.",
 ],
},
{
 "id": 20, "slug": "personalized-financial-advisory-nba",
 "title": "Personalized Financial Advisory & Next-Best-Action",
 "pattern": "debate-critique",
 "problem": (
   "Retail banks and wealth platforms want to proactively recommend relevant financial actions (refinancing, "
   "savings goals, investment products) to customers, but purely revenue-optimized recommendation engines risk "
   "recommending products that don't serve the customer's actual financial interest, creating suitability and "
   "trust issues. A proposer/critic design, mirroring the telecom upsell use case, balances business value "
   "against genuine customer benefit."
 ),
 "proposer": "Revenue-Optimized Product Recommendation Agent",
 "critic": "Customer Financial Wellbeing Critic Agent",
 "arbiter": "Next-Best-Action Arbiter Agent",
 "refs": ["Account & Transaction History", "Product Catalog & Pricing", "Financial Goals (if declared)", "Life-Event Signals"],
 "actions": ["In-App Personalized Recommendation", "Advisor Outreach Prompt", "Recommendation Outcome Tracking"],
 "agents_table": [
   ("Revenue-Optimized Product Recommendation Agent", "Proposes the product/action with highest expected revenue given the customer's profile"),
   ("Customer Financial Wellbeing Critic Agent", "Checks whether the proposal genuinely improves the customer's financial position (e.g., refinancing that actually lowers their cost)"),
   ("Next-Best-Action Arbiter Agent", "Balances revenue and wellbeing signals into a final recommendation with a transparent rationale"),
   ("Life-Event Detection Agent", "Detects signals of major life events (home purchase, new job, retirement approaching) from transaction patterns"),
   ("Outcome Tracking Agent", "Monitors whether accepted recommendations actually improved the customer's financial metrics over time"),
 ],
 "tech_table": [
   ("Transaction analysis", "Categorization and pattern-detection ML on transaction history"),
   ("Recommendation proposer", "Uplift/propensity model for product recommendation, same architecture pattern as Telecom Use Case 20"),
   ("Wellbeing critic", "Rules + LLM reasoning checking financial-benefit criteria (e.g., total-cost comparison for refinancing)"),
   ("Arbitration", "Multi-objective scoring balancing revenue and a mandatory minimum wellbeing-benefit threshold"),
   ("Life-event detection", "Sequence-pattern model on transaction categories signaling major life changes"),
   ("Delivery", "In-app notification + advisor CRM integration for high-value/complex recommendations"),
   ("Compliance", "Suitability documentation auto-generated per recommendation for regulatory record-keeping"),
   ("Outcome tracking", "Longitudinal tracking of accepted-recommendation customer financial outcomes"),
 ],
 "retrospective": [
   "Set a hard minimum wellbeing-benefit threshold that the arbiter cannot override for revenue reasons — this is the direct lesson carried from watching purely revenue-optimized recommenders erode long-term trust in comparable systems.",
   "Would build the outcome-tracking agent from the start rather than adding it later; without it, there was no way to prove the wellbeing critic was actually improving customer outcomes versus just suppressing offers.",
   "Life-event detection had real customer trust upside (e.g., surfacing a genuinely useful savings product after a life change) but needed careful pacing to avoid feeling surveillance-like — added explicit customer transparency about why a recommendation appeared.",
   "Suitability documentation requirements meant the arbiter's rationale had to be far more structured/citation-grounded than an initial free-text version allowed.",
 ],
},
]
