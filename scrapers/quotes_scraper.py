import logging
import time
from datetime import datetime, timezone
from urllib.parse import urljoin

from .common import get_soup

START_URL = "https://quotes.toscrape.com/"

def scrape_quotes():
    records = []
    next_url = START_URL
    visited = set()

    while next_url and next_url not in visited:
        visited.add(next_url)
        soup = get_soup(next_url)
        if soup is None:
            logging.error("Skipping failed quotes page: %s", next_url)
            break

        scraped_at = datetime.now(timezone.utc).isoformat()
        for quote in soup.select("div.quote"):
            text_node = quote.select_one("span.text")
            author_node = quote.select_one("small.author")
            tag_nodes = quote.select("div.tags a.tag")
            quote_text = text_node.get_text(" ", strip=True) if text_node else ""
            author = author_node.get_text(" ", strip=True) if author_node else ""
            tags = ", ".join(tag.get_text(" ", strip=True) for tag in tag_nodes)
            # A quote's page URL is the page on which it was found.
            records.append({
                "source": "Quotes to Scrape",
                "source_url": next_url,
                "name_or_title": quote_text,
                "category": "",
                "price": "",
                "rating": "",
                "author": author,
                "tags": tags,
                "description": "",
                "availability": "",
                "scraped_at": scraped_at,
            })

        next_link = soup.select_one("li.next a")
        next_url = urljoin(next_url, next_link.get("href", "")) if next_link else None
        logging.info("Quotes page processed (records so far: %s)", len(records))
        time.sleep(0.2)

    return records
