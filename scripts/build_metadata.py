import pickle
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "model"
DATA_DIR = BASE_DIR / "data" / "raw"

# Load movies.pkl
with open(MODEL_DIR / "movies.pkl", "rb") as f:
    movies = pickle.load(f)

# Load TMDB CSV
tmdb = pd.read_csv(DATA_DIR / "tmdb_5000_movies.csv")

print("=" * 60)
print("movies.pkl:", len(movies))
print("tmdb csv :", len(tmdb))
print("=" * 60)

matched = movies["title"].isin(tmdb["title"])

print("\nMatched Movies :", matched.sum())
print("Missing Movies :", (~matched).sum())

print("\nFirst 20 Missing Titles:\n")

print(
    movies.loc[~matched, "title"].head(20).to_list()
)

import pickle

with open("model/movies.pkl", "rb") as f:
    movies = pickle.load(f)

titles = movies["title"].tolist()

for title in titles:
    if "Avengers" in title:
        print(title)