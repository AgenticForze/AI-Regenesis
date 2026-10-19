# Contributing

Thank you for helping improve this architecture. Challenges and corrections are as valuable as additions.

## Ways to contribute

- **Challenge a decision.** Open an issue in the AI-Regenesis repository, prefixed `[Agentic Ops]`. Say which decision, what you would do instead, and what evidence or experience supports it.
- **Fix something.** Outdated service names, broken links, unclear wording or diagram errors: open a pull request.
- **Add a platform or pattern.** Propose it in an issue first so we can agree scope and structure.
- **Share an ADR.** If you adapted a decision for your organisation, an anonymised ADR is welcome under `templates/adr/`.

## Conventions

- One topic per Markdown file; keep the `NN-name.md` numbering and the navigation footer.
- Write plainly: short sentences, specific numbers, no marketing language.
- Mermaid for sequences and flows so they stay editable. Icon diagrams are edited through their JSON specs in `diagrams/specs/` and rebuilt with `./scripts/build-diagrams.sh`; the renderer must report no warnings.
- Tools are added to `tools/catalog.yaml`, then `python3 tools/build_catalog.py` regenerates the README and MCP definitions.
- After content changes, run `scripts/publish-site.sh` so the published copy in `../docs/agentic-ops/` stays in sync.
- Name both clouds' equivalents when you add a capability, and update `architecture/aws/19-gcp-to-aws-mapping.md`.
- Cite sources in `BIBLIOGRAPHY.md`.
- Never include confidential information, real internal metrics, customer names or credentials.

## Pull request checklist

- [ ] Links and image paths resolve
- [ ] Both editions considered (or the PR says why not)
- [ ] Bibliography updated if new sources are cited
- [ ] `CHANGELOG.md` updated under *Unreleased*

By contributing you agree that your contributions are licensed under the repository's licences (CC BY 4.0 for content, MIT for code and templates).
