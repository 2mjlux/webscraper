import unittest
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url_https_no_trailing(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_https_with_trailing(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_no_trailing(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_with_trailing(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1(self):
        input_body = "<html><body><h1>Test Title h1</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title h1"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2(self):
        input_body = "<html><body><h2>Test Title h2</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title h2"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_none(self):
        input_body = "<html><body>Test Title none</body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <p>Main paragraph.</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_no_paragrap(self):
        input_body = """<html><body>
            <main>
                <a href=www.boot.dev>This is boot.dev.</a>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main_no_paragrap(self):
        input_body = """<html><body>
                <a href=www.boot.dev>This is boot.dev.</a>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                            <a href="https://crawler-test.com">
                                <span>Boot.dev</span>
                            </a>
                        </body></html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                            <a href="/docABC.html">
                                <span>Boot.dev</span>
                            </a>
                        </body></html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/docABC.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_many(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                            <a href="/docABC.html">
                                <span>Boot.dev</span>
                            </a>
                            <a href="/doc123.html">
                                <span>2nd test link</span>
                            </a>
                        </body></html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/docABC.html",
                    "https://crawler-test.com/doc123.html"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                            <img src="https://crawler-test.com/logo.png" alt="Logo">
                        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_many_mixed(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                            <img src="https://crawler-test.com/logo.png" alt="Logo">
                            <img src="/logo2.png" alt="Logo2">
                        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png",
                    "https://crawler-test.com/logo2.png"]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
