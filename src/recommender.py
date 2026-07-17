"""
Movie recommendation engine combining content-based and mood-based filtering.

This module implements a hybrid recommendation algorithm that:
1. Performs content-based filtering using movie similarity scores
2. Applies mood-based genre filtering
3. Combines both signals using configurable weights (default: 70% content, 30% mood)
"""

import pickle
from pathlib import Path

from config import RECOMMENDATION_COUNT, MOOD_WEIGHT, CONTENT_WEIGHT
from src.mood_engine import mood_mapping, calculate_mood_score
from src.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

# Lazy-loaded model files
_movies_df = None
_similarity_matrix = None
_vectorizer = None


def _load_models():
    """
    Lazy load all required model files from pickle.
    Called once on first recommendation request.
    
    Returns:
        tuple: (movies_df, similarity, vectorizer) or (None, None, None) on error
    """
    global _movies_df, _similarity_matrix, _vectorizer
    
    if _movies_df is not None:
        return _movies_df, _similarity_matrix, _vectorizer
    
    try:
        logger.debug("Loading model files...")
        
        movies_path = MODEL_DIR / "movies.pkl"
        similarity_path = MODEL_DIR / "similarity.pkl"
        vectorizer_path = MODEL_DIR / "vectorizer.pkl"
        
        # Validate files exist
        for path in [movies_path, similarity_path, vectorizer_path]:
            if not path.exists():
                logger.error(f"Model file not found: {path}")
                return None, None, None
        
        with open(movies_path, "rb") as f:
            _movies_df = pickle.load(f)
            logger.debug(f"Loaded movies data: {len(_movies_df)} movies")
        
        with open(similarity_path, "rb") as f:
            _similarity_matrix = pickle.load(f)
            logger.debug(f"Loaded similarity matrix: {_similarity_matrix.shape}")
        
        with open(vectorizer_path, "rb") as f:
            _vectorizer = pickle.load(f)
            logger.debug("Loaded vectorizer")
        
        return _movies_df, _similarity_matrix, _vectorizer
        
    except pickle.PickleError as e:
        logger.error(f"Error loading pickle files: {e}")
        return None, None, None
    except Exception as e:
        logger.exception(f"Unexpected error loading models: {e}")
        return None, None, None


def recommend(movie):
    """
    Get content-based movie recommendations.
    Uses cosine similarity to find movies most similar to the given movie.
    
    Args:
        movie (str): Movie title to get recommendations for
        
    Returns:
        list: Up to 5 recommended movie titles, or empty list if movie not found
    """
    movies_df, similarity, _ = _load_models()
    
    if movies_df is None:
        logger.error("Models not loaded, cannot provide recommendations")
        return []
    
    try:
        # Find the selected movie index
        matches = movies_df[movies_df['title'] == movie]
        if matches.empty:
            logger.warning(f"Movie not found for content-based recommendation: {movie}")
            return []
        
        movie_index = matches.index[0]
        logger.debug(f"Found movie at index {movie_index}: {movie}")
        
        # Get similarity scores for all movies
        distances = similarity[movie_index]
        
        # Sort movies by similarity (excluding the movie itself)
        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:RECOMMENDATION_COUNT + 1]
        
        recommended_movies = [movies_df.iloc[i[0]].title for i in movies_list]
        logger.debug(f"Content-based recommendations: {recommended_movies}")
        
        return recommended_movies
        
    except (IndexError, KeyError) as e:
        logger.error(f"Error in content-based recommendation for '{movie}': {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in recommend(): {e}")
        return []


