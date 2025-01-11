import logging

def scrape_txt(file_path):
    """
    Extracts text from a plain text file.
    
    Args:
        file_path (str): Path to the text file
        
    Returns:
        dict: Contains 'text' (file content) and 'metadata' (file info)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            
        return {
            'text': text,
            'metadata': {
                'file_path': file_path,
                'file_type': 'txt'
            }
        }
    except Exception as e:
        logging.error(f"Error processing text file {file_path}: {str(e)}")
        return None