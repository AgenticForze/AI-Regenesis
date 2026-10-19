package agentops.action

import rego.v1

# Gate G9: decide whether an agent's proposed action may run, needs approval, or is denied.
# Input (illustrative):
# {
#   "agent": {"id": "incident-agent", "allowed_actions": {"k8s.scale_deployment": {"level": "L4", "blast_radius": "single-service"}}},
#   "action": {"name": "k8s.scale_deployment", "blast_radius": "single-service", "target": {"env": "prod", "criticality": "tier-1"}},
#   "context": {"change_freeze": false, "autonomy_kill_switch": false}
# }

levels := {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}

radius_rank := {"none": 0, "single-service": 1, "multi-service": 2, "platform": 3}

forbidden_prefixes := ["iam.", "org.", "billing.", "kms.destroy"]

configured := input.agent.allowed_actions[input.action.name]

default decision := {"result": "deny", "reason": "not on allow-list"}

forbidden if {
	some p in forbidden_prefixes
	startswith(input.action.name, p)
}

over_radius if radius_rank[input.action.blast_radius] > radius_rank[configured.blast_radius]

decision := {"result": "deny", "reason": "forbidden action class"} if forbidden

decision := {"result": "deny", "reason": "kill switch active"} if {
	not forbidden
	input.context.autonomy_kill_switch
}

decision := {"result": "deny", "reason": "blast radius exceeds configuration"} if {
	not forbidden
	not input.context.autonomy_kill_switch
	configured
	over_radius
}

decision := {"result": "require_approval", "reason": "change freeze"} if {
	not forbidden
	not input.context.autonomy_kill_switch
	configured
	not over_radius
	input.context.change_freeze
}

decision := {"result": "require_approval", "reason": sprintf("autonomy %s", [configured.level])} if {
	not forbidden
	not input.context.autonomy_kill_switch
	configured
	not over_radius
	not input.context.change_freeze
	levels[configured.level] == 2
}

decision := {"result": "recommend_only", "reason": sprintf("autonomy %s", [configured.level])} if {
	not forbidden
	not input.context.autonomy_kill_switch
	configured
	not over_radius
	not input.context.change_freeze
	levels[configured.level] < 2
}

decision := {"result": "allow", "reason": sprintf("autonomy %s", [configured.level])} if {
	not forbidden
	not input.context.autonomy_kill_switch
	configured
	not over_radius
	not input.context.change_freeze
	levels[configured.level] >= 3
}
