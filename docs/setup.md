---
icon: lucide/list-checks
---

# Setup checklist

Everything to install, on one page. The first part is done once per computer, the second once per repository. Each item links to the page that explains it; this page only says what to install and the command to do it.

```mermaid
flowchart LR
    subgraph C[Once per computer]
        direction TB
        C1[Harnesses] --> C2[Global AGENTS.md] --> C3[Plugins and skills] --> C4[CLI tools] --> C5[Editor, voice, sessions]
    end
    subgraph R[Once per repository]
        direction TB
        R1[AGENTS.md and CLAUDE.md] --> R2[Toolchain] --> R3[Tests and CI] --> R4[Policies] --> R5[Release notes and docs]
    end
    C --> R
    class C1,C5 harness
    class C2,R1 context
    class C3 skill
    class C4,R2,R3 tool
    class R4,R5 artifact
    --8<-- "mermaid-classes.mmd"
```

## On your computer

### Harnesses

| Install | Command | Page |
|---------|---------|------|
| Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` | [Harnesses](concepts/harnesses.md) |
| Codex CLI | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | [Harnesses](concepts/harnesses.md) |
| OpenCode, pi (optional) | see [opencode.ai](https://opencode.ai/), [pi.dev](https://pi.dev/docs/latest) | [Harnesses](concepts/harnesses.md) |
| VS Code extensions | Extensions view, search **Claude Code** (Anthropic) and **Codex** (OpenAI) | [Models](concepts/models.md) |

Sign in with the subscription accounts (Claude Max, ChatGPT plan), not with API keys. See [plans and billing](concepts/models.md#plans-and-billing).

### Global instruction file

```bash
# ~/AGENTS.md holds the rules for every project; start from the template
ln -s ~/AGENTS.md ~/.claude/CLAUDE.md
```

Template and rules: [CLAUDE.md and AGENTS.md](concepts/instruction-files.md).

### Plugins and skills

```bash
claude plugin install superpowers@claude-plugins-official   # brainstorming, plans, TDD, debugging, review
claude plugin install humanizer@humanizer                    # natural prose
npx skills add JuliusBrussee/caveman -g                      # terse responses, optional
```

What each does: [Skills](concepts/skills.md).

Code intelligence, so the agent sees type errors after every edit and navigates by definition instead of grep. The binary first, then the plugin. Both are global: the binary goes on your `PATH` and `--scope user` enables the plugin in every repository:

```bash
npm install -g pyright
claude plugin install pyright-lsp@claude-plugins-official --scope user
npm install -g typescript-language-server typescript
claude plugin install typescript-lsp@claude-plugins-official --scope user
```

Only if you work in these languages:

```bash
sudo apt install clangd                                      # C and C++; macOS: brew install llvm
claude plugin install clangd-lsp@claude-plugins-official --scope user
brew install jdtls                                           # Java; Linux needs the manual install
claude plugin install jdtls-lsp@claude-plugins-official --scope user
```

Why, the manual jdtls install on Linux and how to check it works: [Code intelligence](tooling.md#code-intelligence).

### Command line tools

| Install | Command | Purpose |
|---------|---------|---------|
| [uv](https://docs.astral.sh/uv/) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Python environments, `uv run`, `uvx` |
| [GitHub CLI](https://cli.github.com) | package manager, then `gh auth login` | pull requests, rulesets, releases |
| Node.js | package manager | needed for the `npx` tools below |
| [rtk](https://github.com/rtk-ai/rtk) (evaluating) | see repository, then `rtk init -g` | compress command output |

The [AXI](https://axi.md/) tools need two global installs. The binary, because our instruction files call the bare command, for example `gh-axi pr create`, and that fails with `command not found` when only `npx -y <tool>` is available. And the skill that tells the agent when to call the tool; `-g` puts it in your user-level skills, so it applies in every repository instead of only the current one:

```bash
npm install -g gh-axi chrome-devtools-axi quota-axi

