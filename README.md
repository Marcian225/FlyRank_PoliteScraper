# Books to Scrape — scraping pipeline

## Target classification

- **Target:** https://books.toscrape.com
- **Why this site:** toscrape.com describes it as "A fictional bookstore that desperately wants to be scraped" — a sandbox built for scraping practice (source: https://toscrape.com).
- **Scope:** the first 3 catalogue pages only 60 books,
  plus each of those books' detail pages. Nothing else on the site.
- **robots.txt:** requested once on 2026-09-21 (15:00 GMT) →
  HTTP 404, no robots file found. A missing file is not permission;
  permission comes from the sandbox statement above.
- **Data collected:** title, price, availability, rating, product URL
- **Why this is appropriate:** Because this website was meant for training purposes

I will not reuse this code on another site without checking its rules and terms first.