import streamlit as st
import pickle
import requests

from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote

API_KEY = "Your TMDB API Key Here"

movies = pickle.load(open('model/movies.pkl', 'rb'))
mood_map = pickle.load(open('model/mood_map.pkl', 'rb'))
cv = pickle.load(open('model/vectorizer.pkl', 'rb'))

vectors = cv.transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)

st.set_page_config(
    page_title="MoodFlix",
    page_icon="🎬",
    layout="wide"
)

st.sidebar.title("🎬 MoodFlix")

st.sidebar.markdown("""
### About

MoodFlix is an Emotion-Aware Movie Recommendation System.

It uses:
- Content-Based Filtering
- Cosine Similarity
- TMDB API

to recommend movies similar to your interests.
""")

st.title("🎬 MoodFlix")

st.markdown("""
Discover movies based on your mood and
find similar films using AI-powered recommendations.
""")

movie_list = movies['title'].values

moods = [
    "Happy",
    "Sad",
    "Excited",
    "Romantic",
    "Motivational",
    "Curious",
    "Scared"
]

mood_genres = {
    "Happy": [
        "Comedy",
        "Family",
        "Adventure"
    ],

    "Sad": [
        "Drama",
        "Romance"
    ],

    "Excited": [
        "Action",
        "Adventure",
        "Science Fiction"
    ],

    "Romantic": [
        "Romance",
        "Drama"
    ],

    "Motivational": [
        "Drama",
        "Adventure"
    ],

    "Curious": [
        "Mystery",
        "Science Fiction"
    ],

    "Scared": [
        "Horror",
        "Thriller"
    ]
}

st.subheader("🎯 Find Your Next Movie")

selected_movie = st.selectbox(
    "🎥 Select Movie",
    movie_list
)

selected_mood = st.selectbox(
    "😀 Select Mood",
    moods
)


@st.cache_data
def fetch_movie_data(movie_title):

    try:

        search_url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}"
            f"&query={quote(movie_title)}"
        )

        response = requests.get(
            search_url,
            timeout=10
        )

        data = response.json()

        results = data.get("results", [])

        if len(results) == 0:

            return (
                None,
                "N/A",
                "N/A",
                "No overview available.",
                []
            )

        movie = results[0]

        poster_path = movie.get(
            "poster_path"
        )

        poster_url = None

        if poster_path:

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

        rating = movie.get(
            "vote_average",
            "N/A"
        )

        release_date = movie.get(
            "release_date",
            "N/A"
        )

        overview = movie.get(
            "overview",
            "No overview available."
        )

        genres = []

        return (
            poster_url,
            rating,
            release_date,
            overview,
            genres
        )

    except Exception:

        return (
            None,
            "N/A",
            "N/A",
            "No overview available.",
            []
        )


def recommend(movie, mood):

    movie_index = movies[
        movies['title'] == movie
    ].index[0]

    distances = similarity[movie_index]
    mood_genres = mood_map.get(
        mood,
        []
    )

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:50]

    filtered_movies = []

    for i in movies_list:

        movie_tags = movies.iloc[
            i[0]
        ]['tags']

        if any(
            genre in movie_tags
            for genre in mood_genres
        ):

            filtered_movies.append(i)

        if len(filtered_movies) == 5:
            break

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_dates = []
    recommended_overviews = []

    for i in filtered_movies:

        movie_title = movies.iloc[i[0]].title

        poster, rating, release_date, overview, genres = fetch_movie_data(
            movie_title
        )

        recommended_movies.append(
            movie_title
        )

        recommended_posters.append(
            poster
        )

        recommended_ratings.append(
            rating
        )

        recommended_dates.append(
            release_date
        )

        recommended_overviews.append(
            overview
        )

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_dates,
        recommended_overviews
    )


if st.button("🎬 Recommend"):

    with st.spinner(
        "Finding the best movies for you..."
    ):

        (
            recommended_movies,
            recommended_posters,
            recommended_ratings,
            recommended_dates,
            recommended_overviews
        ) = recommend(
            selected_movie,
            selected_mood
        )

    st.info(
        f"Current Mood: {selected_mood}"
    )

    st.subheader("🎥 Recommended Movies")

    st.divider()

    if len(recommended_movies) == 0:

        st.warning(
            "No movies found for this mood. Try another mood."
        )

    else:

        cols = st.columns(
            len(recommended_movies)
        )

        for i in range(
            len(recommended_movies)
        ):

            with cols[i]:

                if recommended_posters[i]:

                    st.image(
                        recommended_posters[i]
                    )

                else:

                    st.write(
                        "🎬 Poster Not Available"
                    )

                st.markdown(
                    f"**{recommended_movies[i]}**"
                )

                st.write(
                    f"⭐ {recommended_ratings[i]}"
                )

                st.write(
                    f"📅 {recommended_dates[i]}"
                )

                st.markdown("##### Overview")

                st.write(
                    recommended_overviews[i][:120] + "..."
                )