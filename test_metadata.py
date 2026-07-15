from src.metadata import get_movie_details

movies = [
    "Avatar",
    "Inception",
    "Interstellar",
    "Titanic",
    "The Dark Knight"
]

for movie in movies:
    print("=" * 50)
    print(movie)
    print(get_movie_details(movie))