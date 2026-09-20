# Agentic Workflows documentation

Teaching and onboarding resource for agentic coding: how we use coding agents, which skills and instruction files we rely on, and the best practices we follow. The site is built with [zensical](https://zensical.org) from markdown in `docs/` and deployed to GitHub Pages by `.github/workflows/docs.yml` on every push to `main`.

## Commands

```bash
uv sync                                   # once per checkout, installs the dev group
uv run zensical serve                     # live preview at http://localhost:8000
uv run zensical build --clean --strict    # build into site/
uv run pytest                             # build plus the writing-rule checks; must pass before a pull request
uv run ruff check && uv run ruff format --check && uv run ty check   # for changes under tests/
```

## Adding a page

1. Create `docs/<section>/<name>.md` with a frontmatter `icon` and an `# H1` title.
2. Add it to `nav` in `zensical.toml`.
3. Run `uv run pytest`.

GitHub Pages is served from the `github-pages` environment; one-time setup in the repository is Settings, Pages, Source: GitHub Actions.

## Writing rules

- Write for someone joining the team: explain the why, then the how, then a concrete command.
- Do not invent facts about tools. If unsure what a tool does, link to it and say so.
- Use admonitions (`!!! tip`, `!!! warning`) sparingly, for things people get wrong.
- Every resource link needs one sentence on why it is worth the time.
- Never hard-wrap markdown text. Each paragraph, list item and quote line stays on one line; we soft-wrap in the editor. Only code blocks and tables have their own line structure.
- Keep pages under roughly 300 lines. Split by topic instead of growing a page.
- Diagrams are mermaid flowcharts. Give every node a class from `docs/includes/mermaid-classes.mmd` (human, harness, model, context, skill, tool, artifact, decision) and end the diagram with `--8<-- "mermaid-classes.mmd"`; the legend is on the home page.
- Run `uv run pytest` before finishing; it builds the site strictly and checks nav, links and the writing rules. A failure blocks the pull request.

## Git

- `main` is protected: no direct push, every change goes through a pull request whose `build`, `tests`, `ruff` and `ty` checks pass. Work on a branch, open a pull request with `gh-axi pr create --title <title> --body <text>` and enable auto-merge with `gh-axi pr merge <number> --squash --auto --delete-branch`. The pull request merges when the checks pass, no manual review is required.
- Do not add agent co-author lines to commit messages.
- Commit only when asked.
- Changes are tracked in `release-notes/<version>.md`, one file per tagged release. A pull request that prepares a release adds the note.
- Repository policies live in `.github/rulesets/`; change the JSON and run `apply.sh`, do not click in the web interface.
