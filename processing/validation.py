from urllib.parse import urlparse

KNOWN_SOURCES = {"Books to Scrape", "Quotes to Scrape"}

def validate_record(record: dict):
    if record.get("source") not in KNOWN_SOURCES:
        return False, "Unknown or missing source"
    if not record.get("name_or_title", "").strip():
        return False, "Missing title/quote text"
    parsed = urlparse(record.get("source_url", ""))
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False, "Missing or invalid source URL"
    price = record.get("price", "")
    if price:
        try:
            if float(price) < 0:
                return False, "Price cannot be negative"
        except ValueError:
            return False, "Price is not numeric"
    rating = record.get("rating", "")
    if rating:
        try:
            if not 1 <= int(rating) <= 5:
                return False, "Rating must be between 1 and 5"
        except ValueError:
            return False, "Rating is not an integer"
    return True, "OK"
