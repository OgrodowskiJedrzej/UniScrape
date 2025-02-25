from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


def clean_HTML(text: str) -> str:
    soup = BeautifulSoup(text, "lxml")

    for tag in soup(["script", "style", "nav", "aside", "footer", "form", "noscript", "iframe", "a"]):
        tag.extract()

    main_content = soup.find("article") or soup.find("main") or soup.body

    text = main_content.get_text(
        separator=" ", strip=True) if main_content else soup.get_text(separator=" ", strip=True)

    text = re.sub(r"\s+", " ", text)

    return text


def extract_title_from_url(url: str) -> str:
    title = re.sub(r"[^\w\-]", "_", urlparse(url).path) or "index"
    return title
