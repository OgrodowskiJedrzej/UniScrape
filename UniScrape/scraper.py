import logging
import asyncio
# from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config_manager import ConfigManager

logger_tool = logging.getLogger('UniScrape_tools')


class Scraper:
    def __init__(self, config_manager: ConfigManager):
        self.config: ConfigManager = config_manager
        self.logger_tool = self.config.logger_tool
        self.logger_print = self.config.logger_print
        self.visited_folder = self.config.visited_url_folder
        self.visited_file = self.config.visited_url_file

    def _scrape_text(self, url: str) -> str:
        session = self.create_session(retry_total=1)
        response = session.get(url)
        return response.text

    def start_scraper(self, ulrs_to_scrap: pd.DataFrame, visited_urls: pd.DataFrame):
        """
        Initiates scraper process.
        """
        if not ulrs_to_scrap.empty():
            try:
                # logic, iterate through urls_to_scrap and plug into function
                pass
            except Exception as e:
                self.logger_tool.error(f"Error in scraper: {e}")
                self.logger_print.error(f"Error in scraper: {e}")
        else:
            self.logger_tool.info(f"No urls to scrap in: {ulrs_to_scrap}")

    def create_session(self, retry_total: bool | int = 3, retry_backoff: float = 3.0, verify: bool = False) -> requests.Session:
        session = requests.Session()
        retry = Retry(total=retry_total, backoff_factor=retry_backoff)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.verify = verify
        return session

    # ? Do we need file_name if we assign it globaly?

    def append_to_visited_urls(self, urls_dataframe: pd.DataFrame, file_name: str = None, folder=None, mode='a') -> None:
        if file_name is None:
            file_name = self.visited_file
        if folder is None:
            folder = self.visited_folder

        file_path = os.path.join(folder, file_name)

        try:
            urls_dataframe.to_csv(file_path, sep='\t',
                                  mode=mode, index=False, encoding='utf-8')
            self.logger_tool.info(
                f"Saved {urls_dataframe.shape} to {file_path}")
        except Exception as e:
            self.logger_tool.error(
                f"Error while saving to file: {file_path}: {e}")

    def create_visited_file(self, urls_dataframe: pd.DataFrame, file_name: str) -> None:
        if os.path.exists(os.path.join(self.visited_folder, file_name)):
            self.logger_tool.debug(f"Visited url file already exist!")
        else:
            self.logger_tool.debug(
                f"Visited url file not exist - creating new")
            self.append_to_visited_urls(
                urls_dataframe=urls_dataframe, file_name=file_name, mode='w')
