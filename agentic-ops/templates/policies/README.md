# Example action policies

Two equivalent starting points for gate G9 (action policy):

- [`action_policy.rego`](action_policy.rego) — Open Policy Agent, used in the Google Cloud edition
- [`action_policy.cedar`](action_policy.cedar) — Cedar, used by Amazon Bedrock AgentCore Policy in the AWS edition

Both express the same rules: an action must be on the agent's allow-list, be at or below its configured autonomy level, respect change freezes and blast-radius limits, and never touch IAM or organisation settings. They are illustrative, not production-ready; add tests and adapt the input schema to your gateway.

Test the Rego policy locally:

```bash
opa eval -d action_policy.rego -i example_input.json "data.agentops.action.decision"
```
