"""
User favorites management module.
Handles storing and retrieving user's favorite movies.
"""

import json
from pathlib import Path
import threading

from src.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
FAVORITES_FILE = BASE_DIR / "storage" / "favorites.json"

# Thread lock for file operations
_favorites_lock = threading.Lock()


def load_favorites():
    """
    Load favorites list from JSON file.
    
    Returns:
        list: List of favorite movie titles, empty list if file doesn't exist or on error
    """
    try:
        if not FAVORITES_FILE.exists():
            logger.debug(f"Favorites file not found: {FAVORITES_FILE}")
            return []

        with open(FAVORITES_FILE, "r") as f:
            favorites = json.load(f)
            
            if not isinstance(favorites, list):
                logger.warning("Favorites file doesn't contain a list, returning empty list")
                return []
                
            logger.debug(f"Loaded {len(favorites)} favorites")
            return favorites

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in favorites file: {e}")
        return []
    except FileNotFoundError:
        logger.debug("Favorites file not found")
        return []
    except PermissionError as e:
        logger.error(f"Permission denied accessing favorites file: {e}")
        return []
    except Exception as e:
        logger.exception(f"Error loading favorites: {e}")
        return []


def save_favorites(favorites):
    """
    Save favorites list to JSON file.
    
    Args:
        favorites (list): List of favorite movie titles
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not isinstance(favorites, list):
            logger.error("Favorites must be a list")
            return False

        # Ensure storage directory exists
        FAVORITES_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=4)
            logger.debug(f"Saved {len(favorites)} favorites")
            return True

    except PermissionError as e:
        logger.error(f"Permission denied writing to favorites file: {e}")
        return False
    except Exception as e:
        logger.exception(f"Error saving favorites: {e}")
        return False


def add_favorite(movie):
    """
    Add a movie to user's favorites.
    Prevents duplicate entries.
    
    Args:
        movie (str): Movie title to add
        
    Returns:
        bool: True if added successfully, False otherwise
    """
    if not movie or not isinstance(movie, str):
        logger.warning(f"Invalid movie provided: {movie}")
        return False

    movie = movie.strip()
    
    try:
        with _favorites_lock:
            favorites = load_favorites()

            if movie in favorites:
                logger.info(f"Movie already in favorites: {movie}")
                return False

            favorites.append(movie)
            success = save_favorites(favorites)
            
            if success:
                logger.info(f"Added to favorites: {movie}")
            
            return success

    except Exception as e:
        logger.exception(f"Error adding favorite '{movie}': {e}")
        return False


def remove_favorite(movie):
    """
    Remove a movie from user's favorites.
    
    Args:
        movie (str): Movie title to remove
        
    Returns:
        bool: True if removed successfully, False otherwise
    """
    if not movie or not isinstance(movie, str):
        logger.warning(f"Invalid movie provided: {movie}")
        return False

    movie = movie.strip()
    
    try:
        with _favorites_lock:
            favorites = load_favorites()

            if movie not in favorites:
                logger.debug(f"Movie not in favorites: {movie}")
                return False

            favorites.remove(movie)
            success = save_favorites(favorites)
            
            if success:
                logger.info(f"Removed from favorites: {movie}")
            
            return success

    except Exception as e:
        logger.exception(f"Error removing favorite '{movie}': {e}")
        return False


def get_favorites():
    """
    Get list of all user's favorite movies.
    
    Returns:
        list: List of favorite movie titles
    """
    try:
        return load_favorites()
    except Exception as e:
        logger.exception(f"Error retrieving favorites: {e}")
        return []


def clear_favorites():
    """
    Clear all user favorites.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with _favorites_lock:
            success = save_favorites([])
            if success:
                logger.info("Cleared all favorites")
            return success
    except Exception as e:
        logger.exception(f"Error clearing favorites: {e}")
        return False