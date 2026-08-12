# Pattern: Human-in-the-Loop Escalation Chain

A chain of automation agents attempts full resolution, gated by a **confidence/risk gate** that routes low-confidence or high-risk cases to a human specialist, whose decision feeds back into the automated action layer. Best for regulated or high-consequence decisions where full autonomy is inappropriate but full manual handling doesn't scale.

## Use cases using this pattern

| Domain | Use Case |
|---|---|
| BSS/OSS | [Dunning & Prepaid/Postpaid Collections Automation](../docs/bssoss/16-dunning-collections-automation/README.md) |

---
[← Back to home](../README.md)
