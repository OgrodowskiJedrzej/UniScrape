from config_manager import ConfigManager
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
import pandas as pd
import os


class Crawler:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger_tool = config_manager.logger_tool
        self.logger_print = config_manager.logger_print
        self.sleep_time = config_manager.sleep_time
        self.maximum_links = config_manager.maximum_links_to_visit
        self.folder = config_manager.url_to_scrape_file_name
        self.file_name = config_manager.url_to_scrape_file_name

    def _normalize_url(self, url: str):
        parsed = urlparse(url)
        return parsed.scheme + "://" + parsed.netloc + parsed.path

    def start_crawler(self, starting_url: str) -> bool:
        visited_urls = set()
        urls_to_visit = [starting_url]

        self.logger_print.info(f"Crawler will start in 5 seconds...")
        time.sleep(5)

        while urls_to_visit and len(visited_urls) < self.maximum_links:
            url = urls_to_visit.pop(0)
            normalized_url = self._normalize_url(url)
            if normalized_url in visited_urls:
                continue

            try:
                response = requests.get(url, timeout=5, headers={
                                        "User-Agent": "Mozilla/5.0"})
                if response.status_code != 200:
                    continue

                visited_urls.add(normalized_url)

                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    normalized_full_url = self._normalize_url(full_url)
                    if normalized_full_url.startswith(starting_url) and normalized_full_url not in visited_urls:
                        urls_to_visit.append(full_url)

                time.sleep(self.sleep_time)
            except Exception as e:
                self.logger_print.error(f"Error when crawling: {e}")

    def save_links_to_file(self, links, folder: str = None, file_name: str = None):
        if file_name is None:
            file_name = self.file_name
        if folder is None:
            folder = self.folder

        path = os.path.join(folder, file_name)

        df = pd.DataFrame(list(links), columns=["url"])
        df.to_csv(path, index=False)
