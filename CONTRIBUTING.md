# Contributing

This catalog is generated, not hand-edited. To add or change a use case:

1. **Add/edit source data** in `scripts/telecom_data.py`, `scripts/bssoss_data.py`, or `scripts/finance_data.py`.
   Each entry is a dict with:
   - `id`, `slug`, `title`, `pattern` (one of the keys in `scripts/templates.py::PATTERNS`)
   - pattern-specific fields (e.g. `orchestrator`/`workers` for `orchestrator-worker`, `top`/`mid_layer`/`leaves_by_mid`
     for `hierarchical` — see existing entries for the exact shape per pattern)
   - `problem` (3-5 sentence problem statement)
   - `agents_table` (list of `(agent name, one-line responsibility)` tuples)
   - `tech_table` (list of `(step, technology)` tuples — name real, specific technologies, not placeholders)
   - `retrospective` (list of 3-5 concrete "what we'd improve" bullets)

2. **Regenerate:**
   ```bash
   python3 scripts/build.py
   ```
   This regenerates the Mermaid text source (`architecture.mmd`), the rendered diagram (`architecture.svg`),
   the `README.md`, and the website's inlined data for that use case — all from the same source-of-truth dict.

3. **Update indexes if needed:** domain `README.md` and pattern docs under `patterns/` are regenerated
   automatically from the same source data — do not hand-edit them.

4. Open a merge request. CI (`validate-mermaid`, `verify-generated-artifacts-in-sync`) will fail if generated
   files don't match what `scripts/build.py` produces from your source-data change, or if a Mermaid diagram
   doesn't parse.

## Adding a new architecture pattern

Add a template function to `scripts/templates.py` (Mermaid text source) **and** a matching builder to
`scripts/svg_patterns.py` (the rendered card diagram, using `scripts/svg_engine.py`'s `Diagram` class — see
existing pattern functions for the row/edge API). Register the pattern key in `templates.py::PATTERNS`, wire both
builders into `build_diagram()` / `build_svg()` in `scripts/build.py`, and add a one-paragraph description to
`render_pattern_doc()`'s `descriptions` dict.

## Style guidelines

- Problem statements should name a specific, credible business pain point — not "use agents to do X better."
- Technology choices should be real, named products/frameworks/protocols, matched to what that step actually needs
  (e.g. keep financial calculations in deterministic rules engines, not LLM output — several retrospectives in
  this catalog call that out explicitly as a lesson learned).
- Retrospective bullets should read like something a team actually learned, not generic "iterate and improve."
