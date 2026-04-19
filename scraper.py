"""
Product Scraper — extracts book catalog data from books.toscrape.com
and exports it to CSV.

Usage:
    python scraper.py                         # scrape everything
    python scraper.py --max-pages 5           # limit pages
    python scraper.py --output my_books.csv   # custom output file
"""

import argparse
import csv
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
CATALOG_URL = BASE_URL + "catalogue/page-{page}.html"
DEFAULT_OUTPUT = "books.csv"
REQUEST_DELAY = 0.5  # seconds between requests, polite scraping


# Rating words on the site (e.g., "star-rating Three") map to integers
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def fetch_page(url: str, timeout: int = 10) -> BeautifulSoup | None:
    """Fetch a single URL and return a parsed BeautifulSoup object.
    
    Returns None on 404 (end of pagination) or other request errors.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 404:
            return None  # end of pagination, silent
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"  ! Request failed for {url}: {e}", file=sys.stderr)
        return None


def parse_book(article, base_url: str) -> dict:
    """Extract book details from a single <article> element."""
    # Title + URL
    title_elem = article.h3.a
    title = title_elem["title"]
    rel_url = title_elem["href"]
    product_url = base_url + "catalogue/" + rel_url.replace("../", "")

    # Price (strip currency character, keep float)
    price_text = article.find("p", class_="price_color").text
    price = float(price_text.replace("Â", "").replace("£", "").strip())

    # Availability
    availability = article.find("p", class_="instock availability").text.strip()

    # Rating ("star-rating Three" -> 3)
    rating_classes = article.find("p", class_="star-rating")["class"]
    rating_word = [c for c in rating_classes if c != "star-rating"][0]
    rating = RATING_MAP.get(rating_word, 0)

    return {
        "title": title,
        "price_gbp": price,
        "rating": rating,
        "availability": availability,
        "product_url": product_url,
    }


def scrape_catalog(max_pages: int | None = None) -> list[dict]:
    """Scrape all pages of the catalog. Returns list of book dicts."""
    all_books = []
    page = 1

    while True:
        if max_pages is not None and page > max_pages:
            break

        url = CATALOG_URL.format(page=page)
        print(f"Scraping page {page}...")
        soup = fetch_page(url)

        if soup is None:
            print(f"Reached end of catalog after {page - 1} pages.")
            break

        articles = soup.find_all("article", class_="product_pod")
        if not articles:
            print(f"  No more books found. Scraped {page - 1} pages total.")
            break

        for article in articles:
            try:
                book = parse_book(article, BASE_URL)
                all_books.append(book)
            except (AttributeError, KeyError, ValueError) as e:
                print(f"  ! Skipped a book due to parse error: {e}",
                      file=sys.stderr)
                continue

        page += 1
        time.sleep(REQUEST_DELAY)  # polite delay between requests

    return all_books


def write_csv(books: list[dict], output_path: str) -> None:
    """Write the scraped books to a CSV file."""
    if not books:
        print("No books to write.")
        return

    fieldnames = ["title", "price_gbp", "rating", "availability", "product_url"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    print(f"\nWrote {len(books)} books to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape book catalog from books.toscrape.com"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum number of pages to scrape (default: all)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV file name (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    books = scrape_catalog(max_pages=args.max_pages)
    write_csv(books, args.output)


if __name__ == "__main__":
    main()