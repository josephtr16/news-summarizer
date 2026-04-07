import trafilatura


def fetch_article_text(url: str):
    """
    Fetches and extracts the main article text from a URL.
    Uses trafilatura for clean boilerplate-free extraction.
    Returns the article text, or None if extraction fails.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
        )
        return text.strip() if text else None

    except Exception as e:
        print(f"[scraper] Error fetching {url}: {e}")
        return None