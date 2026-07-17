"""
Data preprocessing pipeline for movie recommendation engine.

This script prepares raw TMDB data for use in the recommendation engine:
1. Loads and merges movie and credits data
2. Extracts and processes genres, keywords, cast, and crew
3. Creates combined 'tags' field for similarity computation
4. Generates vectorized representations and similarity matrix
5. Saves processed data and models to pickle files

Run this script independently when updating movie data:
    python -c "from src.preprocessing import main; main()"
"""

import pandas as pd
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils import convert, convert_cast, fetch_director, stem
from src.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"
DATA_DIR = BASE_DIR / "data"


def main():
    """
    Main preprocessing pipeline.
    
    Loads raw data, processes it, generates similarity matrices,
    and saves artifacts to MODEL_DIR.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Starting movie data preprocessing pipeline...")
        
        # Ensure model directory exists
        MODEL_DIR.mkdir(exist_ok=True)
        logger.debug(f"Model directory: {MODEL_DIR}")
        
        # Load data
        logger.info("Loading raw data...")
        movies_path = DATA_DIR / "raw" / "tmdb_5000_movies.csv"
        credits_path = DATA_DIR / "raw" / "tmdb_5000_credits.csv"
        
        if not movies_path.exists() or not credits_path.exists():
            logger.error(f"Data files not found. Expected:")
            logger.error(f"  {movies_path}")
            logger.error(f"  {credits_path}")
            return False
        
        movies = pd.read_csv(movies_path)
        credits = pd.read_csv(credits_path)
        logger.info(f"Loaded {len(movies)} movies and {len(credits)} credit records")
        
        # Merge datasets
        logger.debug("Merging movies and credits data...")
        movies = movies.merge(credits, on="title")
        logger.info(f"After merge: {len(movies)} records")
        
        # Select relevant columns
        logger.debug("Selecting relevant columns...")
        movies = movies[[
            "movie_id",
            "title",
            "overview",
            "genres",
            "keywords",
            "cast",
            "crew"
        ]]
        
        # Clean data
        logger.debug("Cleaning data...")
        initial_count = len(movies)
        movies.dropna(inplace=True)
        movies.drop_duplicates(inplace=True)
        logger.info(f"Removed {initial_count - len(movies)} rows (null/duplicates)")
        
        # Parse JSON-formatted fields
        logger.debug("Parsing genres, keywords, cast, crew...")
        movies['genres'] = movies['genres'].apply(convert)
        movies['keywords'] = movies['keywords'].apply(convert)
        movies['cast'] = movies['cast'].apply(convert_cast)
        movies['crew'] = movies['crew'].apply(fetch_director)
        
        # Process overview (tokenize)
        movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])
        
        # Remove spaces from tags
        logger.debug("Normalizing tags...")
        movies['genres'] = movies['genres'].apply(
            lambda x: [i.replace(" ", "") for i in x]
        )
        movies['keywords'] = movies['keywords'].apply(
            lambda x: [i.replace(" ", "") for i in x]
        )
        movies['cast'] = movies['cast'].apply(
            lambda x: [i.replace(" ", "") for i in x]
        )
        movies['crew'] = movies['crew'].apply(
            lambda x: [i.replace(" ", "") for i in x]
        )
        
        # Combine all tags
        logger.debug("Combining tags...")
        movies['tags'] = (
            movies['overview']
            + movies['genres']
            + movies['keywords']
            + movies['cast']
            + movies['crew']
        )
        
        # Create final dataset
        logger.debug("Creating final dataset...")
        new_df = movies[['movie_id', 'title', 'tags']].copy()
        new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
        new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
        
        # Apply stemming
        logger.info("Applying stemming (this may take a minute)...")
        new_df['tags'] = new_df['tags'].apply(stem)
        
        logger.info(f"Processed {len(new_df)} movies")
        
        # Vectorization and similarity computation
        logger.info("Vectorizing tags...")
        cv = CountVectorizer(max_features=5000, stop_words="english")
        vectors = cv.fit_transform(new_df["tags"]).toarray()
        logger.debug(f"Vectorizer features: {cv.get_feature_names_out().shape[0]}")
        
        logger.info("Computing cosine similarity matrix...")
        similarity = cosine_similarity(vectors)
        logger.debug(f"Similarity matrix shape: {similarity.shape}")
        
        # Save models
        logger.info("Saving models to pickle files...")
        
        with open(MODEL_DIR / "movies.pkl", "wb") as f:
            pickle.dump(new_df, f)
            logger.debug("Saved movies.pkl")
        
        with open(MODEL_DIR / "vectorizer.pkl", "wb") as f:
            pickle.dump(cv, f)
            logger.debug("Saved vectorizer.pkl")
        
        with open(MODEL_DIR / "similarity.pkl", "wb") as f:
            pickle.dump(similarity, f)
            logger.debug("Saved similarity.pkl")
        
        # Save metadata (optional)
        try:
            metadata = new_df[['movie_id', 'title']].copy()
            with open(MODEL_DIR / "movie_metadata.pkl", "wb") as f:
                pickle.dump(metadata, f)
                logger.debug("Saved movie_metadata.pkl")
        except Exception as e:
            logger.warning(f"Could not save movie_metadata.pkl: {e}")
        
        logger.info("✓ Preprocessing pipeline completed successfully!")
        logger.info(f"  - Processed {len(new_df)} movies")
        logger.info(f"  - Created {len(cv.get_feature_names_out())} features")
        logger.info(f"  - Generated similarity matrix of shape {similarity.shape}")
        
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return False
    except Exception as e:
        logger.exception(f"Error in preprocessing pipeline: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)