# -*- coding: utf-8 -*-
import os, sys, json, re
import yaml as _yaml
sys.path.insert(0, os.path.dirname(__file__))
from templates import (orchestrator_worker, hierarchical, pipeline, blackboard,
                        debate_critique, market_based, event_swarm, human_escalation, PATTERNS)
from svg_patterns import (BUILDERS as SVG_BUILDERS, e2e_platform, decision_engineering_meta_architecture,
                           blueprint_table, rca_deep8_architecture, RCA_BLUEPRINT_ROWS)
from build_order import build_order_for
from deep8_data import PILOTS, CHURN_RETENTION, RCA_REMEDIATION
from deep8_engine import build_deep8_diagram, auto_blueprint_rows, auto_agent_stack, generic_build_order
from bssoss_deep8_data import BSSOSS_SPECS as BSSOSS_DEEP8_SPECS
from finance_deep8_data import FINANCE_SPECS as FINANCE_DEEP8_SPECS
from telecom_deep8_data import TELECOM_SPECS as TELECOM_DEEP8_SPECS

from telecom_data import TELECOM
from finance_data import FINANCE
from bssoss_data import BSSOSS

# ROOT is derived from this file's own location, not hardcoded — the repo can be checked out (or copied,
# as it was for skill/pack packaging) anywhere and this still finds the right docs/ folder. Previously
# hardcoded to "/home/claude/repo", which silently wrote to the wrong location — and silently created a
# second, empty-looking docs/ tree rather than erroring — the moment this script ran from any other path.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

def build_diagram(uc):
    p = uc["pattern"]
    if p == "orchestrator-worker":
        return orchestrator_worker(uc["title"], uc["orchestrator"], uc["workers"], uc["data_sources"],
                                    uc["actions"], uc.get("human_gate"))
    if p == "hierarchical":
        return hierarchical(uc["title"], uc["top"], uc["mid_layer"], uc["leaves_by_mid"], uc["actions"])
    if p == "pipeline":
        return pipeline(uc["title"], uc["stages"], uc["actions"])
    if p == "blackboard":
        return blackboard(uc["title"], uc["controller"], uc["agents"], uc["store_name"], uc["actions"])
    if p == "debate-critique":
        return debate_critique(uc["title"], uc["proposer"], uc["critic"], uc["arbiter"], uc["refs"], uc["actions"])
    if p == "market-based":
        return market_based(uc["title"], uc["auctioneer"], uc["bidders"], uc["actions"])
    if p == "event-swarm":
        return event_swarm(uc["title"], uc["bus_name"], uc["agents"], uc["actions"])
    if p == "human-escalation":
        return human_escalation(uc["title"], uc["auto_agents"], uc["escalation_gate"], uc["human_role"], uc["actions"])
    raise ValueError(p)

def build_svg(uc):
    p = uc["pattern"]
    fn = SVG_BUILDERS[p]
    if p == "orchestrator-worker":
        return fn(uc["title"], uc["orchestrator"], uc["workers"], uc["data_sources"], uc["actions"], uc.get("human_gate"))
    if p == "hierarchical":
        return fn(uc["title"], uc["top"], uc["mid_layer"], uc["leaves_by_mid"], uc["actions"])
    if p == "pipeline":
        return fn(uc["title"], uc["stages"], uc["actions"])
    if p == "blackboard":
        return fn(uc["title"], uc["controller"], uc["agents"], uc["store_name"], uc["actions"])
    if p == "debate-critique":
        return fn(uc["title"], uc["proposer"], uc["critic"], uc["arbiter"], uc["refs"], uc["actions"])
    if p == "market-based":
        return fn(uc["title"], uc["auctioneer"], uc["bidders"], uc["actions"])
    if p == "event-swarm":
        return fn(uc["title"], uc["bus_name"], uc["agents"], uc["actions"])
    if p == "human-escalation":
        return fn(uc["title"], uc["auto_agents"], uc["escalation_gate"], uc["human_role"], uc["actions"])
    raise ValueError(p)

