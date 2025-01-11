import requests
from bs4 import BeautifulSoup
import logging

def scrape_url(url):
    """
    Scrapes text content from a given URL.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        dict: Contains 'text' (main content), 'title' (page title), and 'metadata' (description, keywords)
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'header', 'footer', 'nav']):
            script.decompose()
            
        # Extract text
        text = ' '.join(soup.stripped_strings)
        
        # Extract metadata
        title = soup.title.string if soup.title else ''
        meta_desc = soup.find('meta', {'name': 'description'})
        description = meta_desc['content'] if meta_desc else ''
        
        return {
            'text': text,
            'title': title,
            'metadata': {
                'description': description,
                'url': url
            }
        }
    except Exception as e:
        logging.error(f"Error scraping URL {url}: {str(e)}")
        return None