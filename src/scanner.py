"""
Project scanner.

Builds a context string from the files in a project directory that the AI
can use to understand the existing codebase before responding.
"""

import os
from src.config import (
    MAX_FILE_BYTES,
    MAX_TOTAL_CONTEXT_BYTES,
    TEXT_EXTENSIONS,
    SKIP_DIRS,
)


def _is_text_file(filename: str) -> bool:
    """Return True if the file extension (or base name) is in TEXT_EXTENSIONS."""
    _, ext = os.path.splitext(filename)
    return ext in TEXT_EXTENSIONS or filename in TEXT_EXTENSIONS


def file_tree(project_path: str) -> str:
    """
    Return a compact file-tree string for the project.
    Example output:
        src/
          main.py
          utils.py
        tests/
          test_main.py
    """
    lines: list[str] = []

    for root, dirs, files in os.walk(project_path):
        # Skip unwanted dirs in-place so os.walk won't descend into them
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))

        rel_root = os.path.relpath(root, project_path)
        depth = 0 if rel_root == "." else rel_root.count(os.sep) + 1
        indent = "  " * depth

        if rel_root != ".":
            lines.append(f"{indent}{os.path.basename(root)}/")

        file_indent = "  " * (depth + 1)
        for f in sorted(files):
            if not f.endswith(".bak"):
                lines.append(f"{file_indent}{f}")

    return "\n".join(lines) if lines else "(empty project)"


def read_project_files(project_path: str) -> str:
    """
    Read text files from the project and return them formatted as:

        FILE: path/relative/to/project
        <content>
        ---

    Files over MAX_FILE_BYTES get a size notice instead of their content.
    Total output is capped at MAX_TOTAL_CONTEXT_BYTES.
    """
    chunks: list[str] = []
    total = 0

    for root, dirs, files in os.walk(project_path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))

        for filename in sorted(files):
            if filename.endswith(".bak"):
                continue
            if not _is_text_file(filename):
                continue

            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, project_path)

            try:
                size = os.path.getsize(full_path)
            except OSError:
                continue

            if size > MAX_FILE_BYTES:
                chunk = f"FILE: {rel_path}\n(file too large to include: {size} bytes)\n---\n"
            else:
                try:
                    with open(full_path, "r", errors="replace") as fh:
                        content = fh.read()
                    chunk = f"FILE: {rel_path}\n{content}\n---\n"
                except OSError as e:
                    chunk = f"FILE: {rel_path}\n(could not read: {e})\n---\n"

            if total + len(chunk) > MAX_TOTAL_CONTEXT_BYTES:
                chunks.append("(context limit reached — remaining files omitted)\n")
                break
            chunks.append(chunk)
            total += len(chunk)

    return "\n".join(chunks) if chunks else "(no readable files found)"


def build_context(project_path: str) -> str:
    """
    Build the full project context block injected into every user message.
    """
    tree = file_tree(project_path)
    files = read_project_files(project_path)

    return (
        f"## Project: {os.path.basename(project_path)}\n"
        f"### File Tree\n{tree}\n\n"
        f"### File Contents\n{files}"
    )