def slug_num(uc):
    return f'{uc["id"]:02d}-{uc["slug"]}'

def front_matter(title, description, permalink, extra=None):
    """
    Builds a validated Jekyll YAML front matter block. Uses yaml.safe_dump rather than hand-rolled string
    escaping — generated titles/descriptions often contain colons, ampersands, and arrows (→) that would
    break naively-quoted YAML, and safe_dump handles all of that correctly regardless of content.
    """
    data = {"layout": "default", "title": title, "description": description, "permalink": permalink}
    if extra:
        data.update(extra)
    block = _yaml.safe_dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    # Validate our own output before it ever reaches disk — catches any future edge case immediately
    # instead of silently shipping a page Jekyll can't parse.
    _yaml.safe_load(block)
    return f"---\n{block}---\n\n"


def meta_description(text, max_len=155):
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(" ", 1)[0]
    return cut + "…"


def render_usecase_md(domain, dslug, uc, diagram, deep8_path=None):
    pattern_label = PATTERNS[uc["pattern"]]
    agents_rows = "\n".join(f'| {n} | {r} |' for n, r in uc["agents_table"])
    tech_rows = "\n".join(f'| {step} | {tech} |' for step, tech in uc["tech_table"])
    retro = "\n".join(f'- {r}' for r in uc["retrospective"])
    human_gate_line = f'\n**Human-in-the-loop checkpoint:** {uc["human_gate"]}\n' if uc.get("human_gate") else ""
    build_order = "\n\n".join(build_order_for(uc))
    deep8_line = (
        f"\n> 🧠 **Deep dive available:** this use case also has a full "
        f"[8-Layer Regenerative Architecture breakdown]({{{{ '{deep8_path}' | relative_url }}}}) — the same "
        f"problem mapped through L1–L8, with an agent-level tools/technologies stack and a suggested build "
        f"order by layer.\n"
        if deep8_path else
        "\n> 🧠 **Deep 8-Layer Regenerative Architecture:** not yet built for this use case — see the "
        "[Deep 8-Layer view]({{ '/deep8/' | relative_url }}) for what's currently available.\n"
    )
    permalink = f"/{dslug}/{slug_num(uc)}/"
    fm = front_matter(
        title=f"{uc['title']} — AI-Regenesis",
        description=meta_description(uc["problem"]),
        permalink=permalink,
    )
    md = fm + f"""# {uc['id']:02d}. {uc['title']}

**Domain:** {domain} &nbsp;|&nbsp; **Architecture pattern:** [{pattern_label}]({{{{ '/patterns/{uc['pattern']}/' | relative_url }}}})
{deep8_line}
## 1. Problem Statement & Use Case

{uc['problem']}

## 2. End-to-End Multi-Agent Architecture

The solution is implemented as a **{pattern_label}** architecture. {human_gate_line}
### 2.1 Agents & Sub-Agents

| Agent | Responsibility |
|---|---|
{agents_rows}

### 2.2 Architecture Diagram

<img src="architecture.svg" alt="{uc['title']} architecture diagram" width="100%"/>

> This diagram is organized as a **layered architecture**: Data &amp; Integration → Orchestration → Agent →
> Action &amp; Execution, plus a cross-cutting Observability &amp; Governance layer (tracing, audit log,
> guardrails, and any human review checkpoint — shown in lavender). See the
> [E2E Platform Architecture]({{{{ '/architecture/e2e-platform-architecture/' | relative_url }}}}) for how this
> layering looks across all 60 use cases at once. A [Mermaid text source](architecture.mmd) of the same
> diagram is also available in this folder.

## 3. Technologies Used (per step)

| Step / Layer | Technology |
|---|---|
{tech_rows}

## 4. Suggested Build Order

{build_order}

## 5. If We Rebuilt This: What Would Improve

{retro}

> ⚙️ **Built with the AI-Regenesis engine.** Every diagram and build order on this page was generated from a
> compact spec by the same engine packaged as the free
> [`quick-reference-engine` skill]({{{{ '/skills/#quick-reference-engine' | relative_url }}}}) — drop your
> own use case in and get the same output.

---
[← Back to {domain} index]({{{{ '/{dslug}/' | relative_url }}}}) &nbsp;|&nbsp; [← Back to home]({{{{ '/' | relative_url }}}})
"""
    return md

