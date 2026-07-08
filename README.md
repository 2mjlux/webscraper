# Async Web Scraper

This project is an asynchronous web scraper that crawls pages from a single domain and collects structured page data.

## How it works

1. `main()` starts the program with `asyncio.run(...)`
2. `main()` awaits `crawl_site_async(base_url)`
3. `crawl_site_async` creates an `AsyncCrawler` and uses `async with`
4. Entering `async with` runs `__aenter__`, which opens the HTTP session
5. `crawl()` starts crawling from `self.base_url`
6. `crawl_page()`:
   - skips off-domain URLs
   - normalizes the URL
   - uses `add_page_visit()` to avoid duplicate crawls
   - uses a semaphore to limit concurrent requests
   - fetches HTML
   - extracts page data
   - saves it into shared `self.page_data`
   - creates tasks for linked pages
   - waits for them with `asyncio.gather(...)`
7. Leaving `async with` runs `__aexit__`, which closes the session
8. The final `page_data` dictionary is returned to `main()`

## Key async concepts used

- `await`: pauses until an async operation finishes
- `async with`: manages setup and cleanup for async resources
- `asyncio.Lock`: protects shared state from concurrent access
- `asyncio.Semaphore`: limits how many requests run at once
- `asyncio.create_task()`: starts concurrent crawl tasks
- `asyncio.gather()`: waits for all created tasks to finish

## Shared state

The crawler stores shared crawl results in `self.page_data`.

- Keys: normalized URL strings
- Values: extracted page-data dictionaries

This allows the crawler to:
- avoid visiting the same page twice
- store results for all crawled pages in one place

## Purpose

The goal of the async design is to crawl pages faster than a sequential crawler while still safely managing shared data and limiting request concurrency.
