"""
Movie metadata extraction and retrieval module.
"""

import pickle
import ast
from pathlib import Path

from src.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

# Lazy loading: Load metadata on first use, not at import time
_movie_metadata = None


def _load_metadata():
    """
    Lazy load movie metadata from pickle file.
    
    Returns:
        DataFrame: Movie metadata DataFrame, or None if file not found
    """
    global _movie_metadata
    
    if _movie_metadata is not None:
        return _movie_metadata
    
    try:
        metadata_path = MODEL_DIR / "movie_metadata.pkl"
        if not metadata_path.exists():
            logger.error(f"Movie metadata file not found: {metadata_path}")
            return None
            
        with open(metadata_path, "rb") as f:
            _movie_metadata = pickle.load(f)
            logger.info(f"Loaded movie metadata: {len(_movie_metadata)} movies")
            return _movie_metadata
            
    except pickle.PickleError as e:
        logger.error(f"Error loading pickle file: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error loading metadata: {e}")
        return None


def extract_genres(genres):
    """
    Extract genre names from a string representation of genre list.
    
    Args:
        genres (str): String representation of genres list
        
    Returns:
        str: Comma-separated genre names or "Unknown" if parsing fails
    """
    if not isinstance(genres, str):
        logger.debug(f"Invalid genre type: {type(genres)}")
        return "Unknown"

    try:
        genre_list = ast.literal_eval(genres)

        if not isinstance(genre_list, list):
            return "Unknown"

        names = []
        for genre in genre_list:
            if isinstance(genre, dict) and "name" in genre:
                names.append(genre["name"])

        return ", ".join(names) if names else "Unknown"

    except (ValueError, SyntaxError) as e:
        logger.debug(f"Error parsing genres: {e}")
        return "Unknown"
    except Exception as e:
        logger.exception(f"Unexpected error extracting genres: {e}")
        return "Unknown"


def get_movie_details(title):
    """
    Retrieve detailed information for a movie by title.
    
    Args:
        title (str): Movie title to search for
        
    Returns:
        dict: Movie details including title, overview, rating, etc.
        None: If movie not found or error occurs
    """
    if not title or not isinstance(title, str):
        logger.warning(f"Invalid title provided: {title}")
        return None

    metadata = _load_metadata()
    
    if metadata is None:
        logger.error("Cannot get movie details: metadata not loaded")
        return None

    try:
        movie = metadata[metadata["title"] == title]

        if movie.empty:
            logger.debug(f"Movie not found: {title}")
            return None

        if len(movie) > 1:
            logger.warning(f"Multiple matches found for '{title}', using first match")

        movie = movie.iloc[0]

        # Safely get attributes with fallbacks for missing columns
        result = {
            "title": movie.get("title", title),
            "overview": movie.get("overview", "No description available"),
            "rating": movie.get("vote_average", "N/A"),
            "release_date": movie.get("release_date", "N/A"),
            "genres": extract_genres(movie.get("genres", "Unknown")),
            "runtime": movie.get("runtime", "N/A"),
            "vote_count": movie.get("vote_count", 0),
            "poster": ""  # Will be fetched from TMDB API if needed
        }
        
        return result

    except Exception as e:
        logger.debug(f"Error retrieving movie details for '{title}': {e}")
        # Return minimal info instead of None
        return {
            "title": title,
            "overview": "No description available",
            "rating": "N/A",
            "release_date": "N/A",
            "genres": "Unknown",
            "runtime": "N/A",
            "vote_count": 0,
            "poster": ""
        }