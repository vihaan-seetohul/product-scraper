# Product Scraper

A Python web scraper that extracts book catalog data from
[books.toscrape.com](https://books.toscrape.com/) and exports it to CSV.

Built as a portfolio demonstration of clean Python web scraping
techniques: pagination handling, structured data extraction, error
recovery, and CLI design.

## Features

- Scrapes the full catalog across all pages (1000+ books)
- Extracts title, price (GBP), star rating, availability, and product URL
- Handles pagination automatically
- Polite scraping with built-in request delay
- Graceful error handling for network issues and malformed data
- CLI arguments for flexibility (limit pages, custom output path)
- Clean CSV output with proper UTF-8 encoding

## Installation

```bash
git clone https://github.com/vihaanseetohul/product-scraper.git
cd product-scraper
pip install -r requirements.txt
```

## Usage

Scrape the full catalog (default):

```bash
python scraper.py
```

Limit to first 5 pages:

```bash
python scraper.py --max-pages 5
```

Custom output file:

```bash
python scraper.py --output my_books.csv
```

## Sample Output

The scraper produces a CSV with the following structure:

| title | price_gbp | rating | availability | product_url |
|---|---|---|---|---|
| A Light in the Attic | 51.77 | 3 | In stock | https://books.toscrape.com/... |
| Tipping the Velvet | 53.74 | 1 | In stock | https://books.toscrape.com/... |
| Soumission | 50.10 | 1 | In stock | https://books.toscrape.com/... |

A full sample output (`sample_output.csv`) is included in this repo.

## Technical Details

- **Parser**: BeautifulSoup with lxml backend for speed
- **HTTP client**: requests with timeout and error handling
- **Output**: UTF-8 CSV using Python's built-in csv module
- **Politeness**: 0.5-second delay between requests

## Adapting for Other Sites

The scraper architecture is modular. To adapt for a different site:

1. Update `BASE_URL` and `CATALOG_URL` constants
2. Modify the `parse_book()` function to match the target site's HTML
   structure
3. Adjust `fieldnames` in `write_csv()` for the new data schema

For custom scraping projects tailored to your specific needs, please
reach out via my freelance profiles.

## License

MIT License — free to use, modify, and learn from.

## Author

Built by Vihaan Seetohul as a portfolio project. Available for freelance
Python development work focused on scraping, automation, and data
analysis.
