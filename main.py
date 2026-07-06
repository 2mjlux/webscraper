import sys
from crawl import crawl_page


def main():
    print("Hello from webscraper!")

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    print(f"starting crawl of: {sys.argv[1]}")
    result = crawl_page(sys.argv[1])
    for page in result.values():
        print(f"URL: {page['url']}, heading: {page['heading']}")
    print(f"Number fo URLs crawled: {len(result.keys())}")


if __name__ == "__main__":
    main()
