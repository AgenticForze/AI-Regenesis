# Architecture decision records

Lightweight records of the decisions that shape this architecture, in the format popularised by Michael Nygard. Copy [`0000-template.md`](0000-template.md) to add your own.

| ADR | Decision | Status |
| --- | --- | --- |
| [0001](0001-central-llm-gateway.md) | Put one gateway in front of every model | Accepted |
| [0002](0002-autonomy-per-action-type.md) | Set autonomy per action type, earned with evidence | Accepted |
| [0003](0003-policy-outside-the-prompt.md) | Enforce action policy in a deterministic service, not the prompt | Accepted |
| [0004](0004-separate-reasoning-and-action-identities.md) | Separate reasoning identities from action identities | Accepted |
| [0005](0005-fine-tune-open-weights-not-pretrain.md) | Fine-tune open-weight models; do not pre-train | Accepted |
| [0006](0006-managed-agent-runtime-by-default.md) | Use the cloud's managed agent runtime by default | Accepted |
