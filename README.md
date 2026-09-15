# agentic-workflows

Best practices, workflows and onboarding material for agentic coding: harnesses, instruction files, skills, orchestration and the engineering standards we hold agents to. The collection is opinionated and based on our own workflows. It is updated continuously, and not every page is current.

**Site:** https://matthiaskoenig.github.io/agentic-workflows/

## Develop

```bash
uv sync                    # once
uv run zensical serve      # preview at http://localhost:8000
uv run pytest              # strict build plus checks of nav, links and writing rules
```

Content lives in `docs/`, navigation in `zensical.toml`. Changes go through a pull request against `main`; a merge deploys the site via GitHub Actions (`.github/workflows/docs.yml`).

Guidelines for working on the site are in `CLAUDE.md`.
