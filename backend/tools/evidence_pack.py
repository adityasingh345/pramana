from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generate_evidence_pdf(evidence: dict) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 40

    def draw(text):
        nonlocal y
        pdf.drawString(40, y, text)
        y -= 18
        if y < 40:
            pdf.showPage()
            y = height - 40

    pdf.setFont("Helvetica-Bold", 16)
    draw("EVIDENCE PACK – MISINFORMATION ANALYSIS")

    pdf.setFont("Helvetica", 11)
    draw(f"Case ID: {evidence['case_id']}")
    draw(f"Generated At: {evidence['generated_at']}")
    draw("")

    pdf.setFont("Helvetica-Bold", 12)
    draw("CONTENT SNAPSHOT")
    pdf.setFont("Helvetica", 11)
    draw(evidence["content_snapshot"][:500])
    draw("")

    pdf.setFont("Helvetica-Bold", 12)
    draw("CLAIMS ANALYZED")
    pdf.setFont("Helvetica", 11)
    for claim in evidence["claims_analyzed"]:
        draw(f"- {claim.get('description', 'N/A')} ({claim.get('signal')})")

    draw("")
    pdf.setFont("Helvetica-Bold", 12)
    draw("FINAL VERDICT")
    pdf.setFont("Helvetica", 11)
    draw(evidence["final_verdict"])

    draw("")
    pdf.setFont("Helvetica-Bold", 12)
    draw("ANALYSIS REASON")
    pdf.setFont("Helvetica", 11)
    draw(evidence["analysis_reason"][:500])

    draw("")
    pdf.setFont("Helvetica-Bold", 12)
    draw("LEGAL NOTE")
    pdf.setFont("Helvetica", 10)
    draw(evidence["legal_note"])

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
