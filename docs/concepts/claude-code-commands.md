---
icon: lucide/command
---

# Claude Code commands

Everything you type into Claude Code that starts with a slash is a **command**. Commands steer the harness itself: which account and model it uses, what is in the context window, what it is allowed to do. They are the fastest way to fix a session that has drifted, and most of them cost no tokens.

This page does not repeat the official documentation. It lists the commands we use, says when we reach for them, and links to the page that explains each one. The complete table with every option is the [commands reference](https://code.claude.com/docs/en/commands#all-commands); `/help` shows the same list inside a session. Some entries in the menu are [bundled skills](https://code.claude.com/docs/en/skills#bundled-skills) rather than built-in commands, prompts handed to the model in the same way as the [skills](skills.md) you write yourself. They are marked below.

## Account and model

| Command | When we use it | Documentation |
|---------|----------------|---------------|
| `/login`, `/logout` | Sign in with the subscription account, not an API key, see [plans and billing](models.md#plans-and-billing). Log out to switch between a personal and a team account. | [Authentication](https://code.claude.com/docs/en/authentication) |
| `/model` | Match the model to the task, see [choosing a model](models.md#choosing-a-model-per-task). Without an argument it opens a picker. | [Model configuration](https://code.claude.com/docs/en/model-config#setting-your-model) |
| `/effort` | Lower the effort for routine edits, raise it for design and hard bugs. | [Adjust effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level) |
| `/fast` | The same model with faster output, for interactive sessions where waiting is the bottleneck. | [Fast mode](https://code.claude.com/docs/en/fast-mode) |
| `/config` | Theme, default model, output style and every other setting, also as `/config key=value`. | [Settings](https://code.claude.com/docs/en/settings) |

## Context and usage

The context window is the scarcest resource in a session. The reasoning behind these commands is on the [token maxing](../best-practices/context-management.md) page.

| Command | When we use it | Documentation |
|---------|----------------|---------------|
| `/context` | After setup, to confirm the `CLAUDE.md` files are loaded. Whenever the agent starts to drift, to see what fills the window. | [See what loaded into context](https://code.claude.com/docs/en/debug-your-config#see-what-loaded-into-context) |
| `/usage` | When a session feels slow or a plan limit is near. Shows session cost, the plan usage bars and what skills, subagents and MCP servers consumed. `/cost` is an alias. | [Track your costs](https://code.claude.com/docs/en/costs#track-your-costs) |
| `/stats` | Token and tool call counts of the session, for comparing approaches. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |
| `/clear` | Before every new task. Our rule number one. Pass a name to find the old conversation again with `/resume`. | [Sessions](https://code.claude.com/docs/en/sessions#manage-context-within-a-session) |
| `/compact` | When the task is not finished but the window is full. Pass focus instructions. Prefer `/clear` when the next task is unrelated. | [Context window](https://code.claude.com/docs/en/context-window#what-survives-compaction) |
| `/resume` | Return to a conversation you cleared or branched away from. | [Resume a session](https://code.claude.com/docs/en/sessions#resume-a-session) |
| `/rewind` | The agent went down the wrong path. Rolls code and conversation back to a checkpoint. | [Checkpointing](https://code.claude.com/docs/en/checkpointing) |
| `/btw` | A side question that should not enter the conversation. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |

## Instruction files, skills and plugins

| Command | When we use it | Documentation |
|---------|----------------|---------------|
| `/init` | First `CLAUDE.md` for a repository without one. We then move the content to `AGENTS.md` and symlink it, see [instruction files](instruction-files.md). | [Set up a project CLAUDE.md](https://code.claude.com/docs/en/memory#set-up-a-project-claude-md) |
| `/memory` | Edit the `CLAUDE.md` files, review or switch off auto memory. | [Auto memory](https://code.claude.com/docs/en/memory#auto-memory) |
| `/skills` | See which skills are loaded and create new ones. Custom commands and skills are the same mechanism. | [Skills](https://code.claude.com/docs/en/skills) |
| `/plugin` | Install and manage plugins, for example `/plugin install superpowers@claude-plugins-official`. | [Discover plugins](https://code.claude.com/docs/en/discover-plugins) |
| `/mcp` | Disable the MCP servers you do not use, every server costs context. | [MCP](https://code.claude.com/docs/en/mcp) |
| `/hooks` | Check that a hook is registered before trusting it to enforce something. | [Hooks](https://code.claude.com/docs/en/hooks) |
| `/doctor` | Periodic checkup: installation, unused skills and servers, slow hooks, oversized `CLAUDE.md` files. Bundled skill. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |

## Permissions and safety

| Command | When we use it | Documentation |
|---------|----------------|---------------|
| `/permissions` | Review and edit the allow, ask and deny rules by scope. | [Permissions](https://code.claude.com/docs/en/permissions) |
| `/fewer-permission-prompts` | After a few sessions in a repository, to allow the read-only commands you approve every day. Bundled skill. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |
| `/add-dir` | Give the session access to a second checkout or a data directory. | [Working directories](https://code.claude.com/docs/en/permissions#working-directories) |
| `/sandbox` | Isolate experiments from the machine. | [Sandboxing](https://code.claude.com/docs/en/sandboxing) |

The permission mode itself is cycled with ++shift+tab++. Start strict, then allow the read-only calls you see all the time. See [permission modes](https://code.claude.com/docs/en/permission-modes).

## Working on a task

| Command | When we use it | Documentation |
|---------|----------------|---------------|
| `/plan` | Anything with more than one reasonable design. The agent reads and designs but edits nothing until you approve. The brainstorming skill covers the step before, see the [development loop](../best-practices/index.md). | [Plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) |
| `/diff` | Review the agent's edits before running tests or committing. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |
| `/code-review` | Before opening a pull request, for a review of the diff. `/review` is an alias. Bundled skill. | [Review a diff locally](https://code.claude.com/docs/en/code-review#review-a-diff-locally) |
| `/security-review` | Before merging anything that touches authentication, input handling or secrets. Bundled skill. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |
| `/worktree` | Parallel work in isolated checkouts, see [orchestration](orchestration.md). | [Worktrees](https://code.claude.com/docs/en/worktrees) |
| `/subtask` | A side task whose output should stay out of the conversation. | [Subagents](https://code.claude.com/docs/en/sub-agents) |
| `/tasks` | Check on background work and finished subagents. | [Commands reference](https://code.claude.com/docs/en/commands#all-commands) |
| `/export` | Hand a conversation to a colleague or attach it to a bug report. | [Export session data](https://code.claude.com/docs/en/sessions#export-and-locate-session-data) |

## Keys worth knowing

The full list is in [keyboard shortcuts](https://code.claude.com/docs/en/interactive-mode#keyboard-shortcuts); these are the ones we use daily.

| Key | When we use it |
|-----|----------------|
| `! <command>` | Run a shell command yourself, with the output in the conversation. For interactive logins the agent cannot do, for example `! gh auth login`. See [shell mode](https://code.claude.com/docs/en/interactive-mode#shell-mode-with-prefix). |
| `@path` | Put a file into the context without asking the agent to read it. |
| ++esc++ | Stop the turn as soon as the agent heads in the wrong direction. |
| ++esc++ ++esc++ | Open the rewind menu, same as `/rewind`. |
| ++shift+tab++ | Cycle the permission mode. |

## The daily set

If you remember five commands, remember these:

1. `/clear` before every new task.
2. `/context` when the agent drifts or after changing instruction files.
3. `/model` and `/effort` to match the model to the task.
4. `/usage` when a session feels slow or a limit is near.
5. `/plan` for anything with more than one reasonable design.
