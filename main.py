import sys
from crawl import get_html


def main():
    print("Hello from webscraper!")

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    print(f"starting crawl of: {sys.argv[1]}")
    result = get_html(sys.argv[1])
    print(result)


if __name__ == "__main__":
    main()
