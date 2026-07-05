"""
Project manager.

Lists, selects, and creates project workspaces under PROJECTS_DIR.
"""

import os
from src.config import PROJECTS_DIR


def ensure_projects_dir() -> None:
    """Create the projects root directory if it doesn't exist."""
    os.makedirs(PROJECTS_DIR, exist_ok=True)


def list_projects() -> list[str]:
    """Return sorted list of project folder names."""
    ensure_projects_dir()
    return sorted(
        entry
        for entry in os.listdir(PROJECTS_DIR)
        if os.path.isdir(os.path.join(PROJECTS_DIR, entry))
        and not entry.startswith(".")
    )


def create_project(name: str) -> str:
    """
    Create a new project directory and return its absolute path.
    Raises ValueError if the name is empty or contains path separators.
    """
    name = name.strip()
    if not name:
        raise ValueError("Project name cannot be empty.")
    if os.sep in name or "/" in name:
        raise ValueError(f"Project name must not contain path separators: '{name}'")

    path = os.path.join(PROJECTS_DIR, name)
    os.makedirs(path, exist_ok=True)
    return path


def select_project() -> str | None:
    """
    Interactive project selector.

    Returns the absolute path of the selected (or newly created) project,
    or None if the user cancels.
    """
    projects = list_projects()

    print()
    print("── Projects ─────────────────────────────")

    if not projects:
        print("  (no projects yet)")
    else:
        for i, name in enumerate(projects, 1):
            print(f"  {i})  {name}")

    new_idx = len(projects) + 1
    print(f"  {new_idx})  + New project")
    print("  q)  Quit")
    print("─────────────────────────────────────────")

    raw = input("Select: ").strip()

    if raw.lower() in ("q", "quit", "exit", ""):
        return None

    try:
        choice = int(raw)
    except ValueError:
        print("Invalid choice.")
        return None

    if choice == new_idx:
        name = input("Project name: ").strip()
        try:
            path = create_project(name)
            print(f"Created: {path}")
            return path
        except ValueError as e:
            print(f"Error: {e}")
            return None

    if 1 <= choice <= len(projects):
        return os.path.join(PROJECTS_DIR, projects[choice - 1])

    print("Invalid choice.")
    return None
