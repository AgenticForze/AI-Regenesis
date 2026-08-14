# -*- coding: utf-8 -*-
TELECOM = [
{
 "id": 1, "slug": "network-fault-rca-remediation",
 "title": "Multi-Agent Network Fault RCA & Auto-Remediation",
 "pattern": "orchestrator-worker",
 "problem": (
   "A tier-1 operator's NOC receives thousands of correlated alarms per hour across RAN, transport, and core "
   "domains during a fault storm (e.g., a fiber cut or a core VNF crash). Human engineers spend 40-60 minutes "
   "just correlating alarms to find the true root cause before remediation even starts, driving SLA breaches "
   "and customer complaints. The goal is to compress alarm storms into a single root-cause hypothesis with "
   "confidence score and, where safe, trigger auto-remediation within minutes instead of hours."
 ),
 "orchestrator": "NOC Incident Orchestrator Agent",
 "workers": ["RAN Alarm Correlation Agent", "Transport/IP Topology Agent", "Core Network (5GC/EPC) Agent",
             "Performance-KPI Deviation Agent", "Historical Ticket Similarity Agent"],
 "data_sources": ["FM/PM Alarms (Ceragon/Ericsson/Nokia EMS)", "Network Topology (Netbox/inventory DB)",
                  "Streaming Telemetry (gNMI/Kafka)", "Past Incident Tickets (ServiceNow)"],
 "actions": ["Auto-remediation via Ansible/NETCONF", "ServiceNow Incident Update", "NOC Dashboard/Slack Alert"],
 "human_gate": "SRE Approval for High-Blast-Radius Actions",
 "agents_table": [
   ("NOC Incident Orchestrator", "Fans out alarm bursts to domain agents, aggregates hypotheses, ranks root cause by confidence"),
   ("RAN Alarm Correlation Agent", "Deduplicates and correlates RAN alarms (cell down, PCI conflicts) against topology"),
   ("Transport/IP Topology Agent", "Traces fiber/microwave/IP path failures using topology graph traversal"),
   ("Core Network Agent", "Inspects 5GC/EPC VNF health, pod restarts, and signaling failures via Kubernetes/OSS APIs"),
   ("Performance-KPI Deviation Agent", "Detects statistically abnormal KPI drops (drop call rate, throughput) via time-series models"),
   ("Historical Ticket Similarity Agent", "RAG search over past incident tickets to suggest proven fixes"),
   ("Remediation Execution Agent", "Generates and (post-approval) executes Ansible/NETCONF playbooks"),
 ],
 "tech_table": [
   ("Alarm ingestion", "Kafka + FM/PM adapters (SNMP/gNMI)"),
   ("Agent orchestration", "LangGraph / AWS Bedrock Agents Supervisor pattern"),
   ("Topology graph", "Neo4j graph DB for network topology traversal"),
   ("Time-series anomaly detection", "Prophet / Nixtla + Isolation Forest"),
   ("RAG over tickets", "Vector DB (pgvector/Weaviate) + embeddings"),
   ("LLM reasoning", "Claude (tool-use) for hypothesis generation and NL incident summaries"),
   ("Remediation execution", "Ansible AWX / NETCONF (ncclient) with dry-run diff"),
   ("Observability", "Grafana + OpenTelemetry tracing of agent decisions"),
 ],
 "retrospective": [
   "Add a confidence-calibration step: log every agent's predicted-vs-actual root cause to retrain ranking weights monthly.",
   "Introduce a blast-radius simulator agent that dry-runs remediation against a digital twin before touching production.",
   "Move from a single orchestrator to two-tier hierarchy once alarm volume exceeds ~5k/hr to avoid orchestrator context overload.",
   "Cache topology subgraphs per incident to cut RAG/graph query latency, which dominated the initial p95 response time.",
 ],
},
{
 "id": 2, "slug": "5g-network-slicing-orchestration",
 "title": "5G Network Slice Lifecycle Orchestration",
 "pattern": "hierarchical",
 "problem": (
   "Enterprises request bespoke 5G network slices (low-latency for AR/VR factory floors, high-throughput for "
   "campus video, massive-IoT for sensors) with different SLAs. Manually designing, provisioning, and continuously "
   "assuring each slice across RAN, transport, and core domains takes weeks and is error-prone. The operator needs "
   "closed-loop, SLA-aware slice lifecycle management from intent to decommission."
 ),
 "top": "Slice Lifecycle Orchestrator (E2E)",
 "mid_layer": ["RAN Domain Manager Agent", "Transport Domain Manager Agent", "Core (5GC) Domain Manager Agent"],
 "leaves_by_mid": [
   ["RAN Resource Partitioning Agent", "gNB Config Agent", "RAN SLA Assurance Agent"],
   ["Transport Slicing (VPN/Segment Routing) Agent", "Bandwidth Reservation Agent"],
   ["Network Slice Subnet (NSSMF) Agent", "QoS/5QI Policy Agent", "Core Assurance Agent"],
 ],
 "actions": ["OSS/BSS Order Fulfillment", "SLA Dashboard for Enterprise Customer", "Auto-Scaling Trigger (K8s/CNF)"],
 "agents_table": [
   ("Slice Lifecycle Orchestrator", "Translates enterprise intent (NEST template) into cross-domain design plan and tracks lifecycle state"),
   ("RAN Domain Manager", "Coordinates RAN-side slicing agents and reports RAN SLA compliance upward"),
   ("Transport Domain Manager", "Coordinates segment-routing/VPN agents to guarantee latency/bandwidth across transport"),
   ("Core Domain Manager", "Coordinates 5GC NSSMF/QoS agents for slice subnet instantiation"),
   ("RAN SLA Assurance Agent", "Continuously compares live RAN KPIs vs slice SLA and raises breach events"),
   ("QoS/5QI Policy Agent", "Maps enterprise requirements to 5QI/QoS flow policies in the PCF"),
   ("Core Assurance Agent", "Monitors slice subnet health and triggers auto-scaling of CNFs"),
 ],
 "tech_table": [
   ("Intent capture", "TM Forum NEST/GST templates parsed by an LLM intent-extraction agent"),
   ("Agent framework", "Hierarchical LangGraph graph-of-graphs (top orchestrator invokes sub-graphs)"),
   ("RAN control", "O-RAN RIC (near-RT/non-RT) xApps/rApps"),
   ("Transport control", "Segment Routing / SR-TE controller (Cisco XTC / Juniper)"),
   ("Core control", "5GC NSSMF via 3GPP SA5 APIs, ETSI NFV MANO"),
   ("Assurance/telemetry", "Prometheus + Thanos federated across domains"),
   ("Closed-loop policy", "ONAP CLAMP-style control loops triggered by agent decisions"),
   ("Enterprise portal", "React/Next.js self-service slice ordering UI"),
 ],
 "retrospective": [
   "Start with a shared cross-domain data model (3GPP SA5 + TM Forum) from day one; retrofitting it after each domain manager had its own schema cost a full sprint.",
   "Add a simulation/what-if agent so enterprise customers can preview SLA feasibility before committing an order.",
   "Give domain managers explicit negotiation protocol (not just command-response) so RAN/Transport/Core can jointly resolve conflicting resource constraints.",
   "Instrument each hierarchy level with distributed tracing early — debugging cross-domain failures without it was the biggest time sink.",
 ],
},
{
 "id": 3, "slug": "capacity-planning-traffic-forecasting",
 "title": "Proactive Capacity Planning & Traffic Forecasting",
 "pattern": "pipeline",
 "problem": (
   "Network planning teams manually forecast cell/site capacity using spreadsheets and quarterly reviews, "
   "missing fast-moving demand shifts from new housing developments, events, or seasonal tourism. This leads to "
   "either costly over-provisioning or congestion-driven churn. An automated pipeline is needed that ingests "
   "traffic trends, external signals (events, population growth), and produces prioritized capacity upgrade plans."
 ),
 "stages": ["Data Ingestion Agent (traffic + external signals)", "Forecasting Agent (per-cell demand projection)",
            "Congestion Risk Scoring Agent", "Upgrade Prioritization & Budget Optimization Agent",
            "Plan Narrative & Approval-Pack Generation Agent"],
 "actions": ["Capacity Planning System (Amdocs/Nokia)", "Finance/Budget Approval Workflow", "Field Ops Work Order"],
 "agents_table": [
   ("Data Ingestion Agent", "Pulls PM counters, subscriber growth data, and external event/population feeds"),
   ("Forecasting Agent", "Runs per-cell time-series forecasting (traffic, PRB utilization) 3/6/12 months out"),
   ("Congestion Risk Scoring Agent", "Scores each site by probability and severity of SLA-impacting congestion"),
   ("Upgrade Prioritization Agent", "Optimizes upgrade sequence under a capex budget constraint (knapsack-style)"),
   ("Plan Narrative Agent", "Generates the human-readable business case and approval pack via LLM"),
 ],
 "tech_table": [
   ("Data ingestion", "Airflow DAGs pulling from PM systems and public event/census APIs"),
   ("Forecasting", "Nixtla TimeGPT / Prophet ensembles per cell-sector"),
   ("Risk scoring", "Gradient-boosted classifier (XGBoost) trained on historical congestion incidents"),
   ("Optimization", "OR-Tools / PuLP for constrained upgrade-sequence optimization"),
   ("Narrative generation", "Claude for business-case narrative + auto-generated slides"),
   ("Orchestration", "Prefect/Airflow pipeline invoking each agent as a task"),
   ("Storage", "Snowflake/BigQuery for PM history and forecast outputs"),
   ("Approval workflow", "ServiceNow/Jira integration for capex sign-off"),
 ],
 "retrospective": [
   "Pipeline (strictly sequential) was simpler to build but the forecasting stage became a bottleneck; would parallelize per-region forecasting as an orchestrator-worker sub-step.",
   "Add a feedback loop agent that compares realized traffic vs. forecast quarterly to auto-recalibrate models — this was manual in v1.",
   "Include a scenario-comparison agent (e.g., 'defer upgrade 1 quarter') rather than a single recommended plan.",
   "Validate external event-signal quality (e.g., stale population data) earlier; bad inputs silently degraded forecast accuracy for two release cycles.",
 ],
},
{
 "id": 4, "slug": "self-healing-network-closed-loop",
 "title": "Self-Healing Network (Closed-Loop Automation)",
 "pattern": "event-swarm",
 "problem": (
   "Transient network degradations (interference spikes, memory leaks in CNFs, flapping links) require sub-minute "
   "reaction to avoid customer-visible impact, far faster than human-in-the-loop ticketing allows. The operator "
   "wants an always-on swarm of reactive agents subscribed to a shared event bus that can detect, decide, and act "
   "on well-understood fault classes autonomously, escalating only novel or high-risk situations."
 ),
 "bus_name": "Network Event Bus (Kafka)",
 "agents": ["Link Flap Detector Agent", "CNF Memory/Restart Agent", "Interference Mitigation Agent",
            "Congestion Load-Balancing Agent", "Anomaly Novelty Detector Agent"],
 "actions": ["Automated Remediation (Ansible/K8s)", "Closed-loop Audit Log", "Escalation to NOC Orchestrator"],
 "agents_table": [
   ("Link Flap Detector Agent", "Subscribes to interface state-change events, detects flapping patterns and requests link dampening"),
   ("CNF Memory/Restart Agent", "Watches container memory/CPU metrics, triggers graceful pod restart before OOM-kill"),
   ("Interference Mitigation Agent", "Reacts to RF interference events by requesting PCI/frequency reassignment"),
   ("Congestion Load-Balancing Agent", "Shifts traffic via MLB (mobility load balancing) policies when PRB utilization crosses threshold"),
   ("Anomaly Novelty Detector Agent", "Flags event patterns unseen in the last 90 days and escalates to human/orchestrator rather than auto-acting"),
 ],
 "tech_table": [
   ("Event bus", "Apache Kafka with schema-registry (Avro) topics per domain"),
   ("Agent runtime", "Lightweight event-driven agents (Python asyncio) subscribed via consumer groups"),
   ("Decisioning", "Rules engine (Drools) for known fault classes + LLM fallback for ambiguous events"),
   ("Novelty detection", "Autoencoder-based anomaly scoring on event embeddings"),
   ("Remediation execution", "Kubernetes operators + Ansible for CNF/VNF actions"),
   ("Guardrails", "Rate-limiter and blast-radius policy service to cap concurrent auto-actions"),
   ("Audit/observability", "Immutable audit log (append-only) + Grafana closed-loop dashboard"),
   ("Escalation", "PagerDuty/ServiceNow webhook from Novelty Detector Agent"),
 ],
 "retrospective": [
   "V1 had no global blast-radius guardrail; two agents independently restarting adjacent CNFs caused a cascading outage — added a shared rate-limiter service.",
   "Event schema evolution broke agents silently; would enforce schema-registry compatibility checks in CI from the start.",
   "Add a 'cool-down memory' so the same agent doesn't oscillate (act, revert, act) on a flapping condition — implemented reactively after an incident.",
   "Separate 'decide' and 'act' permissions per agent so lower-trust agents can only recommend, not execute, until proven reliable over N cycles.",
 ],
},
{
 "id": 5, "slug": "churn-prediction-winback",
 "title": "Customer Churn Prediction & Win-Back Orchestration",
 "pattern": "orchestrator-worker",
 "problem": (
   "Postpaid churn is expensive to reverse once a customer has ported out. Existing churn models score risk but "
   "stop short of orchestrating a coordinated, cross-channel retention response (offer design, timing, channel, "
   "agent-assisted call) tailored to the actual churn driver (price, coverage complaints, competitor promo). "
   "The business needs an agentic system that diagnoses *why* a customer is at risk and orchestrates the best "
   "next action within compliance and margin constraints."
 ),
 "orchestrator": "Retention Campaign Orchestrator Agent",
 "workers": ["Churn Risk Scoring Agent", "Churn Driver Diagnosis Agent", "Offer Design & Margin Agent",
             "Channel/Timing Optimization Agent", "Compliance Guardrail Agent"],
 "data_sources": ["CRM/Billing History", "Network Complaint & Trouble Tickets", "Usage/CDR Data",
                  "Competitor Promo Intelligence Feed"],
 "actions": ["Personalized Offer via SMS/App", "Agent-Assist Script for Call Center", "CRM Campaign Log"],
 "human_gate": "Retention Manager Sign-off for High-Value Accounts",
 "agents_table": [
   ("Retention Campaign Orchestrator", "Coordinates diagnosis and offer agents, sequences the outreach plan per customer"),
   ("Churn Risk Scoring Agent", "Real-time propensity score from usage decline, complaint frequency, contract end-date"),
   ("Churn Driver Diagnosis Agent", "LLM-based reasoning over tickets/CDR to classify driver: price, coverage, service, competitor"),
   ("Offer Design & Margin Agent", "Generates offer within approved margin/discount guardrails per driver type"),
   ("Channel/Timing Optimization Agent", "Bandit-based selection of channel and send-time for highest response probability"),
   ("Compliance Guardrail Agent", "Validates offer/messaging against TCPA/regulatory and internal policy before send"),
 ],
 "tech_table": [
   ("Risk scoring model", "XGBoost / LightGBM churn propensity model on Databricks"),
   ("Driver diagnosis", "Claude with RAG over ticket text + structured CDR features"),
   ("Offer optimization", "Constrained optimization (margin bounds) + contextual bandit (Thompson sampling)"),
   ("Orchestration", "LangGraph supervisor with tool-calling into CRM/offer engine"),
   ("Compliance check", "Rules engine + LLM policy-classifier as a gate before dispatch"),
   ("Channel delivery", "Twilio (SMS) / Braze (push) / Genesys (agent-assist)"),
   ("Feedback loop", "Redeemed-offer + post-offer churn outcome fed back to retrain scoring model"),
   ("Data platform", "Snowflake + Feature Store (Feast) for real-time feature serving"),
 ],
 "retrospective": [
   "Add explicit offer-fatigue tracking per customer; early version re-targeted the same segment too often, eroding margin without lifting retention.",
   "Introduce an A/B holdout group by default so campaign lift is measurable, not assumed — this was bolted on after the fact.",
   "Separate the diagnosis agent's confidence into the offer decision explicitly; low-confidence diagnoses should trigger a cheaper generic offer, not a high-margin one.",
   "Give the compliance guardrail agent veto power earlier in the pipeline (pre-offer-design) rather than post-hoc, to avoid wasted optimization cycles on non-compliant offers.",
 ],
},
{
 "id": 6, "slug": "contact-center-triage-resolution",
 "title": "Intelligent Contact Center Triage & Resolution",
 "pattern": "hierarchical",
 "problem": (
   "Telecom contact centers field a mix of billing, technical, sales, and retention calls/chats. Misrouting and "
   "repeated hand-offs frustrate customers and inflate average handle time. The operator wants an agentic layer "
   "that classifies intent, resolves what it safely can end-to-end (plan changes, troubleshooting), and routes "
   "complex cases with full context to the right human specialist."
 ),
 "top": "Contact Center Orchestrator Agent",
 "mid_layer": ["Billing Domain Manager Agent", "Technical Support Domain Manager Agent", "Sales/Retention Domain Manager Agent"],
 "leaves_by_mid": [
   ["Invoice Explanation Agent", "Dispute Intake Agent", "Payment Plan Agent"],
   ["Device Troubleshooting Agent", "Network Outage Lookup Agent", "SIM/eSIM Provisioning Agent"],
   ["Plan Upgrade Agent", "Retention Offer Agent"],
 ],
 "actions": ["CRM Case Update", "Live Human Handoff with Context Summary", "Customer Resolution via Chat/Voice"],
 "agents_table": [
   ("Contact Center Orchestrator", "Classifies intent from the incoming transcript and routes to the right domain manager"),
   ("Billing Domain Manager", "Coordinates billing sub-agents and decides if a human is required (e.g., disputes > $200)"),
   ("Technical Support Domain Manager", "Coordinates diagnostics sub-agents, checks for known outages before troubleshooting"),
   ("Sales/Retention Domain Manager", "Coordinates upgrade/offer sub-agents within approved discount bands"),
   ("Network Outage Lookup Agent", "Queries live outage map/NOC feed to short-circuit unnecessary troubleshooting"),
   ("Device Troubleshooting Agent", "Runs a decision-tree/RAG-grounded diagnostic flow with the customer"),
 ],
 "tech_table": [
   ("Speech/chat interface", "Genesys Cloud / Amazon Connect + real-time ASR (Deepgram)"),
   ("Intent classification", "Fine-tuned classifier + LLM fallback for long-tail intents"),
   ("Orchestration", "Hierarchical LangGraph with domain-manager sub-graphs"),
   ("Knowledge grounding", "RAG over knowledge base (Confluence export) via Weaviate"),
   ("Outage lookup", "Real-time query to NOC outage API"),
   ("Human handoff", "Structured case-summary auto-generated and injected into agent-desktop (Salesforce Service Cloud)"),
   ("Guardrails", "Discount/authority limits enforced as tool-call constraints, not prompt instructions alone"),
   ("Analytics", "Post-call QA scoring agent + dashboard for containment rate, CSAT"),
 ],
 "retrospective": [
   "Initial routing was intent-only; adding customer-value and sentiment signals to the orchestrator's routing decision meaningfully cut escalations for high-value customers.",
   "Handoff summaries were too verbose for agents to scan quickly — redesigned to a 5-bullet structured format after agent feedback.",
   "Would add a 'silent QA' critic agent reviewing bot resolutions in real time, rather than only sampling transcripts after the fact.",
   "Domain managers initially couldn't see each other's context (billing vs retention) causing duplicate offers; added a shared session-state store.",
 ],
},
{
 "id": 7, "slug": "sim-swap-fraud-detection",
 "title": "SIM-Swap & Account-Takeover Fraud Detection",
 "pattern": "debate-critique",
 "problem": (
   "SIM-swap fraud is used to bypass SMS-based 2FA and take over banking/crypto accounts. Static rules generate "
   "too many false positives (blocking legitimate swaps for lost phones) or miss adversarial patterns. A "
   "reflective multi-agent design — a proposer that flags suspicious swaps and a critic that actively tries to "
   "find legitimate explanations — reduces both fraud loss and customer friction."
 ),
 "proposer": "Fraud Hypothesis Proposer Agent",
 "critic": "Legitimate-Explanation Critic Agent",
 "arbiter": "Fraud Decision Arbiter Agent",
 "refs": ["Account/Device History", "SIM-Swap Request Metadata", "Geolocation & Behavioral Biometrics",
          "Known Fraud Ring Patterns DB"],
 "actions": ["Block/Hold SIM Swap", "Step-up Verification Request", "Fraud Case Creation"],
 "agents_table": [
   ("Fraud Hypothesis Proposer Agent", "Flags a swap request as suspicious based on velocity, geo-mismatch, and known fraud-ring signatures"),
   ("Legitimate-Explanation Critic Agent", "Actively searches for evidence supporting a legitimate reason (travel, new device, verified store visit)"),
   ("Fraud Decision Arbiter Agent", "Weighs proposer vs. critic evidence, sets final risk tier and required action"),
   ("Step-up Verification Agent", "Orchestrates additional identity checks (video KYC, security questions) when arbiter requests it"),
   ("Fraud Ring Pattern-Matching Agent", "Cross-references request against graph of known fraud rings/mule device clusters"),
 ],
 "tech_table": [
   ("Graph analytics", "Neo4j fraud graph (devices, SIMs, accounts, IPs) with graph embeddings"),
   ("Proposer/critic reasoning", "Two independently-prompted Claude instances with opposing objectives for adversarial robustness"),
   ("Arbitration logic", "Weighted scoring + human-reviewed calibration set, not a single LLM vote"),
   ("Behavioral biometrics", "Device/typing/location pattern service (BioCatch-style)"),
   ("Step-up verification", "Video KYC vendor API + OTP-alternative flows"),
   ("Real-time decisioning", "Sub-second scoring via a feature store + rules engine hybrid"),
   ("Case management", "Fraud case system (Actimize/SAS) integration"),
   ("Monitoring", "Precision/recall dashboard tracking false-positive customer friction rate"),
 ],
 "retrospective": [
   "Early version let the arbiter be a third LLM vote, which correlated too much with the proposer's framing; replaced with a calibrated scoring function using both agents' extracted evidence.",
   "Add a periodic red-team agent that generates novel fraud patterns to stress-test the proposer/critic pair — this was only done manually at launch.",
   "Track false-positive customer impact (blocked legitimate swaps) as a first-class metric alongside fraud-caught; v1 over-indexed on fraud recall.",
   "Cache the critic's 'legitimate explanation' search results per customer to cut latency — regenerating full context every swap request was the biggest cost driver.",
 ],
},
{
 "id": 8, "slug": "telecom-soc-threat-hunting",
 "title": "Telecom SOC Threat Hunting & Incident Response",
 "pattern": "orchestrator-worker",
 "problem": (
   "Telecom networks are high-value targets (signaling exploits, GTP/Diameter abuse, DDoS against core). SOC "
   "analysts are overwhelmed by SIEM alert volume and struggle to correlate signaling-layer anomalies with "
   "IT-security telemetry. An agentic SOC layer is needed to triage, enrich, and where appropriate auto-contain "
   "threats while keeping analysts in control of high-impact actions."
 ),
 "orchestrator": "SOC Incident Response Orchestrator",
 "workers": ["Signaling Abuse Detection Agent (SS7/Diameter/GTP)", "DDoS Detection Agent", "SIEM Correlation Agent",
             "Threat Intelligence Enrichment Agent", "Insider-Threat Behavioral Agent"],
 "data_sources": ["SIEM (Splunk/Sentinel)", "Signaling Firewall Logs", "NetFlow/sFlow Data", "Threat Intel Feeds (STIX/TAXII)"],
 "actions": ["Auto-block via Signaling Firewall", "SOAR Playbook Execution", "Analyst Case in SOAR Platform"],
 "human_gate": "SOC Tier-2 Analyst Approval for Containment Actions",
 "agents_table": [
   ("SOC Orchestrator", "Fans out incoming alerts to specialized detection agents and aggregates a unified incident view"),
   ("Signaling Abuse Detection Agent", "Detects SS7/Diameter/GTP anomalies indicating location-tracking or fraud attempts"),
   ("DDoS Detection Agent", "Identifies volumetric/protocol attacks against core network elements via NetFlow analysis"),
   ("SIEM Correlation Agent", "Correlates IT-security alerts with telecom-specific signals for a unified kill-chain view"),
   ("Threat Intelligence Enrichment Agent", "Enriches indicators (IPs, IMSIs, ASNs) against external threat intel feeds"),
   ("Containment Execution Agent", "Executes approved SOAR playbooks (block, isolate, rate-limit)"),
 ],
 "tech_table": [
   ("SIEM", "Splunk / Microsoft Sentinel"),
   ("Signaling security", "Signaling firewall (Oracle/Mavenir) log ingestion"),
   ("SOAR", "Palo Alto Cortex XSOAR / Splunk SOAR for playbook execution"),
   ("Threat intel", "MISP + commercial STIX/TAXII feeds"),
   ("Agent orchestration", "LangGraph supervisor with tool-use into SIEM/SOAR APIs"),
   ("Anomaly detection", "Unsupervised clustering (DBSCAN) on signaling traffic features"),
   ("Case management", "ServiceNow Security Incident Response module"),
   ("Guardrails", "Two-person-rule enforcement for any auto-containment above defined blast radius"),
 ],
 "retrospective": [
   "Add a 'threat narrative' agent that produces a single human-readable kill-chain story per incident — analysts initially had to piece together outputs from 5 separate agents.",
   "Would benchmark false-positive containment cost (blocked legitimate signaling) as rigorously as detection recall from the start.",
   "Introduce agent-decision replay/simulation mode so new detection agents can be validated against historical incidents before going live.",
   "Signaling and IT-security data had incompatible time granularity; standardizing on a common event-time schema earlier would have saved significant correlation-agent rework.",
 ],
},
{
 "id": 9, "slug": "field-workforce-dispatch-scheduling",
 "title": "Field Workforce Dispatch & Dynamic Scheduling",
 "pattern": "market-based",
 "problem": (
   "Dispatching field technicians for installs, repairs, and tower maintenance across a large geography with "
   "varying skill requirements, SLA windows, and travel time is a hard combinatorial problem that worsens with "
   "same-day emergency truck-rolls. A market-based multi-agent design, where each open job 'auctions' itself to "
   "available technician agents, adapts faster to real-time changes than a centralized static scheduler."
 ),
 "auctioneer": "Dispatch Clearing Agent",
 "bidders": ["Technician Agent (per available technician, bidding based on skill/location/SLA fit)",
             "Emergency Job Priority Agent", "Sub-contractor Capacity Agent"],
 "actions": ["Work Order Assignment System", "Technician Mobile App Push", "SLA Breach Risk Alert"],
 "agents_table": [
   ("Dispatch Clearing Agent", "Runs a continuous combinatorial auction matching open jobs to technician bids optimizing SLA and travel cost"),
   ("Technician Agent", "Represents each technician's real-time location, skills, and remaining capacity; bids on suitable jobs"),
   ("Emergency Job Priority Agent", "Injects priority weighting for SLA-critical/emergency jobs into the auction"),
   ("Sub-contractor Capacity Agent", "Bids in overflow jobs beyond internal technician capacity, factoring in cost"),
   ("Route Optimization Agent", "Post-auction, sequences each technician's daily route to minimize drive time"),
 ],
 "tech_table": [
   ("Auction mechanism", "Combinatorial auction solver (Vickrey-Clarke-Groves inspired) via OR-Tools"),
   ("Technician agents", "Lightweight per-technician agent processes reading live GPS + skill profile"),
   ("Routing", "Google OR-Tools VRP solver / Mapbox Optimization API"),
   ("Real-time state", "Redis for live technician availability/location state"),
   ("Orchestration", "Event-driven microservices coordinating the auction loop every N minutes"),
   ("Mobile integration", "Push notifications via Firebase to technician app"),
   ("SLA monitoring", "Streaming SLA-risk scoring feeding priority weights back into the auction"),
   ("Reporting", "Ops dashboard showing fill-rate, SLA compliance, and drive-time metrics"),
 ],
 "retrospective": [
   "Pure price/cost-based bidding under-weighted technician fatigue/overtime; added a soft constraint penalizing over-scheduling into the bid function.",
   "Auction re-runs every fixed interval caused unnecessary technician re-assignment churn; switched to event-triggered re-auctioning only on material changes.",
   "Would add an explainability layer so dispatchers can see *why* a job was assigned to a given technician — early version was a black-box optimizer output.",
   "Sub-contractor bidding needed real cost-visibility guardrails; initial version could over-select costly overflow capacity when internal techs were briefly unavailable.",
 ],
},
{
 "id": 10, "slug": "billing-dispute-resolution",
 "title": "Billing Dispute Investigation & Resolution",
 "pattern": "pipeline",
 "problem": (
   "Billing disputes (unexpected roaming charges, double-billing, promo-not-applied) require pulling data across "
   "billing, rating, mediation, and CRM systems — a process that today takes agents 15-30 minutes of manual "
   "cross-system lookup per case. An agentic pipeline can auto-investigate the majority of disputes and produce "
   "a ready-to-approve resolution in seconds."
 ),
 "stages": ["Dispute Intake & Classification Agent", "Cross-System Evidence Gathering Agent",
            "Root-Cause Determination Agent", "Resolution & Credit Calculation Agent",
            "Customer Communication Drafting Agent"],
 "actions": ["Billing System Credit/Adjustment", "Customer Notification (Email/SMS)", "CRM Case Closure"],
 "agents_table": [
   ("Dispute Intake & Classification Agent", "Parses the customer's dispute text/call transcript and classifies dispute type"),
   ("Cross-System Evidence Gathering Agent", "Pulls CDRs, rating engine logs, promo eligibility, and mediation records for the billing period"),
   ("Root-Cause Determination Agent", "Reasons over gathered evidence to determine if the charge was correct, a system error, or a promo miss"),
   ("Resolution & Credit Calculation Agent", "Computes the exact credit/adjustment amount per policy rules"),
   ("Customer Communication Agent", "Drafts a clear, empathetic explanation and resolution notice"),
 ],
 "tech_table": [
   ("Intake/classification", "LLM classifier over dispute transcript/ticket text"),
   ("Evidence gathering", "Tool-calling agent hitting billing (Amdocs/CSG), mediation, and CRM APIs"),
   ("Root cause reasoning", "Claude with structured evidence context and policy-rule tool access"),
   ("Credit calculation", "Deterministic rules engine (not LLM) for financial calculation accuracy"),
   ("Communication drafting", "LLM template-grounded generation with brand voice guidelines"),
   ("Orchestration", "Sequential pipeline via Temporal workflow for durability/retries"),
   ("Audit trail", "Full evidence + reasoning trace stored for regulatory/dispute audit"),
   ("Human review queue", "Low-confidence or high-value disputes routed to billing specialist"),
 ],
 "retrospective": [
   "Kept credit calculation strictly rules-based (not LLM-generated) after an early prototype produced a plausible-but-wrong dollar amount — a hard lesson on where not to trust generative reasoning.",
   "Add a pattern-detection agent across disputes to surface systemic billing bugs (e.g., a promo misconfiguration), not just resolve cases one by one.",
   "Would parallelize evidence-gathering calls (billing, mediation, CRM) rather than the initial sequential pipeline, cutting latency significantly.",
   "Communication drafts needed tighter regulatory-language review; added a compliance-phrase checklist agent step after an early miss.",
 ],
},
{
 "id": 11, "slug": "line-onboarding-kyc-automation",
 "title": "New Line/Device Onboarding & KYC Automation",
 "pattern": "orchestrator-worker",
 "problem": (
   "Activating a new postpaid line or financed device requires identity verification, credit risk assessment, "
   "fraud screening, and provisioning — historically siloed steps causing 20+ minute in-store waits or online "
   "drop-off. A coordinated agent team can run these checks in parallel and assemble a single go/no-go decision "
   "with reasons, in near real time."
 ),
 "orchestrator": "Onboarding Decision Orchestrator Agent",
 "workers": ["Identity Verification (KYC) Agent", "Credit Risk Assessment Agent", "Device Financing Fraud Agent",
             "Address/Coverage Validation Agent"],
 "data_sources": ["Government ID / Document Scan", "Credit Bureau Feed", "Device Financing History", "Coverage Map API"],
 "actions": ["Line Activation/Provisioning System", "Device Financing Approval", "Rejection with Reason Notification"],
 "human_gate": "Manual Review for Borderline Credit/Fraud Scores",
 "agents_table": [
   ("Onboarding Decision Orchestrator", "Coordinates parallel checks and produces a single, explainable activation decision"),
   ("Identity Verification (KYC) Agent", "Validates government ID via document/liveness check and matches against application"),
   ("Credit Risk Assessment Agent", "Pulls credit bureau data and computes a plan/device eligibility tier"),
   ("Device Financing Fraud Agent", "Screens for synthetic-identity and device-financing fraud patterns"),
   ("Address/Coverage Validation Agent", "Confirms service address is within coverage and eligible for the requested plan"),
 ],
 "tech_table": [
   ("Document/ID verification", "Onfido/Jumio API for document + liveness verification"),
   ("Credit data", "Credit bureau API (Experian/Equifax) integration"),
   ("Fraud scoring", "Graph-based synthetic identity detection model"),
   ("Coverage check", "Internal coverage-map geospatial API (PostGIS)"),
   ("Orchestration", "LangGraph supervisor with parallel tool calls and timeout handling"),
   ("Decisioning", "Explainable scorecard combining agent outputs with policy thresholds"),
   ("Provisioning", "OSS activation API (order management system)"),
   ("Compliance logging", "Immutable decision log for fair-lending/regulatory audit"),
 ],
 "retrospective": [
   "Would define clear timeout/fallback behavior per worker agent from day one — an early version stalled the whole onboarding flow when one bureau API was slow.",
   "Add an explicit 'reason codes' contract so rejected applicants get actionable, compliant reasons rather than an opaque decline.",
   "Separate fraud-score threshold tuning from credit-score threshold tuning; conflating them in v1 made bias/fairness audits harder.",
   "Introduce a shadow-mode period for any new worker agent (score but don't decide) before it can affect the activation decision.",
 ],
},
{
 "id": 12, "slug": "rf-cell-site-planning-optimization",
 "title": "RF / Cell-Site Planning & Optimization",
 "pattern": "hierarchical",
 "problem": (
   "Optimizing RF parameters (tilt, power, PCI, handover thresholds) across thousands of cells to balance "
   "coverage, capacity, and interference is a continuous, multi-objective problem that RF engineers can only "
   "review a fraction of manually. A hierarchical agent system spanning cluster-level and cell-level optimization "
   "can propose and validate parameter changes at scale."
 ),
 "top": "Network-wide RF Optimization Orchestrator",
 "mid_layer": ["Cluster Optimization Manager Agent (per geographic cluster)"],
 "leaves_by_mid": [
   ["Coverage/Interference Analysis Agent", "Tilt/Power Tuning Agent", "PCI/Neighbor-list Optimization Agent", "Handover Parameter Agent"],
 ],
 "actions": ["Self-Organizing Network (SON) Parameter Push", "RF Change Validation Report", "Rollback on KPI Regression"],
 "agents_table": [
   ("Network-wide RF Optimization Orchestrator", "Prioritizes clusters needing optimization based on KPI degradation and complaint density"),
   ("Cluster Optimization Manager Agent", "Coordinates cell-level agents within a geographic cluster and resolves inter-cell trade-offs"),
   ("Coverage/Interference Analysis Agent", "Models coverage overlap and interference from PM data and drive-test/crowdsourced data"),
   ("Tilt/Power Tuning Agent", "Proposes antenna tilt and power adjustments to balance coverage vs. capacity"),
   ("PCI/Neighbor-list Optimization Agent", "Detects and resolves PCI conflicts and missing neighbor relations"),
   ("Handover Parameter Agent", "Tunes A3/A5 handover thresholds to reduce ping-pong and dropped handovers"),
 ],
 "tech_table": [
   ("SON platform", "3GPP SON functions integrated via vendor EMS (Ericsson ENM/Nokia NetAct)"),
   ("Propagation modeling", "Ray-tracing / statistical propagation models (Atoll/iBwave data)"),
   ("Optimization", "Multi-objective Bayesian optimization per cluster"),
   ("Agent orchestration", "Hierarchical LangGraph with cluster sub-graphs run in scheduled batches"),
   ("Validation", "Digital twin simulation before pushing parameter changes to production"),
   ("Crowdsourced data", "MDT (Minimization of Drive Tests) + crowdsourced RF data ingestion"),
   ("Rollback safety", "Automatic KPI-regression detection triggering parameter rollback"),
   ("Reporting", "RF engineer dashboard with before/after KPI comparison per change"),
 ],
 "retrospective": [
   "Added a mandatory digital-twin validation gate after an early direct-to-production tilt change caused unexpected coverage holes in an adjacent cluster.",
   "Would model inter-cluster interference explicitly from the start — treating clusters as fully independent caused optimization thrashing at cluster boundaries.",
   "Batch optimization cadence (weekly) was too slow for fast-changing hotspots; added an event-triggered fast path for acute congestion.",
   "RF engineers wanted more control over 'why' — added a rationale/explanation output per proposed change, not just the new parameter value.",
 ],
},
{
 "id": 13, "slug": "roaming-settlement-reconciliation",
 "title": "Roaming Partner Settlement Reconciliation",
 "pattern": "pipeline",
 "problem": (
   "Cross-carrier roaming settlement requires reconciling TAP/CDR records between operators, applying complex "
   "bilateral agreement terms, and resolving discrepancies before invoicing — a process finance teams run manually "
   "each month with significant leakage from unresolved disputes. An agent pipeline can automate matching, "
   "discrepancy detection, and dispute-pack generation."
 ),
 "stages": ["TAP/CDR Ingestion & Normalization Agent", "Bilateral Agreement Rate Application Agent",
            "Record Matching & Discrepancy Detection Agent", "Dispute Pack Generation Agent",
            "Settlement Invoice Generation Agent"],
 "actions": ["Settlement Invoice to Partner Operator", "Finance ERP Posting", "Dispute Case to Roaming Ops"],
 "agents_table": [
   ("TAP/CDR Ingestion Agent", "Parses TAP3 files and internal CDRs into a normalized common schema"),
   ("Bilateral Agreement Rate Agent", "Applies the correct wholesale rates per partner agreement and traffic type"),
   ("Record Matching Agent", "Matches inbound/outbound records between operator and partner files, flags mismatches"),
   ("Discrepancy Detection Agent", "Classifies discrepancy root cause (rate mismatch, missing CDR, duplicate) with evidence"),
   ("Dispute Pack Generation Agent", "Assembles a partner-ready dispute package with supporting CDR evidence"),
   ("Settlement Invoice Agent", "Generates the final net settlement invoice after resolved discrepancies"),
 ],
 "tech_table": [
   ("File ingestion", "TAP3/RAP file parsers (GSMA standard) in a Spark ETL pipeline"),
   ("Rate engine", "Rules engine encoding bilateral roaming agreement terms"),
   ("Matching algorithm", "Probabilistic record-linkage (fuzzy matching on IMSI/timestamp/duration)"),
   ("Discrepancy classification", "LLM-assisted root-cause classification over matched-record diffs"),
   ("Orchestration", "Airflow monthly settlement pipeline with agent tasks"),
   ("Dispute documentation", "Automated PDF/Excel pack generation with evidence attachments"),
   ("ERP integration", "SAP/Oracle Financials posting via API"),
   ("Audit", "Full lineage tracking from raw TAP file to final invoice line item"),
 ],
 "retrospective": [
   "Fuzzy matching thresholds needed per-partner tuning (different clock-sync tolerances); a single global threshold in v1 over-flagged discrepancies with some partners.",
   "Would add a partner-facing self-service discrepancy-status portal instead of email-based dispute packs, which slowed resolution cycles.",
   "Discrepancy root-cause classification accuracy improved substantially after adding historical resolution outcomes as few-shot examples.",
   "Settlement currency/FX handling was an afterthought; would design multi-currency support into the rate-application agent from the start.",
 ],
},
{
 "id": 14, "slug": "iot-fleet-anomaly-detection",
 "title": "IoT Device Fleet Anomaly Detection & Remediation",
 "pattern": "blackboard",
 "problem": (
   "Enterprise IoT customers (fleet trackers, smart meters, industrial sensors) run millions of connected "
   "devices on the operator's network. Device-level anomalies (battery drain, firmware issues, connectivity "
   "flapping, potential compromise) are hard to see individually but form clear patterns at fleet scale. A "
   "blackboard architecture lets specialized agents post partial findings that a controller synthesizes into "
   "fleet-level insight and per-device action."
 ),
 "controller": "Fleet Health Controller Agent",
 "store_name": "IoT Fleet Blackboard (device state + findings)",
 "agents": ["Connectivity Pattern Agent", "Battery/Power Anomaly Agent", "Firmware Version Compliance Agent",
            "Security/Compromise Indicator Agent", "Data-Usage Outlier Agent"],
 "actions": ["Customer Fleet Health Dashboard", "Auto-Remediation (firmware push/reboot)", "Security Alert to Enterprise Customer"],
 "agents_table": [
   ("Fleet Health Controller Agent", "Watches the blackboard, decides which specialist agents to trigger, and synthesizes fleet-level findings"),
   ("Connectivity Pattern Agent", "Posts findings on devices with abnormal attach/detach or signal-loss patterns"),
   ("Battery/Power Anomaly Agent", "Detects devices with abnormal battery drain vs. their device-model baseline"),
   ("Firmware Version Compliance Agent", "Flags devices on vulnerable/outdated firmware versions"),
   ("Security/Compromise Indicator Agent", "Posts findings on devices showing botnet-like traffic patterns"),
   ("Data-Usage Outlier Agent", "Flags devices with usage far outside their expected profile (cost/billing risk for the enterprise customer)"),
 ],
 "tech_table": [
   ("Blackboard store", "Redis/DynamoDB shared state store keyed by device ID"),
   ("Device telemetry", "IoT connectivity platform (e.g., operator's IoT CMP) streaming via MQTT/Kafka"),
   ("Anomaly agents", "Per-signal statistical/ML anomaly detectors (Isolation Forest, seasonal baselines)"),
   ("Security detection", "Traffic fingerprinting against known botnet C2 signatures"),
   ("Controller reasoning", "Claude synthesizing multi-agent blackboard entries into a fleet health narrative"),
   ("Remediation", "Firmware-over-the-air (FOTA) trigger + device reboot via CMP API"),
   ("Customer-facing dashboard", "Multi-tenant React dashboard with per-fleet drill-down"),
   ("Alerting", "Webhook/email alerts to enterprise customer's ops team"),
 ],
 "retrospective": [
   "Blackboard grew unbounded for large fleets (10M+ devices); added TTL-based pruning and per-fleet partitioning to keep controller reasoning tractable.",
   "Would add device-model-specific baselines from the start — a single global battery-drain baseline produced too many false positives for heterogeneous device types.",
   "Controller occasionally over-synthesized (inventing fleet-level trends from sparse data); added a minimum-evidence threshold before surfacing a finding.",
   "Security indicator agent needed tighter false-positive control before auto-alerting enterprise customers; added a confidence-tiered alerting policy after early complaints.",
 ],
},
{
 "id": 15, "slug": "sentiment-social-listening-action",
 "title": "Customer Sentiment & Social Listening to Action",
 "pattern": "event-swarm",
 "problem": (
   "Service outages and billing issues trend on social media faster than internal monitoring detects them. "
   "Brand and comms teams need real-time detection of sentiment spikes tied to specific issues, with automatic "
   "routing to the right internal team (NOC, billing, PR) rather than manual monitoring dashboards nobody watches "
   "continuously."
 ),
 "bus_name": "Social/Sentiment Event Bus",
 "agents": ["Social Mention Ingestion Agent", "Sentiment/Topic Classification Agent", "Outage-Correlation Agent",
            "PR Risk Scoring Agent", "Response Drafting Agent"],
 "actions": ["Internal Team Alert (NOC/Billing/PR)", "Approved Public Response Post", "Trend Dashboard Update"],
 "agents_table": [
   ("Social Mention Ingestion Agent", "Streams mentions from X/Reddit/app-store reviews/forums via listening APIs"),
   ("Sentiment/Topic Classification Agent", "Classifies sentiment and topic (outage, billing, device, competitor comparison)"),
   ("Outage-Correlation Agent", "Cross-checks sentiment spikes against live NOC outage data to confirm root cause"),
   ("PR Risk Scoring Agent", "Scores the reputational risk/velocity of a trending topic"),
   ("Response Drafting Agent", "Drafts on-brand public/internal responses for human approval"),
 ],
 "tech_table": [
   ("Social listening", "Brandwatch/Sprinklr API + X/Reddit APIs"),
   ("Sentiment/topic model", "Fine-tuned transformer classifier + LLM for nuanced/sarcasm cases"),
   ("Event bus", "Kafka topics per source, consumed by downstream agents"),
   ("Outage correlation", "Direct query to NOC outage API for geographic/time correlation"),
   ("Risk scoring", "Velocity + reach-weighted scoring model"),
   ("Response drafting", "Claude with brand-voice guidelines and legal-approved phrase library"),
   ("Human approval workflow", "Slack-based approve/edit/reject workflow before any public post"),
   ("Dashboard", "Real-time trend dashboard for comms/exec team"),
 ],
 "retrospective": [
   "All public-facing responses require human approval by design; would keep this hard constraint even as automation matures elsewhere in the system.",
   "Sarcasm/negation handling was a major early accuracy gap in sentiment classification; LLM-based re-scoring of borderline cases improved precision substantially.",
   "Would add rate-limiting on internal alerts — early version paged NOC/billing teams too often on minor sentiment noise before risk-scoring thresholds were calibrated.",
   "Outage correlation agent needed geographic granularity matching (city vs. national) — mismatched granularity caused false negative correlations initially.",
 ],
},
{
 "id": 16, "slug": "spectrum-interference-detection",
 "title": "Spectrum Interference Detection & Mitigation",
 "pattern": "orchestrator-worker",
 "problem": (
   "Unlicensed spectrum use, faulty equipment, or adjacent-band interference degrades network performance in "
   "hard-to-diagnose ways. RF engineers need to triangulate interference sources from distributed sensor/PM data "
   "and coordinate mitigation (filtering, frequency reassignment, or regulatory enforcement action) quickly."
 ),
 "orchestrator": "Interference Investigation Orchestrator",
 "workers": ["Spectrum Sensor Data Agent", "Interference Source Triangulation Agent", "PM/KPI Impact Correlation Agent",
             "Regulatory Filing Agent"],
 "data_sources": ["Distributed Spectrum Sensors", "PM/KPI Data", "Site Equipment Inventory", "Regulatory Spectrum Database"],
 "actions": ["Frequency Reassignment Request", "Field Investigation Work Order", "Regulatory Complaint Filing"],
 "agents_table": [
   ("Interference Investigation Orchestrator", "Coordinates detection, triangulation, and mitigation-path decision"),
   ("Spectrum Sensor Data Agent", "Aggregates readings from distributed RF sensors and detects anomalous energy in-band"),
   ("Interference Source Triangulation Agent", "Uses time-difference-of-arrival across sensors to estimate source location"),
   ("PM/KPI Impact Correlation Agent", "Confirms whether the interference correlates with degraded cell KPIs"),
   ("Regulatory Filing Agent", "Prepares a regulator-ready complaint package if the source is unlicensed/external"),
 ],
 "tech_table": [
   ("Spectrum sensing", "Distributed SDR-based sensor network reporting to a central platform"),
   ("Triangulation", "TDOA/AOA geolocation algorithms"),
   ("Correlation analysis", "Time-series correlation between interference events and KPI degradation"),
   ("Orchestration", "LangGraph supervisor invoking sensing/triangulation/correlation agents"),
   ("Regulatory data", "Integration with national spectrum regulator's licensed-user database"),
   ("Mitigation execution", "SON-driven frequency reassignment via EMS API"),
   ("Case documentation", "Auto-generated regulatory filing with evidence attachments"),
   ("Field coordination", "Work order system integration for on-site equipment inspection"),
 ],
 "retrospective": [
   "Triangulation accuracy was highly sensitive to sensor density; would prioritize sensor placement optimization as an explicit sub-project before scaling the agent system.",
   "Add a historical interference-pattern library so recurring known sources (e.g., a specific radar system) are identified instantly rather than re-investigated.",
   "Regulatory filing agent needed strict factual grounding — added a mandatory evidence-citation requirement after an early draft included an unverified claim.",
   "Would integrate equipment inventory data earlier; many early 'interference' cases were actually the operator's own faulty equipment, which the triangulation-only flow initially missed.",
 ],
},
{
 "id": 17, "slug": "enterprise-sla-compliance-monitoring",
 "title": "Enterprise SLA Compliance Monitoring & Credit Automation",
 "pattern": "pipeline",
 "problem": (
   "Enterprise connectivity contracts carry strict uptime/latency SLAs with financial penalties. Operators often "
   "under-report breaches (manual, error-prone tracking) or over-pay credits due to measurement disputes. An "
   "automated pipeline continuously monitors SLA metrics per contract and computes accurate, auditable credits."
 ),
 "stages": ["SLA Metric Collection Agent", "Contract Term Interpretation Agent", "Breach Detection & Duration Agent",
            "Credit Calculation Agent", "Customer Report & Dispute-Ready Evidence Agent"],
 "actions": ["Automatic Billing Credit", "Enterprise SLA Report Delivery", "Contract Renewal Risk Flag"],
 "agents_table": [
   ("SLA Metric Collection Agent", "Continuously pulls uptime/latency/jitter metrics per circuit from monitoring systems"),
   ("Contract Term Interpretation Agent", "Extracts SLA thresholds and credit formulas from the contract document (RAG over legal text)"),
   ("Breach Detection & Duration Agent", "Detects threshold breaches and computes precise breach duration per contract's measurement window rules"),
   ("Credit Calculation Agent", "Applies the contract-specific credit formula to compute the exact billing credit"),
   ("Customer Report Agent", "Generates a transparent SLA compliance report with evidence, reducing dispute likelihood"),
 ],
 "tech_table": [
   ("Metric collection", "Network monitoring (ThousandEyes/SolarWinds) API polling"),
   ("Contract parsing", "LLM + RAG over contract PDFs (docx/pdf skill-generated extraction) to structure SLA terms"),
   ("Breach detection", "Rules engine applying contract-specific measurement windows and exclusions (maintenance windows)"),
   ("Credit calculation", "Deterministic financial calculation engine, LLM-generated formulas reviewed by legal before go-live"),
   ("Orchestration", "Temporal workflow running continuously per contract"),
   ("Reporting", "Automated PDF report generation with time-series evidence charts"),
   ("Billing integration", "Direct posting to billing system credit ledger"),
   ("Audit trail", "Immutable log of raw metrics → breach determination → credit amount"),
 ],
 "retrospective": [
   "Contract term interpretation needed human legal sign-off per contract template before automation — fully autonomous interpretation of legal language was too risky to trust blindly.",
   "Would build a contract-term versioning system from the start; contract amendments silently broke breach-detection logic in v1.",
   "Add proactive 'at-risk of breach' alerts to network ops, not just after-the-fact credit calculation — this turns the system from reactive accounting into a retention tool.",
   "Measurement-window edge cases (maintenance exclusions, force majeure) caused the most calculation disputes; would invest more upfront in exhaustive rule coverage.",
 ],
},
{
 "id": 18, "slug": "wholesale-bandwidth-marketplace",
 "title": "Wholesale Bandwidth Marketplace (Capacity Trading)",
 "pattern": "market-based",
 "problem": (
   "Operators with excess backbone/transit capacity in some routes and shortages in others could trade capacity "
   "wholesale, but manual bilateral negotiation is slow and inefficient at matching real-time supply and demand "
   "across a multi-operator marketplace. An agent-based marketplace lets each operator's capacity-selling and "
   "capacity-buying agents trade autonomously within pre-approved commercial policy."
 ),
 "auctioneer": "Marketplace Clearing Agent",
 "bidders": ["Operator Capacity-Seller Agent (per participating operator)", "Operator Capacity-Buyer Agent (per participating operator)"],
 "actions": ["Automated Wholesale Contract Generation", "Capacity Provisioning Trigger", "Settlement/Billing Record"],
 "agents_table": [
   ("Marketplace Clearing Agent", "Runs periodic double-auction clearing across all buy/sell offers, sets clearing prices per route"),
   ("Capacity-Seller Agent", "Represents an operator's excess capacity, posts sell offers within a pre-approved price floor"),
   ("Capacity-Buyer Agent", "Represents an operator's capacity shortfall, posts buy bids within a pre-approved price ceiling"),
   ("Contract Generation Agent", "Auto-drafts the wholesale capacity contract for matched trades per standard commercial terms"),
   ("Provisioning Trigger Agent", "Initiates cross-operator circuit provisioning once a trade clears and contract is signed"),
 ],
 "tech_table": [
   ("Auction mechanism", "Continuous double auction (CDA) engine"),
   ("Agent policy", "Each operator configures price bounds/risk policy; agents never exceed pre-approved commercial authority"),
   ("Orchestration", "Market-based agent framework with a neutral clearing service (potentially blockchain-notarized for trust)"),
   ("Contract automation", "Template-based smart-contract-style generation with legal review threshold"),
   ("Provisioning", "Cross-operator NNI (network-to-network interface) provisioning API"),
   ("Settlement", "Automated invoicing tied to actual provisioned/used capacity"),
   ("Trust/security", "Mutual authentication and audit logging across participating operators"),
   ("Analytics", "Market liquidity and price-trend dashboard for participating operators"),
 ],
 "retrospective": [
   "Would require a neutral, mutually-trusted clearing operator or consortium from day one — bilateral trust issues were the biggest adoption blocker, not the technology.",
   "Add circuit-breaker logic to pause trading during anomalous price swings, similar to financial market safeguards.",
   "Initial version cleared trades faster than provisioning teams could fulfill them; added provisioning-capacity awareness into the clearing agent's matching logic.",
   "Legal review of auto-generated contracts was a bottleneck; would pre-approve a narrower set of standard contract templates to reduce review overhead.",
 ],
},
{
 "id": 19, "slug": "predictive-maintenance-network-hardware",
 "title": "Predictive Maintenance for Network Hardware",
 "pattern": "orchestrator-worker",
 "problem": (
   "Reactive maintenance on RRUs, batteries, generators, and cooling systems at cell sites leads to unplanned "
   "outages and expensive emergency truck-rolls. Sensor data exists but is siloed per equipment type. A "
   "coordinated agent team can fuse multi-equipment signals into unified site-health scores and proactive "
   "maintenance schedules."
 ),
 "orchestrator": "Site Health Orchestrator Agent",
 "workers": ["Battery/Power System Agent", "RRU/Radio Hardware Agent", "HVAC/Cooling Agent", "Generator/Backup Power Agent"],
 "data_sources": ["Site Sensor Telemetry (temp, voltage, vibration)", "Equipment Maintenance History", "Weather Forecast Data"],
 "actions": ["Predictive Maintenance Work Order", "Spare-Parts Pre-Positioning", "Site Risk Dashboard"],
 "agents_table": [
   ("Site Health Orchestrator", "Fuses per-equipment health scores into an overall site risk ranking and maintenance schedule"),
   ("Battery/Power System Agent", "Predicts battery degradation and backup-runtime risk from voltage/temperature trends"),
   ("RRU/Radio Hardware Agent", "Detects early failure signatures in radio units (VSWR trends, temperature anomalies)"),
   ("HVAC/Cooling Agent", "Predicts cooling system failures that risk equipment overheating"),
   ("Generator/Backup Power Agent", "Tracks generator run-hours, fuel levels, and predicts maintenance-due dates"),
 ],
 "tech_table": [
   ("Sensor ingestion", "Site IoT gateway streaming to Kafka/AWS IoT Core"),
   ("Predictive models", "Per-equipment-type survival analysis / remaining-useful-life models (Weibull-based)"),
   ("Orchestration", "LangGraph supervisor combining worker outputs into a composite site risk score"),
   ("Weather integration", "Weather API for heat/storm risk adjustment on cooling and power predictions"),
   ("Maintenance scheduling", "Optimization to bundle nearby-site maintenance into efficient technician routes"),
   ("Spare parts", "Inventory system integration to pre-position likely-needed parts"),
   ("Dashboard", "Site risk heatmap for network operations leadership"),
   ("Feedback loop", "Actual failure events fed back to retrain remaining-useful-life models"),
 ],
 "retrospective": [
   "Individual equipment models were accurate but the orchestrator's initial naive-average site score under-weighted correlated failure modes (e.g., cooling failure causing radio failure); moved to a Bayesian network-based fusion.",
   "Would integrate with the field-dispatch marketplace (use case 9) from the start rather than as a separate work-order silo.",
   "Add cost-benefit reasoning (maintenance cost vs. predicted outage cost) explicitly into the scheduling decision, not just risk ranking.",
   "Sensor data quality varied wildly by site vintage; would budget more upfront effort for sensor data-quality agents/validation before trusting predictions.",
 ],
},
{
 "id": 20, "slug": "personalized-plan-upsell-agent",
 "title": "Personalized Plan Recommendation & Upsell Agent",
 "pattern": "debate-critique",
 "problem": (
   "Generic upsell campaigns (blanket 'upgrade to unlimited' offers) have low conversion and can push customers "
   "onto plans that don't fit their usage, increasing churn later. A reflective agent pair — one proposing a "
   "recommendation optimized for revenue and one critiquing it for actual customer fit — produces recommendations "
   "that are both profitable and durable."
 ),
 "proposer": "Revenue-Optimized Recommendation Agent",
 "critic": "Customer-Fit Critic Agent",
 "arbiter": "Recommendation Arbiter Agent",
 "refs": ["Usage History (data/voice/roaming)", "Plan Catalog & Pricing", "Past Upgrade/Downgrade History", "Customer Segment Profile"],
 "actions": ["In-App/SMS Personalized Offer", "Call-Center Agent Recommendation Panel", "Offer Outcome Tracking"],
 "agents_table": [
   ("Revenue-Optimized Recommendation Agent", "Proposes the plan/add-on combination maximizing expected revenue lift"),
   ("Customer-Fit Critic Agent", "Checks the proposal against actual usage patterns and flags likely-poor-fit or churn-risk recommendations"),
   ("Recommendation Arbiter Agent", "Balances revenue and fit signals into a final recommendation with a rationale"),
   ("Offer Timing Agent", "Determines the best moment to present the offer (e.g., after a positive support interaction)"),
   ("Outcome Tracking Agent", "Monitors acceptance, subsequent usage, and churn to close the feedback loop"),
 ],
 "tech_table": [
   ("Usage analysis", "Feature engineering on CDR/data-usage time series (Databricks)"),
   ("Recommendation proposer", "Uplift-modeling based recommender (causal ML) rather than plain propensity scoring"),
   ("Fit critic", "Rules + LLM reasoning comparing proposed plan against 90-day usage envelope"),
   ("Arbitration", "Weighted multi-objective scoring (expected revenue vs. predicted fit/churn risk)"),
   ("Timing optimization", "Contextual bandit selecting moment/channel"),
   ("Delivery", "In-app SDK + Braze/Twilio for outreach"),
   ("Feedback loop", "Outcome tracking feeding back into both proposer and critic model retraining"),
   ("Experimentation", "Built-in A/B testing framework to measure incremental lift vs. control"),
 ],
 "retrospective": [
   "Would formalize the critic's 'fit' threshold with real churn outcome data from the start; early thresholds were expert-guessed and too conservative, suppressing profitable offers.",
   "Add explicit guardrails against recommending downgrades that cut into revenue without clear churn-prevention justification.",
   "Arbiter's rationale output turned out valuable for call-center agents' trust in the tool — would make explanation-generation a first-class requirement, not an afterthought.",
   "Offer Timing Agent needed fatigue/frequency caps per customer, added after early over-messaging complaints.",
 ],
},
]
