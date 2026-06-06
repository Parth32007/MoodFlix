import streamlit as st
import pickle
import requests

from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "Your_TMDB_API_Key_Here"

movies = pickle.load(open('model/movies.pkl', 'rb'))
cv = pickle.load(open('model/vectorizer.pkl', 'rb'))

vectors = cv.transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)

st.set_page_config(
    page_title="MoodFlix",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 MoodFlix")

st.markdown(
    """
    Discover movies based on your mood and
    find similar films using AI-powered
    recommendations.
    """
)

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select Movie",
    movie_list
)

moods = [
    "Happy",
    "Sad",
    "Excited",
    "Romantic",
    "Motivational",
    "Curious",
    "Scared"
]

selected_mood = st.selectbox(
    "Select Mood",
    moods
)

@st.cache_data
def fetch_movie_data(movie_id):

    try:

        url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}?api_key={API_KEY}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

        else:

            poster_url = None

        rating = data.get(
            "vote_average",
            "N/A"
        )

        release_date = data.get(
            "release_date",
            "N/A"
        )

        return (
            poster_url,
            rating,
            release_date
        )

    except Exception:

        return (
            None,
            "N/A",
            "N/A"
        )


def recommend(movie):

    movie_index = movies[
        movies['title'] == movie
    ].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_dates = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        poster, rating, release_date = fetch_movie_data(
            movie_id
        )

        recommended_movies.append(
            movies.iloc[i[0]].title
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

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_dates
    )


if st.button("Recommend"):

    (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_dates
    ) = recommend(selected_movie)

    st.subheader("🎥 Recommended Movies")
    st.divider()

    cols = st.columns(5)

    for i in range(5):

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
                f"### {recommended_movies[i]}"
            )

            st.markdown(
                f"⭐ **{recommended_ratings[i]}**"
            )

            st.markdown(
                f"📅 **{recommended_dates[i]}**"
            )


    st.info(
        f"Current Mood: {selected_mood}"
    )