def render_domain_index(domain, domain_slug, use_cases):
    rows = "\n".join(
        f"| {uc['id']:02d} | [{uc['title']}]({{{{ '/{domain_slug}/{slug_num(uc)}/' | relative_url }}}}) | {PATTERNS[uc['pattern']]} |"
        for uc in use_cases
    )
    fm = front_matter(
        title=f"{domain} Use Cases — AI-Regenesis",
        description=meta_description(
            f"{len(use_cases)} real multi-agent AI architecture use cases for {domain}, each with a problem "
            f"statement, architecture diagram, agent table, and honest retrospective."
        ),
        permalink=f"/{domain_slug}/",
    )
    return fm + f"""# {domain} — Multi-Agent Use Case Catalog

{len(use_cases)} use cases covering the major {domain.lower()} workflows where multi-agent architectures deliver measurable value: from real-time detection/decisioning to long-running investigation and orchestration workflows.

| # | Use Case | Architecture Pattern |
|---|---|---|
{rows}

---
[← Back to home]({{{{ '/' | relative_url }}}})
"""

def render_pattern_doc(pattern_key, label, all_ucs):
    matches = [(dom, dslug, uc) for dom, dslug, uc in all_ucs if uc["pattern"] == pattern_key]
    rows = "\n".join(
        f"| {dom} | [{uc['title']}]({{{{ '/{dslug}/{slug_num(uc)}/' | relative_url }}}}) |"
        for dom, dslug, uc in matches
    )
    descriptions = {
      "orchestrator-worker": "A central **orchestrator (supervisor) agent** decomposes an incoming task, fans it out to specialized **worker agents** running in parallel, then aggregates their outputs into a single decision or artifact. Best for tasks that decompose cleanly into independent sub-investigations (fraud checks, alarm correlation, onboarding checks) that must complete within a bounded time budget.",
      "hierarchical": "A **top-level orchestrator** delegates to **domain-manager agents**, each of which further delegates to **leaf specialist agents**. Best for problems that naturally decompose into domains-of-domains (network domains, legal/financial/commercial workstreams) where each manager needs autonomy to resolve trade-offs within its domain before reporting up.",
      "pipeline": "Agents execute in a strict **sequential chain**, each consuming the previous agent's output. Best for workflows with a natural linear order (ingest → analyze → decide → generate) where later steps are meaningfully dependent on earlier ones and durability/retryability matters more than parallel speed.",
      "blackboard": "Multiple specialist agents read and write to a **shared blackboard (memory store)**, while a **controller agent** decides which agent to trigger next and synthesizes posted findings. Best for problems where partial, heterogeneous evidence accumulates over time and no single agent has the full picture (fleet health, firm-wide risk).",
      "debate-critique": "A **proposer agent** generates a hypothesis or recommendation; an independently-primed **critic agent** adversarially searches for what the proposer missed or got wrong; an **arbiter agent** weighs both into a final, better-calibrated decision. Best for high-stakes classification/judgment tasks (fraud, surveillance, recommendations) where single-pass LLM reasoning is prone to confirmation bias.",
      "market-based": "Independent agents **bid** for scarce resources (capital, technician time, network capacity) against a **clearing/auctioneer agent** that matches supply and demand. Best for resource-allocation problems with many competing, semi-autonomous stakeholders where a market mechanism adapts faster than centralized scheduling.",
      "event-swarm": "Lightweight agents subscribe to a shared **event bus** and react independently and asynchronously to relevant events, publishing their own findings/actions back to the bus. Best for latency-critical, always-on monitoring where centralized orchestration would add unacceptable latency (real-time fraud scoring, self-healing networks).",
      "human-escalation": "A chain of automation agents attempts full resolution, gated by a **confidence/risk gate** that routes low-confidence or high-risk cases to a human specialist, whose decision feeds back into the automated action layer. Best for regulated or high-consequence decisions where full autonomy is inappropriate but full manual handling doesn't scale.",
    }
    desc_text = descriptions.get(pattern_key, "")
    fm = front_matter(
        title=f"{label} Pattern — AI-Regenesis",
        description=meta_description(re.sub(r"\*\*", "", desc_text)),
        permalink=f"/patterns/{pattern_key}/",
    )
    return fm + f"""# Pattern: {label}

{desc_text}

## Use cases using this pattern

| Domain | Use Case |
|---|---|
{rows}

---
[← Back to home]({{{{ '/' | relative_url }}}})
"""

