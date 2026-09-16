---
icon: lucide/folder-plus
---

# Onboarding a repository

How to bring a repository to the point where an agent can work in it reliably. The same checklist applies to a new project and to an existing one you inherit; the difference is only how much of step one is needed. Budget half a day for an existing repository of moderate size. The investment is repaid on the first task, because every later session starts from a repository that explains itself.

```mermaid
flowchart BT
    %% BT with the corrections edge keeps Foundation on top, TB stacks the rows the other way round
    subgraph S1[Foundation]
        direction LR
        E[1 Explore] --> A[2 AGENTS.md] --> T[3 Toolchain] --> B[4 Test baseline] --> CI[5 CI]
    end
    subgraph S2[Process]
        direction LR
        P[6 Policies] --> R[7 Release note, tag] --> D[8 Docs] --> F[9 First task]
    end
    S2 -->|corrections| S1
    S1 --> S2
    class E,F harness
    class A context
    class T,B,CI tool
    class P,R,D artifact
    --8<-- "mermaid-classes.mmd"
```

The reference implementation of everything below is [sbmlutils](https://github.com/matthiaskoenig/sbmlutils); copy files from there instead of writing them from scratch.

## 1. Understand before you configure

For an existing repository, start a session and let the agent explore before either of you changes anything:

> Explore this repository. Report: what it does, how it is built and tested, the directory layout, the conventions you see (naming, error handling, logging, tests), and anything that looks fragile or inconsistent. Do not change files.

Use a subagent or plan mode so the exploration does not fill the main context. Read the report, correct what it got wrong, and keep it: it becomes the first draft of the instruction file. For a new project, do the [brainstorming](best-practices/index.md) step instead and write down the purpose, the constraints and the first milestone.

## 2. Instruction file

Run `/init` to generate a `CLAUDE.md`, move the content to `AGENTS.md`, symlink `CLAUDE.md` to it, and edit until it holds only what every session needs: build and test commands, layout, conventions, what not to touch, the branch and release workflow. Under 200 lines. See [instruction files](concepts/instruction-files.md).

```bash
ln -s AGENTS.md CLAUDE.md
echo CLAUDE.local.md >> .gitignore
```

Confirm with `/context` in a new session that the file loads.

## 3. Toolchain

For Python, the standard set from [Python code](best-practices/python.md): `pyproject.toml` with a `dev` extra, `uv sync --extra dev`, `.ruff.toml`, `[tool.ty]`, `tox.ini`, `.pre-commit-config.yaml`. Copy the files from the reference repository and adjust names. Run each tool once and fix what it reports, or add a per-file ignore with a reason. An inherited codebase may need a few pull requests of cleanup here; do them before the first feature, with the agent, one tool at a time.

```bash
uv run ruff check --fix && uv run ruff format
uv run ty check
uv run pre-commit install
```

Data models that are dicts or bare dataclasses become pydantic models in this step, boundary by boundary.

## 4. Test baseline

The test suite must run and be green before agents build on it. If there are no tests, add smoke tests around the entry points with the agent: import the package, run the CLI with `--help`, call the main function on a tiny fixture. A green baseline is what lets the [development loop](best-practices/index.md) work, because "the tests pass" means something.

## 5. Continuous integration

One workflow per concern, each with a named job: `ruff.yml`, `ty.yml`, `ci-cd.yml` with a `tests` job that aggregates the matrix, `docs.yml`. All run on `pull_request` and on pushes to the protected branches. Copy them from the reference repository.

## 6. Repository policies

Add `.github/CODEOWNERS`, `.github/rulesets/main.json` (and `develop.json` for a library with releases), and `apply.sh`, then apply:

```bash
.github/rulesets/apply.sh owner/repo
```

From now on every change, including the agent's, is a pull request with green checks. See [repository policies](best-practices/repository-policies.md).

## 7. Release notes and first tag

Create `release-notes/` and write the note for the current state as version `0.1.0` (or the existing version). Add `release.yml`. Tag it. This is the baseline everything after is described against.

## 8. Documentation site

A `docs/` directory with a zensical site and a development page that describes the branch model, the checks, the setup and the release process. Small repositories get a short one; the point is that the next person, or the next agent, reads how the repository works instead of guessing.

## 9. First task, then refine

Run one real task through the full loop: brainstorm, plan, implement with tests, verify, pull request. Every correction you had to make during that task is a candidate line for `AGENTS.md`. Add it after the second occurrence, not the first.

## Checklist

- [ ] Exploration report read and corrected
- [ ] `AGENTS.md` written, `CLAUDE.md` symlinked, loads in `/context`
- [ ] uv, ruff, ty, pre-commit configured and green
- [ ] Data models are pydantic models
- [ ] Test suite green, smoke tests added where there were none
- [ ] CI workflows with named jobs run on pull requests
- [ ] Rulesets applied, `CODEOWNERS` present
- [ ] `release-notes/` with the baseline note, first tag pushed
- [ ] Docs site with a development page
- [ ] First task completed through the loop, `AGENTS.md` refined
