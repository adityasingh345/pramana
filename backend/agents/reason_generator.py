from tools.ollama_client import run_ollama

def generate_reason(verdict, signals):
    prompt = f"""
You are explaining why a news item was marked as {verdict}.
Base explanation ONLY on the signals below.
Be neutral and factual.

Signals:
{signals}
"""
    return run_ollama(prompt)
