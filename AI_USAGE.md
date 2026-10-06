# AI Usage Disclosure

## Tool used
ChatGPT.

## How it was used
- Planned the multi-source scraping pipeline and common record schema.
- Assisted with Requests + BeautifulSoup pagination and parsing code.
- Assisted with cleaning, validation, duplicate detection, logging, tests, and documentation.
- Assisted with troubleshooting the local network limitation during verification.

## Representative prompts
- "Complete this Python web scraping assignment step by step."
- "Build separate Books to Scrape and Quotes to Scrape scrapers with pagination."
- "Add cleaning, validation, deduplication, logging, tests, README and AI_USAGE.md."

## AI-assisted parts
The project structure, scraper templates, processing functions, tests, and documentation were AI-assisted.

## Review and verification
The implementation was reviewed by running the three included unit tests; all 3 passed. The public source pages and their next-page pagination were also checked through web access. The local preparation environment could not resolve the two sites through Python requests, so the included CSV/JSON are clearly labeled as a verified two-page sample and are not represented as a successful full live scrape.

## Important limitation
The candidate should run `python main.py` on a normal internet-connected machine before submission. That run should replace the sample output with the live full dataset and produce a fresh execution log.
