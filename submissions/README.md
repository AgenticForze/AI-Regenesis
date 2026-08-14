# Use Case Submissions

Files here come from the [`/build/`](../docs/build/) live diagram tool's "Submit to AI-Regenesis" button —
someone filled in the structured form, generated a diagram, and proposed it as a new catalog use case.

**Nothing here is live on the site.** A submission landing in this folder (via a direct commit if you're a
collaborator, or via a pull request if it came from a fork) is a *proposal*, not a publish — it only becomes
a real catalog entry once you review it and run the promotion step below.

## Why submissions don't go straight into the catalog

The 60 curated use cases each have three things a structured form can't produce: an **agents table** (real
responsibility descriptions, not just names), a **tech stack table** (specific, defensible technology
choices), and an honest **retrospective** ("if we rebuilt this"). Those are the actual craft — auto-generating
them from a title and a list of agent names would produce plausible-sounding filler, not the real thing this
catalog is built on. So a submission gets you most of the way (title, pattern, component names, a working
diagram) and a human fills in the rest before it's real.

## Reviewing a submission

Each `submissions/{slug}-{timestamp}.json` file is the structured spec the person filled in — the same shape
`quick-reference-engine`'s use-case dicts use, plus a few extra fields:

```json
{
  "title": "...",
  "pattern": "orchestrator-worker",
  "domain_note": "Insurance",           // free text the submitter typed, NOT one of the 3 curated domains
  "submitted_at": "2026-08-12T...",
  "source": "build-tool-v1",
  "orchestrator": "...", "workers": [...], "data_sources": [...], "actions": [...], "human_gate": null
  // (exact extra fields depend on which of the 8 patterns was used — see quick-reference-engine's
  // references/spec-format.md for the full field list per pattern)
}
```

To see what it actually looks like before deciding whether it's worth promoting, regenerate its diagram:

```python
import json, sys
sys.path.insert(0, "skills/quick-reference-engine/scripts")
from svg_patterns import BUILDERS

sub = json.load(open("submissions/the-file.json"))
# build the positional args the same way docs/build/'s JS does — see spec-format.md for the arg order
# per pattern, e.g. for orchestrator-worker:
svg = BUILDERS[sub["pattern"]](sub["title"], sub["orchestrator"], sub["workers"],
                                sub["data_sources"], sub["actions"], sub.get("human_gate"))
open("preview.svg", "w").write(svg)
```

`domain_note` is free text the submitter typed, not one of the three real domains (`telecom`, `bssoss`,
`finance`) — decide which real domain it belongs in yourself (or whether it needs a fourth domain the
catalog doesn't have yet, which is a bigger decision than a single promotion).

## Promoting an accepted submission

`scripts/promote_submission.py` does the mechanical part — turns a submission JSON into a properly-shaped
entry and appends it to the right `*_data.py` file, with the next available `id`/`slug`, and clearly marked
`TODO` placeholders for `agents_table`, `tech_table`, and `retrospective` (the three things it can't write
for you):

```bash
python3 scripts/promote_submission.py submissions/the-file.json --domain telecom
```

Then:

1. Open the target `*_data.py` file and fill in the three `TODO` sections by hand — same bar as the other 20
   entries in that file.
2. Delete the submission's `TODO` markers once done (the promotion script leaves them as a checklist, not as
   something meant to ship).
3. Run `python3 scripts/build.py` to regenerate the site — this is the same step Phase 1a's pipeline already
   uses, so the new use case gets a real page, gets added to `website/data.json`, and shows up in the
   catalog's tree/search automatically. No separate "update the list" step exists outside this.
4. Delete the now-promoted file from `submissions/` (or move it to `submissions/promoted/` if you want a
   record) and commit.

## What this deliberately doesn't do

No submission is ever auto-merged, and no submission ever writes directly to `telecom_data.py` /
`bssoss_data.py` / `finance_data.py` without a human running the promotion step and filling in the three
TODO sections. That's a quality-control choice, not a technical limitation — see the go-to-market roadmap's
own note on not diluting the catalog's credibility.
