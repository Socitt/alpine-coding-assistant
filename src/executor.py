"""
Action executor.

Takes the list of parsed file actions and applies them to the project,
printing a clear summary of what was done.
"""

import os
from typing import List
from src.filesystem import write_file, delete_file, FileSystemError
from src.parser import Action, WriteAction, DeleteAction


def execute_actions(project_path: str, actions: List[Action]) -> None:
    """
    Apply a list of WriteAction / DeleteAction objects to the project.

    Prints a result line for each action.
    """
    if not actions:
        return

    print()
    print("── Applying changes ──────────────────────")

    for action in actions:
        if isinstance(action, WriteAction):
            _do_write(project_path, action)
        elif isinstance(action, DeleteAction):
            _do_delete(project_path, action)

    print("─────────────────────────────────────────")
    print()


def _do_write(project_path: str, action: WriteAction) -> None:
    existed = os.path.exists(os.path.join(project_path, action.path))
    verb = "EDIT " if existed else "WRITE"
    try:
        write_file(project_path, action.path, action.content)
        print(f"  ✓ {verb}  {action.path}")
    except FileSystemError as e:
        print(f"  ✗ {verb}  {action.path}  ({e})")


def _do_delete(project_path: str, action: DeleteAction) -> None:
    try:
        delete_file(project_path, action.path)
        print(f"  ✓ DELETE  {action.path}")
    except FileSystemError as e:
        print(f"  ✗ DELETE  {action.path}  ({e})")
