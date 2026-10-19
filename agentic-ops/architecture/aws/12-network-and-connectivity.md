# Network and connectivity

## 12.1 Direct Connect primary, Site-to-Site VPN backup

Data centres connect through Dedicated Direct Connect in the maximum-resiliency model: four connections across two Direct Connect locations per Region pair, with MACsec on 10 and 100 Gbps ports. Transit virtual interfaces land on a Direct Connect gateway associated with Transit Gateways in each Region. Accelerated Site-to-Site VPN attachments on the Transit Gateways carry the same prefixes with a longer AS path, so they only take traffic when Direct Connect fails; they also serve branches and partners. Cloud WAN can replace per-Region Transit Gateways for global segmentation as the estate grows.

![AWS hybrid connectivity with Direct Connect primary and VPN backup](../../diagrams/png/aws-hybrid-connectivity.png)
[SVG version](../../diagrams/svg/aws-hybrid-connectivity.svg)

*Figure 10. Hybrid transit on AWS. VPN paths are dashed amber; the enclave is reachable only through PrivateLink.*

| Link | Purpose | Encryption | Routing |
| --- | --- | --- | --- |
| Dedicated Direct Connect (4 × 10/100G) | Primary DC connectivity, telemetry, on-prem actions | MACsec; optional private IP VPN over DX for IPsec end to end | Transit VIF to DX gateway, BGP communities for local preference |
| Site-to-Site VPN (accelerated) | Backup path, branches, partners | IKEv2 IPsec, AES-256-GCM | BGP, AS-path prepended |
| Partner VPN | Vendors into a scoped partner VPC | IPsec, certificate auth via Private CA | Isolated TGW route table |
| Partner interconnect to other clouds | Actions on Azure and Google Cloud workloads | MACsec or IPsec | BGP to TGW / Cloud WAN |
| PrivateLink and VPC Lattice | AWS services, tools in workload accounts, enclave access | TLS | No routing between VPCs needed |

## 12.2 VPC and IP design

IP addressing is allocated by VPC IPAM from the network account. Platform VPCs are shared to platform accounts with AWS RAM; inspection is centralised in an inspection VPC with Network Firewall in appliance mode on the Transit Gateway.

| Network | Range | Notes |
| --- | --- | --- |
| Inspection VPC | 10.0.0.0/22 | Network Firewall endpoints per AZ, TGW attachment subnets |
| Egress VPC | 10.0.4.0/22 | NAT gateways behind Network Firewall domain allow-list |
| Platform prod (Region A) | 10.16.0.0/16 | Private subnets per AZ for EKS (prefix delegation), AgentCore VPC config, endpoints |
| Platform prod (Region B) | 10.17.0.0/16 | Mirror |
| Restricted enclave | 10.32.0.0/16 | No IGW, no NAT, no TGW route to the internet |
| Nonprod | 10.48.0.0/15 | Separate TGW route table |
| On-prem | 172.16.0.0/12 | Summarised per data centre |

## 12.3 Private access, egress and east-west

- **AWS services.** Interface endpoints for Bedrock runtime, AgentCore, STS, KMS, Secrets Manager, CloudWatch, SSM and others, plus gateway endpoints for S3 and DynamoDB, all with endpoint policies restricted to our organisation.
- **DNS.** Route 53 Resolver inbound and outbound endpoints for hybrid resolution, private hosted zones shared through RAM, and Route 53 Resolver DNS Firewall blocking unapproved domains.
- **Egress.** Denied by default. SaaS calls from executors leave through the egress VPC, where Network Firewall stateful rules allow only listed SNI domains per source CIDR, and NAT gateways present fixed IPs that SaaS vendors can allow-list. Model and enclave subnets have no egress path.
- **East-west.** VPC Lattice service networks with IAM auth policies define which agent may call which tool; security groups reference each other rather than CIDRs.
- **Admin access.** No bastions: Systems Manager Session Manager for instances and nodes, Verified Access for internal web tools, temporary elevated access through an approval workflow on IAM Identity Center permission sets, and break-glass IAM users with hardware MFA monitored by GuardDuty and EventBridge.

---

[← Full system architecture](11-full-system-architecture.md) · [Index](README.md) · [Security gates →](13-security-gates.md)
