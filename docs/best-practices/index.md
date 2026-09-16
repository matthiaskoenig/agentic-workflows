---
icon: lucide/repeat
---

# The development loop

Every task, from a one-line fix to a new subsystem, goes through the same loop. The size of each step scales with the task; the order does not change. The `superpowers` skills implement this loop, so most of it happens by asking the agent to do the work and letting the skills fire.

```mermaid
flowchart LR
    C["/clear"] --> B[Brainstorm]
    B --> P[Plan]
    P --> I[Implement<br/>with TDD]
    I --> V[Verify]
    V --> R[Review]
    R --> M[Merge]
    M --> C
    class C,B,P,I,V skill
    class R human
    class M artifact
    --8<-- "mermaid-classes.mmd"
```

## 1. Start clean

Run `/clear` (or open a new session). Leftover context from the previous task pollutes the model's attention and costs tokens on every turn. Anything worth keeping from the last task should already be in a file or a commit.

## 2. Brainstorm before building

State the goal, not the solution. Let the `brainstorming` skill ask its questions. Answer them one at a time. The output is a short design in chat for small changes, or a spec file under `docs/superpowers/specs/` for anything architectural.

Do not let the agent write code before you have said yes to a design. This is the cheapest point in the loop to catch a wrong assumption.

## 3. Plan

For anything larger than a single-file change, ask for a written plan (`writing-plans` skill). A plan lists ordered steps, the files each touches, and how each will be verified. Plans live in the repository so they survive `/clear` and can be handed to another agent or run overnight.

## 4. Implement with tests first

The agent writes a failing test, makes it pass, then refactors. Insist on it. A change without a test is a change you cannot verify tomorrow. For bug fixes, the test *is* the reproduction: see [engineering standards](engineering-standards.md).

Independent steps of a plan can run in parallel subagents or worktrees. See [orchestration](../concepts/orchestration.md).

## 5. Verify with evidence

"Done" means the test suite, linter and build were run *and the output was shown*. The `verification-before-completion` skill enforces this. If the agent reports success without output, ask for the output.

## 6. Review

Two layers:

- **Agent review.** `/code-review` or the `feature-dev` reviewer agent reads the diff for bugs, security issues and convention violations. Cheap, run it every time.
- **Human review.** You read the diff. For UI work, use a browser feedback surface such as lavish rather than guessing from the code.

When feedback comes back, the `receiving-code-review` skill makes the agent verify each point instead of agreeing blindly.

## 7. Merge and reset

Squash or merge, delete the worktree, `/clear`, next task.

## Sizing the loop

| Task | Brainstorm | Plan file | TDD | Review |
|------|------------|-----------|-----|--------|
| Typo, config tweak | Two sentences in chat | No | If testable | Agent |
| Bug fix | Reproduce first, then short design | No | Yes, reproduction test | Agent + human |
| Feature in existing flow | Questions, short design in chat | Optional | Yes | Agent + human |
| New subsystem or project | Full: questions, approaches, spec | Yes | Yes | Agent + human, per step |

## Anti-patterns

- **Prompting the solution.** "Add a Redis cache" skips the question of whether caching is the problem. State the symptom and the goal.
- **Skipping the design gate because it is small.** Small tasks hide the most unexamined assumptions.
- **One giant session.** Context fills, the model forgets the early constraints, quality drops. `/clear` between tasks.
- **Trusting "all tests pass" without output.** Ask for the log.
- **Fixing symptoms.** A fix without a reproduction is a guess.
