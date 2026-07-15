import pickle
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "model"

with open(MODEL_DIR / "movie_metadata.pkl", "rb") as f:
    movie_metadata = pickle.load(f)

def extract_genres(genres):

    if not isinstance(genres, str):

        return "Unknown"

    try:

        genres = ast.literal_eval(genres)

        names = []

        for genre in genres:

            names.append(genre["name"])

        return ", ".join(names)

    except:

        return "Unknown"

def get_movie_details(title):

    movie = movie_metadata[movie_metadata["title"] == title]

    if movie.empty:
        return None

    movie = movie.iloc[0]

    return {

        "title": movie["title"],

        "overview": movie["overview"],

        "rating": movie["vote_average"],

        "release_date": movie["release_date"],

        "genres": extract_genres(movie["genres"]),

        "runtime": movie["runtime"],

        "vote_count": movie["vote_count"]

    }