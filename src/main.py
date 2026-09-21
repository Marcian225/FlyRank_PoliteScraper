import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

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

    CACHE_DIR.mkdir(exist_ok=True)
    cache_path.write_bytes(page)
    print(f"FETCH {url} ({len(page)} bytes)")
    return page

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
        book_links += [urljoin(page_url, a["href"]) for a in soup.select("article.product_pod h3 a")]

        next_link = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_link["href"]) if next_link else None

    unique_urls = list(dict.fromkeys(book_links))
    print(f"catalogue_pages={catalogue_pages}, discovered={len(book_links)}, unique_urls={len(unique_urls)}")

if __name__ == "__main__":
    main()