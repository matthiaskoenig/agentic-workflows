---
icon: lucide/rocket
---

# Getting started

This page takes you from a clean machine to a working agent setup that matches the rest of this site. Budget about an hour.

If you only want the list of things to install, with commands and no explanation, see the [setup checklist](setup.md).

## 1. Install a harness

We primarily use [Claude Code](https://code.claude.com/docs/en/setup). Other harnesses are covered on the [harnesses](concepts/harnesses.md) page; the setup below is Claude Code specific unless noted.

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```

Then run `claude` inside any git repository and log in when prompted.

!!! tip "Read how it works before you use it"
    Spend 15 minutes on [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works). Understanding the loop (prompt, tool call, tool result, repeat) explains almost every behaviour you will see later.

## 2. Create your global instruction file

Every agent session starts with a fresh context. Instructions you want in *every* session belong in a global file. We keep one `AGENTS.md` in the home directory and symlink it so every harness finds it:

```bash
# ~/AGENTS.md is the single source of truth
ln -s ~/AGENTS.md ~/.claude/CLAUDE.md
```

Start from the template on the [instruction files](concepts/instruction-files.md) page. Keep it short. Add a line only when you have corrected an agent twice for the same thing.

## 3. Install the plugins we rely on

```bash
claude plugin install superpowers@claude-plugins-official
claude plugin install humanizer@humanizer
```

`superpowers` provides the process skills (brainstorming, planning, TDD, systematic debugging, code review). `humanizer` improves the tone of written output. The [skills](concepts/skills.md) page explains what each does and when it fires.

Inside a session you can also run `/plugin install <name>` instead of the shell command.

## 4. Set up a project

In each repository:

```bash
# project instructions, shared with the team via git
ln -s AGENTS.md CLAUDE.md
```

If the project has no `AGENTS.md` yet, run `/init` in Claude Code to generate a first version, then move the content into `AGENTS.md` and symlink as above.

Add `CLAUDE.local.md` to `.gitignore` for personal, per-project notes.

## 5. Run your first session

1. Open a terminal in the project, run `claude`.
2. Run `/context` and confirm your `CLAUDE.md` files appear under **Memory files**.
3. Describe a small, real task. Let the brainstorming skill ask its questions.
4. Approve the design, let the agent implement with tests, and review the diff.
5. Run `/clear` before starting the next task.

That is the whole loop. The [development loop](best-practices/index.md) page goes through each step in detail.

## Onboarding checklist

- [ ] Harness installed and logged in
- [ ] `~/AGENTS.md` written and symlinked to `~/.claude/CLAUDE.md`
- [ ] `superpowers` and `humanizer` plugins installed
- [ ] Project `AGENTS.md` symlinked as `CLAUDE.md`
- [ ] `/context` shows the memory files
- [ ] First task completed through brainstorm, plan, implement, review
- [ ] Read [token maxing](best-practices/context-management.md)
- [ ] Read [engineering standards](best-practices/engineering-standards.md)
