# Books to Scrape — scraping pipeline (FlyRank Internship Assignment)
Python lane: Python 3.10+, `requests`, `beautifulsoup4`, `pydantic`, managed with [uv](https://docs.astral.sh/uv/).

## Target classification

- **Target:** https://books.toscrape.com
- **Why this site:** toscrape.com describes it as "A fictional bookstore that desperately wants to be scraped" — a sandbox built for scraping practice (source: https://toscrape.com).
- **Scope:** the first 3 catalogue pages only (60 books),
  plus each of those books' detail pages. Nothing else on the site.
- **robots.txt:** requested once on 2026-09-21 (15:00 GMT) →
  HTTP 404, no robots file found. A missing file is not permission;
  permission comes from the sandbox statement above.
- **Data collected:** title, price, availability, rating, description, product URL, and where/when each page was fetched
- **Why this is appropriate:** Because this website was meant for training purposes

I will not reuse this code on another site without checking its rules and terms first.



## Installation
Install uv (once), then clone:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/Marcian225/FlyRank_PoliteScraper.git
cd FlyRank_PoliteScraper
```

## Run

```bash
uv run src/main.py
```

`uv run` creates the environment and installs dependencies automatically on first use.
Output: `output/books.json`, `output/errors.json`, `output/run-report.json`.
Downloaded pages are cached in `cache/` (not committed), so later runs don't contact the site.

## Record schema

Defined in `src/schema.py` (Pydantic). Every record is validated before it is stored; failures go to `output/errors.json` with the reason.

| Field | Type | Notes |
|---|---|---|
| `title` | string | required, non-empty |
| `product_url` | string | required, `https://`; the record's identity |
| `price_text` | string | raw, as on the page (`"£51.77"`) |
| `price_gbp` | number | parsed from `price_text`, > 0 |
| `availability_text` | string | raw |
| `rating_text` | string | raw (`"One"`–`"Five"`) |
| `description` | string or null | `null` when the page has none |
| `source_page` | string | catalogue page where the link was found |
| `fetched_at` | datetime (UTC) | when the page was downloaded |

## Politeness rules

- User-agent: `FlyRankInternship-A9/1.0 (https://github.com/Marcian225/FlyRank_PoliteScraper)`
- At least 0.5 s between real requests; cached pages cause no request
- 10 s timeout on every request
- One retry after 2 s for timeouts and 5xx only; never for 404 or 403
- Scope fixed to the first 3 catalogue pages (63 pages total)

## Known limitation

The selectors match the site's current HTML. A redesign of the site would mean the scraper no longer works correctly.



## Example run report

```json
{
  "started_at": "2026-09-22T09:51:16Z",
  "duration_seconds": 0.35,
  "catalogue_pages": 3,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0,
  "failed_page_details": []
}
```

## Why no browser

A browser is needed when a page builds its content with JavaScript *after* loading. Here the data is already in the HTML the server sends, so a browser would only add unnecessary steps.

## Ethics

Always use the official API if one is available.

Never bypass logins, paywalls, or blocks. Those are clear signs that access is not allowed (app never retries a 403 response)

Collect only what is needed: 60 books, 6 fields, nothing else.