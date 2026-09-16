---
icon: lucide/lightbulb
---

# Introduction to agentic coding

This page is the conceptual entry point: what agentic coding is, how it differs from what came before, which few concepts matter first, and a short list of resources to learn from. It is also the outline of the first session of a workshop on agentic AI for researchers. Everything else on this site builds on it.

## From autocomplete to agents

The crucial transition to understand is **autocomplete, then chat, then agentic coding**.

| Stage | What the AI does | What you do |
|-------|------------------|-------------|
| Autocomplete | Suggests the next lines of code | Accept or reject, line by line |
| Chat | Tells you what to do, in prose and snippets | Copy, adapt, run, report back |
| Agent | Takes a goal, inspects the repository, edits several files, runs commands, reads failures, corrects itself, verifies the result | State the goal, review the plan, review the diff |

With an agent you stop dictating solutions. You give it a goal and the means to check its own work, and you move to the boundaries: the specification at the start and the review at the end.

```mermaid
flowchart LR
    A[Autocomplete<br/>suggests code] --> C[Chat<br/>tells you what to do] --> G[Agent<br/>inspects, edits, runs, verifies]
    class A,C model
    class G harness
    --8<-- "mermaid-classes.mmd"
```

## The loop

Every agent, whatever the harness, runs the same loop:

**goal, inspect context, plan, act with tools, observe results, test and verify, iterate**

```mermaid
flowchart LR
    G([Goal]) --> I[Inspect<br/>context]
    I --> P[Plan]
    P --> A[Act with<br/>tools]
    A --> O[Observe<br/>results]
    O --> V{Verified?}
    V -->|no| P
    V -->|yes| D([Done:<br/>review the diff])
    class G,D human
    class I,P,O harness
    class A tool
    class V decision
    --8<-- "mermaid-classes.mmd"
```

The model decides what to do next; the [harness](concepts/harnesses.md) runs the tools and shows the results. Quality comes from what the loop can see (the repository, the instruction file) and from what it can check (tests, lint, types), not from the prompt alone.

## Six concepts for a first session

Teach and learn these six first. Everything else can wait.

1. **Repository context.** The agent works from what it can read: the code, the tests, the instruction file. A repository that explains itself gets better results. See [onboarding a repository](onboarding-repository.md).
2. **Good task specifications.** State the goal, the constraints and how success is checked. Symptom and outcome, not the solution.
3. **Plan, implement, verify.** Ask for a plan, approve it, then let the agent implement and verify. See [the development loop](best-practices/index.md).
4. **`CLAUDE.md`.** The persistent instructions every session starts with. See [instruction files](concepts/instruction-files.md).
5. **Tests, lint and type checking as feedback loops.** They are what lets the agent correct itself instead of guessing. See [Python code](best-practices/python.md).
6. **Git and diff review as the human verification boundary.** You read the diff. Nothing reaches `main` without it. See [repository policies](best-practices/repository-policies.md).

Only afterwards: [skills](concepts/skills.md), MCP, subagents and [parallel agents](concepts/orchestration.md).

## What not to start with

Do not begin with LangChain, CrewAI, multi-agent architectures, or implementing MCP servers. They are about *building* agentic applications, not about working effectively with a coding agent. The same holds for [12-Factor Agents](https://github.com/humanlayer/12-factor-agents): an excellent text on building reliable agent software, and the wrong first read for a user of coding agents. Anthropic's [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) is the exception worth reading early, because its distinction between workflows and agents explains why simple setups usually win.

## Self-study in 90 minutes

Before a workshop, or as a first afternoon:

1. Read the MIT lecture on agentic coding, about 30 minutes.
2. Watch the first part of Claude Code: Foundations, about 30 minutes.
3. Spend 30 minutes giving Claude Code a real, small Python repository with the task: understand it, plan a small change, make it, run the tests, explain the diff.

The third step teaches more than several hours of slides.

## Resources

The field changes quickly, so this list is short and recent. Each entry says why it is worth the time.

| Resource | Why | Level |
|----------|-----|-------|
| [MIT Missing Semester 2026: Agentic Coding](https://missing.csail.mit.edu/2026/agentic-coding/) | The best neutral introduction. Explains the agent loop, context, permissions, `AGENTS.md` and `CLAUDE.md`, skills, subagents, parallel agents and security, with exercises. | Start here |
| [Claude Code: Foundations](https://www.anthropic.com/webinars/claude-code-foundations) (Anthropic) | One-hour practical introduction, recorded July 2026: install, inspect a repository, plan, fix a bug, verify, `CLAUDE.md`, then skills, MCP and subagents. | Start here |
| [Claude Code: common developer use cases](https://support.claude.com/en/articles/14553517-claude-code-common-developer-use-cases) | Concrete workflows: understand a repository, fix tests, debug errors, refactor in plan mode, write tests, review pull requests, work an issue end to end. | Beginner |
| [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) (Anthropic) | The best short conceptual explanation of workflow versus agent, tool use and feedback loops, and why simple architectures are usually preferable. | Conceptual |
| [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) (Anthropic course) | Free structured course covering context management, project instructions, MCP, hooks and GitHub integration. | Beginner to intermediate |
| [Tutorial: Agentic coding in VS Code](https://code.visualstudio.com/docs/agents/agents-tutorial) | Accessible hands-on tutorial: an agent plans, edits several files, runs tools, reviews diffs and commits. | Beginner |
| [Codex for Builders](https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-for-builders) (OpenAI Academy) | Useful after Claude Code: shows that repository context, delegation, verification and agent instructions are tool-independent. | Beginner to intermediate |
| [Claude Code documentation](https://code.claude.com/docs) | The reference for everything on this site that is Claude Code specific. | Reference |

The pages to hand to workshop participants: the MIT lecture, Claude Code: Foundations, the Claude Code documentation, Building Effective Agents, and Claude Code in Action.

## Where to go next

[Getting started](getting-started.md) installs everything; the [setup checklist](setup.md) is the same as a list. The concept pages explain [harnesses](concepts/harnesses.md), [models](concepts/models.md), [instruction files](concepts/instruction-files.md), [skills](concepts/skills.md) and [orchestration](concepts/orchestration.md). The best practice pages are the rules we hold ourselves and our agents to.
