import sys
from pathlib import Path, PurePosixPath 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from datetime import datetime, timezone

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternship-A9/1.0 (https://github.com/Marcian225/FlyRank_PoliteScraper)"
TIMEOUT_SECONDS = 10
REQUEST_DELAY_SECONDS = 0.5
MAX_PAGES = 3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"


def fetch(url):
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    except requests.RequestException as error:
        print(f"FAILED {url}: {type(error).__name__}")
        return None

    if response.status_code != 200:
        print(f"FAILED {url}: status {response.status_code}")
        return None

    return response.content

def get_page(url, cache_name):
    cache_path = CACHE_DIR / cache_name
    if cache_path.exists():
        page = cache_path.read_bytes()
        print(f"CACHE HIT {cache_name} ({len(page)} bytes)")
        return page

    time.sleep(REQUEST_DELAY_SECONDS)
    page = fetch(url)
    if page is None:
        return None

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(page)
    print(f"FETCH {url} ({len(page)} bytes)")
    return page

def book_cache_name(url):
    slug = PurePosixPath(urlparse(url).path).parent.name
    return f"books/{slug}.html"

def extract_book(page, url):
    soup = BeautifulSoup(page, "html.parser")
    product = soup.select_one("div.product_main")

    rating_tag = product.select_one("p.star-rating")
    rating_classes = [c for c in rating_tag["class"] if c != "star-rating"]


    description_tag = soup.select_one("article.product_page #product_description + p")
    description = description_tag.get_text(strip=True) if description_tag else None
    return {
        "title": product.select_one("h1").get_text(strip=True),
        "product_url": url,
        "price_text": product.select_one("p.price_color").get_text(strip=True),
        "availability_text": product.select_one("p.availability").get_text(strip=True),
        "rating_text": rating_classes[0] if rating_classes else None,
        "description": description,
    }

def fetched_at(cache_name):
    mtime = (CACHE_DIR / cache_name).stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    page_url = START_URL
    catalogue_pages = 0
    book_links = []
    while page_url and catalogue_pages < MAX_PAGES:
        page = get_page(page_url, f"catalogue-page-{catalogue_pages + 1}.html")
        if page is None:
            sys.exit(1)
        catalogue_pages += 1

        soup = BeautifulSoup(page, "html.parser")
        book_links += [(urljoin(page_url, a["href"]), page_url) for a in soup.select("article.product_pod h3 a")]

        next_link = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_link["href"]) if next_link else None

    source_by_url = {}
    for url, source_page in book_links:
        source_by_url.setdefault(url, source_page)  # first sighting wins
    print(f"catalogue_pages={catalogue_pages}, discovered={len(book_links)}, unique_urls={len(source_by_url)}")

    records = []
    for url, source_page in source_by_url.items():
        cache_name = book_cache_name(url)
        page = get_page(url, cache_name)
        if page is None:
            continue
        record = extract_book(page, url)
        record["source_page"] = source_page
        record["fetched_at"] = fetched_at(cache_name)
        records.append(record)

    print(json.dumps(records[0], indent=2, ensure_ascii=False))
    print("last record's source_page:", records[-1]["source_page"])
    print(f"detail_pages={len(records)}")



if __name__ == "__main__":
    main()