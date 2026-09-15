---
icon: lucide/circle-help
---

# Open questions

Things we have not settled yet. Each entry says what we know, what is open, and the next step. When a question is answered, the answer moves to the page it belongs to and the entry here is removed. If you try something out, write the result down here, even a negative one.

## Voice programming: how to set it up and use it

**What we know.** Speaking a task description is faster than typing it and produces better specifications. On macOS, [OpenSuperWhisper](https://github.com/Starmel/OpenSuperWhisper) dictates into any text field, including the terminal running Claude Code. See [voice](tooling.md#voice).

**Open.**

- A Linux setup: a local speech-to-text model (`whisper.cpp`, Parakeet) with push-to-talk that types into the active window.
- Whether dictating into the terminal prompt is good enough, or whether a dedicated input field (the VS Code extension panel) works better for long descriptions.
- Voice for the review side: reading a diff summary aloud while checking it.

**Next step.** Try one Linux push-to-talk tool for a week of brainstorming sessions and record what breaks.

## Long-running tasks over night

**What we know.** The pattern is documented in [orchestration](concepts/orchestration.md#overnight-runs): brainstorm and plan by day, start the agent in herdr or tmux in the evening with the plan file, review in the morning. Branch protection makes a bad night cheap.

**Open.**

- Permission prompts stop an unattended run. Which permission mode to use, and which allow rules in the settings file are safe enough for a run nobody watches.
- How to be notified when the run finishes or gets stuck (hooks on stop, a message, a pull request opened automatically).
- What to do when the plan turns out wrong halfway: let the agent stop and write a report, or let it re-plan within limits.
- Plan usage: how much of the daily and weekly quota an overnight run consumes, and how to see it in the morning.

**Next step.** Run one real plan overnight with the `Stop` hook sending a notification, and note every point at which it waited for a human.

## Settings files for agents and budgets

**What we know.** Claude Code reads settings from several layers: managed policy, user (`~/.claude/settings.json`), project (`.claude/settings.json`, shared via git) and local (`.claude/settings.local.json`, ignored). They hold permissions (allow and deny rules for tools and commands), hooks, environment variables and the default model. Instruction files ask; settings and hooks enforce. See [instruction files](concepts/instruction-files.md) and [harnesses](concepts/harnesses.md).

**Open.**

- A shared baseline `settings.json` for our repositories: the read-only commands that never need a prompt, the commands that always need one, the formatter and lint hooks.
- Whether to commit `.claude/settings.json` to every repository or to keep one user-level file per machine.
- Budgets: there is no per-project budget in a subscription plan. `quota-axi` reads the remaining quota; what we lack is a rule for which tasks get the strongest model and which a cheaper one, applied automatically.
- The same for Codex: its config file, its permission model, and how far the two can share a vocabulary.

**Next step.** Draft the baseline settings file in this repository, use it for two weeks, then copy it to the reference repository.

## herdr on all machines with a continuously running server

**What we know.** [herdr](https://herdr.dev/) keeps agent sessions running in the background and reachable across machines, and is the tool we want for anything longer than a single sitting. See [remote connections](concepts/orchestration.md#remote-connections).

**Open.**

- Topology: one always-on server (the GPU server or a small VM) running herdr with the agents, and laptops as thin clients. Which machine holds the checkouts, and how the laptops reach it (ssh, tailscale, herdr's own transport).
- Authentication of the agent CLIs on the server: signing in to Claude Code and Codex once on a headless machine, and how long the sessions last.
- Whether one herdr installation per machine is needed, or only on the server.
- How herdr and the VS Code extension coexist: attaching the editor to a session that lives on the server.

**Next step.** Install herdr on the GPU server, run one agent for a week from two laptops, and document the setup on the orchestration page.

## Managing tokens and team members

**What we know.** We work on subscription plans, not per-token billing: Claude Max and a standard ChatGPT plan, see [plans and billing](concepts/models.md#plans-and-billing). Repository policies are the same for every member and are applied with `apply.sh`, see [repository policies](best-practices/repository-policies.md).

**Open.**

- When a second person joins: individual Max plans, or a Claude Team or Enterprise plan with shared administration and usage visibility. What the team plans add for Claude Code specifically.
- Usage visibility: how to see per-person consumption without an API key, and whether that matters if everyone is on a flat plan.
- Which parts of the setup are per person (global `AGENTS.md`, user settings, plugins) and which are per repository (project `AGENTS.md`, project settings, rulesets), written down as an onboarding step for a new member.
- API keys for automation (scheduled cloud agents, CI): who owns them, where they live, and a spending limit.

**Next step.** Compare the Team plan with two Max plans on price and on what the administration adds, before the next person joins.

## Multiple accounts

**What we know.** One person may hold a personal subscription and an institutional account. Claude Code signs in with `/login` and keeps one account per configuration directory; a second configuration directory can be selected with the `CLAUDE_CONFIG_DIR` environment variable. The GitHub CLI supports several accounts with `gh auth switch`.

**Open.**

- A clean way to run two Claude Code identities on one machine: separate configuration directories with a shell alias, and what that does to plugins, memory and settings, which live in the same directory.
- The same for Codex and for the VS Code extensions, which may not support switching at all.
- Which account an overnight run on the server uses, and how quota is shared between interactive and unattended use.

**Next step.** Set up a second configuration directory, note what has to be duplicated, and write the recipe on the harnesses page.

## One harness for all models

**What we know.** We use Claude Code for nearly everything and Codex much less, mostly for second opinions. Each ties us to one vendor's models, so switching models means switching tools, commands, skills, hooks and permissions. OpenCode and pi are provider-agnostic and read the same `AGENTS.md`; both are installed and in an evaluation phase. See [harnesses](concepts/harnesses.md#harnesses-we-use).

**Open.**

- Whether OpenCode or pi with Claude models matches Claude Code on real tasks: plan quality, tool use, permission handling, and how much of our plugins and skills carry over.
- Whether the same harness can run GPT and open-weight models well enough that Codex and a separate local setup become unnecessary.
- What we would lose: Claude Code specifics such as bundled skills, worktrees, subagents and the VS Code extension, see [Claude Code commands](concepts/claude-code-commands.md).

**Next step.** Run the same three tasks, one design, one bug fix, one review, through Claude Code, OpenCode and pi with the same Claude model, and record the differences here.

## Tools mentioned but not yet evaluated

- **treehouse**, a git worktree helper. Where it fits next to the `using-git-worktrees` skill. See [orchestration](concepts/orchestration.md).
- **backpass**, mining past sessions for recurring corrections and proposing instruction-file updates. See [instruction files](concepts/instruction-files.md).
- **no-mistakes pipeline**, a fixed sequence of automated checks before a human looks at an agent's change. Our required checks are the first version of this; what else belongs in it. See [orchestration](concepts/orchestration.md).
- **rtk** and **headroom** for output compression: measure the saving with `/context` on a real task. See [token maxing](best-practices/context-management.md).
- **DeepSeek V4 Flash** on the GPU server via Ollama as a local model for sensitive data. See [models](concepts/models.md).
