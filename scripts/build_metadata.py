import pickle
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "model"

DATA_DIR = BASE_DIR / "data" / "raw"

# Load recommender dataset
with open(MODEL_DIR / "movies.pkl", "rb") as f:
    movies = pickle.load(f)

# Load TMDB dataset
tmdb = pd.read_csv(DATA_DIR / "tmdb_5000_movies.csv")

# Keep only required columns
metadata = tmdb[
    [
        "title",
        "genres",
        "overview",
        "release_date",
        "vote_average",
        "runtime",
        "vote_count"
    ]
].copy()

# Merge using title
movie_metadata = movies.merge(
    metadata,
    on="title",
    how="left"
)

# Save
with open(MODEL_DIR / "movie_metadata.pkl", "wb") as f:
    pickle.dump(movie_metadata, f)

print("=" * 50)
print("Metadata Created Successfully")
print("=" * 50)

print()

print(movie_metadata.head())

print()

print("Rows:", len(movie_metadata))