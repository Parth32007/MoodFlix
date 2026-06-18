import streamlit as st
import pickle
import requests
import os

from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote

API_KEY = "Your_TMDB_API_Key_Here"  # Replace with your actual TMDB API key

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

FAVORITES_FILE = "user_data/favorites.pkl"
os.makedirs(
    "user_data",
    exist_ok=True
)
if os.path.exists(FAVORITES_FILE):
    favorites = pickle.load(
        open(FAVORITES_FILE, "rb")
    )
else:
    favorites = []

WATCHLIST_FILE = "user_data/watchlist.pkl"
if os.path.exists(WATCHLIST_FILE):
    watchlist = pickle.load(
        open(WATCHLIST_FILE, "rb")
    )
else:
    watchlist = []

HISTORY_FILE = "user_data/history.pkl"
if os.path.exists(HISTORY_FILE):
    history = pickle.load(
        open(HISTORY_FILE, "rb")
    )
else:
    history = []


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

st.sidebar.markdown("---")
st.sidebar.subheader("❤️ Favorites")
if len(favorites) == 0:

    st.sidebar.write(
        "No favorites yet."
    )

else:

    for movie in favorites:

        col1, col2 = st.sidebar.columns([4,1])

        with col1:
            st.write(movie)

        with col2:
            if st.button(
                "❌",
                key=f"fav_{movie}"
            ):

                favorites.remove(movie)

                pickle.dump(
                    favorites,
                    open(
                        FAVORITES_FILE,
                        "wb"
                    )
                )

                st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Watchlist")
if len(watchlist) == 0:

    st.sidebar.write(
        "No movies in watchlist."
    )

else:

    for movie in watchlist:

        col1, col2 = st.sidebar.columns([4,1])

        with col1:
            st.write(movie)

        with col2:
            if st.button(
                "❌",
                key=f"watch_{movie}"
            ):

                watchlist.remove(movie)

                pickle.dump(
                    watchlist,
                    open(
                        WATCHLIST_FILE,
                        "wb"
                    )
                )

                st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Recent Searches")

if len(history) == 0:

    st.sidebar.write(
        "No searches yet."
    )

else:

    for item in history[-5:][::-1]:

        st.sidebar.write(
            "• " + item
        )

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Dashboard")
col1, col2 = st.sidebar.columns(2)

with col1:
    st.metric(
        "❤️",
        len(favorites)
    )

with col2:
    st.metric(
        "📌",
        len(watchlist)
    )

st.sidebar.metric(
    "🕒 Searches",
    len(history)
)

st.sidebar.markdown("---")

most_used_mood = "N/A"

if len(history) > 0:

    moods_used = []

    for item in history:

        if "→" in item:

            moods_used.append(
                item.split("→")[1].strip()
            )

    if len(moods_used) > 0:

        most_used_mood = max(
            set(moods_used),
            key=moods_used.count
        )

st.sidebar.write(
    f"😀 Most Used Mood: {most_used_mood}"
)

st.sidebar.caption(
    "MoodFlix v1.0"
)

st.title("🎬 MoodFlix")

st.caption(
    "Emotion-Aware Movie Recommendation System"
)

st.markdown("""
Discover movies based on your mood and
find similar films using AI-powered recommendations.
""")

moods = [
    "Happy",
    "Sad",
    "Excited",
    "Romantic",
    "Motivational",
    "Curious",
    "Scared"
]

st.subheader("🎯 Find Your Next Movie")

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
            headers=HEADERS,
            timeout=20
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
        movie_id = movie.get("id")
        genres = []

        if movie_id:

            details_url = (
                f"https://api.themoviedb.org/3/movie/"
                f"{movie_id}"
                f"?api_key={API_KEY}"
            )

            details_response = requests.get(
                details_url,
                timeout=10
            )

            details_data = details_response.json()

            genres = [
                genre["name"]
                for genre in details_data.get(
                    "genres",
                    []
                )
            ]

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
    
