---
icon: lucide/git-pull-request
---

# Repository policies

Every repository we maintain uses the same branch protection: nothing is pushed to the default branch directly, every change arrives as a pull request whose checks are green, and the history stays linear. This applies to people and agents alike. An agent that finishes a task opens a pull request; it never pushes to `main`.

This page documents the policy as it is applied to this repository. Library repositories with a `develop` branch and releases (for example [sbmlutils](https://github.com/matthiaskoenig/sbmlutils)) add a `develop` ruleset and a tag ruleset on top of the same pattern.

## Rules on the default branch

| Rule | Effect |
|------|--------|
| Pull request required | No direct push. A change is merged from a pull request. |
| Required status checks | `build` (the strict zensical build, `docs.yml`), `tests` (pytest, `tests.yml`), `ruff` and `ty` (lint, format and type check of the test code, `tests.yml`). |
| Conversations resolved | Every review thread is resolved before the merge. |
| Stale approvals dismissed | A new push to the branch dismisses earlier approvals. |
| Extra approval for unattributed changes | Commits not attributed to the pull request author need an extra approval. |
| Squash or rebase only | Merge commits are disabled, so the history of `main` stays linear. |
| No force push, no deletion | `main` cannot be rewritten or removed. |
| No bypass | The rule set has no bypass actors. It applies to the maintainer as well. |

The ruleset does not require an approving review. On a personal repository a ruleset cannot ask for an approval from somebody else only, and requiring one would block the pull requests of the maintainer, who cannot approve their own. The maintainer is the code owner (`.github/CODEOWNERS`) and is requested for review on every pull request. Once a second person has write access, an approving review of a code owner can be required. Which changes need a human review before the merge is a working rule rather than a ruleset, see [Review](index.md#6-review).

## Repository settings

Applied together with the ruleset:

- auto-merge enabled, so a pull request can be queued and merges as soon as the checks pass,
- delete branch on merge,
- update branch suggestion enabled,
- squash and rebase as the only merge methods.

## Rulesets live in the repository

The protection is implemented with [repository rulesets](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets). The JSON is kept in `.github/rulesets/` so that a policy change is reviewed like any other change instead of only living in the web interface.

```text
.github/
├── CODEOWNERS            # * @matthiaskoenig
└── rulesets/
    ├── apply.sh          # applies settings and rulesets, idempotent
    └── main.json         # the ruleset for the default branch
```

Changing a policy means editing the JSON and applying it:

```bash
gh auth login
.github/rulesets/apply.sh            # this repository
.github/rulesets/apply.sh owner/repo # another repository
```

The script updates rulesets that exist, creates missing ones, and sets the repository merge settings. It needs the [GitHub CLI](https://cli.github.com) authenticated as a user with admin permission.

## Workflow for a change

```mermaid
flowchart LR
    B[Branch<br/>off main] --> C[Commits] --> PR[Pull<br/>request]
    PR --> CH{Checks<br/>green?}
    CH -->|no| C
    CH -->|yes| RV{Threads<br/>resolved?}
    RV -->|no| C
    RV -->|yes| M[Squash or<br/>rebase merge]
    M --> D[Branch<br/>deleted]
    M --> T[Tag<br/>x.y.z] --> R[GitHub release<br/>from the release note]
    class B,C,PR,M,D,T,R artifact
    class CH,RV decision
    --8<-- "mermaid-classes.mmd"
```

1. Branch off `main`: `git switch -c <topic>`.
2. Commit, push, open a pull request. With the GitHub CLI: `gh pr create --fill`.
3. Wait for `build` to pass. Fix and push again if it fails.
4. Resolve review threads. Enable auto-merge with `gh pr merge --squash --auto --delete-branch` and let GitHub merge when the checks are green. No manual review is required.
5. The branch is deleted automatically after the merge.

!!! warning "What agents must know"
    An agent working in this repository cannot push to `main`. Instruct it to work on a branch, open a pull request and enable auto-merge. The `CLAUDE.md` of this repository says so.

## Adding a required check

A required check is the `name` of a job, not of a workflow. To add one:

1. Give the job an explicit `name:` in the workflow and make the workflow run on `pull_request`.
2. Add `{"context": "<job name>"}` to `required_status_checks` in `main.json`.
3. Run `apply.sh`.

The `tests` check runs `tests/test_docs.py`: the strict build succeeds, every navigation entry is rendered and every page is in the navigation, relative links resolve, and the markdown follows the writing rules (no em dash, no hard-wrapped paragraphs). A pull request that breaks any of this cannot be merged. For Python library repositories the same four names are used, with `tests` running the pytest matrix, see [Python code](python.md).

## Releases and release notes

Changes are tracked through release notes, not through a changelog that grows commit by commit. Every release has a file `release-notes/<version>.md` that describes what changed for the reader of the site or the user of the package: features, breaking changes, fixes, and a development section for what changed under the hood. The file is written as part of the pull request that prepares the release, so the description is reviewed together with the code.

```text
release-notes/
├── 0.1.0.md
└── 0.2.0.md
```

A release is a tag on `main` following [semantic versioning](https://semver.org/). Pushing the tag triggers `release.yml`, which checks that the release note exists and creates the GitHub release with the note as its body:

```bash
git switch main && git pull
git tag 0.2.0
git push origin 0.2.0
```

Library repositories additionally check that the tag matches the version in `pyproject.toml` and publish the package in the same workflow.

!!! tip "Small project, same design"
    Rulesets, required checks, release notes and tagged releases cost a few files and pay for themselves the first time something needs to be found, reverted or explained. We apply the same design to every repository, whether it is a documentation site with one workflow or a library with a test matrix. Agents work best in repositories with a clear structure, and so do people joining later.
