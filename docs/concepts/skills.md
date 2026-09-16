---
icon: lucide/sparkles
---

# Skills

A **skill** is a markdown file (plus optional scripts and references) that teaches the agent a procedure: how to debug, how to write a plan, how to create a slide deck. Skills load on demand, when you invoke them or when the agent decides one applies, so they cost nothing until they are needed.

Instruction files say *what we always want*. Skills say *how to do a specific kind of task*. Keep procedures in skills and the instruction file stays short.

## Skills we install

### superpowers

[superpowers](https://github.com/obra/superpowers) is a complete development methodology packaged as skills. It is the backbone of our [development loop](../best-practices/index.md).

```bash
claude plugin install superpowers@claude-plugins-official
```

| Skill | When it fires | What it does |
|-------|---------------|--------------|
| `brainstorming` | Before any new feature or change | Asks clarifying questions one at a time, proposes approaches, gets your approval before code |
| `writing-plans` | After a design is approved | Produces a step-by-step implementation plan |
| `executing-plans` / `subagent-driven-development` | Executing a plan | Runs plan steps, optionally in subagents, with review checkpoints |
| `test-driven-development` | Any implementation | Red, green, refactor. Test first, always |
| `systematic-debugging` | Any bug or failing test | Reproduce, isolate, find the root cause before touching a fix |
| `verification-before-completion` | Before claiming "done" | Runs the checks and shows evidence |
| `requesting-code-review` / `receiving-code-review` | Around review | Checklist before review; rigorous, non-sycophantic response to feedback |
| `using-git-worktrees` | Starting isolated work | Creates a worktree so parallel tasks do not collide |
| `finishing-a-development-branch` | Work complete | Decides merge, PR or discard |
| `dispatching-parallel-agents` | 2+ independent tasks | Fans work out to subagents |
| `writing-skills` | Creating a skill | Best practices for skill files |

### feature-dev

[feature-dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev) from Anthropic adds guided feature development with three specialised agents: a code explorer, a code architect and a code reviewer. Use `/feature-dev` when the change touches an unfamiliar part of a large codebase.

### humanizer

```bash
claude plugin install humanizer@humanizer
```

Rewrites agent prose so it reads like a person wrote it: fewer filler phrases, no "delve", no bullet-point salad. Useful for commit messages, PR descriptions and documentation.

### caveman

[caveman](https://github.com/JuliusBrussee/caveman) makes the agent answer in terse language while keeping code, commands and errors intact. It has intensity levels from "lite" to "ultra". Good for long sessions where every response token counts.

```bash
npx skills add JuliusBrussee/caveman -g
```

### planning with files

A lightweight practice rather than a plugin: the agent writes its plan, its progress and its open questions to files in the repository (for example `docs/superpowers/plans/`) instead of keeping them only in the conversation. The plan survives `/clear`, compaction and hand-off to another agent or person. `superpowers` does this by default for specs and plans.

## Creating your own skills

When you notice yourself explaining the same procedure a third time, make it a skill. Two ways:

1. Ask the agent: "use the writing-skills skill to create a skill for X". It knows the file format and the conventions.
2. Use a skill scaffolder, for example `npx skills add <owner/repo>` to install community skills from GitHub, or the skill creator documented at [aihero.dev](https://www.aihero.dev/).

A good skill is:

- **Triggered clearly.** Its description says exactly when to use it.
- **Short.** One procedure, one page. Reference material goes in a `references/` folder.
- **Testable.** You can run it on a small example and see whether the agent followed it.

## Skills versus other mechanisms

```mermaid
flowchart TD
    Q1{Must always run?} -->|yes| HOOK[Harness hook]
    Q1 -->|no| Q2{Every session?}
    Q2 -->|yes| Q3{Only some files?}
    Q3 -->|yes| RULE[".claude/rules/ with paths"]
    Q3 -->|no| AGENTS["AGENTS.md / CLAUDE.md"]
    Q2 -->|no| Q4{A procedure?}
    Q4 -->|yes| SKILL[Skill]
    Q4 -->|no| PROMPT[Say it in the prompt]
    class Q1,Q2,Q3,Q4 decision
    class HOOK,SKILL skill
    class RULE,AGENTS context
    class PROMPT human
    --8<-- "mermaid-classes.mmd"
```

| Need | Use |
|------|-----|
| A rule that applies every session | [Instruction file](instruction-files.md) |
| A procedure for a kind of task | Skill |
| Something that must run at a fixed point, no exceptions | Harness hook |
| A rule for one directory or file type | `.claude/rules/` with a `paths` scope |
| Access to an external system | MCP server or an [AXI](../best-practices/context-management.md) CLI |