@st.cache_data(ttl=3600)
def fetch_trending_movies():

    try:

        url = (
            f"https://api.themoviedb.org/3/trending/movie/day"
            f"?api_key={API_KEY}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        trending_movies = []

        for movie in data.get(
            "results",
            []
        )[:5]:

            trending_movies.append(
                movie["title"]
            )

        return trending_movies

    except Exception as e:

        st.warning(
            "Trending movies temporarily unavailable."
        )

        return []

@st.cache_data(ttl=3600)
def fetch_top_rated_movies():

    try:

        url = (
            f"https://api.themoviedb.org/3/movie/top_rated"
            f"?api_key={API_KEY}"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        data = response.json()

        top_rated_movies = []

        for movie in data.get(
            "results",
            []
        )[:5]:

            top_rated_movies.append(
                movie["title"]
            )

        return top_rated_movies

    except Exception:

        return []
    
trending_movies = fetch_trending_movies()
top_rated_movies = fetch_top_rated_movies()

if len(trending_movies) > 0:

    st.session_state.trending_movies = (
        trending_movies
    )

elif "trending_movies" in st.session_state:

    trending_movies = (
        st.session_state.trending_movies
    )

if len(trending_movies) > 0:

    st.markdown("""
        ## 🔥 Trending Movies Today
        See what's popular right now.
    """)

    cols = st.columns(
        len(trending_movies)
    )

    for i in range(
        len(trending_movies)
    ):

        with cols[i]:

            st.write(
                trending_movies[i]
            )

    st.divider()

if len(top_rated_movies) > 0:

    st.session_state.top_rated_movies = (
        top_rated_movies
    )

elif "top_rated_movies" in st.session_state:

    top_rated_movies = (
        st.session_state.top_rated_movies
    )

if len(top_rated_movies) > 0:

    st.markdown("""
        ## ⭐ Top Rated Movies
        Highest rated movies on TMDB.
    """)

    cols = st.columns(
        len(top_rated_movies)
    )

    for i in range(
        len(top_rated_movies)
    ):

        with cols[i]:

            st.write(
                top_rated_movies[i]
            )

    st.divider()

st.info(
    "Search for a movie and select your mood to get personalized recommendations."
)

search_query = st.text_input(
    "🔍 Search Movie"
)

movie_list = movies['title'].tolist()

if search_query:

    movie_list = [
    movie
    for movie in movie_list
    if search_query.lower().replace("-", " ").strip()
    in movie.lower().replace("-", " ")
]

if len(movie_list) == 0:

    st.warning(
        "No movies found."
    )

    st.stop()

selected_movie = st.selectbox(
    "🎥 Select Movie",
    movie_list
)

selected_mood = st.selectbox(
    "😀 Select Mood",
    moods
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
    recommended_genres = []
    recommended_reasons = []
    recommended_scores = []

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

        recommended_genres.append(
            genres
        )

        recommended_reason = (
            f"Similar to {movie} • {mood} mood"
        )

        recommended_reasons.append(
            recommended_reason
        )

        match_score = round(
            i[1] * 100
        )

        recommended_scores.append(
                match_score
        )

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_dates,
        recommended_overviews,
        recommended_genres,
        recommended_reasons,
        recommended_scores
    )

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if st.button("🎬 Recommend"):

    with st.spinner(
        "Finding the best movies for you..."
    ):

        st.session_state.recommendations = recommend(
            selected_movie,
            selected_mood
        )

        st.session_state.current_mood = selected_mood

        search_entry = (
            f"{selected_movie} → {selected_mood}"
        )

        history.append(
            search_entry
        )

        pickle.dump(
            history,
            open(
                HISTORY_FILE,
                "wb"
            )
        )

if st.session_state.recommendations:

    (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_dates,
        recommended_overviews,
        recommended_genres,
        recommended_reasons,
        recommended_scores
    ) = st.session_state.recommendations

    st.success(
        f"😀 Mood Selected: {st.session_state.current_mood}"
    )

    st.markdown(
        f"## 🎥 Recommendations for {selected_movie}"
    )

    st.divider()

    cols = st.columns(5)

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

            title = recommended_movies[i]

            if len(title) > 30:
                title = title[:30] + "..."

            st.markdown(f"### {title}")

            st.write(
                f"🎯 Match Score: {recommended_scores[i]}%"
            )

            st.write(
                f"⭐ {recommended_ratings[i]}"
            )

            st.write(
                f"📅 {recommended_dates[i]}"
            )

            if len(recommended_genres[i]) > 0:

                st.write(
                    "🏷 " +
                    " | ".join(
                        recommended_genres[i]
                    )
                )

            st.caption("📝 Overview")

            st.write(
                recommended_overviews[i][:120] + "..."
            )

            st.info(
                "💡 " + recommended_reasons[i]
            )

            if st.button(
                f"❤️ Favorite {i}"
            ):

                if recommended_movies[i] not in favorites:

                    favorites.append(
                        recommended_movies[i]
                    )

                    pickle.dump(
                        favorites,
                        open(
                            FAVORITES_FILE,
                            "wb"
                        )
                    )

                    st.rerun()
            
            if st.button(
                f"📌 Watchlist {i}"
            ):

                if recommended_movies[i] not in watchlist:

                    watchlist.append(
                        recommended_movies[i]
                    )

                    pickle.dump(
                        watchlist,
                        open(
                            WATCHLIST_FILE,
                            "wb"
                        )
                    )

                    st.rerun()

st.markdown("---")

st.caption(
    "🎬 MoodFlix | Built with ❤️ using Streamlit, Scikit-Learn and TMDB API"
)