s API and provides a simple interactive CLI for generating code, exploring projects, and building small applications directly from the terminal.

---

## Features

- Terminal-based AI coding assistant
- Project selection system
- Multi-project workspace support
- Groq API integration (LLaMA models)
- Simple interactive CLI
- Works in minimal Linux environments (Alpine/iSH)
- Designed for extensibility

---

## Project Structure

code-assistant/
- code.py              Main CLI entry point
- agent.py             AI API wrapper (Groq)
- projects.py          Project selector / manager
- scanner.py           Reads project files (context builder)
- filesystem.py        Safe file write tools (future)
- project_index.py     File search utilities
- config.py            Rules and behavior config
- README.md

---

## Setup

1. Install dependencies:
pip install requests

2. Set your Groq API key:
export GROQ_API_KEY="your_api_key_here"

To persist it:
echo 'export GROQ_API_KEY="your_api_key_here"' >> ~/.profile
source ~/.profile

3. Run the assistant:
python3 code.py

---

## Usage

Select a project, then type prompts like:
code> create a simple ascii radar animation

The assistant will generate code based on your request and project context.

---

## Project System

Projects are stored in:
/root/projects/

Each folder is treated as an isolated workspace. The assistant reads files to understand context before responding.

---

## Limitations

- No safe file writing system yet
- No Git automation yet
- No patch-based editing yet
- No long-term memory
- No sandboxing

---

## Roadmap

- Safe file writer (WRITE / EDIT / DELETE system)
- Git auto-commit integration
- Diff-based editing system
- Project memory indexing
- Command modes (chat / edit / plan)
- Plugin system

---

## Philosophy

Minimal, transparent, terminal-native AI coding assistant designed for constrained environments like iSH. Full user control, no hidden automation.

---

## License

MIT License# Alpine Coding Assistant

A lightweight terminal-based AI coding assistant that runs on Linux environments (including iSH on iPhone). It connects to Groqb
