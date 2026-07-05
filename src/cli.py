"""
Main CLI loop for Alpine Code Assistant.

Commands available at the prompt:
  /help        Show this help
  /project     Switch to a different project
  /clear       Clear conversation history
  /tree        Print the current project file tree
  /read <file> Print a file from the project
  /undo <file> Restore a file's .bak backup
  /quit        Exit
"""

import os
import sys

from src.ai import ask, AIError
from src.history import History
from src.parser import extract_plan, extract_actions, has_actions
from src.executor import execute_actions
from src.scanner import build_context, file_tree
from src.projects import select_project
from src.filesystem import read_file, FileSystemError
from src.config import MODEL

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HELP_TEXT = """
Commands:
  /help           This message
  /project        Switch project (clears history)
  /clear          Clear conversation history
  /tree           Show project file tree
  /read <path>    Print a file from the project
  /undo <path>    Restore <path> from its .bak backup
  /quit           Exit

Everything else is sent to the AI.
Use natural language: "add a CLI flag for verbose mode",
"refactor utils.py to use dataclasses", etc.
""".strip()


def _banner(project_path: str) -> None:
    name = os.path.basename(project_path)
    print()
    print("╔══════════════════════════════════════════╗")
    print("║       Alpine Code Assistant  🏔           ║")
    print("╚══════════════════════════════════════════╝")
    print(f"  Model  : {MODEL}")
    print(f"  Project: {name}")
    print(f"  Path   : {project_path}")
    print()
    print("  Type /help for commands.")
    print()


def _handle_command(
    raw: str,
    project_path: str,
    history: History,
) -> tuple[str | None, bool]:
    """
    Handle a /command line.

    Returns (new_project_path_or_None, should_continue).
    If should_continue is False the caller should exit the loop.
    """
    parts = raw.strip().split(None, 1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in ("/quit", "/exit", "/q"):
        print("Goodbye.")
        return project_path, False

    if cmd == "/help":
        print(HELP_TEXT)
        return project_path, True

    if cmd == "/clear":
        history.clear()
        print("History cleared.")
        return project_path, True

    if cmd == "/tree":
        print()
        print(file_tree(project_path))
        print()
        return project_path, True

    if cmd == "/read":
        if not arg:
            print("Usage: /read <relative/path>")
            return project_path, True
        try:
            content = read_file(project_path, arg)
            print()
            print(f"── {arg} " + "─" * max(0, 42 - len(arg)))
            print(content)
            print("─" * 44)
            print()
        except FileSystemError as e:
            print(f"Error: {e}")
        return project_path, True

    if cmd == "/undo":
        if not arg:
            print("Usage: /undo <relative/path>")
            return project_path, True
        bak = arg + ".bak"
        try:
            content = read_file(project_path, bak)
            from src.filesystem import write_file
            write_file(project_path, arg, content)
            print(f"Restored {arg} from backup.")
        except FileSystemError as e:
            print(f"Error: {e}")
        return project_path, True

    if cmd == "/project":
        new_path = select_project()
        if new_path:
            history.clear()
            print(f"Switched to: {os.path.basename(new_path)}")
            return new_path, True
        return project_path, True

    print(f"Unknown command '{cmd}'. Type /help for available commands.")
    return project_path, True


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run() -> None:
    """Start the interactive CLI."""
    project_path = select_project()

    if not project_path:
        print("No project selected. Exiting.")
        sys.exit(0)

    _banner(project_path)
    history = History()

    while True:
        try:
            raw = input("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        # ── Built-in commands ─────────────────────────────────────────────
        if raw.startswith("/"):
            project_path, should_continue = _handle_command(raw, project_path, history)
            if not should_continue:
                break
            continue

        # ── AI request ───────────────────────────────────────────────────
        context = build_context(project_path)
        user_message = f"{context}\n\n## Task\n{raw}"

        history.add_user(user_message)

        print()
        print("Thinking…")

        try:
            reply = ask(history.get())
        except AIError as e:
            print(f"\nAI Error: {e}\n")
            # Remove the last user message so the history stays clean
            history._messages.pop()
            continue

        history.add_assistant(reply)

        # ── Print the reply (strip FILE block content to keep output clean)
        _print_reply(reply)

        # ── Apply file actions if present ─────────────────────────────────
        if has_actions(reply):
            actions = extract_actions(reply)
            if actions:
                execute_actions(project_path, actions)


def _print_reply(reply: str) -> None:
    """
    Print the AI reply, replacing bulky FILE block content with a summary
    so the terminal output stays readable.
    """
    import re

    # Replace file content blocks with a short summary line
    clean = re.sub(
        r"<<<FILE:\s*(.+?)\n.*?>>>",
        lambda m: f"<<<FILE: {m.group(1).strip()} — content written above>>>",
        reply,
        flags=re.DOTALL,
    )

    print()
    print(clean)
    print()
