# Autonomy promotion checklist

Copy this file into your decision log for each promotion. One action type, one level at a time.

| Field | Value |
| --- | --- |
| Agent | |
| Action type | |
| Current level → proposed level | L_ → L_ |
| Evidence window | from YYYY-MM-DD to YYYY-MM-DD |
| Requested by | |
| Service owner approving | |

## Evidence

- [ ] At least 200 executions **and** at least 30 days at the current level
- [ ] Plan precision ≥ 98% (attach query or dashboard link)
- [ ] Zero severity-1 incidents caused by this action type
- [ ] Rollback exercised in production or a production-like environment (link to run)
- [ ] Human override rate trending down or stable
- [ ] Blast radius limits configured in policy and tested
- [ ] Kill switch for this action type tested within the window
- [ ] Offline evaluation on the latest golden set shows no regression

## Risk review

- [ ] Data classes touched by this action are allowed at the proposed level
- [ ] Change-freeze calendar applies to this action
- [ ] Audit records capture plan, policy decision, approver (if any) and side effect
- [ ] Regulatory or contractual constraints reviewed (if applicable)

## Decision

- [ ] Approved
- [ ] Approved with conditions:
- [ ] Rejected, reason:

Policy change PR: 
Next review date: 
