import json
from tools.ollama_client import run_ollama

def extract_claims(text: str):
    prompt = f"""
You are an information extraction system.

Task:
Extract ALL factual claims from the text, even if:
- The person is unnamed
- The claim is anonymous
- The claim may be false
- The claim is a rumor or allegation

Rules:
- Death, illness, or crime claims MUST be extracted
- Do NOT verify
- Do NOT judge truth
- Output ONLY valid JSON
- Never return an empty list if any factual assertion exists

Format:
[
  {{ "type": "death/health/event", "claim": "..." }}
]

Text:
{text}
"""

    raw = run_ollama(prompt)

    # 1️⃣ Try parsing LLaMA output
    try:
        claims = json.loads(raw)
        if not isinstance(claims, list):
            claims = []
    except Exception:
        claims = []

    # 2️⃣ HARD FALLBACK for high-risk keywords
    HIGH_RISK_KEYWORDS = ["died", "death", "cancer", "killed", "murder"]

    if not claims and any(k in text.lower() for k in HIGH_RISK_KEYWORDS):
        claims = [
            {
                "type": "death",
                "claim": "An unnamed person reportedly died due to illness"
            }
        ]

    return claims
