# Network and connectivity

## 12.1 Hybrid connectivity: Interconnect primary, HA VPN backup

On-premises and other clouds connect through a hub-and-spoke design anchored on Network Connectivity Center. Dedicated Interconnect in the 99.99% topology (four circuits across two metros and two regions) carries production traffic with MACsec encryption at layer 2. HA VPN tunnels over the internet provide an encrypted backup path with lower BGP preference, and serve smaller sites and partners that cannot justify an Interconnect. Cross-Cloud Interconnect links to AWS and Azure where agents need to act on workloads there.

![Hybrid connectivity with Interconnect primary and HA VPN backup](../../diagrams/png/gcp-hybrid-connectivity.png)
[SVG version](../../diagrams/svg/gcp-hybrid-connectivity.svg)

*Figure 10. Hybrid transit. VPN tunnels advertise the same prefixes with a worse MED so they carry traffic only when Interconnect fails.*

| Link | Purpose | Encryption | Availability | Routing |
| --- | --- | --- | --- | --- |
| Dedicated Interconnect (4 × 10/100G) | Primary data centre connectivity, telemetry ingest, agent actions on-prem | MACsec; optional HA VPN over Interconnect for IPsec end to end on regulated flows | 99.99% SLA topology | BGP, MED 100, custom advertised ranges only |
| HA VPN (2 gateways × 2 tunnels) | Backup path, branch sites, partners | IKEv2 IPsec, AES-256-GCM | 99.99% SLA per gateway pair | BGP, MED 200 for DC prefixes |
| Partner HA VPN | Managed-service vendors needing access to a scoped partner spoke | IKEv2 IPsec with certificate authentication | 99.99% | Only the partner spoke's /24 advertised; NGFW rules by secure tag |
| Cross-Cloud Interconnect | Agent actions and telemetry for AWS and Azure workloads | MACsec | 99.99% with redundant pairs | BGP to NCC hub |
| Private Service Connect | Google APIs, Apigee southbound, MCP tools into workload projects | TLS inside Google network | Regional | Consumer endpoints, no VPC peering |

## 12.2 VPC and IP design

A dedicated network hub project hosts the NCC hub, Cloud Routers, NGFW endpoints, Secure Web Proxy and DNS. Platform, nonprod and restricted workloads each get their own Shared VPC host project so that firewall and perimeter changes can be scoped. The ranges below are illustrative and sized for GKE with alias IPs.

| Network | Range | Subnets |
| --- | --- | --- |
| Hub transit | 10.0.0.0/20 | Cloud Router interfaces, NGFW endpoints, SWP, PSC endpoints for Google APIs (10.0.8.0/24) |
| Prod platform (region A) | 10.16.0.0/16 | Nodes 10.16.0.0/20; pods 10.16.64.0/18; services 10.16.128.0/20; Cloud Run direct VPC egress 10.16.16.0/20; PSC consumer 10.16.200.0/24; proxy-only 10.16.250.0/23 |
| Prod platform (region B) | 10.17.0.0/16 | Mirror of region A |
| Restricted enclave | 10.32.0.0/16 | Confidential GKE nodes 10.32.0.0/20; pods 10.32.64.0/18; no Cloud NAT, no internet routes |
| Nonprod | 10.48.0.0/15 | Dev, test, eval replay |
| Partner spoke | 10.60.0.0/24 | Vendor jump services behind IAP only |
| On-prem (advertised to GCP) | 172.16.0.0/12 | Summarised per data centre |

## 12.3 Private access to Google and platform services

