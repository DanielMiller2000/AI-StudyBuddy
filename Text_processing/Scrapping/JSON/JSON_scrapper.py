import json
import logging

def scrape_json(file_path, text_fields=None):
    """
    Extracts text content from specified fields in a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        text_fields (list): List of field names to extract text from. If None, extracts all string values.
        
    Returns:
        dict: Contains 'text' (combined text content) and 'metadata' (structure info)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        def extract_text(obj, fields=None):
            text = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if fields is None or key in fields:
                        if isinstance(value, str):
                            text.append(value)
                        elif isinstance(value, (dict, list)):
                            text.extend(extract_text(value, fields))
            elif isinstance(obj, list):
                for item in obj:
                    text.extend(extract_text(item, fields))
            return text
        
        extracted_text = extract_text(data, text_fields)
        
        return {
            'text': ' '.join(extracted_text),
            'metadata': {
                'file_path': file_path,
                'text_fields': text_fields
            }
        }
    except Exception as e:
        logging.error(f"Error processing JSON {file_path}: {str(e)}")
        return None