npx skills add kunchenguid/gh-axi --skill gh-axi -g                            # GitHub for agents, token efficient
npx skills add kunchenguid/chrome-devtools-axi --skill chrome-devtools-axi -g  # browser automation for agents
npx skills add kunchenguid/quota-axi --skill quota-axi -g                      # plan quota per vendor
```

With nvm the global binaries belong to one Node.js version. After `nvm install <version>`, run the `npm install -g` line again.

Why these: [Token maxing](best-practices/context-management.md).

### Editor, voice, sessions

| Install | Command | Page |
|---------|---------|------|
| Terminal multiplexer | package manager | [Orchestration](concepts/orchestration.md) |
| [herdr](https://herdr.dev/) | `curl -fsSL https://herdr.dev/install.sh \| sh` | [Orchestration](concepts/orchestration.md) |
| [firstmate](https://github.com/kunchenguid/firstmate) | `git clone https://github.com/kunchenguid/firstmate` | [Orchestration](concepts/orchestration.md) |
| [OpenSuperWhisper](https://github.com/Starmel/OpenSuperWhisper) (macOS) | `brew install opensuperwhisper` | [Tooling](tooling.md#voice) |
| [text2speech](https://github.com/matthiaskoenig/text2speech) (GPU server) | `git clone` then `uv sync` | [Tooling](tooling.md#voice) |

### Browser

Install [Claude in Chrome](https://claude.ai/chrome), the browser extension that lets Claude Code open pages, click, read the console and take screenshots in your own Chrome. Sign in to claude.ai with the same account as Claude Code and grant the extension access per site.

!!! tip "Keep Chrome open in the background"
    The extension only works while Chrome is running. Whenever the agent works on a homepage, a docs site or any other UI, start Google Chrome before you start the task and leave it open. The agent then validates every change in the real browser: it sees what you would see and gets a screenshot back in seconds. Without the browser it falls back to headless tooling and reading rendered HTML, which is slower and misses layout problems.

### Computer checklist

- [ ] Claude Code and Codex installed and signed in
- [ ] VS Code extensions installed
- [ ] `~/AGENTS.md` written and symlinked to `~/.claude/CLAUDE.md`
- [ ] `superpowers` and `humanizer` installed
- [ ] `pyright-lsp` and `typescript-lsp` installed with their language servers
- [ ] `uv`, `gh` (authenticated), Node.js
- [ ] A terminal multiplexer or herdr for sessions that outlive the terminal
- [ ] Claude in Chrome installed, and Chrome open whenever the agent works on a web page

## In a repository

Copy files from the reference repository [sbmlutils](https://github.com/matthiaskoenig/sbmlutils) or from this one, then adjust names. The order is the one of [Onboarding a repository](onboarding-repository.md).

### Instruction files

```bash
ln -s AGENTS.md CLAUDE.md
echo CLAUDE.local.md >> .gitignore
```

### Toolchain (Python)

| File | Content | Page |
|------|---------|------|
| `pyproject.toml` | project metadata, `dev` dependency group with `pytest`, `ruff`, `ty`, `pre-commit`, `tox`, `zensical`; `[tool.ty]` | [Python code](best-practices/python.md) |
| `.python-version` | the Python version uv installs | |
| `.ruff.toml` | lint and format configuration | [Python code](best-practices/python.md) |
| `.pre-commit-config.yaml` | ruff, ty and hygiene hooks | [Python code](best-practices/python.md) |
| `tox.ini` | test matrix and `ty` environment | [Python code](best-practices/python.md) |
| `uv.lock` | generated by `uv sync`, committed | |

```bash
uv sync --extra dev          # or `uv sync` when the tools are a dependency group
uv run pre-commit install
```

Data models are pydantic models with validation.

### Tests and continuous integration

| File | Job name | Content |
|------|----------|---------|
| `.github/workflows/ci-cd.yml` | `tests` | pytest matrix, aggregated into one job |
| `.github/workflows/ruff.yml` | `ruff` | `ruff check`, `ruff format --check` |
| `.github/workflows/ty.yml` | `ty` | `ty check` |
| `.github/workflows/docs.yml` | `build` or `docs` | zensical build, deploy from the default branch |

For a small repository the checks can share one workflow with named jobs, as `tests.yml` in this repository does.

### Policies

| File | Content |
|------|---------|
| `.github/CODEOWNERS` | `* @matthiaskoenig` |
| `.github/rulesets/main.json` | pull request required, the checks above, linear history, no bypass |
| `.github/rulesets/develop.json`, `tags.json` | libraries with a `develop` branch and releases |
| `.github/rulesets/apply.sh` | applies rulesets and merge settings, idempotent |

```bash
.github/rulesets/apply.sh owner/repo
```

Details: [Repository policies](best-practices/repository-policies.md).

### Release notes and documentation

| File | Content |
|------|---------|
| `release-notes/<version>.md` | one note per tagged release |
| `.github/workflows/release.yml` | GitHub release from the note on a version tag |
| `zensical.toml`, `docs/` | the documentation site with a development page |
| `tests/test_docs.py` | strict build and writing-rule checks of the docs (copy from this repository) |

### Repository checklist

- [ ] `AGENTS.md` written, `CLAUDE.md` symlinked, `/context` shows it
- [ ] `pyproject.toml`, `.ruff.toml`, `[tool.ty]`, `.pre-commit-config.yaml`, `tox.ini`
- [ ] tests green, `uv run pytest`
- [ ] workflows with named jobs run on pull requests
- [ ] `CODEOWNERS` and rulesets applied
- [ ] `release-notes/` with the baseline note, tag pushed
- [ ] docs site builds
