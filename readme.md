# 🏔 Alpine Code Assistant

A lightweight, terminal-native AI coding assistant built for constrained environments — primarily **iSH on iPhone** running Alpine Linux, but works on any Linux/macOS terminal.

It connects to the **Groq API** (free tier available) and gives you a Kiro-style interactive loop where you can ask it to read, write, edit, and delete files inside a project — all from your terminal.

---

## Features

- **Interactive AI coding loop** — describe what you want, the AI reads your project and acts on it
- **Full file write/edit/delete** — the AI outputs structured file actions that are applied automatically
- **Multi-language support** — Python, JS/TS, HTML, CSS, Shell, Go, Rust, YAML, JSON, Markdown, and more
- **Project workspace system** — isolated `/root/projects/<name>` workspaces
- **Conversation history** — context-aware multi-turn conversation with automatic trimming
- **Project context injection** — every message includes the current file tree and file contents so the AI always knows your codebase
- **Safe file writes** — automatic `.bak` backup before overwriting any file
- **Path traversal protection** — file operations are sandboxed to the project root
- **/undo command** — restore any file from its last backup instantly
- **Minimal dependencies** — only `requests` (no LangChain, no heavy frameworks)
- **Fast on low-spec hardware** — designed for iSH's constrained CPU/RAM

---

## How It Works

```
You type a task  →  AI sees your file tree + file contents  →  AI outputs a PLAN + FILE blocks
→  Assistant prints plan  →  Files are written/edited/deleted automatically
```

The AI is instructed to always scan before writing, prefer editing existing files over creating new ones, and output complete file contents (no partial diffs).

---

## Project Structure

```
alpine-code-assistant/
├── main.py              Entry point — run this
├── requirements.txt     Python dependencies (just `requests`)
├── install.sh           One-shot Alpine/iSH setup script
├── README.md
└── src/
    ├── __init__.py
    ├── config.py        API keys, model, limits, system prompt
    ├── cli.py           Interactive CLI loop + slash commands
    ├── ai.py            Groq API wrapper
    ├── history.py       Conversation history with token-budget trimming
    ├── scanner.py       Project file tree + context builder
    ├── parser.py        AI response parser (extracts FILE/DELETE blocks)
    ├── executor.py      Applies parsed file actions to disk
    ├── filesystem.py    Safe file read/write/delete with .bak backups
    └── projects.py      Project selector and workspace manager
```

---

## Setup

### 1. On iSH (Alpine Linux)

```sh
# Install git and clone
apk add git
git clone https://github.com/yourname/alpine-code-assistant
cd alpine-code-assistant

# Run the setup script
sh install.sh
```

### 2. On any Linux / macOS

```sh
git clone https://github.com/yourname/alpine-code-assistant
cd alpine-code-assistant
pip3 install -r requirements.txt
mkdir -p /root/projects   # or set KIRO_PROJECTS_DIR to any path
```

### 3. Set your Groq API key

Get a free key at [console.groq.com](https://console.groq.com).

```sh
export GROQ_API_KEY="gsk_your_key_here"
```

To persist across sessions:

```sh
echo 'export GROQ_API_KEY="gsk_your_key_here"' >> ~/.profile
source ~/.profile
```

### 4. Run

```sh
python3 main.py
```

---

## Usage

### Project selector

On launch you'll see your project list:

```
── Projects ─────────────────────────────
  1)  my-web-app
  2)  cli-tool
  3)  + New project
  q)  Quit
─────────────────────────────────────────
Select:
```

### The prompt

After selecting a project you get the interactive prompt:

```
❯ 
```

Type natural language tasks:

```
❯ create a Flask app with a /health endpoint
❯ add argparse to main.py for a --verbose flag
❯ refactor utils.py to use dataclasses instead of plain dicts
❯ write a Dockerfile for this Python project
❯ add unit tests for the parse_date function in utils.py
```

The AI reads your entire project first, then outputs a plan and writes the files.

### Slash commands

| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/tree` | Print the project file tree |
| `/read <path>` | Print a file's contents |
| `/undo <path>` | Restore a file from its `.bak` backup |
| `/project` | Switch to a different project (clears history) |
| `/clear` | Clear conversation history |
| `/quit` | Exit |

---

## File Action Format (for reference)

The AI uses this structured format when it needs to write files:

```
PLAN:
  WRITE  src/app.py
  EDIT   requirements.txt
  DELETE src/old_stuff.py

<<<FILE: src/app.py
(full file content)
>>>

<<<FILE: requirements.txt
(full file content)
>>>

<<<DELETE: src/old_stuff.py>>>
```

The assistant automatically detects these blocks and applies them. You don't need to copy-paste anything.

---

## Configuration

All settings are in `src/config.py`:

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | `$GROQ_API_KEY` env var | Your Groq API key |
| `MODEL` | `llama-3.3-70b-versatile` | Groq model to use |
| `PROJECTS_DIR` | `/root/projects` | Root for all projects |
| `MAX_FILE_BYTES` | `8000` | Files larger than this get a size note |
| `MAX_TOTAL_CONTEXT_BYTES` | `60000` | Total context cap per request |
| `TIMEOUT` | `300` | API request timeout (seconds) |

You can override `PROJECTS_DIR` via environment:

```sh
export KIRO_PROJECTS_DIR=/home/myuser/code
```

---

## Customising the System Prompt

The AI's behaviour is controlled by the system prompt in `src/config.py` → `SYSTEM_PROMPT`. Edit it to:

- Change the assistant's tone or verbosity
- Add project-specific rules (e.g. "always use async/await", "use Tailwind for CSS")
- Restrict what kinds of files it can create

---

## Limitations

- No streaming output (full response arrives at once — can feel slow on first run)
- No interactive file confirmation (plan is shown, then files are written automatically)
- Conversation history is in-memory only (cleared on exit / project switch)
- Large projects may hit context limits (files are capped and trimmed automatically)
- Requires network access to Groq (no local model support yet)

---

## Roadmap

- [ ] Streaming responses (print tokens as they arrive)
- [ ] `/diff` command to show a before/after diff before writing
- [ ] Persistent conversation history (saved to `.kiro_history.json` per project)
- [ ] `.kiroignore` file to exclude files from context
- [ ] Git integration (`/commit` command to stage and commit AI changes)
- [ ] Local model support via Ollama
- [ ] Plugin / hook system for custom commands

---

## Philosophy

Minimal, transparent, terminal-native. No hidden automation, no heavy frameworks, no cloud sync. You see exactly what the AI plans to do before it does it. Designed to work on the most constrained Linux environment you have — your phone.

---

## License

MIT
