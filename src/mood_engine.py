mood_mapping = {
    "Happy": ["Comedy", "Family", "Adventure"],
    "Sad": ["Drama", "Biography"],
    "Romantic": ["Romance", "Drama"],
    "Excited": ["Action", "Adventure", "Sci-Fi"],
    "Fear": ["Horror", "Thriller", "Mystery"],
    "Relaxed": ["Animation", "Family", "Fantasy"],
    "Motivated": ["Biography", "Sport", "History"],
    "Curious": ["Mystery", "Sci-Fi", "Crime"],
    "Lonely": ["Drama", "Romance"],
    "Inspired": ["Biography", "Drama", "Adventure"]
}

def calculate_mood_score(tags, mood):

    mood_genres = mood_mapping[mood]

    score = 0

    for genre in mood_genres:

        if genre.lower() in tags:
            score += 1

    return score