def render_deep8_md(pilot, quick_path, blueprint_svg_name, diagram_svg_name, permalink):
    agent_rows = "\n".join(
        f"| {layer} | {name} | {purpose} | {io} | {learn} | {prod} |"
        for layer, name, purpose, io, learn, prod in pilot["agent_stack"]
    )
    build_order = "\n\n".join(pilot["build_order"])
    fm = front_matter(
        title=f"{pilot['title']} — Deep 8-Layer — AI-Regenesis",
        description=meta_description(pilot["problem"]),
        permalink=permalink,
    )
    return fm + f"""# Deep 8-Layer Regenerative Architecture: {pilot['title']}

**Domain:** {pilot.get('domain', 'Telecommunications')} &nbsp;|&nbsp; **Quick Reference counterpart:** [{pilot['quick_title']}]({{{{ '{quick_path}' | relative_url }}}}) ({pilot['quick_pattern_label']})

{pilot['intro']}

## 1. Problem Statement & Use Case

{pilot['problem']}

## 2. The 8-Layer Blueprint

<img src="{blueprint_svg_name}" alt="8-layer blueprint: reference model vs. this use case's architecture" width="100%"/>

## 3. Architecture Diagram (Flow View)

<img src="{diagram_svg_name}" alt="8-layer flow diagram with layer labels" width="100%"/>

**Reading the diagram:** {pilot['diagram_note']}

## 4. Agent-Level Architecture Stack

| Layer | Agent Name | Agent Purpose | Inputs / Outputs | Learning Stack | Production Stack |
|---|---|---|---|---|---|
{agent_rows}

## 5. Suggested Build Order (by Layer)

{build_order}

> ⚙️ **Built with the AI-Regenesis engine.** This layer breakdown, the blueprint table, and the build order
> were generated from a compact spec by the same engine packaged as the free
> [`deep8-architecture-engine` skill]({{{{ '/skills/#deep8-architecture-engine' | relative_url }}}}) — map
> your own use case onto the 8-layer framework the same way.

---
[← Back to Deep 8-Layer index]({{{{ '/deep8/' | relative_url }}}}) &nbsp;|&nbsp; [← Back to home]({{{{ '/' | relative_url }}}})
"""

