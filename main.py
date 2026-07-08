import sys
import asyncio
from crawl import crawl_site_async


async def main():
    print("Hello from the async webscraper!")

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    print(f"starting crawl of: {sys.argv[1]}")
    page_data = await crawl_site_async(sys.argv[1])
    for page in page_data.values():
        print(f"URL: {page['url']}, heading: {page['heading']}")
    print(f"Number of URLs crawled: {len(page_data)}")


if __name__ == "__main__":
    asyncio.run(main())
