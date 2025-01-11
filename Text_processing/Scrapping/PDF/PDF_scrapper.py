import PyPDF2
import io
import logging

def scrape_pdf(file_path):
    """
    Extracts text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        dict: Contains 'text' (full content) and 'metadata' (number of pages, etc.)
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            
            return {
                'text': ' '.join(text),
                'metadata': {
                    'num_pages': len(reader.pages),
                    'file_path': file_path
                }
            }
    except Exception as e:
        logging.error(f"Error processing PDF {file_path}: {str(e)}")
        return None