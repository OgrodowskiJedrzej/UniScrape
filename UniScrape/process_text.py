from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from typing import Tuple


def clean_HTML(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "nav", "aside", "footer", "form", "noscript", "iframe", "a"]):
        tag.extract()

    main_content = soup.find("article") or soup.find("main") or soup.body

    html = main_content.get_text(
        separator=" ", strip=True) if main_content else soup.get_text(separator=" ", strip=True)

    html = re.sub(r"\s+", " ", html)

    return html


def process_metadata(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("meta", property="og:title")
    title_content = title["content"] if title else "Title not found"

    return title_content