- **Google APIs.** A PSC endpoint for the `vpc-sc` API bundle, with private Cloud DNS zones mapping `*.googleapis.com` to it. Vertex AI, BigQuery, Storage and all other API calls stay on Google's network and are forced through VPC-SC checks.
- **On-prem to Google APIs.** On-prem DNS forwards `googleapis.com` to Cloud DNS inbound forwarders; Cloud Routers advertise the PSC endpoint range over Interconnect, so on-prem collectors can write telemetry without internet paths.
- **Apigee X.** Northbound through the global ALB; southbound to agents through PSC, with no VPC peering between Apigee's tenant network and ours.
- **MCP tool reach.** Tools that must act inside a business unit's VPC are published as PSC service attachments from that VPC, so the platform gets one IP per tool with no broad network routes to workload subnets.
- **DNS security.** Private zones per environment, DNSSEC on public zones, and DNS response policies that block resolution of unapproved external domains from the platform core.

## 12.4 Ingress paths

| Caller | Path | Authentication |
| --- | --- | --- |
| Employees (ops console, Gemini Enterprise) | Chrome Enterprise Premium, Cloud Armor, global ALB, IAP, Apigee | Workforce SSO with phishing-resistant MFA, device posture, context-aware access levels |
| Google Chat approvals | Google Chat app to Cloud Run endpoint behind ALB | Google-signed bearer token verified on every event |
| Slack and Teams bots | Cloud Armor (allow-listed source ranges), ALB, Apigee | Request signature verification plus mTLS where supported |
| ITSM and alerting webhooks | Cloud Armor, ALB, Apigee, Pub/Sub | OAuth client credentials or HMAC signatures, replay protection |
| On-prem monitoring and logs | Interconnect, NGFW, internal ALB or Pub/Sub via PSC | Workload Identity Federation with short-lived tokens |
| Partner engineers | HA VPN to partner spoke, then IAP TCP forwarding | Federated partner identity, PAM time-bound grant |

## 12.5 Egress control

Egress is denied by default at the hierarchical firewall policy. Model-serving nodes and the restricted enclave have no egress at all. Agents and MCP tools that must call SaaS go through Secure Web Proxy with an FQDN allow-list per tool service account (for example only the ServiceNow instance for the ITSM executor), TLS inspection where policy allows, and Cloud NAT with static IPs that SaaS vendors can allow-list. Model weights and container images are never pulled at runtime; they enter only through the build project, are scanned and signed, and are served from Artifact Registry.

## 12.6 East-west and microsegmentation

Inside the perimeter, Cloud Service Mesh enforces mTLS with workload identities for every hop, and authorization policies state which agent may call which tool service (for example the incident agent may call the Kubernetes executor but not the IAM executor). Cloud NGFW network firewall policies use IAM-governed secure tags rather than IP ranges, so a compromised workload cannot relabel itself into a broader rule.

| Level | Rule | Action |
| --- | --- | --- |
| Organisation | Allow Google health-check and IAP ranges to tagged backends | Allow |
| Organisation | Deny known malicious IPs (Google threat intelligence) and sanctioned geographies | Deny |
| Organisation | Deny all egress to 0.0.0.0/0 except via SWP and NAT tagged workloads | Deny |
| Folder: agentic-platform | Allow tag `agent-runtime` to `llm-gateway` on 443 | Allow + IPS inspect |
| Folder: agentic-platform | Allow tag `tool-executor` to on-prem 172.16.0.0/12 on declared ports | Allow + IPS inspect + log |
| Folder: agentic-platform | Deny `agent-runtime` to any workload subnet directly | Deny + log |
| Restricted enclave | Allow only `llm-gateway` to `enclave-llm` on 8443 | Allow; everything else deny |

## 12.7 Administrative access

There are no bastion hosts with public IPs and no standing admin roles. Engineers reach the console and APIs through Chrome Enterprise Premium with context-aware access, reach VMs and nodes through IAP TCP forwarding, and gain elevated roles only through Privileged Access Manager with a justification, an approver and an expiry. Two break-glass accounts protected by hardware security keys exist per perimeter; any use pages the security on-call and opens a SecOps case automatically.

---

[← Full system architecture](11-full-system-architecture.md) · [Index](README.md) · [Security gates →](13-security-gates.md)
