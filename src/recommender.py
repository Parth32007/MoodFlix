import pickle
from pathlib import Path
from src.mood_engine import (
    mood_mapping,
    calculate_mood_score
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"


with open(MODEL_DIR / "movies.pkl", "rb") as file:
    new_df = pickle.load(file)

with open(MODEL_DIR / "similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

with open(MODEL_DIR / "vectorizer.pkl", "rb") as file:
    cv = pickle.load(file)

def recommend(movie):

    # Find the selected movie index
    movie_index = new_df[new_df['title'] == movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Sort movies based on similarity
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    # Store recommendations
    recommended_movies = []

    # Add recommended movie titles
    for i in movies_list:
        recommended_movies.append(new_df.iloc[i[0]].title)

    return recommended_movies

def recommend_by_mood(movie, mood):

    # Check if the mood exists
    if mood not in mood_mapping:
        return ["Invalid mood selected."]

    # Get normal recommendations
    recommendations = recommend(movie)

    # Get genres related to the selected mood
    mood_genres = mood_mapping[mood]

    # Create a new list for filtered recommendations
    filtered_movies = []

    # Check every recommended movie
    for movie_name in recommendations:

        # Get the tags of that movie
        tags = new_df[new_df['title'] == movie_name]['tags'].values[0]

        # Check whether any mood genre is present
        for genre in mood_genres:

            if genre.lower() in tags:
                filtered_movies.append(movie_name)
                break

    return filtered_movies

def recommend_hybrid(movie, mood):

    # Validate mood
    if mood not in mood_mapping:
        return ["Invalid mood selected."]

    movie = movie.strip()

    titles = new_df["title"].tolist()

    # Exact match (case-insensitive)
    exact_match = next(
        (title for title in titles if title.lower() == movie.lower()),
        None
        )

    if exact_match:
        movie = exact_match
    else:
        # Partial match
        partial_match = next(
            (title for title in titles if movie.lower() in title.lower()),
            None
        )

        if partial_match:
            movie = partial_match
        else:
            return ["Movie not found."]

    # Find movie index
    movie_index = new_df[new_df['title'] == movie].index[0]

    # Similarity scores
    distances = similarity[movie_index]

    ranked_movies = []

    # Loop through every movie
    for idx, sim_score in enumerate(distances):

        # Skip the selected movie itself
        if idx == movie_index:
            continue

        # Get movie tags
        tags = new_df.iloc[idx]['tags']

        # Calculate mood score
        mood_score = calculate_mood_score(tags, mood)

        # Normalize mood score
        mood_score = mood_score / 3

        # Final score
        final_score = (0.7 * sim_score) + (0.3 * mood_score)

        ranked_movies.append(
            (idx, final_score)
        )

    ranked_movies = sorted(
        ranked_movies,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for movie in ranked_movies[:5]:
        recommendations.append(
            new_df.iloc[movie[0]].title
        )

    return recommendations