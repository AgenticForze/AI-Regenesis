// Gate G9 for the AWS edition, in Cedar (as used by Amazon Bedrock AgentCore Policy).
// Illustrative only: adapt entity types and attributes to your AgentCore Gateway schema.
// Cedar is default-deny; forbid always overrides permit.

// Incident agent may scale or restart workloads, only for single-service blast radius,
// outside a change freeze.
permit (
  principal == Agent::"incident-agent",
  action in [Action::"k8s.scale_deployment", Action::"k8s.restart_pods"],
  resource
)
when {
  context.blast_radius == "single-service" &&
  context.change_freeze == false
};

// Database failover is permitted only when a human approval token is present (autonomy L2).
permit (
  principal == Agent::"incident-agent",
  action == Action::"db.failover",
  resource
)
when {
  context has approval &&
  context.approval.status == "approved" &&
  context.approval.approver != context.requester
};

// No agent may ever change identity, organisation or key-destruction settings.
forbid (
  principal,
  action in [Action::"iam.attach_role_policy", Action::"iam.create_access_key", Action::"org.update_policy", Action::"kms.schedule_key_deletion"],
  resource
);

// Global kill switch.
forbid (principal, action, resource)
when { context.autonomy_kill_switch == true };
