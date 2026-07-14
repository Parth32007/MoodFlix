import requests

API_KEY = "YOUR_TMDB_API_KEY"  # Replace with your actual TMDb API key

BASE_URL = "https://api.themoviedb.org/3"


def fetch_movie_details(movie_name):

    search_url = (
        f"{BASE_URL}/search/movie"
        f"?api_key={API_KEY}"
        f"&query={movie_name}"
    )

    response = requests.get(search_url)

    data = response.json()

    if data["results"]:

        movie = data["results"][0]

        poster = (
            "https://image.tmdb.org/t/p/w500"
            + movie["poster_path"]
            if movie["poster_path"]
            else ""
        )

        return {

            "title": movie["title"],

            "poster": poster,

            "rating": movie["vote_average"],

            "release_date": movie["release_date"],

            "overview": movie["overview"]

        }

    return None