def main():
    os.makedirs(DOCS, exist_ok=True)
    domains = [
        ("Telecommunications", "telecom", TELECOM),
        ("Financial Services", "finance", FINANCE),
        ("BSS/OSS", "bssoss", BSSOSS),
    ]

    # --- Deep 8-Layer Regenerative Architecture pilots ---------------------------------------
    DEEP8_REGISTRY = [
        {"pilot": CHURN_RETENTION, "diagram_fn": decision_engineering_meta_architecture, "blueprint_rows": None},
        {"pilot": RCA_REMEDIATION, "diagram_fn": rca_deep8_architecture, "blueprint_rows": RCA_BLUEPRINT_ROWS},
    ]
    domain_lookup = {dslug: (domain, use_cases) for domain, dslug, use_cases in domains}
    deep8_lookup = {}   # (dslug, id) -> relative path from the quick use case's own folder
    deep8_json = []     # for the website's Deep 8-Layer tree
    deep8_available_ids = set()  # (dslug, id) tuples that have deep8 content

    def _emit_deep8(dslug, ucid, title, quick_title, quick_pattern_label, intro, problem, diagram_note,
                     diagram_svg, blueprint_svg, agent_stack, build_order):
        domain, use_cases = domain_lookup[dslug]
        uc = next(u for u in use_cases if u["id"] == ucid)
        qslug = slug_num(uc)
        deep_dir = os.path.join(DOCS, "deep8", dslug, qslug)
        os.makedirs(deep_dir, exist_ok=True)
        with open(os.path.join(deep_dir, "diagram.svg"), "w") as f:
            f.write(diagram_svg)
        with open(os.path.join(deep_dir, "blueprint.svg"), "w") as f:
            f.write(blueprint_svg)
        quick_permalink = f"/{dslug}/{qslug}/"
        deep8_permalink = f"/deep8/{dslug}/{qslug}/"
        pilot_like = {
            "title": title, "quick_title": quick_title, "quick_pattern_label": quick_pattern_label,
            "intro": intro, "problem": problem, "diagram_note": diagram_note,
            "agent_stack": agent_stack, "build_order": build_order, "domain": domain,
        }
        deep_md = render_deep8_md(pilot_like, quick_permalink, "blueprint.svg", "diagram.svg", deep8_permalink)
        with open(os.path.join(deep_dir, "README.md"), "w") as f:
            f.write(deep_md)

        deep8_lookup[(dslug, ucid)] = deep8_permalink
        deep8_available_ids.add((dslug, ucid))
        deep8_json.append({
            "domain": domain, "domain_slug": dslug, "id": ucid, "title": title,
            "quick_title": quick_title, "slug": qslug, "diagram_svg": diagram_svg,
            "blueprint_svg": blueprint_svg, "problem": problem, "intro": intro,
            "diagram_note": diagram_note, "agent_stack": agent_stack, "build_order": build_order,
            "path": f"docs/deep8/{dslug}/{qslug}/README.md",
            "quick_path": f"docs/{dslug}/{qslug}/README.md",
        })

    # --- the two bespoke, hand-built pilots ---
    for entry in DEEP8_REGISTRY:
        pilot = entry["pilot"]
        diagram_svg = entry["diagram_fn"]()
        blueprint_svg = blueprint_table(entry["blueprint_rows"]) if entry["blueprint_rows"] is not None else blueprint_table()
        _emit_deep8(pilot["dslug"], pilot["id"], pilot["title"], pilot["quick_title"], pilot["quick_pattern_label"],
                    pilot["intro"], pilot["problem"], pilot["diagram_note"], diagram_svg, blueprint_svg,
                    pilot["agent_stack"], pilot["build_order"])

    # --- the spec-driven batch (BSS/OSS, Finance, Telecom) ---
    for dslug, specs in [("bssoss", BSSOSS_DEEP8_SPECS), ("finance", FINANCE_DEEP8_SPECS), ("telecom", TELECOM_DEEP8_SPECS)]:
        for spec_wrap in specs:
            diagram_svg = build_deep8_diagram(spec_wrap["spec"])
            blueprint_svg = blueprint_table(auto_blueprint_rows(spec_wrap["spec"]))
            agent_stack = auto_agent_stack(spec_wrap["spec"])
            build_order = generic_build_order(*spec_wrap["build_order_params"])
            _emit_deep8(dslug, spec_wrap["id"], spec_wrap["title"], spec_wrap["quick_title"],
                        spec_wrap["quick_pattern_label"], spec_wrap["intro"], spec_wrap["problem"],
                        spec_wrap["diagram_note"], diagram_svg, blueprint_svg, agent_stack, build_order)

    all_for_patterns = []
    catalog_json = []
    deep8_roadmap = []  # every use case, flagged available or not, for the "coming soon" tree

    for domain, dslug, use_cases in domains:
        ddir = os.path.join(DOCS, dslug)
        os.makedirs(ddir, exist_ok=True)
        for uc in use_cases:
            diagram = build_diagram(uc)
            diagram_svg = build_svg(uc)
            ucdir = os.path.join(ddir, slug_num(uc))
            os.makedirs(ucdir, exist_ok=True)
            deep8_path = deep8_lookup.get((dslug, uc["id"]))
            md = render_usecase_md(domain, dslug, uc, diagram, deep8_path)
            with open(os.path.join(ucdir, "README.md"), "w") as f:
                f.write(md)
            with open(os.path.join(ucdir, "architecture.mmd"), "w") as f:
                f.write(diagram)
            with open(os.path.join(ucdir, "architecture.svg"), "w") as f:
                f.write(diagram_svg)
            all_for_patterns.append((domain, dslug, uc))
            catalog_json.append({
                "id": uc["id"], "domain": domain, "domain_slug": dslug, "slug": slug_num(uc),
                "title": uc["title"], "pattern": uc["pattern"], "pattern_label": PATTERNS[uc["pattern"]],
                "problem": uc["problem"], "diagram_svg": diagram_svg,
                "agents": uc["agents_table"], "tech": uc["tech_table"], "retro": uc["retrospective"],
                "build_order": build_order_for(uc),
                "path": f"docs/{dslug}/{slug_num(uc)}/README.md",
                "deep8_available": (dslug, uc["id"]) in deep8_available_ids,
            })
            deep8_roadmap.append({
                "domain": domain, "domain_slug": dslug, "id": uc["id"], "title": uc["title"],
                "available": (dslug, uc["id"]) in deep8_available_ids,
                "qslug": slug_num(uc),
            })
        with open(os.path.join(ddir, "README.md"), "w") as f:
            f.write(render_domain_index(domain, dslug, use_cases))

    # patterns
    pdir = os.path.join(DOCS, "patterns")
    os.makedirs(pdir, exist_ok=True)
    for pkey, label in PATTERNS.items():
        with open(os.path.join(pdir, f"{pkey}.md"), "w") as f:
            f.write(render_pattern_doc(pkey, label, all_for_patterns))

    with open(os.path.join(ROOT, "website", "data.json"), "w") as f:
        json.dump(catalog_json, f)

    # Deep 8-Layer index page (roadmap: what's built, what's coming)
    deep8_dir = os.path.join(DOCS, "deep8")
    os.makedirs(deep8_dir, exist_ok=True)
    by_domain = {}
    for row in deep8_roadmap:
        by_domain.setdefault(row["domain"], []).append(row)
    domain_sections = []
    for dname, rows in by_domain.items():
        lines = [f"### {dname}\n", "| # | Use Case | Deep 8-Layer |", "|---|---|---|"]
        for r in rows:
            if r["available"]:
                dslug = r["domain_slug"]
                link = f"[Available →]({{{{ '/deep8/{dslug}/{r['qslug']}/' | relative_url }}}})"
            else:
                link = "Coming soon"
            lines.append(f'| {r["id"]:02d} | {r["title"]} | {link} |')
        domain_sections.append("\n".join(lines))
    fm = front_matter(
        title="Deep 8-Layer Regenerative Architecture — AI-Regenesis",
        description=meta_description(
            "The Deep 8-Layer view maps every use case through the full Integrated Decision Engineering "
            "Meta-Architecture, from foundational data through the regenerative feedback loop."
        ),
        permalink="/deep8/",
    )
    deep8_index_md = fm + f"""# Deep 8-Layer Regenerative Architecture — Index

The Deep 8-Layer view maps a use case through the full Integrated Decision Engineering Meta-Architecture
(L1 Foundational Data & Infrastructure → L8 Feedback & Reinforcement Loops), with an agent-level tools/technologies
stack and a suggested build order by layer. This is a deeper, slower-to-build companion to the
[Quick Reference Architecture]({{{{ '/' | relative_url }}}}) — {"now available for all 60 use cases across Telecom, Financial Services, and BSS/OSS." if len(deep8_available_ids) == 60 else f"currently available for {len(deep8_available_ids)} of 60 use cases, with the rest on the roadmap."}

{chr(10).join(domain_sections)}

---
[← Back to home]({{{{ '/' | relative_url }}}})
"""
    with open(os.path.join(deep8_dir, "README.md"), "w") as f:
        f.write(deep8_index_md)

    # Generate the E2E platform diagram in the same SVG card style and write it alongside its doc
    arch_dir = os.path.join(DOCS, "architecture")
    os.makedirs(arch_dir, exist_ok=True)
    platform_svg = e2e_platform()
    with open(os.path.join(arch_dir, "e2e-platform-architecture.svg"), "w") as f:
        f.write(platform_svg)
    platform_entry = {
        "title": "E2E Platform Reference Architecture",
        "diagram_svg": platform_svg,
        "path": "docs/architecture/e2e-platform-architecture.md",
        "description": (
            "How channels, orchestration, the agent mesh, systems of record, and observability/"
            "governance fit together across all three domains at once. Every individual use case "
            "diagram is a zoomed-in slice of this same layered shape."
        ),
    }

    # Generate the 8-layer Decision Engineering Meta-Architecture flagship example
    deme_svg = decision_engineering_meta_architecture()
    with open(os.path.join(arch_dir, "decision-engineering-meta-architecture.svg"), "w") as f:
        f.write(deme_svg)
    deme_blueprint_svg = blueprint_table()
    with open(os.path.join(arch_dir, "decision-engineering-meta-architecture-blueprint.svg"), "w") as f:
        f.write(deme_blueprint_svg)
    deme_entry = {
        "title": "Decision Engineering Meta-Architecture (8-Layer)",
        "diagram_svg": deme_svg,
        "blueprint_svg": deme_blueprint_svg,
        "path": "docs/architecture/decision-engineering-meta-architecture.md",
        "description": (
            "The full 8-layer stack (Base → Brain → Thinking Center → Conscience → Action → Nervous "
            "System → Leadership Portal → Self-Healing Loop) applied to one concrete high-stakes "
            "decision, with the AI Gateway, Agent Plane, four-part Memory Layer, conditional routing, "
            "and internal/external data stores all made explicit."
        ),
    }
    references = [platform_entry, deme_entry]

    # Inline everything into the website template so index.html works standalone
    tmpl_path = os.path.join(ROOT, "website", "index.template.html")
    if os.path.exists(tmpl_path):
        with open(tmpl_path) as f:
            tmpl = f.read()
        payload = {
            "catalog": catalog_json,
            "references": references,
            "deep8": deep8_json,
            "deep8_roadmap": deep8_roadmap,
        }
        html = tmpl.replace("__DATA_JSON__", json.dumps(payload))
        with open(os.path.join(ROOT, "website", "index.html"), "w") as f:
            f.write(html)
        # Also write to docs/index.html — this is the file GitHub Pages actually serves as the homepage
        # once Pages is set to build from /docs. No Jekyll front matter here on purpose (starts with
        # <!DOCTYPE html>, not "---"), so Jekyll copies it through untouched rather than trying to process it.
        with open(os.path.join(DOCS, "index.html"), "w") as f:
            f.write(html)

    print(f"Built {len(catalog_json)} use cases. Deep 8-Layer available for {len(deep8_available_ids)}.")

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "website"), exist_ok=True)
    main()
