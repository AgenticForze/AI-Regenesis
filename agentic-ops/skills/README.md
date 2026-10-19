# Skills

Claude skills that make work on this architecture repeatable. A skill is a folder with a `SKILL.md` and any scripts it needs.

| Skill | What it does |
| --- | --- |
| [`architecture-diagrams`](architecture-diagrams/SKILL.md) | Draws and edits the icon diagrams from JSON specs: static SVG, themed SVG and 2× PNG, with layout checks |

## Using a skill with Claude

Zip the skill folder (for example `architecture-diagrams/`) and add it where you manage skills in Claude's settings. Claude then uses it whenever you ask for a diagram in this style, for example:

> Add a "Model gateway routing" diagram to the Google Cloud edition, same style.
> Build the Azure version of the hybrid connectivity diagram.
> Move the Secure Web Proxy below Cloud DNS and re-render.

## Using the renderer without Claude

```bash
pip install cairosvg
python3 skills/architecture-diagrams/scripts/render.py diagrams/specs/gcp-hybrid-connectivity.json -o out --png
./scripts/build-diagrams.sh     # rebuild every diagram in the repo
```

## Planned

| Skill | Purpose |
| --- | --- |
| cloud-edition-builder | Map the cloud-neutral model to a new cloud and generate its chapter set and diagrams |
| architecture-review | Review a design against the principles, runtime gates and delivery gates |
| adr-writer | Draft ADRs in this repository's format |
| agent-spec-generator | Turn an interview with a team into `agent-spec.yaml`, a starter policy and a promotion checklist |
