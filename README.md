# agentic-workflows

Best practices, workflows and onboarding material for agentic coding: harnesses, instruction files, skills, orchestration and the engineering standards we hold agents to. A collection of tools, practises and information without 

**Site:** https://matthiaskoenig.github.io/agentic-workflows/

## Develop

```bash
uv sync                    # once
uv run zensical serve      # preview at http://localhost:8000
uv run pytest              # strict build plus checks of nav, links and writing rules
```

Content lives in `docs/`, navigation in `zensical.toml`. Pushing to `main` deploys via GitHub Actions (`.github/workflows/docs.yml`).

Guidelines for working on the site are in `CLAUDE.md`.