def recommend_by_mood(movie, mood):
    """
    Get mood-filtered movie recommendations.
    First gets content-based recommendations, then filters by mood-related genres.
    
    Args:
        movie (str): Movie title
        mood (str): User mood (must be in mood_mapping)
        
    Returns:
        list: Recommendations filtered by mood-related genres
        Empty list if movie not found or mood invalid
    """
    movies_df, _, _ = _load_models()
    
    if movies_df is None:
        logger.error("Models not loaded, cannot provide recommendations")
        return []
    
    if mood not in mood_mapping:
        logger.warning(f"Invalid mood: {mood}")
        return []
    
    try:
        # Get normal content-based recommendations
        recommendations = recommend(movie)
        
        if not recommendations:
            return []
        
        mood_genres = mood_mapping[mood]
        filtered_movies = []
        
        # Filter recommendations by mood-related genres
        for movie_name in recommendations:
            movie_data = movies_df[movies_df['title'] == movie_name]
            if movie_data.empty:
                continue
            
            tags = movie_data.iloc[0]['tags']
            
            # Check if any mood genre is present in tags
            for genre in mood_genres:
                if genre.lower() in tags.lower():
                    filtered_movies.append(movie_name)
                    break
        
        logger.debug(f"Mood-based recommendations ({mood}): {filtered_movies}")
        return filtered_movies
        
    except Exception as e:
        logger.exception(f"Error in recommend_by_mood(): {e}")
        return []


def recommend_hybrid(movie, mood):
    """
    Hybrid recommendation combining content-based and mood-based filtering.
    
    Algorithm:
    1. Find movie in dataset (exact or partial match)
    2. Get similarity scores for all movies
    3. For each candidate, calculate:
       - Content score: Movie similarity score
       - Mood score: Based on genre overlap with mood preferences
       - Final score: MOOD_WEIGHT * content + CONTENT_WEIGHT * mood
    4. Return top-N recommendations by final score
    
    Args:
        movie (str): Movie title to base recommendations on
        mood (str): User mood (must be in mood_mapping)
        
    Returns:
        list: Top-N (N=RECOMMENDATION_COUNT) hybrid recommendations
        Empty list if movie not found or mood invalid
    """
    movies_df, similarity, _ = _load_models()
    
    if movies_df is None:
        logger.error("Models not loaded, cannot provide recommendations")
        return []
    
    if mood not in mood_mapping:
        logger.warning(f"Invalid mood provided: {mood}")
        return []
    
    try:
        movie = movie.strip()
        
        # Get all movie titles for matching
        titles = movies_df["title"].tolist()
        
        # Try exact match (case-insensitive)
        exact_match = next(
            (title for title in titles if title.lower() == movie.lower()),
            None
        )
        
        if exact_match:
            movie = exact_match
            logger.debug(f"Found exact movie match: {movie}")
        else:
            # Try partial match
            partial_match = next(
                (title for title in titles if movie.lower() in title.lower()),
                None
            )
            
            if partial_match:
                movie = partial_match
                logger.debug(f"Found partial movie match: {movie}")
            else:
                logger.warning(f"No movie found matching: {movie}")
                return []
        
        # Find movie index
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        
        # Get similarity scores for all movies
        distances = similarity[movie_index]
        
        ranked_movies = []
        
        # Evaluate every movie except the selected one
        for idx, sim_score in enumerate(distances):
            if idx == movie_index:
                continue
            
            try:
                # Get movie tags
                tags = movies_df.iloc[idx]['tags']
                
                # Calculate mood score
                mood_score = calculate_mood_score(tags, mood)
                
                # Normalize mood score (0-1 range assuming 0-3 raw score)
                mood_score = mood_score / 3.0
                
                # Combined score: weighted average of content + mood
                final_score = (MOOD_WEIGHT * sim_score) + (CONTENT_WEIGHT * mood_score)
                
                ranked_movies.append((idx, final_score))
                
            except (KeyError, IndexError) as e:
                logger.debug(f"Error evaluating movie at index {idx}: {e}")
                continue
        
        # Sort by final score
        ranked_movies = sorted(
            ranked_movies,
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top-N recommendations
        recommendations = [
            movies_df.iloc[movie_tuple[0]].title
            for movie_tuple in ranked_movies[:RECOMMENDATION_COUNT]
        ]
        
        logger.info(f"Hybrid recommendations for '{movie}' (mood: {mood}): {recommendations}")
        return recommendations
        
    except (IndexError, KeyError) as e:
        logger.error(f"Error in hybrid recommendation for '{movie}': {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in recommend_hybrid(): {e}")
        return []