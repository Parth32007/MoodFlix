"""
TMDB API client for fetching movie metadata.
Handles communication with The Movie Database API.
"""

import os
from requests.exceptions import RequestException, Timeout
import requests

from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_REQUEST_TIMEOUT
from src.logger import get_logger

logger = get_logger(__name__)

# Validate API key is configured
if not TMDB_API_KEY:
    logger.warning("TMDB_API_KEY not configured. Set the TMDB_API_KEY environment variable.")

BASE_URL = TMDB_BASE_URL
API_KEY = TMDB_API_KEY

session = requests.Session()


def fetch_movie_details(movie_name):
    """
    Fetch movie details from TMDB API.
    
    Args:
        movie_name (str): Name of the movie to search for
        
    Returns:
        dict: Movie details including title, poster, rating, release_date, overview
        None: If movie not found or API request fails
    """
    if not API_KEY:
        logger.error("Cannot fetch movie details: TMDB_API_KEY not configured")
        return None

    if not movie_name or not isinstance(movie_name, str):
        logger.warning(f"Invalid movie name provided: {movie_name}")
        return None

    search_url = (
        f"{BASE_URL}/search/movie"
        f"?api_key={API_KEY}"
        f"&query={movie_name}"
    )

    try:
        logger.debug(f"Fetching details for movie: {movie_name}")
        response = session.get(search_url, timeout=TMDB_REQUEST_TIMEOUT)
        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            logger.info(f"No results found for movie: {movie_name}")
            return None

        movie = data["results"][0]
        logger.debug(f"Found movie: {movie.get('title', 'Unknown')}")

        poster = ""
        if movie.get("poster_path"):
            poster = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]

        return {
            "title": movie.get("title", "Unknown"),
            "poster": poster,
            "rating": movie.get("vote_average", "N/A"),
            "release_date": movie.get("release_date", "Unknown"),
            "overview": movie.get("overview", "")
        }

    except Timeout as e:
        logger.error(f"TMDB API timeout for movie '{movie_name}': {e}")
        return None

    except RequestException as e:
        logger.error(f"TMDB API request error for movie '{movie_name}': {e}")
        return None

    except (ValueError, KeyError) as e:
        logger.error(f"Error parsing TMDB response for '{movie_name}': {e}")
        return None

    except Exception as e:
        logger.exception(f"Unexpected error fetching movie details for '{movie_name}': {e}")
        return None