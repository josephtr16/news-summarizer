import requests
from bs4 import BeautifulSoup

def scrape_article(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove nav, ads, scripts
    for tag in soup(["script","style","nav","footer","aside"]):
        tag.decompose()

    # Get paragraphs
    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text() for p in paragraphs)
    return text.strip()