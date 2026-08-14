# -*- coding: utf-8 -*-
"""
Combines a Quick-Reference use-case spec (and, optionally, a matching Deep 8-Layer spec entry) plus
engagement details into client-ready proposal CONTENT — structured markdown text, section by section.

Deliberately does NOT generate a .docx or .pptx file itself — that's the `docx` / `pptx` skills' job, and
they're already good at it. This engine's job is the part that's actually this project's IP: turning a
catalog use case (or a client's own described problem) into accurate, well-sequenced proposal prose, priced
against the go-to-market roadmap's own service ladder. See SKILL.md's "Handing off to docx/pptx" section for
how to take this module's output and actually produce the file.
"""

# The four rungs of the consulting service ladder (go-to-market-roadmap.md, Phase 4). Each is a dict of
# display name + a one-line description used in the proposal's "Recommended engagement" section. Pricing
# itself is never hardcoded here — every use of PRICING below takes it as a required argument, because a
# real number is a per-engagement decision, not something this engine should default silently.
SERVICE_TIERS = {
    "audit": {
        "name": "Architecture Audit",
        "description": "A bounded, flat-fee engagement: we run your existing system through the framework "
                        "and deliver a written gap report — fast to start, fast to finish.",
    },
    "workshop": {
        "name": "Workshop",
        "description": "A 1-2 day, mid-ticket engagement: we teach the framework to your team directly, "
                        "using worked examples from the catalog as reference material.",
    },
    "advisory": {
        "name": "Embedded / Fractional Advisory",
        "description": "A retainer engagement: the framework becomes your team's standing operating "
                        "methodology, with ongoing hands-on involvement, not a one-off deliverable.",
    },
    "certification": {
        "name": "Certification Program",
        "description": "License the framework and training materials for your own consultancy to deliver "
                        "under, with direct support during your first engagements.",
    },
}


class ProposalInputError(ValueError):
    pass


def _require(d, key, context):
    if key not in d or not d[key]:
        raise ProposalInputError(f"Missing required field '{key}' in {context}")
    return d[key]


def _executive_summary(client_name, uc, tier_key):
    tier = SERVICE_TIERS[tier_key]
    # Deliberately does NOT lowercase uc["title"] and splice it into a sentence — several catalog titles
    # contain acronyms (RCA, KYC, AML) that read as broken English once lowercased mid-sentence (caught by
    # reading the rendered example: "an AI/agentic approach to multi-agent network fault rca &
    # auto-remediation"). Bolding the title as its own clause avoids needing to change its case at all.
    return (
        f"{client_name} is evaluating an AI/agentic approach to the following problem: **{uc['title']}**. "
        f"This proposal lays out a reference architecture for it — the {tier['name'].lower()} described "
        f"below is scoped to get {client_name} from this reference design to a working, governed system, "
        f"using the same 8-layer framework this architecture was designed against."
    )


def _problem_section(uc):
    return uc["problem"]


def _approach_section(uc, deep8_entry=None):
    # "a/an" has to track the pattern name's actual first sound — "orchestrator-worker" and "event-swarm"
    # both start with a vowel sound, "hierarchical"/"pipeline"/"blackboard"/etc. don't. Caught by reading
    # the rendered example ("a orchestrator-worker pattern" is wrong). A plain vowel-letter check is enough
    # here since none of the 8 pattern names have a silent leading letter or an exception case like "hour".
    article = "an" if uc["pattern"][0].lower() in "aeiou" else "a"
    lines = [
        f"We'd approach this as {article} **{uc['pattern']}** pattern — see the attached architecture "
        f"diagram for the full agent/data-flow layout.",
    ]
    if deep8_entry is not None:
        lines.append(
            "For the governed, production-ready version of this architecture, we'd map it onto the "
            "8-layer Decision Engineering Meta-Architecture (L1 Foundational Data through L8 Feedback & "
            "Reinforcement Loops) — see the attached Deep 8-Layer diagram and blueprint table for the "
            "layer-by-layer build."
        )
    return "\n\n".join(lines)


