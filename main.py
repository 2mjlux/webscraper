import sys
import asyncio
from crawl import crawl_site_async


async def main():
    print("Hello from the async webscraper!")

    if len(sys.argv) != 4:
        print("webscraper requires url, maximum concurrency and maximum pages")
        sys.exit(1)
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print(f"starting crawl of: {sys.argv[1]}")
    page_data = await crawl_site_async(sys.argv[1], max_concurrency, max_pages)
    for page in page_data.values():
        if page:
            print(f"URL: {page['url']}, heading: {page['heading']}")
    print(f"Number of URLs crawled: {len(page_data)}")


if __name__ == "__main__":
    asyncio.run(main())
