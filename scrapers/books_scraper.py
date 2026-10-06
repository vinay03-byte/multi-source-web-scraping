import logging
import time
from datetime import datetime, timezone
from urllib.parse import urljoin

from .common import get_soup

START_URL = "https://books.toscrape.com/"


def get_rating(rating_node):
    """Convert star-rating class into a number from 1 to 5."""
    if not rating_node:
        return ""

    classes = rating_node.get("class", [])
    rating_words = {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5",
    }

    return next(
        (rating_words[class_name] for class_name in classes if class_name in rating_words),
        "",
    )


def scrape_book_details(book_url):
    """Scrape additional information from an individual book page."""

    soup = get_soup(book_url)

    if soup is None:
        logging.warning("Could not fetch book details: %s", book_url)
        return {
            "category": "",
            "description": "",
            "availability": "",
            "price": "",
            "rating": "",
            "tags": "",
        }

    # Price
    price_node = soup.select_one(".price_color")
    price = price_node.get_text(strip=True) if price_node else ""

    # Rating
    rating_node = soup.select_one("p.star-rating")
    rating = get_rating(rating_node)

    # Availability
    availability_node = soup.select_one(".availability")
    availability = (
        availability_node.get_text(" ", strip=True)
        if availability_node
        else ""
    )

    # Category
    category = ""
    breadcrumb_links = soup.select("ul.breadcrumb li a")

    if len(breadcrumb_links) >= 3:
        category = breadcrumb_links[-1].get_text(" ", strip=True)

    # Description
    description = ""
    description_node = soup.select_one("#product_description + p")

    if description_node:
        description = description_node.get_text(" ", strip=True)

    # Tags
    tags = []
    tag_links = soup.select(".table.table-striped a")

    for tag in tag_links:
        tag_text = tag.get_text(" ", strip=True)
        if tag_text:
            tags.append(tag_text)

    return {
        "category": category,
        "description": description,
        "availability": availability,
        "price": price,
        "rating": rating,
        "tags": ", ".join(tags),
    }


def scrape_books():
    records = []
    next_url = START_URL
    visited = set()

    while next_url and next_url not in visited:
        visited.add(next_url)

        soup = get_soup(next_url)

        if soup is None:
            logging.error("Skipping failed books page: %s", next_url)
            break

        cards = soup.select("article.product_pod")

        if not cards:
            logging.warning("No book cards found on %s", next_url)

        scraped_at = datetime.now(timezone.utc).isoformat()

        for card in cards:

            title_node = card.select_one("h3 a")

            if not title_node:
                continue

            title = title_node.get("title", "").strip()

            product_url = urljoin(
                next_url,
                title_node.get("href", "")
            )

            # Get details from individual product page
            details = scrape_book_details(product_url)

            records.append({
                "source": "Books to Scrape",
                "source_url": product_url,
                "name_or_title": title,
                "category": details["category"],
                "price": details["price"],
                "rating": details["rating"],
                "author": "",
                "tags": details["tags"],
                "description": details["description"],
                "availability": details["availability"],
                "scraped_at": scraped_at,
            })

            time.sleep(0.1)

        next_link = soup.select_one("li.next a")

        if next_link:
            next_url = urljoin(
                next_url,
                next_link.get("href", "")
            )
        else:
            next_url = None

        logging.info(
            "Books page processed: %s (records so far: %s)",
            next_url or "last page",
            len(records),
        )

        time.sleep(0.2)

    return records