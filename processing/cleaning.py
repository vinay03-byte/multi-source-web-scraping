from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

def clean_text(value):
    if value is None:
        return ""
    return " ".join(str(value).split()).strip()

def clean_record(record: dict) -> dict:
    cleaned = {key: clean_text(value) for key, value in record.items()}
    # Normalize book prices into numeric strings; leave empty if not a valid number.
    if cleaned.get("price"):
        raw = cleaned["price"].replace("£", "").replace(",", "").strip()
        try:
            cleaned["price"] = f"{Decimal(raw):.2f}"
        except InvalidOperation:
            cleaned["price"] = ""
    if cleaned.get("rating"):
        try:
            rating = int(cleaned["rating"])
            cleaned["rating"] = str(rating) if 1 <= rating <= 5 else ""
        except ValueError:
            cleaned["rating"] = ""
    # A valid-looking URL must have an HTTP(S) scheme and a hostname.
    url = cleaned.get("source_url", "")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        cleaned["source_url"] = ""
    return cleaned
