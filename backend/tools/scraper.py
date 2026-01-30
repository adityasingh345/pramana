from newspaper import Article

def scrape_url(url: str):
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text,
            "source": url
        }
    except Exception as e:
        return {
            "title": "",
            "text": "",
            "source": url,
            "error": str(e)
        }
