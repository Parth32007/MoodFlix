import pandas as pd
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import (
    convert,
    convert_cast,
    fetch_director,
    stem
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

MODEL_DIR.mkdir(exist_ok=True)

movies = pd.read_csv("data/raw/tmdb_5000_movies.csv")
credits = pd.read_csv("data/raw/tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")

movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew"
    ]
]

movies.dropna(inplace=True)

movies.drop_duplicates(inplace=True)

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

movies['cast'] = movies['cast'].apply(convert_cast)

movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

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

movies['tags'] = (
    movies['overview']
    + movies['genres']
    + movies['keywords']
    + movies['cast']
    + movies['crew']
)

new_df = movies[['movie_id', 'title', 'tags']]

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

new_df['tags'] = new_df['tags'].apply(stem)

# new_df.to_csv("processed_movies.csv", index=False)

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(new_df["tags"]).toarray()

similarity = cosine_similarity(vectors)

with open(MODEL_DIR / "movies.pkl", "wb") as file:
    pickle.dump(new_df, file)

with open(MODEL_DIR / "vectorizer.pkl", "wb") as file:
    pickle.dump(cv, file)

with open(MODEL_DIR / "similarity.pkl", "wb") as file:
    pickle.dump(similarity, file)