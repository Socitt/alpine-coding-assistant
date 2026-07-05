"""
Conversation history manager.

Keeps a rolling window of messages so the AI has context without blowing
the token limit on a constrained device.
"""

from typing import Dict, List
from src.config import MAX_TOTAL_CONTEXT_BYTES

# Rough chars-per-token estimate. Conservative to avoid overruns.
_CHARS_PER_TOKEN = 4
_MAX_HISTORY_TOKENS = 6_000
_MAX_HISTORY_CHARS = _MAX_HISTORY_TOKENS * _CHARS_PER_TOKEN


class History:
    def __init__(self) -> None:
        self._messages: List[Dict] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})
        self._trim()

    def add_assistant(self, content: str) -> None:
        self._messages.append({"role": "assistant", "content": content})
        self._trim()

    def get(self) -> List[Dict]:
        """Return a copy of the current history."""
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()

    def __len__(self) -> int:
        return len(self._messages)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _trim(self) -> None:
        """
        Drop oldest messages (in pairs where possible) until total
        character count is within budget. Always keeps at least the
        last user message.
        """
        while len(self._messages) > 1 and self._total_chars() > _MAX_HISTORY_CHARS:
            # Remove oldest message; if it's a user msg try to also remove
            # the immediately following assistant reply so history stays balanced.
            self._messages.pop(0)

    def _total_chars(self) -> int:
        return sum(len(m["content"]) for m in self._messages)
