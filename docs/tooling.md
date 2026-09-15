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

## Session management

- [tmux](https://github.com/tmux/tmux) for several agents on one screen
- [herdr](https://herdr.dev/) for agents that outlive your laptop session

See [orchestration](concepts/orchestration.md).

## Plugin marketplaces

Claude Code plugins are installed from marketplaces:

```bash
claude plugin install superpowers@claude-plugins-official
claude plugin install humanizer@humanizer
```

`claude-plugins-official` is Anthropic's marketplace and contains `superpowers`, `feature-dev` and others. Run `/plugin` inside a session to browse.
