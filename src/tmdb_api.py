import requests
from requests.exceptions import RequestException
import requests


API_KEY = "YOUR_API_KEY"

BASE_URL = "https://api.themoviedb.org/3"

session = requests.Session()

def fetch_movie_details(movie_name):

    search_url = (
        f"{BASE_URL}/search/movie"
        f"?api_key={API_KEY}"
        f"&query={movie_name}"
    )

    try:

        response = session.get(search_url, timeout=10)

        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            return None

        movie = data["results"][0]

        poster = ""

        if movie.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
            )

        return {

            "title": movie.get("title", "Unknown"),

            "poster": poster,

            "rating": movie.get("vote_average", "N/A"),

            "release_date": movie.get("release_date", "Unknown"),

            "overview": movie.get("overview", "")

        }

    except RequestException as e:

        print("TMDB Request Error:", e)

        return None

    except Exception as e:

        print("Unexpected Error:", e)

        return None