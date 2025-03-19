from config_manager import ConfigManager
from crawler import Crawler
from scraper import Scraper
from pdf import Pdf

import pandas as pd
import logging
import os

config = ConfigManager(
    print_to_console=True
)

logger_tool = logging.getLogger('UniScrape_tools')

url = "https://amu.edu.pl/uniwersytet/o-uam"


def crawl_and_scrape():
    crawler = Crawler(config_manager=config)
    # Start crawler
    if crawler.start_crawler(url):
        # Configure scraper
        scraper = Scraper(config_manager=config)
        docs = scraper.start_scraper(crawler.get_urls_to_scrap())
        config.logger_tool.info(f"Scraped {docs} documents.")


def scrape_pdfs(folder: str) -> None:
    scraper = Pdf(config_manager=config)
    count = scraper.start_scraper_pdf(folder_path=folder)
    print(f'\n\n {count}')
