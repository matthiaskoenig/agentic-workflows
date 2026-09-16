---
icon: lucide/wrench
---

# Tooling

Tools around the harness that make daily agent work faster. None of these are required; each solves one specific annoyance.

## Voice

Voice enters agentic work from two sides: speech to text for talking to the agent, and text to speech for turning written material into narration.

### Speech to text: talking to the agent

Long prompts are faster spoken than typed, and a brainstorming conversation is mostly prose. Speaking also changes what you say: people describe the goal and the constraints instead of dictating the solution, which is exactly what the [development loop](best-practices/index.md) wants. Speech recognition models such as OpenAI's Whisper and NVIDIA's Parakeet run locally on a laptop with good accuracy for technical vocabulary, so nothing leaves the machine.

- [OpenSuperWhisper](https://github.com/Starmel/OpenSuperWhisper): macOS dictation app with real-time transcription using Whisper and Parakeet models. Apple Silicon only. `brew install opensuperwhisper` or download a release. Dictate into any text field, including the agent's prompt.

On Linux we do not have a settled recommendation yet; `whisper.cpp` with a small push-to-talk wrapper is the usual starting point.

### Text to speech: AI voice-over

The reverse direction turns written material into spoken audio: lecture notes into a narrated recording, a thesis chapter into something to listen to, slides into a voiced video. Current text to speech models produce natural speech in many languages and can clone a voice from a short sample, so a course can be narrated in a consistent voice without recording sessions.

Our [text2speech](https://github.com/matthiaskoenig/text2speech) tool converts markdown files into spoken-word audio with [Coqui XTTS-v2](https://huggingface.co/coqui/XTTS-v2), a multilingual voice-cloning model. It runs on CPU, but a GPU makes it practical for whole chapters; several GPUs are used in parallel automatically. Note the model's non-commercial license.

```bash
uv run converter.py input/            # every .md file in a directory to output/<name>.mp3
uv run converter.py --list-speakers   # built-in voices
```

Typical uses: narrated versions of teaching material such as this site, voice-over for talk recordings and screencasts, and audio proof-listening of long texts, where hearing a sentence catches errors that reading skips.

## Editor integration

### VS Code

Claude Code ships a VS Code extension; Codex and others have their own. [Continue](https://marketplace.visualstudio.com/items?itemName=Continue.continue) is a provider-agnostic alternative if you want one extension for several models.

### Clickable links in the terminal

Agents often produce an HTML report (test coverage, a preview, a screenshot diff). Opening it should be one click, not a copy-paste of a path. With the Python `rich` library, print a hyperlink the terminal understands:

```python
from rich.console import Console

console = Console()
console.print("[link=file:///home/user/report.html]Open HTML report[/link]")
```

Most modern terminals (VS Code's integrated terminal, iTerm2, kitty, WezTerm) render this as a clickable link. Add it to the scripts your agents run so the report is one click away.

## Token-saving CLIs

Covered in detail on [token maxing](best-practices/context-management.md):

- [AXI tools](https://axi.md/) such as `gh-axi` and `chrome-devtools-axi`
- [rtk](https://github.com/rtk-ai/rtk) and [headroom](https://github.com/headroomlabs-ai/headroom) for output compression
- [TOON](https://toonformat.dev/) for compact structured data

## Browser

[Claude in Chrome](https://claude.ai/chrome) connects Claude Code to your running Chrome, so the agent checks a page the way you would: open it, click through it, read the console, take a screenshot. Keep Chrome open in the background whenever the task touches a web page, otherwise the extension is not reachable and validation gets slower and less reliable. Installation is on the [setup checklist](setup.md#browser).

## Session management

- [tmux](https://github.com/tmux/tmux) for several agents on one screen
- [herdr](https://herdr.dev/) for agents that outlive your laptop session

See [orchestration](concepts/orchestration.md).

## Code intelligence

Without a language server, the agent finds definitions and references with grep and learns about a type error only when it runs the type checker. [Code intelligence plugins](https://code.claude.com/docs/en/discover-plugins#code-intelligence) connect Claude Code to a Language Server Protocol server, the same machinery behind VS Code's code navigation. The agent then sees errors and warnings right after every edit and fixes them in the same turn, and it can jump to definitions, find references and trace call hierarchies instead of guessing from search results. The plugin page explains what the agent gains and lists the plugin and binary for each language.

Two steps per language: install the language server binary yourself, then install the plugin. The plugin only wires the binary in, it does not install it.

```bash
# Python: pyright
uv tool install pyright                    # or: npm install -g pyright
claude plugin install pyright-lsp@claude-plugins-official

# TypeScript and JavaScript
npm install -g typescript-language-server typescript
claude plugin install typescript-lsp@claude-plugins-official
```

Nothing else to configure. In a session, a line such as `Found 3 new diagnostic issues in 2 files` means the server is working; press `Ctrl+O` to read the diagnostics yourself. If the `/plugin` Errors tab says `Executable not found in $PATH`, the binary is missing or not on the `PATH` that Claude Code sees. Cloud sessions do not start language servers, so this only helps locally.

!!! tip
    If pyright or the TypeScript server is already installed, Claude Code may offer to install the matching plugin when you open a project. Accept it.

## Plugin marketplaces

Claude Code plugins are installed from marketplaces:

```bash
claude plugin install superpowers@claude-plugins-official
claude plugin install humanizer@humanizer
```

`claude-plugins-official` is Anthropic's marketplace and contains `superpowers`, `feature-dev` and others. Run `/plugin` inside a session to browse.
