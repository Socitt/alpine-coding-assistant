import requests

from config import API_KEY
from config import API_URL
from config import MODEL
from config import SYSTEM_PROMPT


def ask(history):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + history
    }

    r = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=300
    )

    r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"]