def _timeline_section(build_order_phases):
    # No leading "**Suggested build order:**" line — the caller already renders this under a
    # "## Suggested Build Order" heading (see render_proposal_markdown), so a bolded restatement directly
    # underneath it just repeats the same words twice in a row. Caught by reading the rendered example.
    lines = []
    for i, phase in enumerate(build_order_phases, start=1):
        lines.append(f"{i}. {phase}")
    return "\n".join(lines)


def _engagement_section(tier_key, price, timeframe, client_name):
    tier = SERVICE_TIERS[tier_key]
    return (
        f"**Recommended engagement: {tier['name']}**\n\n"
        f"{tier['description']}\n\n"
        f"**Investment:** {price}\n\n"
        f"**Timeframe:** {timeframe}\n\n"
        f"Next step: a 30-minute call to confirm scope and schedule the {tier['name'].lower()} for "
        f"{client_name}."
    )


def assemble_proposal_sections(client_name, uc, build_order_phases, tier_key, price, timeframe,
                                deep8_entry=None, consultant_name=None):
    """
    Returns an ordered dict of section_title -> section_markdown_body. Use this if you need the sections
    individually (e.g. to place them into specific docx/pptx slide or page slots) instead of one flat
    document — render_proposal_markdown just joins these with headers.
    """
    if tier_key not in SERVICE_TIERS:
        raise ProposalInputError(f"Unknown service tier '{tier_key}'. Must be one of: "
                                  f"{sorted(SERVICE_TIERS.keys())}")
    _require(uc, "title", "use case")
    _require(uc, "problem", "use case")
    _require(uc, "pattern", "use case")
    if not build_order_phases:
        raise ProposalInputError("build_order_phases must be a non-empty list — pass the output of "
                                  "build_order_for(uc) from the quick-reference-engine skill.")
    if not price:
        raise ProposalInputError("price is required — this engine never invents a number. Pass a real "
                                  "figure or range for this specific engagement.")
    if not timeframe:
        raise ProposalInputError("timeframe is required for the same reason as price.")

    sections = {
        "Executive Summary": _executive_summary(client_name, uc, tier_key),
        "The Problem": _problem_section(uc),
        "Proposed Architecture": _approach_section(uc, deep8_entry),
        "Suggested Build Order": _timeline_section(build_order_phases),
        "Recommended Engagement": _engagement_section(tier_key, price, timeframe, client_name),
    }
    return sections


def render_proposal_markdown(client_name, uc, build_order_phases, tier_key, price, timeframe,
                              deep8_entry=None, consultant_name=None, prepared_date=None):
    """
    Full markdown document, ready to hand to the docx skill (or present directly as a markdown deliverable).
    Embeds `<img>` references to sibling diagram files by convention (see SKILL.md) rather than inlining SVG.
    """
    sections = assemble_proposal_sections(client_name, uc, build_order_phases, tier_key, price, timeframe,
                                           deep8_entry, consultant_name)

    lines = [f"# Proposal: {uc['title']} — {client_name}", ""]
    meta_bits = []
    if consultant_name:
        meta_bits.append(f"Prepared by: {consultant_name}")
    if prepared_date:
        meta_bits.append(f"Date: {prepared_date}")
    if meta_bits:
        lines.append("*" + " · ".join(meta_bits) + "*")
        lines.append("")

    for title, body in sections.items():
        lines.append(f"## {title}")
        lines.append("")
        lines.append(body)
        lines.append("")
        if title == "Proposed Architecture":
            # Diagrams follow the paragraph that says "see the attached diagram" — placing them first
            # (the original order) meant the image appeared with nothing yet explaining what it was.
            # Caught by reading the rendered example end to end.
            lines.append("![Architecture diagram](diagram.svg)")
            lines.append("")
            if deep8_entry is not None:
                lines.append("![Deep 8-Layer diagram](deep8_diagram.svg)")
                lines.append("")

    return "\n".join(lines)
