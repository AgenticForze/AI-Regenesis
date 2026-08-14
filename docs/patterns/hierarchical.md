---
layout: default
title: Hierarchical Multi-Agent (Manager-of-Managers) Pattern — AI-Regenesis
description: A top-level orchestrator delegates to domain-manager agents, each of
  which further delegates to leaf specialist agents. Best for problems that naturally…
permalink: /patterns/hierarchical/
---

# Pattern: Hierarchical Multi-Agent (Manager-of-Managers)

A **top-level orchestrator** delegates to **domain-manager agents**, each of which further delegates to **leaf specialist agents**. Best for problems that naturally decompose into domains-of-domains (network domains, legal/financial/commercial workstreams) where each manager needs autonomy to resolve trade-offs within its domain before reporting up.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [5G Network Slice Lifecycle Orchestration]({{ '/telecom/02-5g-network-slicing-orchestration/' | relative_url }}) |
| Telecommunications | [Intelligent Contact Center Triage & Resolution]({{ '/telecom/06-contact-center-triage-resolution/' | relative_url }}) |
| Telecommunications | [RF / Cell-Site Planning & Optimization]({{ '/telecom/12-rf-cell-site-planning-optimization/' | relative_url }}) |
| Financial Services | [Credit Underwriting & Loan Origination]({{ '/finance/02-credit-underwriting-loan-origination/' | relative_url }}) |
| Financial Services | [Regulatory Compliance Monitoring & Reg Reporting]({{ '/finance/07-regulatory-compliance-monitoring-reporting/' | relative_url }}) |
| Financial Services | [Mergers & Acquisitions Due Diligence]({{ '/finance/14-ma-due-diligence/' | relative_url }}) |
| Financial Services | [Customer Complaint Handling (Regulatory Compliance)]({{ '/finance/18-complaint-handling-regulatory-compliance/' | relative_url }}) |
| BSS/OSS | [Product Catalog & Offer Management Automation]({{ '/bssoss/02-product-catalog-offer-management/' | relative_url }}) |
| BSS/OSS | [Subscription Lifecycle & Entitlement Management]({{ '/bssoss/09-subscription-lifecycle-entitlement/' | relative_url }}) |
| BSS/OSS | [Service Catalog-to-Network Activation Mapping (TMF Open APIs)]({{ '/bssoss/12-service-catalog-network-activation-mapping/' | relative_url }}) |

---
[← Back to home]({{ '/' | relative_url }})
