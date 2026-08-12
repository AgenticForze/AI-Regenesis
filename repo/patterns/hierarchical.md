# Pattern: Hierarchical Multi-Agent (Manager-of-Managers)

A **top-level orchestrator** delegates to **domain-manager agents**, each of which further delegates to **leaf specialist agents**. Best for problems that naturally decompose into domains-of-domains (network domains, legal/financial/commercial workstreams) where each manager needs autonomy to resolve trade-offs within its domain before reporting up.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| Telecommunications | [5G Network Slice Lifecycle Orchestration](../docs/telecom/02-5g-network-slicing-orchestration/README.md) |
| Telecommunications | [Intelligent Contact Center Triage & Resolution](../docs/telecom/06-contact-center-triage-resolution/README.md) |
| Telecommunications | [RF / Cell-Site Planning & Optimization](../docs/telecom/12-rf-cell-site-planning-optimization/README.md) |
| Financial Services | [Credit Underwriting & Loan Origination](../docs/finance/02-credit-underwriting-loan-origination/README.md) |
| Financial Services | [Regulatory Compliance Monitoring & Reg Reporting](../docs/finance/07-regulatory-compliance-monitoring-reporting/README.md) |
| Financial Services | [Mergers & Acquisitions Due Diligence](../docs/finance/14-ma-due-diligence/README.md) |
| Financial Services | [Customer Complaint Handling (Regulatory Compliance)](../docs/finance/18-complaint-handling-regulatory-compliance/README.md) |
| BSS/OSS | [Product Catalog & Offer Management Automation](../docs/bssoss/02-product-catalog-offer-management/README.md) |
| BSS/OSS | [Subscription Lifecycle & Entitlement Management](../docs/bssoss/09-subscription-lifecycle-entitlement/README.md) |
| BSS/OSS | [Service Catalog-to-Network Activation Mapping (TMF Open APIs)](../docs/bssoss/12-service-catalog-network-activation-mapping/README.md) |

---
[← Back to home](../README.md)
