import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_web(query: str, max_results: int = 5):
    """
    Simple web search using DuckDuckGo HTML
    (No API key required – hackathon safe)
    """
    search_url = "https://duckduckgo.com/html/"
    params = {"q": query}

    res = requests.post(search_url, data=params, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for a in soup.select("a.result__a", limit=max_results):
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)

    return links
