import logging
import asyncio
# from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os

from config_manager import ConfigManager

logger_tool = logging.getLogger('UniScrape_tools')


class Scraper:
    def __init__(self, config_manager: ConfigManager):
        self.config: ConfigManager = config_manager
        self.logger_tool = self.config.logger_tool
        self.logger_print = self.config.logger_print

        # TODO: Move this to config
        self.visited_folder = "visited/"
        self.visited_file = "visited_urls.csv"

    def _scrape_text():
        pass

    def start_scraper(self, ulrs_to_scrap: pd.DataFrame, visited_urls: pd.DataFrame):
        """
        Initiates scraper process.
        """
        if ulrs_to_scrap.size > 0:
            try:
                self._scrape_text()
            except Exception as e:
                self.logger_tool.error(f"Error in scraper: {e}")
                self.logger_print.error(f"Error in scraper: {e}")
        else:
            self.logger_tool.info(f"No urls to scrap in: {ulrs_to_scrap}")

    def append_to_visited_urls(self, urls_dataframe: pd.DataFrame, file_name: str = None, folder=None, mode='a'):
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
        self.visited_path = "visited/visited_urls.csv"
        if os.path.exists(self.visited_path):
            self.logger_tool.debug(f"Visited url file already exist!")
        else:
            self.logger_tool.debug(
                f"Visited url file not exist - creating new")
            self.append_to_visited_urls(
                urls_dataframe=urls_dataframe, file_name=file_name, mode='w')
