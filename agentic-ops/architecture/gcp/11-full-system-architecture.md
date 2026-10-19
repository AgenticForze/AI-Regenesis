# Full system architecture

This view places every platform component in its network trust zone and shows the physical and logical paths between them: public edge, hybrid transit (Interconnect and VPN), the hub network, the platform perimeter, the restricted enclave and the security management zone. Nothing in the platform core has a public IP; the only internet-facing surface is the global load balancer protected by Cloud Armor.

![Full system architecture across trust zones](../../diagrams/png/gcp-full-system-architecture.png)
[SVG version](../../diagrams/svg/gcp-full-system-architecture.svg)

*Figure 9. Full system view across trust zones. Solid lines are request paths; dotted lines are control, audit or backup paths.*

## Trust zones

| Zone | What lives there | Entry rule | Key controls |
| --- | --- | --- | --- |
| Z0 External | Users, partners, SaaS, on-prem, other clouds | Untrusted by default | Device posture, identity federation, contractual controls for SaaS |
| Z1 Global edge | Global ALB, Cloud Armor, IAP | Only public IPs in the estate; HTTPS 443 only | WAF (OWASP CRS), Adaptive Protection, bot management, rate limits, geo policy, TLS 1.2+ with modern cipher policy |
| Z2 Hybrid transit and hub | Interconnect, HA VPN, NCC, Cloud Routers, NGFW, Secure Web Proxy, DNS | BGP-learned routes from approved prefixes only | MACsec on Interconnect, IPsec on VPN, IPS inspection on all north-south traffic, route filtering, FQDN egress allow-list |
| Z3 Platform core | Apigee, agents, gateway, SLMs, tools, knowledge | Through Apigee or NGFW only; VPC-SC perimeter on all Google APIs | No external IPs (org policy), service mesh mTLS, per-agent service accounts, CMEK |
| Z4 Restricted enclave | In-house LLM, regulated data, security telemetry with PII | Perimeter bridge from LLM gateway only, one direction | Separate VPC-SC perimeter, Confidential Computing, Cloud EKM or HSM keys, Access Approval, no internet egress at all |
| Z5 Security and management | KMS, SCC, SecOps, log sinks, PAM | Security team identities only, via PAM with justification | Separate perimeter and folder, locked log buckets with retention, dual control on keys |

---

[← Security and governance](10-security-and-governance.md) · [Index](README.md) · [Network and connectivity →](12-network-and-connectivity.md)
