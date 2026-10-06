from __future__ import annotations

import csv
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import deduplicate_records

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
LOGS = ROOT / "logs"
DATASET_FIELDS = [
    "source", "source_url", "name_or_title", "category", "price", "rating",
    "author", "tags", "description", "availability", "scraped_at"
]

def setup_logging():
    LOGS.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOGS / "execution.log", encoding="utf-8")
        ],
    )

def write_csv(path: Path, records: list[dict]):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=DATASET_FIELDS)
        writer.writeheader()
        writer.writerows(records)

def main():
    setup_logging()
    started = time.time()
    OUTPUT.mkdir(exist_ok=True)

    logging.info("Starting multi-source scraping pipeline")
    books = scrape_books()
    quotes = scrape_quotes()
    collected = books + quotes
    logging.info("Collected %s records total", len(collected))

    cleaned = [clean_record(row) for row in collected]
    valid, rejected = [], []
    for row in cleaned:
        ok, reason = validate_record(row)
        if ok:
            valid.append(row)
        else:
            rejected.append({"source": row.get("source"), "source_url": row.get("source_url"), "reason": reason})
            logging.warning("Rejected record: %s", reason)

    unique, duplicate_count = deduplicate_records(valid)
    write_csv(OUTPUT / "final_dataset.csv", unique)

    per_source = {}
    for source in ("Books to Scrape", "Quotes to Scrape"):
        per_source[source] = {
            "collected": sum(r.get("source") == source for r in collected),
            "after_cleaning": sum(r.get("source") == source for r in cleaned),
            "valid_before_deduplication": sum(r.get("source") == source for r in valid),
            "final_records": sum(r.get("source") == source for r in unique),
        }

    report = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_seconds": round(time.time() - started, 2),
        "records_collected": len(collected),
        "records_after_cleaning": len(cleaned),
        "records_rejected": len(rejected),
        "duplicates_detected_and_removed": duplicate_count,
        "final_record_count": len(unique),
        "per_source": per_source,
        "rejection_samples": rejected[:50],
        "notes": [
            "Blank fields mean the source does not provide that field in the listing being scraped.",
            "Duplicate matching uses source plus normalized title/quote and source URL."
        ]
    }
    (OUTPUT / "summary_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logging.info("Finished. Final records: %s; duplicates removed: %s", len(unique), duplicate_count)
    logging.info("Dataset: %s", OUTPUT / "final_dataset.csv")
    logging.info("Summary: %s", OUTPUT / "summary_report.json")

if __name__ == "__main__":
    main()
