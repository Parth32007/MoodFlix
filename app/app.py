import streamlit as st
import pickle
import requests

from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "c2fb1984938ade31af22a9c8d1077408"

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
st.write("Emotion-based Movie Recommendation System")

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
def fetch_poster(movie_id):

    try:

        url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}?api_key={API_KEY}"
        )

        data = requests.get(url).json()

        poster_path = data.get("poster_path")

        if poster_path:
            return (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

    except Exception:
        pass

    return None


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

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


if st.button("Recommend"):

    recommended_movies, recommended_posters = recommend(
        selected_movie
    )

    st.subheader("🎥 Recommended Movies")

    cols = st.columns(5)

    for i in range(len(recommended_movies)):

        with cols[i]:

            if recommended_posters[i]:

                st.image(
                    recommended_posters[i],
                    use_container_width=True
                )

            else:

                st.write("🎬 Poster Not Available")

            st.caption(
                recommended_movies[i]
            )

    st.success(
        f"Mood Selected: {selected_mood}"
    )