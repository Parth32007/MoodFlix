import streamlit as st
import pickle
import requests
import os
import pandas as pd 

from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote

API_KEY = "Your TMDB API Key"  # Replace with your actual TMDB API key

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

@st.cache_resource
def load_similarity():

    vectors = cv.transform(
        movies['tags']
    ).toarray()

    similarity = cosine_similarity(
        vectors
    )

    return similarity

similarity = load_similarity()

st.set_page_config(
    page_title="MoodFlix",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

/* ---------- Main App ---------- */

.stApp{
    background-color:#0F172A;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #1F2937;
}

/* ---------- Headings ---------- */

h1,h2,h3,h4{
    color:#F8FAFC;
}

/* ---------- Paragraphs ---------- */

p,label,span{
    color:#CBD5E1;
}

/* ---------- Buttons ---------- */

.stButton>button{
    width:100%;
    background:#F97316;
    color:white;
    border:none;
    border-radius:10px;
    font-weight:600;
    transition:0.3s;
}

.stButton>button:hover{
    background:#EA580C;
}

/* ---------- Metrics ---------- */

div[data-testid="metric-container"]{
    background:#1E293B;
    padding:12px;
    border-radius:12px;
    border:1px solid #334155;
}

/* ---------- Images ---------- */

img{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

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

if len(favorites) > 0:

    favorites_df = pd.DataFrame(
        {
            "Movie Title": favorites
        }
    )

    csv = favorites_df.to_csv(
        index=False
    )

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

mood_counts = {}

for item in history:

    if "→" in item:

        mood = item.split(
            "→"
        )[1].strip()

        mood_counts[mood] = (
            mood_counts.get(
                mood,
                0
            ) + 1
        )

st.sidebar.write(
    f"😀 Most Used Mood: {most_used_mood}"
)

if len(favorites) > 0:

    st.sidebar.download_button(
        label="⬇ Download Favorites",
        data=csv,
        file_name="favorites.csv",
        mime="text/csv"
    )

st.sidebar.markdown("---")

st.sidebar.subheader(
    "📈 Mood Trends"
)

if len(mood_counts) == 0:

    st.sidebar.write(
        "No mood data yet."
    )

else:

    sorted_moods = sorted(
        mood_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for mood, count in sorted_moods:

        st.sidebar.write(
            f"{mood}: {count}"
        )

st.sidebar.caption(
    "MoodFlix v1.0"
)

hero = st.container()

with hero:

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#1E293B,#0F172A);
        padding:30px;
        border-radius:18px;
        border:1px solid #334155;
        margin-bottom:20px;
    ">
    <h1 style="margin-bottom:8px;">
        🎬 MoodFlix
    </h1>

    <p style="
        color:#CBD5E1;
        font-size:18px;
    ">
        Discover great movies based on your mood using AI-powered recommendations.
    </p>

    </div>
    """,
    unsafe_allow_html=True)

dashboard = st.container()

with dashboard:

    stats1, stats2, stats3 = st.columns(3)

    with stats1:
        st.metric(
            "❤️ Favorites",
            len(favorites)
        )

    with stats2:
        st.metric(
            "📌 Watchlist",
            len(watchlist)
        )

    with stats3:
        st.metric(
            "🔍 Searches",
            len(history)
        )

st.divider()

st.markdown("---")

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

@st.cache_data(ttl=86400)
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
            headers=HEADERS,
            timeout=20
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
    
def movie_card(movie_title):

    poster, rating, release_date, overview, genres = fetch_movie_data(
        movie_title
    )

    with st.container():

        if poster:

            st.image(
                poster,
                use_container_width=True
            )

        else:

            st.image(
                "https://via.placeholder.com/300x450?text=No+Poster",
                use_container_width=True
            )

        st.markdown(
            f"### {movie_title}"
        )

        year = (
            release_date[:4]
            if release_date != "N/A"
            else "N/A"
        )

        info1, info2 = st.columns(2)

        with info1:
            st.caption(f"⭐ {rating}")

        with info2:
            st.caption(f"📅 {year}")

        if genres:

            st.caption(
                "🎭 " +
                ", ".join(genres[:2])
            )

        st.divider()

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

trending_section = st.container()

with trending_section:

    if len(trending_movies) > 0:

        st.markdown("## 🔥 Trending Now")
        st.caption("Most popular movies today")

        cols = st.columns(
            len(trending_movies)
        )

        for i in range(
            len(trending_movies)
        ):

            with cols[i]:

                movie_card(
                    trending_movies[i]
                )

        st.markdown("<br>", unsafe_allow_html=True)

if len(top_rated_movies) > 0:

    st.session_state.top_rated_movies = (
        top_rated_movies
    )

elif "top_rated_movies" in st.session_state:

    top_rated_movies = (
        st.session_state.top_rated_movies
    )

top_rated_section = st.container()

with top_rated_section:

    if len(top_rated_movies) > 0:

        st.markdown("## ⭐ Top Rated")
        st.caption("Highest rated movies on TMDB")

        cols = st.columns(
            len(top_rated_movies)
        )

        for i in range(
            len(top_rated_movies)
        ):

            with cols[i]:

                movie_card(
                    top_rated_movies[i]
                )   

        st.markdown("<br>", unsafe_allow_html=True)

search_section = st.container()

with search_section:

    st.subheader("🔍 Search Movies")

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


@st.cache_data
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

        if len(genres) > 0:

            genre_text = ", ".join(
                genres[:3]
            )

            recommended_reason = (
                f"Recommended because it includes "
                f"{genre_text} themes and matches "
                f"your {mood} mood."
            )

        else:

            recommended_reason = (
                f"Recommended because it matches "
                f"your {mood} mood and shares "
                f"similar themes."
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

recommendation_section = st.container()

with recommendation_section:

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