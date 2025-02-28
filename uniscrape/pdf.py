"""
PDF Module

This module contains all functions to work with PDFs.
"""
import logging
import pymupdf

from config_manager import ConfigManager
from process_text import clean_PDF, process_pdf_metadata

logger_tool = logging.getLogger('UniScrape_tools')


class Pdf:
    def __init__(self, config_manager: ConfigManager):
        self.config: ConfigManager = config_manager
        self.logger_tool = self.config.logger_tool
        self.logger_print = self.config.logger_print

    def _get_text_from_pdf(self, path: str) -> str:
        doc = pymupdf.open(path)
        text = "\n".join(page.get_text()
                         for page in doc)
        return text
