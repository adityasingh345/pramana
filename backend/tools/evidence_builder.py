from datetime import datetime
import uuid

def build_evidence_pack(content, verdict, claims, reason) -> dict:
    return {
        "case_id": f"EV-{uuid.uuid4().hex[:8].upper()}",
        "generated_at": datetime.utcnow().isoformat(),
        "content_snapshot": content,
        "claims_analyzed": claims,
        "final_verdict": verdict,
        "analysis_reason": reason,
        "confidence_level": "High" if verdict == "Fake" else "Medium",
        "legal_note": (
            "This document is AI-assisted and intended for investigative support only. "
            "It does not constitute a legal determination."
        ),
    }
