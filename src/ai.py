"""
Groq API wrapper.
Sends conversation history + system prompt and returns the assistant reply.
"""

import requests

from src.config import API_KEY, API_URL, MODEL, SYSTEM_PROMPT, TIMEOUT


class AIError(Exception):
    """Raised when the Groq API returns an unexpected response."""


def ask(history: list[dict]) -> str:
    """
    Send the full conversation history to Groq and return the assistant reply.

    Args:
        history: List of {"role": "user"|"assistant", "content": str} dicts.

    Returns:
        The assistant's reply as a plain string.

    Raises:
        AIError: On HTTP errors or unexpected response shape.
    """
    if not API_KEY:
        raise AIError(
            "GROQ_API_KEY environment variable is not set.\n"
            "Run:  export GROQ_API_KEY='your_key_here'"
        )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2,   # lower = more deterministic code output
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise AIError("Request timed out. The model may be under load — try again.")
    except requests.exceptions.HTTPError as e:
        body = ""
        try:
            body = response.json().get("error", {}).get("message", response.text)
        except Exception:
            body = response.text
        raise AIError(f"API error {response.status_code}: {body}") from e
    except requests.exceptions.RequestException as e:
        raise AIError(f"Network error: {e}") from e

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise AIError(f"Unexpected API response shape: {response.text}") from e
