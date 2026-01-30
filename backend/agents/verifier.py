from tools.source_check import search_web
from tools.scraper import scrape_url

def verify_claims(claims, original_text):
    results = []

    for c in claims:
        claim_text = c["claim"]

        urls = search_web(claim_text)
        evidence_found = False

        for url in urls:
            article_text = scrape_url(url)
            if claim_text.lower() in article_text.lower():
                evidence_found = True
                break

        results.append({
            "claim": claim_text,
            "type": c["type"],
            "status": "verified" if evidence_found else "no_evidence_found"
        })

    return results
