import sys
from pathlib import Path
import requests

URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternship-A9/1.0 (https://github.com/Marcian225/FlyRank_PoliteScraper)"
TIMEOUT_SECONDS = 10

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"


def fetch(url):
    """Return the page as bytes, or None if the fetch failed."""
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    except requests.RequestException as error:
        print(f"FAILED {url}: {type(error).__name__}")
        return None

    if response.status_code != 200:
        print(f"FAILED {url}: status {response.status_code}")
        return None

    return response.content


def main():
    cache_path = CACHE_DIR / "catalogue-page-1.html"

    if cache_path.exists():
        page = cache_path.read_bytes()
        print(f"CACHE HIT {cache_path.name} ({len(page)} bytes)")
        return

    page = fetch(URL)
    if page is None:
        sys.exit(1)

    CACHE_DIR.mkdir(exist_ok=True)
    cache_path.write_bytes(page)
    print(f"FETCH {URL} ({len(page)} bytes)")


if __name__ == "__main__":
    main()