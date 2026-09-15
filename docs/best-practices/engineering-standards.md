---
icon: lucide/shield-check
---

# Engineering standards

These are the rules in our global instruction file, with the reasoning behind each. The agent reads the rule; you should understand the why, so you can tell when the agent is cutting corners.

## Reproduce before you fix

> When doing bug fixes, always start with reproducing the bug in an E2E setting as closely aligned with how an end user would observe the bug.

A fix without a reproduction is a guess. Agents are very good at producing a plausible patch for a plausible cause, and that patch will often make a symptom disappear while the real defect stays. Reproducing from the user's side (the real command, the real browser flow, the real input file) forces the agent to find the actual failure path. The reproduction then becomes the regression test.

The `systematic-debugging` skill encodes this: reproduce, isolate, root cause, then fix.

## Quality over development cost

> When making technical decisions, do not give much weight to development cost. Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.

With an agent, implementation time is cheap. The expensive thing is the code you have to live with. Left alone, models optimise for the shortest path to a passing test. Telling them explicitly that effort is not the constraint changes the designs they propose.

## Fix what you see

> Be picky about the UI you see and be obsessed with pixel perfection. If something clearly looks off, even if it is not directly related to what you are doing, try to get it fixed along the way.
>
> Apply the same high standard to engineering excellence: lint, test failures, and test flakiness. If you see one even if it is not caused by what you are working on right now, still get it fixed.

Broken windows compound. An agent that steps over a flaky test today teaches the next session that flaky tests are normal. Fixing adjacent problems costs a few minutes of agent time and keeps the baseline green, which is what makes overnight and parallel runs trustworthy.

Judgement still applies: a drive-by fix should be small and obviously correct. Anything larger becomes its own task with its own loop.

## Do not touch generated files

> Never manually modify CHANGELOG.md files or any files that are marked as auto-generated.

Edits to generated files are silently overwritten by the next generation run, and agents cannot tell a generated file from a hand-written one unless told. The rule is cheaper than the debugging session.

## Commit hygiene

> When writing commit messages, NEVER auto-add your agent name as co-author.

Commit authorship is a statement about responsibility. The person who reviewed and merged the change is the author. We keep agent attribution out of the git history so that `git blame` and release notes stay meaningful.

## Style

> Never use the em dash character. Use plain dash "-" instead.

A small rule with a large effect: model-written prose has recognisable tics, and the em dash is the most visible. Removing it, and running the `humanizer` skill on longer texts, keeps documentation and PR descriptions readable as something a colleague wrote.

## Verification before completion

Not in the instruction file, but enforced by the `verification-before-completion` skill and by you: no claim of success without the command output that proves it. Tests, lint, build, and for UI work a screenshot or a browser check.

## Adding a rule

Add a line to `~/AGENTS.md` when:

1. an agent has made the same mistake twice, or
2. a review caught something the agent should have known.

Write it as a concrete, verifiable instruction, and add the reasoning to this page so the next person understands it.
