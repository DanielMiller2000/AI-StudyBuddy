# main.py
import logging
from URL_scrapper import scrape_url
logging.basicConfig(level=logging.INFO)

class TextScraper:
    """Main class to handle different types of text scraping"""
    
    def __init__(self):
        self.supported_types = ['url', 'pdf', 'json', 'txt']
    
    def scrape(self, source, source_type, **kwargs):
        """
        Scrapes text from the given source based on its type.
        
        Args:
            source (str): URL or file path
            source_type (str): Type of source ('url', 'pdf', 'json', 'txt')
            **kwargs: Additional arguments for specific scrapers
            
        Returns:
            dict: Contains scraped text and metadata
        """
        if source_type not in self.supported_types:
            raise ValueError(f"Unsupported source type. Must be one of {self.supported_types}")
            
        if source_type == 'url':
            return scrape_url(source)
        elif source_type == 'pdf':
            return scrape_pdf(source)
        elif source_type == 'json':
            text_fields = kwargs.get('text_fields')
            return scrape_json(source, text_fields)
        elif source_type == 'txt':
            return scrape_txt(source)