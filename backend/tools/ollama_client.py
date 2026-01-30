import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def run_ollama(prompt: str) -> str:
    payload = {
        "model": "llama3.1:latest",
        "prompt": prompt,
        "stream": False
    }
    res = requests.post(OLLAMA_URL, json=payload)

    if res.status_code != 200:
        raise RuntimeError(f"Ollama error: {res.text}")

    data = res.json()

    if "response" in data:
        return data["response"]

    if "error" in data:
        raise RuntimeError(f"Ollama returned error: {data['error']}")

    return ""