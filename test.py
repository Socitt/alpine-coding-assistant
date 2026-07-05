import os
import requests

key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": "Reply with exactly: Hello from Groq!"
        }
    ]
}

r = requests.post(url, headers=headers, json=payload, timeout=60)

print(r.status_code)
print(r.text)
