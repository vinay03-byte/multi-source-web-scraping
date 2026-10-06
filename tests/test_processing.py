import unittest
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import deduplicate_records

class ProcessingTests(unittest.TestCase):
    def sample(self, title="Example Book"):
        return {
            "source": "Books to Scrape",
            "source_url": "https://books.toscrape.com/catalogue/example_1/index.html",
            "name_or_title": title,
            "category": "",
            "price": "£12.50",
            "rating": "4",
            "author": "",
            "tags": "",
            "description": "",
            "availability": "In stock",
            "scraped_at": "2026-10-06T00:00:00+00:00",
        }

    def test_clean_price_and_whitespace(self):
        row = clean_record(self.sample("  Example   Book "))
        self.assertEqual(row["name_or_title"], "Example Book")
        self.assertEqual(row["price"], "12.50")

    def test_valid_record(self):
        self.assertTrue(validate_record(clean_record(self.sample()))[0])

    def test_deduplication_case_and_whitespace(self):
        a = clean_record(self.sample("Example Book"))
        b = clean_record(self.sample(" EXAMPLE   BOOK "))
        unique, duplicate_count = deduplicate_records([a, b])
        self.assertEqual(len(unique), 1)
        self.assertEqual(duplicate_count, 1)

if __name__ == "__main__":
    unittest.main()
