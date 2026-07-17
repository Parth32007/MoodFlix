"""
Utility functions for text processing and data conversion.

Provides functions for converting genre/cast/crew JSON strings,
and text preprocessing like stemming.
"""

import ast
from nltk.stem.porter import PorterStemmer

from src.logger import get_logger

logger = get_logger(__name__)

ps = PorterStemmer()


def convert(text):
    """
    Extract names from a JSON-formatted string list of objects.
    
    Args:
        text (str): String representation of list of dicts with 'name' key
                   e.g., "[{'name': 'Genre1'}, {'name': 'Genre2'}]"
        
    Returns:
        list: List of extracted names
        empty list: If parsing fails
        
    Example:
        >>> convert("[{'name': 'Action'}, {'name': 'Drama'}]")
        ['Action', 'Drama']
    """
    try:
        L = []
        parsed = ast.literal_eval(text)
        
        if not isinstance(parsed, list):
            logger.warning(f"Expected list but got {type(parsed)}")
            return []
        
        for item in parsed:
            if isinstance(item, dict) and 'name' in item:
                L.append(item['name'])
        
        return L
        
    except (ValueError, SyntaxError) as e:
        logger.debug(f"Error parsing text in convert(): {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in convert(): {e}")
        return []


def convert_cast(text, limit=3):
    """
    Extract cast member names from a JSON-formatted string, limited to N actors.
    
    Args:
        text (str): String representation of list of cast dicts
        limit (int): Maximum number of cast members to extract (default: 3)
        
    Returns:
        list: List of cast member names (up to limit items)
        empty list: If parsing fails
        
    Example:
        >>> convert_cast("[{'name': 'Actor1'}, {'name': 'Actor2'}, {'name': 'Actor3'}]", 2)
        ['Actor1', 'Actor2']
    """
    try:
        L = []
        counter = 0
        parsed = ast.literal_eval(text)
        
        if not isinstance(parsed, list):
            logger.warning(f"Expected list but got {type(parsed)}")
            return []
        
        for item in parsed:
            if counter >= limit:
                break
            
            if isinstance(item, dict) and 'name' in item:
                L.append(item['name'])
                counter += 1
        
        return L
        
    except (ValueError, SyntaxError) as e:
        logger.debug(f"Error parsing cast in convert_cast(): {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in convert_cast(): {e}")
        return []


def fetch_director(text):
    """
    Extract director names from a JSON-formatted crew string.
    
    Looks for crew members with job='Director' and extracts their names.
    
    Args:
        text (str): String representation of crew list with 'name' and 'job' keys
                   e.g., "[{'name': 'Director Name', 'job': 'Director'}, ...]"
        
    Returns:
        list: List of director names
        empty list: If parsing fails or no directors found
        
    Example:
        >>> fetch_director("[{'name': 'Christopher Nolan', 'job': 'Director'}]")
        ['Christopher Nolan']
    """
    try:
        L = []
        parsed = ast.literal_eval(text)
        
        if not isinstance(parsed, list):
            logger.warning(f"Expected list but got {type(parsed)}")
            return []
        
        for item in parsed:
            if isinstance(item, dict):
                if item.get('job') == 'Director' and 'name' in item:
                    L.append(item['name'])
        
        return L
        
    except (ValueError, SyntaxError) as e:
        logger.debug(f"Error parsing crew in fetch_director(): {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in fetch_director(): {e}")
        return []


def stem(text):
    """
    Apply Porter stemming to each word in a text string.
    
    Reduces words to their root form (e.g., 'running' -> 'run').
    Useful for text normalization before similarity comparisons.
    
    Args:
        text (str): Text to stem, words separated by spaces
        
    Returns:
        str: Stemmed text with stems separated by spaces
        empty string: If input is invalid
        
    Example:
        >>> stem("running quickly running")
        'run quickli run'
    """
    if not isinstance(text, str):
        logger.warning(f"Expected string but got {type(text)}")
        return ""
    
    try:
        words = []
        for word in text.split():
            words.append(ps.stem(word))
        
        return " ".join(words)
        
    except Exception as e:
        logger.exception(f"Error in stem(): {e}")
        return ""