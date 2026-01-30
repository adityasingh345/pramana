from agents.claim_extractor import extract_claims
from agents.verifier import verify_claims
from agents.reason_generator import generate_reason
from tools.scraper import scrape_url

def is_valid_url(url: str) -> bool:
    return isinstance(url, str) and url.startswith(("http://", "https://"))


def fact_check_pipeline(input_text: str, url: str = None):
    HIGH_RISK_TYPES = ["death", "health"]

    # 1️⃣ Get text
    if url and is_valid_url(url):
        scraped = scrape_url(url)
        text = scraped.get("text", "")
    else:
        text = input_text or ""

    # 2️⃣ Extract claims
    claims = extract_claims(text)

    # 🚨 HARD FALLBACK: no claims
    if not claims:
        return {
            "verdict": "Unverified",
            "claims": [],
            "reason": (
                "The information could not be verified because it lacks "
                "identifiable claims or credible supporting evidence."
            )
        }

    # 3️⃣ Detect high-risk claims
    high_risk = any(c.get("type") in HIGH_RISK_TYPES for c in claims)

    # 4️⃣ Verify claims
    verification = verify_claims(claims, text)

    # 5️⃣ High-risk + no URL → IMMEDIATE FAKE
    if high_risk and not url:
        return {
            "verdict": "Fake",
            "claims": verification,
            "reason": (
                "This claim involves a reported death or serious illness, "
                "but no confirmation was found from credible or official sources. "
                "Such claims are commonly associated with misinformation."
            )
        }

    # 6️⃣ Evidence-based decision
    fake_signals = [
        v for v in verification
        if v.get("status") == "no_evidence_found"
    ]

    verdict = "Fake" if fake_signals else "Unverified"

    # 7️⃣ Only call LLaMA if signals exist
    if verification:
        reason = generate_reason(verdict, verification)
    else:
        reason = (
            "No sufficient verification signals were available to reach "
            "a definitive conclusion."
        )

    return {
        "verdict": verdict,
        "claims": verification,
        "reason": reason
    }
