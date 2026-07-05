"""
Response parser.

Extracts structured file actions (WRITE, DELETE) from the AI's reply
so they can be executed by the file system module.
"""

import re
from dataclasses import dataclass
from typing import List, Literal, Optional, Union


@dataclass
class WriteAction:
    kind: Literal["write"] = "write"
    path: str = ""
    content: str = ""


@dataclass
class DeleteAction:
    kind: Literal["delete"] = "delete"
    path: str = ""


Action = Union[WriteAction, DeleteAction]


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches:  <<<FILE: some/path.py\n<content>\n>>>
_FILE_BLOCK = re.compile(
    r"<<<FILE:\s*(.+?)\n(.*?)>>>",
    re.DOTALL,
)

# Matches:  <<<DELETE: some/path.py>>>
_DELETE_BLOCK = re.compile(
    r"<<<DELETE:\s*(.+?)>>>",
    re.DOTALL,
)

# PLAN block — we surface this to the user before applying actions
_PLAN_BLOCK = re.compile(
    r"PLAN:\s*\n((?:[ \t]+(?:WRITE|EDIT|DELETE)\s+\S.*\n?)+)",
    re.IGNORECASE,
)


def extract_plan(text: str) -> Optional[str]:
    """
    Return the raw PLAN: block text if present, else None.
    """
    match = _PLAN_BLOCK.search(text)
    return match.group(0).strip() if match else None


def extract_actions(text: str) -> List[Action]:
    """
    Parse FILE and DELETE blocks from the AI response.

    Returns a list of WriteAction / DeleteAction objects in document order.
    """
    actions: List[Action] = []
    positions: List[tuple] = []

    for m in _FILE_BLOCK.finditer(text):
        path = m.group(1).strip()
        content = m.group(2)
        # Strip exactly one leading newline that the model often adds
        content = content.lstrip("\n")
        positions.append((m.start(), WriteAction(path=path, content=content)))

    for m in _DELETE_BLOCK.finditer(text):
        path = m.group(1).strip()
        positions.append((m.start(), DeleteAction(path=path)))

    # Return in document order
    positions.sort(key=lambda x: x[0])
    actions = [a for _, a in positions]

    return actions


def has_actions(text: str) -> bool:
    """Return True if the response contains any file actions."""
    return bool(_FILE_BLOCK.search(text) or _DELETE_BLOCK.search(text))
