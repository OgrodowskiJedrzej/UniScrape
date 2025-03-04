from config_manager import ConfigManager
from crawler import Crawler
from scraper import Scraper

import pandas as pd

config = ConfigManager(
    print_to_console=True
)

url = "https://amu.edu.pl/uniwersytet/o-uam"

crawler = Crawler(config_manager=config)
# Start crawler
if crawler.start_crawler(url):
    # Configure scraper
    scraper = Scraper(config_manager=config)
    docs = scraper.start_scraper(crawler.get_urls_to_scrap())
