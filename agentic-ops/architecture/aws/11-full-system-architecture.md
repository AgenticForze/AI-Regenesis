# Full system architecture

Every component placed in its trust zone. Nothing in the platform accounts has an internet gateway except the dedicated edge and egress-inspection VPCs; users reach the platform through CloudFront, WAF and Verified Access, and data centres through Direct Connect.

![AWS full system architecture across trust zones](../../diagrams/png/aws-full-system-architecture.png)
[SVG version](../../diagrams/svg/aws-full-system-architecture.svg)

*Figure 9. AWS full system view. Solid lines are request paths; dotted and dashed lines are control, audit or backup paths.*

| Zone | What lives there | Key controls |
| --- | --- | --- |
| Z0 External | Users, partners, SaaS, on-prem, other clouds | Device posture via Verified Access trust providers, federated identity |
| Z1 Global edge | CloudFront, WAF, Shield Advanced, ALB, Identity Center | Managed rule groups, bot control, rate-based rules, geo match, TLS 1.2+ security policy |
| Z2 Network account | Direct Connect, VPN, Cloud WAN, Transit Gateway, Network Firewall, Route 53 Resolver | MACsec, IPsec, route-table segmentation, centralised inspection, DNS Firewall |
| Z3 Platform core | API Gateway, Guardrails, AgentCore, gateway, SLMs, tools, knowledge | Private subnets only, VPC endpoints, SCPs, per-agent roles, KMS CMKs |
| Z4 Restricted enclave | In-house LLM, regulated data | Separate account and OU, no IGW or NAT, PrivateLink-only ingress, KMS external key store, Nitro-based isolation, Nitro Enclaves for key handling |
| Z5 Security and Log Archive | KMS, Security Hub, GuardDuty, Security Lake, CloudTrail Lake | Delegated administrator accounts, S3 Object Lock on logs, break-glass with hardware MFA |

---

[← Security and governance](10-security-and-governance.md) · [Index](README.md) · [Network and connectivity →](12-network-and-connectivity.md)
