"""
Mood-based genre mapping and scoring module.

Maps user emotions to movie genres for mood-based recommendation filtering.
Also provides scoring functions to evaluate how well a movie matches a mood.
"""

from src.logger import get_logger

logger = get_logger(__name__)

# Comprehensive mood-to-genre mapping
# Maps emotional states to genres that typically evoke or match that emotion
mood_mapping = {
    "Happy": ["Comedy", "Family", "Adventure"],
    "Sad": ["Drama", "Biography"],
    "Romantic": ["Romance", "Drama"],
    "Excited": ["Action", "Adventure", "Sci-Fi"],
    "Fear": ["Horror", "Thriller", "Mystery"],
    "Relaxed": ["Animation", "Family", "Fantasy"],
    "Motivated": ["Biography", "Sport", "History"],
    "Curious": ["Mystery", "Sci-Fi", "Crime"],
    "Lonely": ["Drama", "Romance"],
    "Inspired": ["Biography", "Drama", "Adventure"]
}


def get_available_moods():
    """
    Get list of all available mood categories.
    
    Returns:
        list: All mood keys from mood_mapping
    """
    return list(mood_mapping.keys())


def get_mood_genres(mood):
    """
    Get genres associated with a specific mood.
    
    Args:
        mood (str): Mood name (must be in mood_mapping)
        
    Returns:
        list: Associated genres, empty list if mood not found
    """
    if mood not in mood_mapping:
        logger.warning(f"Unknown mood: {mood}")
        return []
    
    return mood_mapping[mood]


def is_valid_mood(mood):
    """
    Check if a mood is recognized.
    
    Args:
        mood (str): Mood to validate
        
    Returns:
        bool: True if mood exists in mapping
    """
    return mood in mood_mapping


def calculate_mood_score(tags, mood):
    """
    Calculate how well a movie's genres match a mood.
    
    Scoring algorithm:
    - Checks if any genre associated with the mood appears in movie tags
    - Returns count of matching genres (0-3 in most cases)
    - Case-insensitive matching
    
    Args:
        tags (str): Comma-separated genre tags of a movie (usually lowercase)
        mood (str): User's current mood (must be in mood_mapping)
        
    Returns:
        int: Number of matching genres (higher = better match)
        0: If mood not found or no matches
    """
    if not isinstance(tags, str):
        logger.debug(f"Invalid tags type: {type(tags)}")
        return 0
    
    if mood not in mood_mapping:
        logger.warning(f"Unknown mood in calculate_mood_score: {mood}")
        return 0
    
    try:
        mood_genres = mood_mapping[mood]
        score = 0
        
        # Count how many mood-relevant genres appear in the movie's tags
        tags_lower = tags.lower()
        for genre in mood_genres:
            if genre.lower() in tags_lower:
                score += 1
        
        return score
        
    except Exception as e:
        logger.exception(f"Error calculating mood score: {e}")
        return 0


def normalize_mood_score(raw_score, max_possible=3):
    """
    Normalize raw mood score to 0-1 range for hybrid scoring.
    
    Args:
        raw_score (int): Raw mood score from calculate_mood_score
        max_possible (int): Maximum possible score (typically 3, number of genres per mood)
        
    Returns:
        float: Normalized score in range [0, 1]
    """
    if max_possible <= 0:
        logger.error("max_possible must be positive")
        return 0.0
    
    normalized = min(1.0, raw_score / max_possible)
    return normalized