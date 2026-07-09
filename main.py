import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report


async def main():
    print("Hello from the async webscraper!")

    if len(sys.argv) != 4:
        print("webscraper requires url, maximum concurrency and maximum pages")
        sys.exit(1)
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print(f"starting crawl of: {sys.argv[1]}")
    page_data = await crawl_site_async(sys.argv[1], max_concurrency, max_pages)
    for key, value in page_data.items():
        if not isinstance(value, dict) or "url" not in value:
            print(f"BAD ENTRY -> key: {key!r}, value: {value!r}")
    write_json_report(page_data)


if __name__ == "__main__":
    asyncio.run(main())
