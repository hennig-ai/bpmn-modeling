# BPMN Modeling

An agent skill that creates and modifies BPMN process models
in Markdown table format based on the BPMN Database Schema.

This skill follows the open [Agent Skills](https://agentskills.io) standard.
Your AI agent must support skills to use it.

## What it does

- **New model creation** from natural language process descriptions
- **Model modification** of existing BPMN Markdown models
- **Automated validation** via `validate_bpmn.py` with auto-repair loop
- Full referential integrity (PK/FK validation)
- BPMN 2.0 conformance checks

## Prerequisites

- **Python** >= 3.10
- **pip** (up to date — run `python -m pip install --upgrade pip` if installs fail)
- **Git**

## Installation

Pre-installing dependencies avoids the agent downloading and building wheels at the start of every session. Clone the tagged version and install dependencies once:

```bash
git clone --depth 1 --branch pre-wheel-merge-1.0.2 https://github.com/hennig-ai/bpmn-modeling.git <skill-path>
pip install <skill-path>
```

`--depth 1` fetches only the tagged commit. `pip install` pulls all dependencies (`bpmn-lib`, `basic-framework`) from PyPI.

Replace `<skill-path>` with the skills directory for your platform:

| Platform | Project-level | Personal |
|----------|--------------|----------|
| Claude Code | `.claude/skills/bpmn-modeling` | `~/.claude/skills/bpmn-modeling` |
| OpenAI Codex CLI | `.agents/skills/bpmn-modeling` | — |
| GitHub Copilot | `.github/skills/bpmn-modeling` | — |

> **Windows note:** `~` is only expanded in Git Bash/MSYS2, not in PowerShell or CMD. Use `$HOME` or `%USERPROFILE%` instead.

## Usage

Trigger the skill with BPMN-specific requests, e.g.:
- "Create a BPMN model for an order process"
- "Add an Exclusive Gateway to the model"
- "Validate the BPMN model"

## License

MIT — see [LICENSE](LICENSE) for details.
