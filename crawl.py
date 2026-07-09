from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, Tag
import asyncio
import aiohttp


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


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    abs_urls = []
    anchors = soup.find_all("a")
    for anchor in anchors:
        orig_url = anchor.get("href")
        if not orig_url:
            continue
        abs_url = urljoin(base_url, orig_url)
        abs_urls.append(abs_url)
    return abs_urls


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    abs_urls = []
    sources = soup.find_all("img")
    for source in sources:
        orig_url = source.get("src")
        if not orig_url:
            continue
        abs_url = urljoin(base_url, orig_url)
        abs_urls.append(abs_url)
    return abs_urls


def extract_page_data(html, page_url):
    extracted_page_data = {}
    extracted_page_data["url"] = page_url
    extracted_page_data["heading"] = get_heading_from_html(html)
    extracted_page_data["first_paragraph"] = get_first_paragraph_from_html(html)
    extracted_page_data["outgoing_links"] = get_urls_from_html(html, page_url)
    extracted_page_data["image_urls"] = get_images_from_html(html, page_url)
    return extracted_page_data


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.parsed_base_url = urlparse(base_url)
        self.base_domain = self.parsed_base_url.netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
        self.pages_crawled = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.pages_crawled) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return False
            if normalized_url not in self.page_data:
                self.page_data[normalized_url] = {}
                return True
            else:
                return False

    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as r:
                content_type = r.headers.get("Content-Type", "")
                if r.status >= 400:
                    print(f"HTTP error: {r.status}")
                    return None
                if "text/html" not in content_type:
                    print("No text/html content")
                    return None
                return await r.text()
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def crawl_page(self, current_url):
        if self.should_stop:
            return
        try:
            # Register this task in all_tasks so it can be cancelled later if
            # max_pages is reached. Note: the parent that spawned this task (via
            # asyncio.create_task in the loop below) may have already added this
            # exact same Task object to all_tasks. That's intentional and safe:
            # sets automatically ignore duplicate entries, and there's a brief
            # window after a task is created but before it starts running where
            # only the parent's registration would exist. Registering here too
            # closes that gap, guaranteeing this task is tracked as soon as its
            # own code starts executing, even if the parent's registration
            # hadn't happened yet for some reason.
            current_task = asyncio.current_task()
            self.all_tasks.add(current_task)
            if current_url is None:
                current_url = self.base_url
            parsed_current_url = urlparse(current_url)
            if parsed_current_url.netloc != self.base_domain:
                return
            current_url_norm = normalize_url(current_url)
            is_new = await self.add_page_visit(current_url_norm)
            if not is_new:
                return
            async with self.semaphore:
                html = await self.get_html(current_url)
                if html is None:
                    return
                print(f"crawling {current_url}")
                current_url_page_data = extract_page_data(html, current_url)
                async with self.lock:
                    self.page_data[current_url_norm] = current_url_page_data
                    self.pages_crawled += 1
                tasks = []
                for url in current_url_page_data["outgoing_links"]:
                    task = asyncio.create_task(self.crawl_page(url))
                    tasks.append(task)
                    self.all_tasks.add(task)
            await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            self.all_tasks.remove(current_task)

    async def crawl(self):
        task = asyncio.create_task(self.crawl_page(self.base_url))
        try:
            await task
        except asyncio.CancelledError:
            pass
        return self.page_data


async def crawl_site_async(url, max_concurrency, max_pages):
    async with AsyncCrawler(url, max_concurrency, max_pages) as async_crawler:
        return await async_crawler.crawl()
