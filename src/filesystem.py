"""
Safe file I/O operations for the assistant.

All paths are resolved relative to the active project root.
A single .bak backup is created before overwriting any existing file.
"""

import os
import shutil


class FileSystemError(Exception):
    """Raised when a file operation fails."""


def _resolve(project_path: str, relative_path: str) -> str:
    """
    Resolve a relative path inside the project root.
    Raises FileSystemError if the result escapes the project root
    (path traversal protection).
    """
    # Normalise and absolutise
    project_abs = os.path.realpath(project_path)
    target = os.path.realpath(os.path.join(project_abs, relative_path))

    if not target.startswith(project_abs + os.sep) and target != project_abs:
        raise FileSystemError(
            f"Path traversal detected: '{relative_path}' resolves outside project root."
        )
    return target


def write_file(project_path: str, relative_path: str, content: str) -> str:
    """
    Write content to relative_path inside project_path.

    - Creates parent directories as needed.
    - Makes a .bak backup if the file already exists (only one level).

    Returns the absolute path that was written.
    """
    target = _resolve(project_path, relative_path)
    parent = os.path.dirname(target)

    os.makedirs(parent, exist_ok=True)

    # One-shot backup
    if os.path.exists(target):
        backup = target + ".bak"
        shutil.copy2(target, backup)

    with open(target, "w", encoding="utf-8") as fh:
        fh.write(content)

    return target


def delete_file(project_path: str, relative_path: str) -> str:
    """
    Delete relative_path inside project_path.

    Returns the absolute path that was deleted.
    Raises FileSystemError if the file does not exist.
    """
    target = _resolve(project_path, relative_path)

    if not os.path.exists(target):
        raise FileSystemError(f"Cannot delete '{relative_path}': file not found.")

    os.remove(target)
    return target


def read_file(project_path: str, relative_path: str) -> str:
    """
    Read and return the content of a file inside the project.
    """
    target = _resolve(project_path, relative_path)

    if not os.path.exists(target):
        raise FileSystemError(f"File not found: '{relative_path}'")

    with open(target, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()
