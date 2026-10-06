# Multi-Source Web Scraping & Data Consolidation

## Overview
A Python project that collects records from Books to Scrape and Quotes to Scrape, standardizes the fields, validates records, removes duplicates, and writes a CSV dataset plus JSON summary.

## Requirements
- Python 3.10 or newer
- Internet connection
- Requests and BeautifulSoup 4

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```
If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

## Run tests
```powershell
python -m unittest discover -s tests -v
```

## Pagination
Each scraper starts at the source homepage and follows the `li.next a` link until there is no next-page link. A visited-URL set prevents loops. Failed pages are logged and the scraper continues where possible.

## Data model
`source`, `source_url`, `name_or_title`, `category`, `price`, `rating`, `author`, `tags`, `description`, `availability`, `scraped_at`.
Blank values are used where a field is not provided by that source's listing page. The books listing does not expose category directly, so category is blank rather than guessed. Quotes use the quote text as `name_or_title`, and the page containing the quote as `source_url`.

## Cleaning
Whitespace is collapsed; book prices are converted to two-decimal numeric strings; ratings are normalized to integers from 1 to 5; URLs are checked for an HTTP(S) scheme and hostname.

## Validation
Records must have a recognized source, non-empty title/quote text, and a valid-looking source URL. Existing prices must be numeric and non-negative; ratings must be integers from 1 to 5.

## Deduplication
Records are compared using source, case-insensitive whitespace-normalized title/quote text, and normalized source URL. The first occurrence is retained and later matching records are removed. Source is part of the key because a book and a quote are different kinds of records.

## Logging and error handling
Requests use a timeout, up to three attempts, and a short delay between retries. HTTP/network errors are logged. A failed page is skipped/stops that source's pagination rather than crashing the other source. Missing HTML elements produce blank values.

## Outputs
- `output/final_dataset.csv`: consolidated records
- `output/summary_report.json`: totals per source, rejected count, duplicates removed, execution duration
- `logs/execution.log`: execution log

## Assumptions and limitations
- Only the two public practice websites specified in the assignment are used.
- No authentication, CAPTCHA, or access controls are bypassed.
- Category and description are blank where not exposed on the listing page.
- Quote source URLs identify the page on which the quote appeared, not a unique detail page.
- The site structure may change; selectors may need updating.
- Scraping results depend on network availability and the sites' current responses.

## AI usage
See `AI_USAGE.md`. Review the code and be ready to explain the design choices before submission.


## Verification note
The source websites and their pagination were verified during preparation. In the sandbox used to prepare this submission, direct Python DNS/network access to the sites was unavailable, so the included output is explicitly a verified two-page sample rather than a claimed full live scrape. On a normal machine with internet access, run `python main.py` to regenerate the live dataset across all available pages. The program itself is the authoritative reproducible scraper.
