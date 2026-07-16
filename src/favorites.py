import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FAVORITES_FILE = BASE_DIR / "storage" / "favorites.json"


def load_favorites():

    if not FAVORITES_FILE.exists():
        return []

    try:
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_favorites(favorites):

    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)


def add_favorite(movie):

    favorites = load_favorites()

    if movie not in favorites:

        favorites.append(movie)

        save_favorites(favorites)


def remove_favorite(movie):

    favorites = load_favorites()

    if movie in favorites:

        favorites.remove(movie)

        save_favorites(favorites)