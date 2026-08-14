# -*- coding: utf-8 -*-
"""
Promotes an accepted submissions/*.json file (from the /build/ page's "Submit to AI-Regenesis" button) into
a real entry in telecom_data.py / bssoss_data.py / finance_data.py.

Usage:
    python3 scripts/promote_submission.py submissions/the-file.json --domain telecom

Writes the new entry with the next available id/slug, fills in every field the submission actually has, and
inserts clearly-marked TODO placeholders for agents_table, tech_table, and retrospective — the three things
that need real curation and that this script deliberately does not fabricate (see submissions/README.md for
why). Does NOT delete the submission file or touch website/data.json — run scripts/build.py separately after
filling in the TODOs, same as any other manual edit to a *_data.py file.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

DOMAIN_FILES = {
    "telecom": ("telecom_data.py", "TELECOM"),
    "bssoss": ("bssoss_data.py", "BSSOSS"),
    "finance": ("finance_data.py", "FINANCE"),
}

# Every field a submission might carry, per pattern, beyond title/pattern/problem — used to pull only the
# real spec fields out of the submission dict (it also carries domain_note/problem_statement/submitted_at/
# source, which are either consumed separately or dropped, not written verbatim into the catalog entry).
PATTERN_SPEC_FIELDS = {
    "orchestrator-worker": ["orchestrator", "workers", "data_sources", "actions", "human_gate"],
    "hierarchical": ["top", "mid_layer", "leaves_by_mid", "actions"],
    "pipeline": ["stages", "actions"],
    "blackboard": ["controller", "agents", "store_name", "actions"],
    "debate-critique": ["proposer", "critic", "arbiter", "refs", "actions"],
    "market-based": ["auctioneer", "bidders", "actions"],
    "event-swarm": ["bus_name", "agents", "actions"],
    "human-escalation": ["auto_agents", "escalation_gate", "human_role", "actions"],
}


class PromotionError(ValueError):
    pass


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60] or "use-case"


def load_target(domain):
    if domain not in DOMAIN_FILES:
        raise PromotionError(f"Unknown domain '{domain}'. Must be one of: {sorted(DOMAIN_FILES)}")
    filename, list_name = DOMAIN_FILES[domain]
    path = os.path.join(SCRIPTS, filename)
    module = __import__(filename[:-3])
    existing = getattr(module, list_name)
    return path, list_name, existing


def next_id_and_slug(existing, title):
    next_id = max((uc["id"] for uc in existing), default=0) + 1
    base_slug = slugify(title)
    existing_slugs = {uc["slug"] for uc in existing}
    slug = base_slug
    n = 2
    while slug in existing_slugs:
        slug = f"{base_slug}-{n}"
        n += 1
    return next_id, slug


def py_repr(value, indent=1):
    """Pretty-print a Python literal the same way the hand-written entries in *_data.py are formatted —
    lists of strings on their own indented lines, tuples for table rows. Good enough for the mechanical
    fields; the TODO table fields are inserted as raw placeholder text, not run through this."""
    pad = "  " * indent
    if isinstance(value, list):
        if not value:
            return "[]"
        inner = ",\n".join(f"{pad}  {py_repr(v, indent + 1)}" for v in value)
        return "[\n" + inner + f",\n{pad}]"
    if isinstance(value, str):
        return repr(value)
    if value is None:
        return "None"
    return repr(value)


def build_entry_source(uc_id, slug, submission, pattern):
    spec_fields = PATTERN_SPEC_FIELDS[pattern]
    missing = [f for f in spec_fields if f not in submission and f != "human_gate"]
    if missing:
        raise PromotionError(f"Submission is missing required field(s) for pattern '{pattern}': {missing}")

    lines = ["{"]
    lines.append(f' "id": {uc_id}, "slug": "{slug}",')
    lines.append(f' "title": {py_repr(submission["title"])},')
    lines.append(f' "pattern": {py_repr(pattern)},')
    problem = submission.get("problem_statement") or (
        "TODO: write a real problem statement — 2-4 sentences on the actual operational pain this solves "
        "and why it matters. The submitter's own words, if they gave any, are in `problem_statement` in "
        "the original submission JSON — check submissions/ before overwriting this."
    )
    lines.append(f' "problem": (\n   {py_repr(problem)}\n ),')
    for field in spec_fields:
        val = submission.get(field)
        if field == "human_gate" and not val:
            continue  # omit entirely when absent, matching existing entries' convention
        lines.append(f' "{field}": {py_repr(val)},')

    lines.append(' "agents_table": [')
    lines.append('   # TODO: one (name, responsibility) tuple per agent — see any existing entry in this')
    lines.append('   # file for the expected level of specificity. Draft names from the submission below;')
    lines.append('   # responsibilities are NOT filled in and must not ship as-is.')
    for name in _all_agent_names(submission, pattern):
        lines.append(f'   ({py_repr(name)}, "TODO: what does this agent actually do, specifically?"),')
    lines.append(' ],')

    lines.append(' "tech_table": [')
    lines.append('   # TODO: (step/layer, specific technology) tuples — no placeholders shipped here at all,')
    lines.append('   # this needs real technology decisions, not a generated guess.')
    lines.append(' ],')

    lines.append(' "retrospective": [')
    lines.append('   # TODO: 3-5 honest "if we rebuilt this" bullets — this is the credibility engine of')
    lines.append('   # the whole catalog (see go-to-market-roadmap.md); do not skip or fake this section.')
    lines.append(' ],')
    lines.append("},")
    return "\n".join(lines)


def _all_agent_names(submission, pattern):
    """Best-effort list of agent-like names from the submission, for scaffolding agents_table rows only —
    never used for anything that ships without review."""
    names = []
    for key in ("orchestrator", "top", "controller", "proposer", "critic", "arbiter", "auctioneer",
                "escalation_gate", "human_role"):
        if submission.get(key):
            names.append(submission[key])
    for key in ("workers", "agents", "bidders", "auto_agents", "mid_layer", "stages"):
        if submission.get(key):
            names.extend(submission[key])
    if submission.get("leaves_by_mid"):
        for leaves in submission["leaves_by_mid"]:
            names.extend(leaves)
    seen = set()
    out = []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def promote(submission_path, domain):
    submission = json.load(open(submission_path))
    pattern = submission.get("pattern")
    if pattern not in PATTERN_SPEC_FIELDS:
        raise PromotionError(f"Submission has unknown/missing pattern: {pattern!r}")

    path, list_name, existing = load_target(domain)
    uc_id, slug = next_id_and_slug(existing, submission["title"])
    entry_source = build_entry_source(uc_id, slug, submission, pattern)

    with open(path, "r") as f:
        content = f.read()

    # Insert the new entry right before the list's closing "]" — matches the existing file's own
    # formatting convention (each entry ends with "},\n" and the list ends with "]\n").
    closing_idx = content.rstrip().rfind("]")
    if closing_idx == -1:
        raise PromotionError(f"Couldn't find the closing ']' for {list_name} in {path} — file may have "
                              f"been reformatted since this script was written; insert manually.")
    new_content = content[:closing_idx] + entry_source + "\n" + content[closing_idx:]

    with open(path, "w") as f:
        f.write(new_content)

    return {"path": path, "id": uc_id, "slug": slug, "list_name": list_name}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("submission_path", help="Path to a submissions/*.json file")
    ap.add_argument("--domain", required=True, choices=sorted(DOMAIN_FILES),
                     help="Which real catalog domain to promote this into")
    args = ap.parse_args()

    result = promote(args.submission_path, args.domain)
    print(f"Promoted into {result['path']} as id={result['id']} slug={result['slug']}.")
    print("Next steps (see submissions/README.md):")
    print("  1. Fill in the agents_table / tech_table / retrospective TODOs by hand.")
    print("  2. Run: python3 scripts/build.py")
    print(f"  3. Remove {args.submission_path} (or move it to submissions/promoted/) and commit.")


if __name__ == "__main__":
    main()
