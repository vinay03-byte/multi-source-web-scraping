import logging
import time
import requests
from bs4 import BeautifulSoup

USER_AGENT = "LearningScraper/1.0 (educational practice project)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

def get_soup(url: str, retries: int = 3):
    """Fetch a public practice page with a timeout and small retry delay."""
    for attempt in range(retries):
        try:
            response = SESSION.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as exc:
            logging.warning("Request failed (%s/%s) for %s: %s", attempt + 1, retries, url, exc)
            if attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
    return None

def text_or_blank(parent, selector: str) -> str:
    node = parent.select_one(selector)
    return node.get_text(" ", strip=True) if node else ""

def absolute_url(base: str, href: str) -> str:
    from urllib.parse import urljoin
    return urljoin(base, href)
