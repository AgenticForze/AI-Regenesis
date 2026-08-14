# -*- coding: utf-8 -*-
BSSOSS = [
{
 "id": 1, "slug": "order-to-activation-orchestration",
 "title": "Order-to-Activation Orchestration",
 "pattern": "pipeline",
 "problem": (
   "A single customer order (e.g., broadband + mobile bundle with a new router) fans out into dozens of "
   "downstream tasks across CRM, product catalog, provisioning, network activation, and billing systems. "
   "Order orchestration engines today are largely static workflow engines that break silently when a product "
   "combination or a network element behaves unexpectedly, leaving orders stuck in fallout queues for days. "
   "An agentic order orchestrator can reason about failures in context and self-correct rather than just halting."
 ),
 "stages": ["Order Validation & Decomposition Agent", "Product-to-Service Mapping Agent",
            "Cross-Domain Provisioning Sequencing Agent", "Activation Confirmation Agent",
            "Billing Activation & First-Invoice Trigger Agent"],
 "actions": ["Order Management System (OMS) State Update", "Network Provisioning Trigger", "Customer Order-Status Notification"],
 "agents_table": [
   ("Order Validation & Decomposition Agent", "Validates the order against catalog rules and decomposes it into an ordered set of fulfillment tasks"),
   ("Product-to-Service Mapping Agent", "Maps commercial product/offer definitions to the technical service specifications each system needs"),
   ("Cross-Domain Provisioning Sequencing Agent", "Determines the correct execution order across CRM/network/billing to avoid race conditions (e.g., number must be ported before SIM activation)"),
   ("Activation Confirmation Agent", "Confirms successful activation at each domain and reconciles partial failures"),
   ("Billing Activation Agent", "Triggers billing-plan activation and proration only once service is confirmed live"),
 ],
 "tech_table": [
   ("Order capture", "CRM/eCommerce front-end (Salesforce Industries / Amdocs CRM)"),
   ("Product catalog", "TM Forum SID-based product catalog (Amdocs/Netcracker Catalog)"),
   ("Orchestration engine", "Temporal workflow with agent-based decision steps at each stage"),
   ("Provisioning APIs", "TM Forum Open API (TMF641 Service Ordering) calls into OSS activation systems"),
   ("LLM reasoning", "Claude for fallout diagnosis and next-best-recovery-action reasoning at each stage"),
   ("State tracking", "Order state machine persisted in a durable workflow store (Temporal/Camunda)"),
   ("Notification", "Customer status updates via SMS/app push tied to order milestones"),
   ("Observability", "End-to-end order tracing (OpenTelemetry) across all downstream systems"),
 ],
 "retrospective": [
   "Kept strict sequential staging (not parallel) after an early parallel-execution prototype created race conditions between number-porting and SIM activation — order matters more than speed here.",
   "Would add a fallout-pattern library from day one; the same handful of failure signatures (address mismatch, duplicate MSISDN, catalog version drift) accounted for most fallout and could have been auto-resolved sooner.",
   "Customers valued milestone-level status updates far more than a single 'processing' message — added granular status mapping after early NPS feedback.",
   "Would separate 'diagnose' and 'auto-fix' permissions per stage; early version let the agent both diagnose and silently retry indefinitely on some failure types, masking systemic catalog bugs.",
 ],
},
{
 "id": 2, "slug": "product-catalog-offer-management",
 "title": "Product Catalog & Offer Management Automation",
 "pattern": "hierarchical",
 "problem": (
   "Launching a new bundled offer requires coordinating pricing, eligibility rules, technical service "
   "specifications, and channel-specific presentation across a sprawling product catalog — a process that "
   "commercial teams describe as the single biggest bottleneck to speed-to-market. A hierarchical agent team "
   "spanning commercial and technical catalog domains can validate and publish new offers in hours instead of weeks."
 ),
 "top": "Catalog Publication Orchestrator",
 "mid_layer": ["Commercial Offer Manager Agent", "Technical Specification Manager Agent"],
 "leaves_by_mid": [
   ["Pricing & Discount Rule Agent", "Eligibility & Segment Targeting Agent", "Channel Presentation Agent"],
   ["Service Specification Mapping Agent", "Cross-Product Dependency Agent"],
 ],
 "actions": ["Product Catalog Publish (TMF620)", "Channel Content Management System Update", "Order Management Test-Order Validation"],
 "agents_table": [
   ("Catalog Publication Orchestrator", "Coordinates commercial and technical managers and gates final publication on cross-checks passing"),
   ("Commercial Offer Manager", "Oversees pricing, eligibility, and channel-presentation sub-agents"),
   ("Technical Specification Manager", "Oversees service-spec mapping and cross-product dependency sub-agents"),
   ("Pricing & Discount Rule Agent", "Validates the new offer's pricing against margin floors and existing discount stacking rules"),
   ("Eligibility & Segment Targeting Agent", "Encodes which customer segments/geographies can purchase the offer"),
   ("Cross-Product Dependency Agent", "Checks for conflicts with existing bundles (e.g., a device financing plan incompatible with a new SIM-only offer)"),
 ],
 "tech_table": [
   ("Catalog platform", "TM Forum TMF620 Product Catalog Management API"),
   ("Orchestration", "Hierarchical LangGraph with commercial/technical sub-graphs"),
   ("Pricing validation", "Rules engine encoding margin-floor and discount-stacking policy"),
   ("Dependency checking", "Graph-based product-relationship model (Neo4j) to detect bundle conflicts"),
   ("Test-order validation", "Automated synthetic order run through the OMS pipeline before go-live"),
   ("Channel publishing", "CMS/e-commerce integration for storefront and call-center script updates"),
   ("LLM usage", "Claude drafting customer-facing offer copy and internal launch-readiness summaries"),
   ("Governance", "Full approval-chain audit log (commercial + technical + legal sign-off)"),
 ],
 "retrospective": [
   "Would run the synthetic test-order validation earlier in the flow, not just before go-live — several offers passed catalog validation but failed silently in the OMS pipeline, discovered too late in v1.",
   "Cross-product dependency checking had the highest ROI of any sub-agent; would prioritize building this before pricing/eligibility automation if starting over.",
   "Channel presentation agent initially generated inconsistent copy across web/app/call-center for the same offer — added a single shared offer-narrative source of truth all channels pull from.",
   "Add a post-launch monitoring agent that watches early order volume/fallout rate for a new offer and can auto-pause publication if fallout spikes.",
 ],
},
{
 "id": 3, "slug": "revenue-assurance-leakage-detection",
 "title": "Revenue Assurance & Leakage Detection",
 "pattern": "blackboard",
 "problem": (
   "Revenue leakage — unbilled usage, mis-rated services, un-activated but delivered services, discount "
   "misapplication — typically runs 1-3% of telecom revenue and is notoriously hard to find because evidence is "
   "scattered across mediation, rating, billing, and provisioning systems. A blackboard of specialized leakage "
   "detectors, synthesized by a controller, surfaces high-confidence, high-value leakage cases for recovery."
 ),
 "controller": "Revenue Assurance Controller Agent",
 "store_name": "Revenue Assurance Blackboard (usage, rating, billing, provisioning cross-references)",
 "agents": ["Usage-to-Billing Reconciliation Agent", "Discount Misapplication Agent", "Un-activated Service Agent",
            "Rating Configuration Drift Agent", "Zero-Usage/Zero-Billing Anomaly Agent"],
 "actions": ["Leakage Case for Finance Review", "Automated Re-billing/Correction", "Systemic Root-Cause Ticket to Engineering"],
 "agents_table": [
   ("Revenue Assurance Controller Agent", "Synthesizes blackboard findings into prioritized leakage cases ranked by recovery value"),
   ("Usage-to-Billing Reconciliation Agent", "Compares network usage records (mediation output) against what was actually billed"),
   ("Discount Misapplication Agent", "Detects discounts applied outside eligibility rules or beyond promotional end-dates"),
   ("Un-activated Service Agent", "Finds services provisioned and delivered in the network but never activated in billing"),
   ("Rating Configuration Drift Agent", "Detects rating engine configuration changes that silently under-charge a usage category"),
   ("Zero-Usage/Zero-Billing Anomaly Agent", "Flags active subscriptions generating usage but zero corresponding billing records"),
 ],
 "tech_table": [
   ("Data sources", "Mediation platform, rating engine, billing system, and provisioning/OSS inventory feeds"),
   ("Blackboard store", "Columnar data warehouse (Snowflake/BigQuery) as the shared cross-reference store"),
   ("Reconciliation logic", "Large-scale SQL/Spark reconciliation jobs feeding structured findings to the blackboard"),
   ("Controller reasoning", "Claude synthesizing multi-agent findings into a prioritized, dollar-quantified leakage report"),
   ("Configuration drift detection", "Diff-based monitoring of rating engine configuration changes over time"),
   ("Case management", "Revenue assurance case tracking (in-house or RA platform like cVidya/Subex)"),
   ("Correction execution", "Automated re-billing trigger for high-confidence, policy-approved correction types"),
   ("Reporting", "Finance-facing dashboard quantifying recovered vs. at-risk revenue"),
 ],
 "retrospective": [
   "Would keep automated re-billing scoped to only the highest-confidence, previously-human-validated leakage patterns — an early broader auto-correction attempt risked customer-facing billing errors in the other direction.",
   "Rating configuration drift detection caught issues no other agent could see (a silent config push, not a data mismatch) — would build this sub-agent earlier given its outsized impact.",
   "Blackboard cross-referencing across four large systems was the main performance bottleneck; would design a pre-aggregated daily snapshot layer from the start instead of live cross-system joins.",
   "Finance wanted leakage cases grouped by root cause (not just by account) to prioritize systemic fixes over one-off corrections — restructured the controller's output format after this feedback.",
 ],
},
{
 "id": 4, "slug": "order-fallout-detection-recovery",
 "title": "Order Fallout Detection & Auto-Recovery",
 "pattern": "event-swarm",
 "problem": (
   "Orders that stall mid-fulfillment ('fallout') due to system timeouts, data mismatches, or catalog/network "
   "inconsistencies pile up in manual work queues, delaying customer activations for days. Most fallout falls "
   "into a small number of recurring, well-understood patterns that a swarm of reactive agents can detect and "
   "resolve automatically the moment an order-state event indicates trouble, rather than waiting for a nightly "
   "batch report."
 ),
 "bus_name": "Order State Event Bus",
 "agents": ["Timeout/Retry Agent", "Data Mismatch Detection Agent", "Duplicate Order Detection Agent",
            "Catalog-Version Drift Agent", "Novel Fallout Escalation Agent"],
 "actions": ["Automated Order Retry/Correction", "Fallout Queue Update", "Escalation to Order Management Specialist"],
 "agents_table": [
   ("Timeout/Retry Agent", "Detects orders stalled on a downstream system timeout and retries with backoff before escalating"),
   ("Data Mismatch Detection Agent", "Identifies field-level mismatches (address format, MSISDN format) between systems causing rejection"),
   ("Duplicate Order Detection Agent", "Detects and merges duplicate orders created by customer retries or channel double-submission"),
   ("Catalog-Version Drift Agent", "Flags fallout caused by a catalog change that orphaned in-flight orders on the old version"),
   ("Novel Fallout Escalation Agent", "Recognizes fallout patterns not matching any known signature and routes to a human specialist with full context"),
 ],
 "tech_table": [
   ("Event bus", "Kafka topics per order-state transition"),
   ("Agent runtime", "Event-driven microservices (Python asyncio) per fallout-pattern agent"),
   ("Pattern matching", "Rules engine for known fallout signatures + embedding-similarity search against historical resolved cases"),
   ("Data correction", "Tool-calling into CRM/OMS APIs for approved auto-correction actions"),
   ("Novelty detection", "Anomaly scoring on fallout event feature vectors to catch unseen patterns"),
   ("Escalation", "Structured case handoff to order management specialists via ServiceNow/Jira"),
   ("Guardrails", "Retry-count caps and blast-radius limits per correction type"),
   ("Analytics", "Fallout-rate and auto-resolution-rate dashboard by fallout category"),
 ],
 "retrospective": [
   "Would add hard retry-count caps from day one — an early version retried a doomed order dozens of times against a permanently-broken downstream dependency before a cap was added.",
   "Catalog-version drift turned out to be a much bigger fallout driver than expected; would build this detector earlier rather than treating it as a rare edge case.",
   "Novel fallout escalation needed richer context handoff (full event history, not just the current state) — early escalations left specialists re-investigating from scratch.",
   "Would track auto-resolution accuracy per pattern type over time and auto-disable a pattern's automation if its false-fix rate rises, rather than assuming static reliability.",
 ],
},
{
 "id": 5, "slug": "network-inventory-discovery-reconciliation",
 "title": "Network Inventory Discovery & Reconciliation",
 "pattern": "orchestrator-worker",
 "problem": (
   "OSS inventory systems drift out of sync with the physical/logical network over time (undocumented field "
   "changes, decommissioned equipment never removed, ghost records), which cascades into failed provisioning, "
   "inaccurate capacity planning, and wasted truck-rolls. A coordinated agent team can continuously discover "
   "actual network state and reconcile it against the system-of-record inventory."
 ),
 "orchestrator": "Inventory Reconciliation Orchestrator Agent",
 "workers": ["Physical Layer Discovery Agent", "Logical/Service Layer Discovery Agent", "Ghost Record Detection Agent",
             "Discrepancy Classification & Impact Agent"],
 "data_sources": ["EMS/NMS Live Network State", "OSS Inventory System of Record", "Field Technician Close-out Reports"],
 "actions": ["Inventory System Auto-Correction", "Field Audit Work Order for Unresolvable Discrepancies", "Capacity Planning Data Refresh"],
 "human_gate": "Inventory Manager Approval for Bulk Corrections",
 "agents_table": [
   ("Inventory Reconciliation Orchestrator", "Coordinates discovery agents and produces a prioritized reconciliation plan"),
   ("Physical Layer Discovery Agent", "Queries EMS/NMS for actual installed equipment and compares to inventory records"),
   ("Logical/Service Layer Discovery Agent", "Discovers actual active services/circuits and compares to the logical inventory"),
   ("Ghost Record Detection Agent", "Identifies inventory records with no corresponding live network element (decommissioned, never removed)"),
   ("Discrepancy Classification & Impact Agent", "Classifies each discrepancy's likely cause and business impact (blocks provisioning vs. cosmetic)"),
 ],
 "tech_table": [
   ("Network discovery", "SNMP/NETCONF/gNMI polling plus vendor EMS APIs for live state"),
   ("Inventory system", "OSS inventory platform (Netcracker/Amdocs/Blue Planet) as system of record"),
   ("Orchestration", "LangGraph supervisor running discovery agents on a scheduled sweep cadence"),
   ("Discrepancy matching", "Entity-resolution matching (fuzzy key matching on serial numbers/circuit IDs)"),
   ("Impact classification", "Claude reasoning over discrepancy type and downstream provisioning dependency graph"),
   ("Correction execution", "Automated low-risk correction (e.g., updating a firmware version field) vs. human-gated bulk changes"),
   ("Field integration", "Technician close-out report parsing to catch undocumented field changes"),
   ("Reporting", "Inventory accuracy score trend dashboard by network domain"),
 ],
 "retrospective": [
   "Would gate all bulk/high-volume corrections behind human approval from the start — an early auto-correction run on ghost records deleted a handful of legitimately-planned-but-not-yet-installed equipment records.",
   "Field technician close-out report parsing caught undocumented changes no network polling could see; would prioritize this data source earlier.",
   "Discrepancy impact classification (does this block provisioning or is it cosmetic) was essential for prioritization — v1 treated all discrepancies equally and buried the important ones.",
   "Reconciliation sweep frequency needed to vary by network domain — access-layer equipment changes far more often than core, and a uniform sweep schedule wasted compute on stable domains.",
 ],
},
{
 "id": 6, "slug": "mediation-cdr-xdr-processing",
 "title": "Mediation & CDR/xDR Processing Pipeline",
 "pattern": "pipeline",
 "problem": (
   "Mediation systems must ingest, validate, correlate, and transform billions of daily call/data/event detail "
   "records (CDRs/xDRs) from heterogeneous network elements into a normalized format for rating and billing. "
   "Format drift from vendor firmware updates and silent data-quality issues cause downstream rating errors that "
   "are expensive to trace back. An agent pipeline adds intelligent validation and self-describing error handling "
   "on top of the raw mediation engine."
 ),
 "stages": ["Record Ingestion & Format Detection Agent", "Data Quality Validation Agent", "Correlation & De-duplication Agent",
            "Normalization & Enrichment Agent", "Exception Routing Agent"],
 "actions": ["Rating Engine Feed", "Data Quality Exception Dashboard", "Vendor Format-Change Alert"],
 "agents_table": [
   ("Record Ingestion & Format Detection Agent", "Identifies the source format/vendor variant of incoming records and routes to the right parser"),
   ("Data Quality Validation Agent", "Validates record completeness and field-level sanity (e.g., call duration within plausible bounds)"),
   ("Correlation & De-duplication Agent", "Correlates partial records (e.g., call-leg records) and removes network-generated duplicates"),
   ("Normalization & Enrichment Agent", "Converts to the canonical xDR schema and enriches with subscriber/service context"),
   ("Exception Routing Agent", "Routes malformed or unresolvable records to the appropriate exception queue with a diagnosis"),
 ],
 "tech_table": [
   ("Mediation engine", "Existing mediation platform (Openwave/Digital Route MediationZone) as the base processing engine"),
   ("Format detection", "Schema-inference classifier trained on known vendor CDR/xDR variants"),
   ("Data quality rules", "Great Expectations-style validation rules layered with an LLM fallback for ambiguous cases"),
   ("Correlation logic", "Stream-processing correlation (Apache Flink) for multi-leg record stitching"),
   ("Orchestration", "Pipeline implemented as a Flink/Kafka Streams topology with agent-based exception-handling steps"),
   ("Enrichment", "Real-time subscriber/service lookup against the customer 360 store (see BSS/OSS Use Case 8)"),
   ("Exception diagnosis", "Claude generating a plain-language diagnosis for engineering when a new vendor format variant appears"),
   ("Monitoring", "Record-loss and data-quality-exception-rate dashboards per network element type"),
 ],
 "retrospective": [
   "Would add automatic vendor format-change alerting from day one — a firmware update on one vendor's equipment silently changed a field format and went undetected for two billing cycles in v1.",
   "Correlation/de-duplication was the highest-defect-risk stage; would invest in more exhaustive test coverage here specifically given how directly it affects billing accuracy.",
   "Exception routing needed clearer severity tiering — early version treated a single malformed record the same as a systemic feed-level failure, burying critical alerts in noise.",
   "Enrichment lookups against the customer 360 store added meaningful latency at billion-record scale; would pre-compute and cache enrichment context rather than looking it up per record.",
 ],
},
{
 "id": 7, "slug": "charging-rating-anomaly-detection",
 "title": "Charging & Rating Engine Anomaly Detection",
 "pattern": "debate-critique",
 "problem": (
   "Real-time charging and rating engines occasionally under- or over-charge due to configuration errors, "
   "promo-interaction bugs, or edge-case usage patterns — costly in direct revenue impact and in customer trust "
   "when overcharges occur. A proposer/critic pair, similar in spirit to fraud detection, distinguishes genuine "
   "rating anomalies from legitimate edge cases (e.g., a valid but unusual promo stacking) before alerting revenue "
   "assurance or auto-correcting."
 ),
 "proposer": "Rating Anomaly Proposer Agent",
 "critic": "Legitimate Rating Explanation Critic Agent",
 "arbiter": "Rating Anomaly Arbiter Agent",
 "refs": ["Real-Time Charging Records", "Rate Plan & Promo Configuration", "Historical Rating Baseline", "Customer Plan/Entitlement Data"],
 "actions": ["Auto-Correction of Confirmed Rating Error", "Revenue Assurance Case", "Rating Engine Configuration Alert"],
 "agents_table": [
   ("Rating Anomaly Proposer Agent", "Flags charging events that deviate from expected rate-plan pricing given usage and plan terms"),
   ("Legitimate Rating Explanation Critic Agent", "Searches for a legitimate explanation — an active promo, a plan change mid-cycle, an approved manual adjustment"),
   ("Rating Anomaly Arbiter Agent", "Weighs both agents' evidence into a confirmed-error vs. legitimate-variance determination"),
   ("Configuration Drift Cross-Check Agent", "Checks whether a recent rating engine configuration deployment correlates with the anomaly's onset"),
   ("Correction Execution Agent", "Applies approved auto-correction for confirmed, low-risk rating errors within policy limits"),
 ],
 "tech_table": [
   ("Charging platform", "Existing real-time charging system (Ericsson/Amdocs/Netcracker Convergent Charging) as the event source"),
   ("Baseline modeling", "Statistical baseline of expected charge amount per rate plan and usage profile"),
   ("Proposer/critic reasoning", "Two independently-prompted Claude passes, mirroring the design used in the AML and insider-trading use cases"),
   ("Configuration tracking", "Version-controlled rating configuration with deployment-time correlation analysis"),
   ("Arbitration", "Weighted evidence scoring calibrated against historically-confirmed rating errors"),
   ("Correction execution", "Automated micro-correction for small, high-confidence, policy-bounded cases only"),
   ("Case management", "Revenue assurance case system integration for anything above the auto-correction threshold"),
   ("Monitoring", "Rating-accuracy dashboard tracking both false-positive noise and confirmed-error recovery value"),
 ],
 "retrospective": [
   "Kept the critic agent's evidence search fully independent from the proposer, consistent with the design lesson from the AML and insider-trading use cases — shared context caused the same confirmation-bias problem here in early testing.",
   "Configuration-deployment correlation turned out to be the single strongest signal for confirmed errors; would surface deployment timestamps to the proposer as a first-class signal, not an afterthought sub-agent.",
   "Auto-correction threshold was initially too permissive on dollar amount — tightened significantly after realizing 'small per-event' errors summed to material revenue impact at scale.",
   "Would add customer-facing transparency for any correction that resulted in a customer credit, since customers noticed unexplained credit-memo line items and contacted support confused.",
 ],
},
{
 "id": 8, "slug": "customer-360-master-data-unification",
 "title": "Customer 360 / Master Data Unification",
 "pattern": "blackboard",
 "problem": (
   "Customer data is fragmented across CRM, billing, provisioning, loyalty, and support systems, each with its "
   "own partial and sometimes conflicting view of 'who this customer is.' Building a trustworthy unified customer "
   "profile in real time — needed for personalization, support, and fraud/risk decisions across many of this "
   "catalog's other use cases — requires synthesizing partial, conflicting evidence continuously as source systems "
   "change."
 ),
 "controller": "Customer 360 Synthesis Controller Agent",
 "store_name": "Customer Master Data Blackboard",
 "agents": ["Identity Resolution Agent", "Contact/Address Conflict Resolution Agent", "Product/Service Holdings Agent",
            "Preference & Consent Agent", "Data Quality Confidence Scoring Agent"],
 "actions": ["Unified Customer Profile API", "Downstream System Sync (CRM/Billing/Support)", "Data Steward Review Queue"],
 "agents_table": [
   ("Customer 360 Synthesis Controller Agent", "Watches the blackboard for new/conflicting source-system events and synthesizes the authoritative unified profile"),
   ("Identity Resolution Agent", "Resolves whether records across systems represent the same real-world customer/household"),
   ("Contact/Address Conflict Resolution Agent", "Determines the most current, trustworthy contact details when source systems disagree"),
   ("Product/Service Holdings Agent", "Maintains an accurate real-time view of everything the customer currently holds across product lines"),
   ("Preference & Consent Agent", "Consolidates marketing/communication consent and channel preferences, respecting the most restrictive valid consent"),
   ("Data Quality Confidence Scoring Agent", "Scores the overall profile's confidence/freshness so downstream consumers know how much to trust it"),
 ],
 "tech_table": [
   ("Source systems", "CRM, billing, provisioning, loyalty, and support platforms feeding change events"),
   ("Blackboard store", "Master data management platform (Informatica MDM/Reltio) as the shared entity store"),
   ("Identity resolution", "Probabilistic entity resolution (fuzzy matching + graph clustering) on customer identifiers"),
   ("Controller reasoning", "Claude synthesizing conflicting source-system evidence into a resolved profile field with a rationale"),
   ("Consent management", "Consent-tracking layer enforcing most-restrictive-wins logic for compliance (GDPR/TCPA)"),
   ("Sync mechanism", "Event-driven sync back to consuming systems via Kafka/CDC (change data capture)"),
   ("API layer", "TM Forum TMF629 Customer Management API exposing the unified profile"),
   ("Governance", "Data steward review workflow for low-confidence or high-impact conflicting fields"),
 ],
 "retrospective": [
   "Consent/preference conflicts needed a hard 'most restrictive wins' rule with no agent override — this was made non-negotiable after an early version optimistically resolved a consent conflict in favor of marketing reach.",
   "Identity resolution false-merges (incorrectly linking two different real customers) were far more damaging than false-splits, so would tune matching thresholds more conservatively from the start.",
   "Confidence scoring for the unified profile turned out to be as valuable to downstream consumers as the profile data itself — several other use cases in this catalog now check profile confidence before acting.",
   "Would build the data steward review queue earlier; without a clear human escalation path for genuinely ambiguous conflicts, the controller was pressured into low-confidence auto-resolutions in v1.",
 ],
},
{
 "id": 9, "slug": "subscription-lifecycle-entitlement",
 "title": "Subscription Lifecycle & Entitlement Management",
 "pattern": "hierarchical",
 "problem": (
   "Modern telecom offers bundle subscriptions (streaming partnerships, cloud storage, device insurance) whose "
   "entitlements must stay perfectly synchronized with billing state across upgrades, downgrades, suspensions, "
   "and cancellations — a coordination problem that grows combinatorially with each new partner integration. A "
   "hierarchical agent team keeps entitlement state correct across the subscription's full lifecycle."
 ),
 "top": "Subscription Lifecycle Orchestrator",
 "mid_layer": ["Internal Product Entitlement Manager Agent", "Third-Party Partner Entitlement Manager Agent"],
 "leaves_by_mid": [
   ["Plan Change Entitlement Agent", "Suspension/Resume Entitlement Agent"],
   ["Partner API Sync Agent", "Partner Billing Reconciliation Agent"],
 ],
 "actions": ["Entitlement System Update", "Partner Platform Provisioning Call", "Customer Notification of Entitlement Change"],
 "agents_table": [
   ("Subscription Lifecycle Orchestrator", "Tracks every subscription's lifecycle state and coordinates internal and partner entitlement managers on any change"),
   ("Internal Product Entitlement Manager", "Oversees entitlement changes for the operator's own bundled products"),
   ("Third-Party Partner Entitlement Manager", "Oversees synchronization with external partner platforms (streaming, cloud, insurance providers)"),
   ("Plan Change Entitlement Agent", "Updates entitlements correctly on upgrade/downgrade, handling proration and grandfathering rules"),
   ("Partner API Sync Agent", "Calls partner provisioning APIs to activate/deactivate the partner service in lockstep with billing state"),
   ("Partner Billing Reconciliation Agent", "Reconciles what the operator billed the customer against what it owes/is owed by the partner"),
 ],
 "tech_table": [
   ("Entitlement store", "Central entitlement management system (or extension of the OSS inventory platform)"),
   ("Orchestration", "Hierarchical LangGraph with an internal/partner split mirroring organizational ownership"),
   ("Partner integration", "Partner-specific REST/SOAP APIs, normalized through an internal adapter layer"),
   ("Proration logic", "Deterministic billing-proration rules engine, not LLM-generated, for calculation accuracy"),
   ("Reconciliation", "Scheduled reconciliation jobs comparing internal billing records against partner settlement statements"),
   ("Notification", "Customer-facing entitlement-change notifications (e.g., 'your streaming subscription is now active')"),
   ("Monitoring", "Entitlement drift dashboard flagging customers whose billing and entitlement state have diverged"),
   ("Audit", "Full change history per subscription for dispute resolution and partner settlement audit"),
 ],
 "retrospective": [
   "Would build the entitlement-drift monitoring dashboard from day one rather than discovering drift reactively through customer complaints — this became the most valuable proactive signal post-launch.",
   "Partner API reliability varied enormously; would design the Partner API Sync Agent with robust async retry/reconciliation from the start rather than assuming synchronous success.",
   "Kept proration math in a deterministic rules engine after seeing the same lesson play out in the billing-dispute and redress-calculation use cases elsewhere in this catalog.",
   "Grandfathering rules (customers on legacy plans keeping old entitlement terms) were undocumented tribal knowledge; would formalize this into the entitlement rules engine earlier instead of hardcoding exceptions ad hoc.",
 ],
},
{
 "id": 10, "slug": "number-portability-orchestration",
 "title": "Number Portability Orchestration",
 "pattern": "pipeline",
 "problem": (
   "Porting a phone number between operators (or between prepaid/postpaid within the same operator) involves a "
   "strict, regulator-defined sequence of validation, donor-operator confirmation, network cutover, and billing "
   "adjustment steps with tight SLA windows. Missing a step or executing out of order causes service disruption "
   "and regulatory reporting obligations — this is a domain where a disciplined, auditable pipeline matters more "
   "than adaptive flexibility."
 ),
 "stages": ["Port Request Validation Agent", "Donor Operator Confirmation Agent", "Number Portability Database (NPDB) Update Agent",
            "Network Cutover Sequencing Agent", "Post-Port Billing & Service Reconciliation Agent"],
 "actions": ["NPDB/Central Registry Update", "Network Switch Cutover Execution", "Customer Service Continuity Confirmation"],
 "agents_table": [
   ("Port Request Validation Agent", "Validates the port request against regulator rules (correct account holder, no contract-lock conflicts)"),
   ("Donor Operator Confirmation Agent", "Manages the confirm/reject handshake with the losing operator within the regulatory SLA window"),
   ("Number Portability Database Update Agent", "Updates the central number portability registry once confirmed"),
   ("Network Cutover Sequencing Agent", "Sequences the precise cutover timing to minimize service interruption for the customer"),
   ("Post-Port Billing & Service Reconciliation Agent", "Confirms billing and service entitlements are correctly reflected on the gaining operator's systems post-cutover"),
 ],
 "tech_table": [
   ("Regulatory integration", "Central number portability clearinghouse API (e.g., NPAC in the US, equivalent national registries elsewhere)"),
   ("Validation rules", "Rules engine encoding jurisdiction-specific porting eligibility requirements"),
   ("Orchestration", "Temporal workflow enforcing strict step ordering and regulator SLA deadlines"),
   ("Cutover coordination", "Real-time coordination with switch/HLR-HSS systems for the network cutover moment"),
   ("LLM usage", "Claude for customer-facing status explanations and internal exception-narrative generation only, not for core sequencing logic"),
   ("Monitoring", "SLA-compliance dashboard tracking every port request against regulatory deadlines"),
   ("Audit", "Full immutable audit trail per port required for regulatory dispute resolution"),
   ("Rollback handling", "Defined rollback procedure agent for failed cutovers to restore service on the donor network"),
 ],
 "retrospective": [
   "Deliberately kept this pipeline rigid and rules-driven rather than adaptive — the regulatory and customer-service-continuity stakes of a mis-sequenced port are far higher than the efficiency gain from flexibility.",
   "Would build the rollback-handling agent with equal rigor to the forward path from the start; early versions treated rollback as an afterthought, and a handful of failed cutovers left customers without service longer than necessary.",
   "Donor operator confirmation timeouts (silence interpreted as rejection under some regulatory regimes) needed very precise SLA-clock handling — a timezone/clock-sync bug caused incorrect timeout determinations in early testing.",
   "Customers found generic 'porting in progress' messages frustrating during multi-day ports; added stage-specific status messaging generated by the LLM layer, grounded strictly in actual pipeline state.",
 ],
},
{
 "id": 11, "slug": "wholesale-partner-interconnect-onboarding",
 "title": "Wholesale/Partner Interconnect Onboarding",
 "pattern": "orchestrator-worker",
 "problem": (
   "Onboarding a new wholesale/interconnect partner (MVNO, roaming partner, transit provider) requires "
   "coordinating commercial contract terms, technical interconnection setup, billing/settlement configuration, "
   "and security/compliance checks — traditionally a multi-month project with heavy manual project management "
   "overhead. An agent team can parallelize the workstreams and produce a single onboarding-readiness view."
 ),
 "orchestrator": "Partner Onboarding Orchestrator Agent",
 "workers": ["Contract Terms Configuration Agent", "Technical Interconnection Setup Agent", "Billing/Settlement Configuration Agent",
             "Security & Compliance Verification Agent"],
 "data_sources": ["Signed Interconnect Agreement", "Partner Technical Specification Documents", "Compliance/Security Questionnaire Responses"],
 "actions": ["Interconnect Provisioning Execution", "Settlement System Configuration", "Go-Live Readiness Report"],
 "human_gate": "Commercial and Security Sign-off Before Go-Live",
 "agents_table": [
   ("Partner Onboarding Orchestrator", "Tracks all workstreams in parallel and produces a unified go-live readiness assessment"),
   ("Contract Terms Configuration Agent", "Extracts commercial terms (rates, volume commitments, SLAs) from the signed agreement and configures the rating/billing systems accordingly"),
   ("Technical Interconnection Setup Agent", "Coordinates SS7/Diameter/SIP interconnection configuration per the partner's technical specification"),
   ("Billing/Settlement Configuration Agent", "Sets up the settlement rate cards and invoicing cadence matching the contract terms"),
   ("Security & Compliance Verification Agent", "Verifies the partner's security posture and compliance documentation meets interconnection requirements"),
 ],
 "tech_table": [
   ("Contract extraction", "Claude + RAG over the signed interconnect agreement (docx/pdf skill patterns)"),
   ("Technical setup", "Signaling gateway/session border controller (SBC) configuration APIs"),
   ("Billing configuration", "Rating engine and settlement system (mirrors Telecom's roaming settlement use case) rate-card setup"),
   ("Orchestration", "LangGraph supervisor with parallel workstream tracking and a unified readiness dashboard"),
   ("Security verification", "Security questionnaire analysis against a standardized interconnection security baseline"),
   ("Project tracking", "Integration with a project management tool (Jira/Smartsheet) for cross-team visibility"),
   ("Testing", "Automated interconnection test-call/test-transaction validation before go-live"),
   ("Documentation", "Auto-generated onboarding runbook and go-live checklist per partner"),
 ],
 "retrospective": [
   "Would add the automated test-call/test-transaction validation earlier in the process — several early onboardings passed all individual workstream checks but failed on first real traffic due to an untested configuration interaction.",
   "Contract term extraction accuracy needed a mandatory commercial-team review step; automated extraction was a strong first draft but rate-card errors carry direct financial risk.",
   "Would formalize the security baseline checklist earlier — early onboardings applied inconsistent ad hoc security standards per partner before this was standardized.",
   "Cross-workstream dependency awareness was missing in v1 (e.g., billing configuration proceeding before technical setup confirmed a required parameter) — added explicit dependency gates between workers.",
 ],
},
{
 "id": 12, "slug": "service-catalog-network-activation-mapping",
 "title": "Service Catalog-to-Network Activation Mapping (TMF Open APIs)",
 "pattern": "hierarchical",
 "problem": (
   "Translating a commercial service catalog entry into the correct sequence of TM Forum Open API calls across "
   "heterogeneous OSS/network domains requires deep, often tribal-knowledge mapping logic that breaks whenever "
   "either the catalog or an underlying OSS API changes. A hierarchical agent team maintains this mapping layer "
   "as a living, self-validating system rather than static integration code."
 ),
 "top": "Catalog-to-Network Mapping Orchestrator",
 "mid_layer": ["Access Network Domain Mapping Agent", "Core Network Domain Mapping Agent"],
 "leaves_by_mid": [
   ["Fixed Access (GPON/DSL) Mapping Agent", "Mobile Access (RAN) Mapping Agent"],
   ["Core Network Function Mapping Agent", "IMS/Voice Core Mapping Agent"],
 ],
 "actions": ["TMF641 Service Order Execution", "Mapping Validation Test Suite Run", "API Contract Drift Alert"],
 "agents_table": [
   ("Catalog-to-Network Mapping Orchestrator", "Routes each service catalog entry to the correct domain mapping managers and validates end-to-end coverage"),
   ("Access Network Domain Mapping Agent", "Oversees fixed and mobile access mapping sub-agents"),
   ("Core Network Domain Mapping Agent", "Oversees core network function and IMS/voice mapping sub-agents"),
   ("Fixed Access (GPON/DSL) Mapping Agent", "Maps broadband catalog entries to the correct OLT/DSLAM provisioning API sequence"),
   ("Mobile Access (RAN) Mapping Agent", "Maps mobile service entries to RAN configuration and QoS profile API calls"),
   ("Core Network Function Mapping Agent", "Maps service entries to 5GC/EPC network function provisioning calls"),
 ],
 "tech_table": [
   ("Catalog source", "TM Forum TMF620 Product Catalog as the mapping input"),
   ("API layer", "TM Forum TMF641 (Service Ordering), TMF638 (Service Inventory) Open APIs"),
   ("Orchestration", "Hierarchical LangGraph mirroring the operator's actual network domain org structure"),
   ("Mapping validation", "Automated regression test suite re-validating every mapping whenever a catalog or API contract changes"),
   ("Drift detection", "API contract diffing (OpenAPI spec comparison) to catch breaking changes from OSS vendors"),
   ("LLM usage", "Claude proposing updated mapping logic when drift is detected, with mandatory engineer review before deployment"),
   ("Version control", "Git-based versioning of mapping logic with full change history"),
   ("Monitoring", "Mapping success-rate dashboard per catalog entry and network domain"),
 ],
 "retrospective": [
   "API contract drift detection was the single highest-value addition — would build it before any of the mapping agents themselves, since undetected vendor API changes were the dominant cause of production mapping failures.",
   "Would require mandatory engineer review of any LLM-proposed mapping change before deployment as a hard rule from the start, not something added after an early unreviewed change caused a provisioning outage.",
   "Domain mapping managers initially couldn't see cross-domain dependencies (e.g., a service needing both RAN and core changes) — added explicit cross-domain coordination logic at the top orchestrator level.",
   "Regression testing needed to run on every catalog change, not just every API change — an early gap here let a catalog update silently break a previously-working mapping.",
 ],
},
{
 "id": 13, "slug": "trouble-ticket-cross-domain-assurance",
 "title": "Trouble Ticket Management & Cross-Domain Assurance (OSS)",
 "pattern": "orchestrator-worker",
 "problem": (
   "OSS trouble tickets for service-affecting issues often require cross-domain investigation (is it access, "
   "transport, or core?) before the right team can even start fixing it, and tickets frequently bounce between "
   "teams before landing correctly. An agent team can run a first-pass cross-domain diagnostic in parallel, "
   "assigning the ticket correctly the first time and pre-populating diagnostic evidence."
 ),
 "orchestrator": "Trouble Ticket Triage Orchestrator",
 "workers": ["Access Domain Diagnostic Agent", "Transport Domain Diagnostic Agent", "Core Domain Diagnostic Agent",
             "Customer Premises Equipment (CPE) Diagnostic Agent"],
 "data_sources": ["Customer-Reported Symptom Description", "Real-Time Alarm/PM Data", "CPE Remote Diagnostics", "Historical Ticket Resolution Data"],
 "actions": ["Correct Team Ticket Assignment", "Pre-Populated Diagnostic Evidence Attachment", "Auto-Resolution for Known Simple Issues"],
 "agents_table": [
   ("Trouble Ticket Triage Orchestrator", "Runs cross-domain diagnostics in parallel and assigns the ticket to the correct team with evidence attached"),
   ("Access Domain Diagnostic Agent", "Checks access-layer health (line quality, port status, recent access-network alarms) relevant to the symptom"),
   ("Transport Domain Diagnostic Agent", "Checks for transport-layer issues (link errors, path degradation) that could explain the symptom"),
   ("Core Domain Diagnostic Agent", "Checks core network element health relevant to the reported symptom"),
   ("CPE Diagnostic Agent", "Runs remote diagnostics against the customer's premises equipment to rule out local causes"),
 ],
 "tech_table": [
   ("Ticket intake", "Customer service system (Salesforce Service Cloud) generating the initial ticket"),
   ("Diagnostic APIs", "EMS/NMS query APIs per network domain plus CPE remote-management (TR-069/USP) protocols"),
   ("Orchestration", "LangGraph supervisor running domain diagnostics in parallel with a shared time budget"),
   ("Symptom classification", "LLM classifier mapping free-text customer symptom descriptions to likely diagnostic domains"),
   ("Auto-resolution", "Rules engine for well-understood simple fixes (e.g., remote CPE reboot) executed automatically with customer consent"),
   ("Ticket routing", "OSS trouble ticket system (Remedy/ServiceNow) integration for correct-team assignment"),
   ("Historical grounding", "RAG over historical resolved tickets to suggest likely root cause"),
   ("Analytics", "First-time-right assignment rate and mean-time-to-resolution dashboard"),
 ],
 "retrospective": [
   "Auto-resolution (e.g., remote CPE reboot) required explicit customer consent before executing, added after an early version reset a customer's equipment mid-video-call without warning.",
   "Would build the historical-ticket RAG grounding earlier — it dramatically improved diagnostic accuracy for the long tail of unusual symptom descriptions once added.",
   "First-time-right assignment was the metric that mattered most to operations leadership, more than average diagnostic accuracy per domain — would have led with this KPI from the start.",
   "CPE diagnostics needed graceful degradation for older equipment lacking remote-management support — early version had no fallback and silently skipped diagnosis for a meaningful fraction of the install base.",
 ],
},
{
 "id": 14, "slug": "digital-bss-oss-migration-reconciliation",
 "title": "Digital BSS/OSS Migration & Data Reconciliation",
 "pattern": "pipeline",
 "problem": (
   "Migrating customers from a legacy BSS/OSS stack to a modern digital platform (common after an M&A or a "
   "multi-year transformation program) requires migrating millions of customer, product, and billing records "
   "without service disruption or billing errors — historically requiring large manual reconciliation teams "
   "working through cutover weekends. An agent pipeline can validate and reconcile migrated data continuously "
   "throughout the program rather than only at cutover."
 ),
 "stages": ["Legacy Data Extraction & Profiling Agent", "Transformation Mapping Agent", "Migration Validation Agent",
            "Discrepancy Investigation Agent", "Cutover Readiness Certification Agent"],
 "actions": ["New Platform Data Load", "Migration Discrepancy Report", "Cutover Go/No-Go Recommendation"],
 "agents_table": [
   ("Legacy Data Extraction & Profiling Agent", "Extracts and profiles legacy data quality/completeness before migration begins"),
   ("Transformation Mapping Agent", "Applies the legacy-to-new-platform field/schema transformation rules"),
   ("Migration Validation Agent", "Compares migrated records in the new platform against the legacy source for accuracy"),
   ("Discrepancy Investigation Agent", "Investigates root cause for any record that fails validation (mapping bug vs. legacy data quality issue)"),
   ("Cutover Readiness Certification Agent", "Aggregates validation results into a data-driven go/no-go recommendation per migration wave"),
 ],
 "tech_table": [
   ("Legacy extraction", "ETL from legacy BSS/OSS databases (often decades-old schemas) via custom connectors"),
   ("Transformation", "dbt-based transformation pipeline encoding legacy-to-new-platform mapping rules"),
   ("Validation", "Automated record-level and aggregate-level reconciliation (counts, sums, sampled deep-diffs)"),
   ("Orchestration", "Airflow pipeline processing migration waves with agent-based validation gates between stages"),
   ("Discrepancy diagnosis", "Claude reasoning over failed-validation records to classify root cause"),
   ("Reporting", "Wave-by-wave migration health dashboard for the program management office"),
   ("Rollback capability", "Defined rollback procedure per wave if cutover certification fails"),
   ("Audit", "Full before/after record comparison retained for regulatory and financial audit of the migration"),
 ],
 "retrospective": [
   "Would run continuous validation throughout each migration wave rather than only at the cutover checkpoint — catching mapping bugs weeks earlier saved significant rework in later waves.",
   "Discrepancy root-cause classification (mapping bug vs. legacy data quality issue) was essential for prioritization — without it, engineering and data-quality teams both assumed issues were the other team's problem.",
   "Would build rollback procedures with equal investment to forward migration logic from the start; one wave's rollback in v1 took far longer than the original migration due to under-investment here.",
   "Sampled deep-diffs (not just aggregate counts) caught systematic errors that count-based validation completely missed — would make deep-diff sampling the default validation method, not an optional extra check.",
 ],
},
{
 "id": 15, "slug": "promotions-campaign-configuration-engine",
 "title": "Promotions & Campaign Configuration Engine",
 "pattern": "debate-critique",
 "problem": (
   "Marketing teams want to launch promotions quickly (a holiday data bonus, a referral discount), but poorly "
   "modeled promotions can be gamed, cannibalize existing revenue, or interact unexpectedly with other active "
   "promotions in ways that erode margin. A proposer/critic pair — one designing the promotion for marketing "
   "impact, one adversarially checking for gaming and cannibalization risk — catches problems before launch "
   "rather than after the damage is done."
 ),
 "proposer": "Promotion Design Proposer Agent",
 "critic": "Gaming & Cannibalization Critic Agent",
 "arbiter": "Promotion Launch Arbiter Agent",
 "refs": ["Active Promotion Catalog", "Historical Promotion Performance Data", "Customer Segment & Eligibility Rules", "Margin/Cost Model"],
 "actions": ["Product Catalog Promotion Publish", "Marketing Campaign Launch", "Finance Margin-Impact Sign-off Request"],
 "agents_table": [
   ("Promotion Design Proposer Agent", "Designs the promotion mechanics (discount structure, eligibility, duration) to maximize the stated marketing objective"),
   ("Gaming & Cannibalization Critic Agent", "Actively searches for ways the promotion could be gamed (e.g., repeated sign-up/cancel cycles) or would cannibalize existing full-price customers"),
   ("Promotion Launch Arbiter Agent", "Weighs marketing impact against gaming/cannibalization risk into a launch decision or required modification"),
   ("Promotion Interaction Agent", "Checks how the new promotion interacts with all currently active promotions for compounding-discount risk"),
   ("Margin Impact Modeling Agent", "Quantifies the expected margin impact under both intended-use and worst-case-gaming scenarios"),
 ],
 "tech_table": [
   ("Promotion configuration", "Extension of the product catalog platform's promotion/discount module"),
   ("Proposer/critic reasoning", "Two independently-prompted Claude passes with opposing objectives, consistent with this catalog's other debate-critique designs"),
   ("Gaming simulation", "Monte Carlo simulation of adversarial customer behavior against the proposed promotion rules"),
   ("Interaction checking", "Rules engine cross-referencing all active promotions for stacking/compounding conflicts"),
   ("Margin modeling", "Financial model integrating historical redemption rates and worst-case gaming scenarios"),
   ("Arbitration", "Weighted decision combining marketing-impact and risk scores, with a required finance sign-off above a materiality threshold"),
   ("Launch execution", "Automated publish to catalog and marketing campaign systems once approved"),
   ("Post-launch monitoring", "Real-time redemption-pattern monitoring to catch actual gaming behavior the pre-launch simulation missed"),
 ],
 "retrospective": [
   "Gaming simulation via Monte Carlo against adversarial behavior caught a sign-up/cancel loophole that the critic's qualitative review alone missed — would combine simulation and qualitative critique from the start rather than adding simulation later.",
   "Promotion interaction checking prevented a stacking scenario that would have resulted in negative-margin transactions — this sub-agent had outsized value relative to its build cost and should be prioritized in any similar system.",
   "Would add post-launch monitoring as a mandatory companion to every launch, not an optional extra — pre-launch simulation is necessarily incomplete, and real gaming patterns emerged that hadn't been anticipated.",
   "Marketing teams initially found the critic's pushback frustrating when they were confident in a promotion; reframing the critic's output as 'risk-adjusted launch options' rather than a blocking veto improved adoption.",
 ],
},
{
 "id": 16, "slug": "dunning-collections-automation",
 "title": "Dunning & Prepaid/Postpaid Collections Automation",
 "pattern": "human-escalation",
 "problem": (
   "Postpaid telecom collections and prepaid low-balance dunning need to run at massive scale (millions of "
   "customers) with automated reminders, service restrictions, and suspension actions — but must escalate to "
   "human agents for hardship situations, disputes, or high-value customers where a purely automated action risks "
   "real harm or churn of a valuable relationship. A confidence/risk-gated escalation chain balances scale with "
   "care."
 ),
 "auto_agents": ["Payment Reminder Agent", "Grace Period & Partial Payment Agent", "Service Restriction Agent"],
 "escalation_gate": "Hardship/Dispute/High-Value Risk Gate",
 "human_role": "Collections Specialist",
 "actions": ["Automated Reminder/Restriction Execution", "Customer Service Continuity Adjustment", "Hardship Program Enrollment"],
 "agents_table": [
   ("Payment Reminder Agent", "Sends escalating, compliant reminders as a payment due-date approaches and passes"),
   ("Grace Period & Partial Payment Agent", "Manages grace-period extensions and partial-payment plan offers within policy limits"),
   ("Service Restriction Agent", "Applies data/voice restrictions and eventual suspension per the escalation ladder if payment remains outstanding"),
   ("Hardship/Dispute/High-Value Risk Gate", "Screens every case before restriction/suspension for hardship indicators, an open billing dispute, or high customer lifetime value"),
   ("Collections Specialist", "Reviews gated cases and decides on hardship enrollment, dispute hold, or manual account handling"),
 ],
 "tech_table": [
   ("Payment tracking", "Billing system real-time payment status feed"),
   ("Reminder automation", "SMS/email/app-push sequencing engine with compliant frequency limits"),
   ("Risk gate scoring", "Model combining payment history, customer value (CLV), open dispute flags, and hardship-indicator signals"),
   ("Orchestration", "Sequential automation chain (LangGraph) with the risk gate as a mandatory checkpoint before any restriction"),
   ("Human workflow", "Collections specialist case queue integrated with the billing and CRM systems"),
   ("Hardship programs", "Integration with hardship/payment-assistance program enrollment systems"),
   ("Compliance", "Regulatory contact-frequency and disclosure rules enforced identically to the finance-domain collections use case"),
   ("Monitoring", "Restriction/suspension rate, complaint rate, and recovery-rate dashboard segmented by risk-gate outcome"),
 ],
 "retrospective": [
   "The risk gate blocking automated suspension for flagged cases was a hard requirement from launch, not an afterthought — this is the same principle applied in the finance-domain collections use case, and it proved just as important here.",
   "Would incorporate open-dispute status into the risk gate from day one; an early version suspended service for a customer with an active, legitimate billing dispute, which became a notable complaint driver.",
   "High-value customer identification needed to consider full household/multi-line value, not just the single delinquent line — a customer with five other paid-up lines was nearly suspended over one small overdue line in early testing.",
   "Would add a lighter-touch first-contact channel (in-app nudge before SMS) for customers with strong payment history but a rare late payment, rather than treating every delinquency identically on the escalation ladder.",
 ],
},
{
 "id": 17, "slug": "api-gateway-tmf-governance",
 "title": "API Gateway & TMF Open API Orchestration Governance",
 "pattern": "event-swarm",
 "problem": (
   "As operators expose more TM Forum Open APIs to partners, MVNOs, and internal digital channels, API misuse, "
   "quota abuse, contract-breaking changes, and performance degradation need real-time detection across a "
   "growing API surface. A swarm of lightweight agents subscribed to the API gateway's event stream can enforce "
   "governance continuously rather than through periodic manual API audits."
 ),
 "bus_name": "API Gateway Event Bus",
 "agents": ["Rate Limit/Quota Abuse Agent", "Contract Compliance (OpenAPI Spec) Agent", "Latency/Error-Rate Degradation Agent",
            "Unauthorized Access Pattern Agent", "Deprecated Version Usage Agent"],
 "actions": ["Automated Throttling/Block", "API Consumer Notification", "Platform Team Governance Alert"],
 "agents_table": [
   ("Rate Limit/Quota Abuse Agent", "Detects API consumers exceeding contracted rate limits or exhibiting abusive call patterns"),
   ("Contract Compliance Agent", "Validates that API responses/requests conform to the published OpenAPI/TMF specification, flagging drift"),
   ("Latency/Error-Rate Degradation Agent", "Detects when a specific API or backend is degrading and could breach partner SLAs"),
   ("Unauthorized Access Pattern Agent", "Flags access patterns suggesting credential misuse or scope escalation attempts"),
   ("Deprecated Version Usage Agent", "Tracks consumers still calling deprecated API versions and drives migration outreach before sunset"),
 ],
 "tech_table": [
   ("API gateway", "Kong/Apigee/MuleSoft as the API gateway emitting a real-time event stream"),
   ("Event bus", "Kafka topics per event category (rate-limit, contract-violation, latency, security)"),
   ("Contract validation", "OpenAPI spec validation middleware comparing live traffic against the published TMF contract"),
   ("Abuse detection", "Anomaly detection on per-consumer call-pattern time series"),
   ("Security detection", "Correlation with IAM/OAuth scope logs for unauthorized access pattern detection"),
   ("Automated response", "Gateway-level throttling/blocking policy execution for confirmed abuse"),
   ("Consumer communication", "Automated developer-portal notifications for quota warnings and deprecated-version usage"),
   ("Governance dashboard", "API health, compliance, and consumer-behavior dashboard for the platform team"),
 ],
 "retrospective": [
   "Would tune automated throttling conservatively from the start — an early false-positive on the abuse detector throttled a legitimate high-volume partner during a peak traffic event.",
   "Contract compliance validation caught internal team changes breaking the published spec before partners noticed, which became one of the most valued outputs of the whole system.",
   "Deprecated version usage tracking needed proactive outreach automation, not just a dashboard — early version just reported the data and migration lagged until outreach was automated.",
   "Would correlate rate-limit and latency-degradation signals together from the start; a partner's abusive traffic pattern was, in one incident, the actual root cause of a broader latency degradation that was initially investigated as an unrelated infrastructure issue.",
 ],
},
{
 "id": 18, "slug": "credit-limit-fraud-threshold-management",
 "title": "Credit Limit & Fraud Threshold Management (BSS)",
 "pattern": "debate-critique",
 "problem": (
   "Postpaid credit limits and usage-based fraud thresholds (e.g., data roaming caps, premium SMS spend limits) "
   "must balance protecting the operator from bad debt/fraud exposure against not needlessly restricting "
   "legitimate high-usage customers. Static, one-size-fits-all thresholds either let too much bad debt through or "
   "generate excessive false-positive service interruptions for legitimate power users."
 ),
 "proposer": "Threshold Tightening Proposer Agent",
 "critic": "Legitimate Usage Pattern Critic Agent",
 "arbiter": "Threshold Policy Arbiter Agent",
 "refs": ["Customer Payment/Credit History", "Real-Time Usage Data", "Historical Bad-Debt Outcomes", "Roaming/Premium Service Usage Patterns"],
 "actions": ["Dynamic Credit Limit Adjustment", "Real-Time Spend Cap Alert to Customer", "Service Restriction on Threshold Breach"],
 "agents_table": [
   ("Threshold Tightening Proposer Agent", "Proposes tighter credit limits/usage caps for accounts showing early bad-debt or fraud risk signals"),
   ("Legitimate Usage Pattern Critic Agent", "Checks whether flagged high-usage behavior matches a known legitimate pattern (business travel, seasonal usage, family plan sharing)"),
   ("Threshold Policy Arbiter Agent", "Sets the final dynamic threshold per account, balancing risk protection against legitimate-customer friction"),
   ("Bad-Debt Outcome Feedback Agent", "Feeds actual bad-debt write-off outcomes back to calibrate the proposer's risk signals over time"),
   ("Real-Time Spend Cap Notification Agent", "Proactively alerts customers approaching their threshold, giving them a chance to act before restriction"),
 ],
 "tech_table": [
   ("Credit/usage data", "Billing and real-time charging system feeds for payment history and live usage"),
   ("Risk scoring", "Bad-debt propensity model trained on historical write-off outcomes"),
   ("Proposer/critic reasoning", "Two independently-prompted Claude passes, consistent with this catalog's fraud/anomaly debate-critique designs"),
   ("Legitimate-pattern detection", "Sequence-pattern model recognizing known legitimate high-usage archetypes (roaming business travelers, etc.)"),
   ("Arbitration", "Dynamic threshold-setting model calibrated against both bad-debt cost and customer-friction cost"),
   ("Notification", "Real-time proactive spend-cap alerts via SMS/app push before restriction triggers"),
   ("Feedback loop", "Automated ingestion of realized bad-debt outcomes to retrain the proposer's risk model monthly"),
   ("Monitoring", "Bad-debt-prevented vs. legitimate-customer-friction dashboard, tracked as co-equal KPIs"),
 ],
 "retrospective": [
   "Would track legitimate-customer friction (unnecessary restrictions) as a first-class KPI alongside bad-debt prevention from the very start — v1 over-indexed on the risk-prevention side and generated avoidable complaints from legitimate roaming customers.",
   "Proactive spend-cap notifications before restriction meaningfully reduced complaints versus a hard cutoff with no warning — would make this notification step non-optional in any similar system.",
   "The bad-debt outcome feedback loop took months to accumulate enough labeled outcomes to meaningfully improve the proposer; would start this feedback collection from day one even before the model is mature enough to use it.",
   "Family plan usage sharing was initially misread as anomalous single-user behavior; would model multi-line household usage patterns explicitly rather than per-line in isolation.",
 ],
},
{
 "id": 19, "slug": "partner-revenue-share-settlement",
 "title": "Partner Revenue Share & Settlement Automation",
 "pattern": "market-based",
 "problem": (
   "Content and platform partnerships (app-store billing, streaming bundles, IoT platform revenue share) involve "
   "complex, often-disputed revenue-share calculations across many partners with different commercial terms. "
   "Manual settlement reconciliation is slow and disputes over calculation methodology sour partner relationships. "
   "A market-based clearing approach, where each partner's settlement agent submits its claim against a neutral "
   "clearing agent that applies contract terms transparently, reduces disputes and settlement cycle time."
 ),
 "auctioneer": "Revenue Share Clearing Agent",
 "bidders": ["Partner Settlement Claim Agent (per revenue-share partner)", "Internal Revenue Attribution Agent"],
 "actions": ["Automated Partner Payment", "Settlement Statement Generation", "Dispute Case for Unresolved Claims"],
 "agents_table": [
   ("Revenue Share Clearing Agent", "Applies each partner's specific contract terms transparently to attributed revenue and clears the final settlement amount"),
   ("Partner Settlement Claim Agent", "Represents each partner's expected settlement calculation based on their view of usage/revenue attribution"),
   ("Internal Revenue Attribution Agent", "Provides the operator's authoritative view of usage and revenue attributable to each partner"),
   ("Contract Terms Interpretation Agent", "Extracts and applies the specific revenue-share formula, minimums, and tiering from each partner contract"),
   ("Dispute Resolution Support Agent", "When the clearing agent and a partner's claim disagree beyond a tolerance threshold, assembles the evidence package for human-mediated resolution"),
 ],
 "tech_table": [
   ("Revenue attribution", "Usage/revenue attribution pipeline feeding the internal agent's authoritative claim"),
   ("Contract terms", "Claude + RAG extraction of revenue-share terms from partner contracts, mirroring the finance-domain contract review use case"),
   ("Clearing mechanism", "Transparent, auditable calculation engine (not a negotiation — a deterministic application of agreed contract terms) with a neutral audit trail visible to both sides"),
   ("Partner portal", "Self-service portal where partners can view the calculation inputs and methodology, reducing dispute volume"),
   ("Settlement execution", "Automated payment processing for cleared, undisputed settlements"),
   ("Dispute tooling", "Automated evidence-package generation for the sub-tolerance-threshold percentage of claims requiring human mediation"),
   ("Orchestration", "Scheduled monthly/quarterly clearing runs per partner contract cycle"),
   ("Audit", "Full calculation lineage retained for financial audit and partner dispute resolution"),
 ],
 "retrospective": [
   "The partner-facing transparency portal (showing exact calculation inputs and methodology) reduced dispute volume more than any improvement to calculation accuracy itself — would prioritize transparency tooling from the start, not as a later addition.",
   "Would keep the clearing calculation strictly deterministic and auditable rather than any form of LLM-mediated negotiation — partners needed to trust the math was contractually mechanical, not a black box.",
   "Revenue attribution disagreements were usually a data-source timing issue (partner counting a different billing cycle boundary) rather than a genuine contract-interpretation dispute — would build cycle-boundary reconciliation logic earlier given how much dispute volume it accounted for.",
   "Would set a tighter, contract-specified dispute tolerance threshold per partner rather than one global tolerance — a single global threshold let small-but-persistent discrepancies with one large partner accumulate unnoticed.",
 ],
},
{
 "id": 20, "slug": "legacy-system-decommissioning-archival",
 "title": "Legacy System Decommissioning & Data Archival",
 "pattern": "orchestrator-worker",
 "problem": (
   "Decommissioning a legacy BSS/OSS system after a migration (see Use Case 14) requires exhaustively mapping "
   "every remaining dependency (batch jobs, reports, undocumented integrations), archiving historical data for "
   "regulatory retention, and validating nothing breaks before the final shutdown — work that is high-risk, "
   "tedious, and prone to missed dependencies when done manually under program-timeline pressure."
 ),
 "orchestrator": "Decommissioning Orchestrator Agent",
 "workers": ["Dependency Discovery Agent", "Data Archival & Retention Compliance Agent", "Downstream Consumer Notification Agent",
             "Cutover Validation Agent"],
 "data_sources": ["Network Traffic to Legacy System (integration discovery)", "Batch Job Scheduler Logs", "Regulatory Data Retention Requirements", "System Documentation (often incomplete)"],
 "actions": ["Final Data Archive to Compliant Storage", "System Shutdown Execution", "Decommissioning Sign-off Report"],
 "human_gate": "Program Sponsor Final Shutdown Approval",
 "agents_table": [
   ("Decommissioning Orchestrator Agent", "Coordinates dependency discovery, archival, and validation, gating final shutdown on all checks passing"),
   ("Dependency Discovery Agent", "Analyzes live network traffic and batch job logs to find undocumented integrations still calling the legacy system"),
   ("Data Archival & Retention Compliance Agent", "Identifies data requiring regulatory retention and archives it to compliant long-term storage before shutdown"),
   ("Downstream Consumer Notification Agent", "Notifies every discovered downstream consumer team well ahead of the shutdown date"),
   ("Cutover Validation Agent", "Runs a final validation pass confirming zero live traffic to the legacy system before sign-off"),
 ],
 "tech_table": [
   ("Traffic analysis", "Network flow monitoring (NetFlow/packet capture) to discover live integrations empirically, not just from documentation"),
   ("Batch job analysis", "Scheduler log mining (Control-M/Autosys logs) to find scheduled jobs still touching the legacy system"),
   ("Retention compliance", "Regulatory retention rules engine (varies by data type and jurisdiction, e.g., 7-year call detail retention)"),
   ("Archival storage", "Compliant cold storage (e.g., S3 Glacier with legal hold/WORM configuration)"),
   ("Orchestration", "LangGraph supervisor with a hard gate requiring all worker agents to report zero blocking dependencies"),
   ("Notification", "Automated stakeholder notification workflow with escalating reminders as shutdown approaches"),
   ("Validation", "Final traffic-monitoring validation window (e.g., 30 days of zero traffic) before executing shutdown"),
   ("Documentation", "Auto-generated decommissioning report for audit and knowledge-retention purposes"),
 ],
 "retrospective": [
   "Empirical traffic-based dependency discovery found integrations that no documentation or interview process surfaced — would always prioritize this over relying on documentation/tribal knowledge, which was consistently incomplete.",
   "Would build in a longer mandatory zero-traffic validation window from the start; an early decommissioning shut down a system that still received a rare monthly batch job, which the shorter initial validation window missed.",
   "Regulatory retention requirements varied more than expected by data type within the same legacy system — would engage compliance/legal earlier to build a more granular retention rules engine rather than one blanket retention period.",
   "Downstream consumer notification needed much longer lead times and more escalation than initially planned — several teams only acted on the final reminder, and would build in earlier, more insistent outreach next time.",
 ],
},
]
