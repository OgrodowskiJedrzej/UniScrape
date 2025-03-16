"""
PDF Module

This module contains all functions to work with PDFs.
"""
import logging
import pymupdf
from pdf2image import convert_from_path
import easyocr
import numpy as np

from config_manager import ConfigManager
from process_text import clean_PDF, process_pdf_metadata

logger_tool = logging.getLogger('UniScrape_tools')


class Pdf:
    def __init__(self, config_manager: ConfigManager):
        self.config: ConfigManager = config_manager
        self.logger_tool = self.config.logger_tool
        self.logger_print = self.config.logger_print
        self.ocr_reader = easyocr.Reader(['pl', 'en'])

    def _get_text_from_pdf(self, path: str) -> str:
        doc = pymupdf.open(path)
        text = "\n".join(page.get_text() for page in doc)

        if text.strip():
            return text

        self.logger_tool.warning(f"Using OCR for {path}...")
        return self._extract_text_with_ocr(path)

    def _extract_text_with_ocr(self, path: str) -> str:
        try:
            images = convert_from_path(path, dpi=300)
            extracted_text = []

            for i, img in enumerate(images):
                text = self.ocr_reader.readtext(np.array(img), detail=0)
                extracted_text.append(" ".join(text))

            return "\n".join(extracted_text)

        except Exception as e:
            self.logger_tool.error(f"Error for OCR, PDF {path}: {str(e)}")
            return ""
