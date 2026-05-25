import pandas as pd
import ast
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

movies = movies.merge(credits, on='title')

movies = movies[['movie_id',
                 'title',
                 'overview',
                 'genres',
                 'keywords',
                 'cast',
                 'crew']]

movies.dropna(inplace=True)

def convert(text):

    L = []

    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert_cast(text):

    L = []
    counter = 0

    for i in ast.literal_eval(text):

        if counter != 3:
            L.append(i['name'])
            counter += 1

        else:
            break

    return L

movies['cast'] = movies['cast'].apply(convert_cast)

def fetch_director(text):

    L = []

    for i in ast.literal_eval(text):

        if i['job'] == 'Director':
            L.append(i['name'])

    return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['tags'] = movies['overview'] + \
                 movies['genres'] + \
                 movies['keywords'] + \
                 movies['cast'] + \
                 movies['crew']

new_df = movies[['movie_id', 'title', 'tags']]

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(new_df['tags']).toarray()

similarity = cosine_similarity(vectors)

def recommend(movie):

    if movie not in new_df['title'].values:
        print("Movie not found!")
        return

    movie_index = new_df[new_df['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    print(f"\nRecommended movies for {movie}:\n")

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

recommend('Avatar')

pickle.dump(new_df, open('model/movies.pkl', 'wb'))