from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag


def normalize_url(input_url):
    parsed = urlparse(input_url)
    normalized_url = parsed.netloc + parsed.path.rstrip("/")
    return normalized_url


def get_heading_from_html(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    heading_1 = soup.find("h1")
    if heading_1:
        # no need to re-parse; soup is already the parsed document
        return heading_1.get_text().strip()
    heading_2 = soup.find("h2")
    if heading_2:
        # no need to re-parse; soup is already the parsed document
        return heading_2.get_text().strip()
    else:
        return ""


def get_first_paragraph_from_html(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    main_section = soup.find("main")
    if main_section:
        first_paragraph = main_section.find("p")
        if first_paragraph:
            return first_paragraph.get_text().strip()
    first_paragraph = soup.find("p")
    if first_paragraph:
        return first_paragraph.get_text().strip()
    else:
        return ""
