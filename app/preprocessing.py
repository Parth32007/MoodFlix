import pandas as pd
import numpy as np
import ast
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Loading datasets
movies=pd.read_csv('data/tmdb_5000_movies.csv')
credits=pd.read_csv('data/tmdb_5000_credits.csv')

# Merging datasets
movies=movies.merge(credits, on='title')

# Selecting important columns
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# Removing null values
movies.dropna(inplace=True)

# Converting genres and keywords
def convert(text):
    L=[]
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

# Extracting top 3 cast members
def convert_cast(text):
    L=[]
    counter=0
    for i in ast.literal_eval(text):
        if counter!=3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L

movies['cast']=movies['cast'].apply(convert_cast)

# Extracting director
def fetch_director(text):
    L=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            L.append(i['name'])
    return L

movies['crew']=movies['crew'].apply(fetch_director)

# Process overview
movies['overview']=movies['overview'].apply(lambda x:x.split())

# Removing spaces between words
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x])

movies['keywords']=movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['cast']=movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['crew']=movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Creating tags
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

# Final dataframe
new_df=movies[['movie_id', 'title', 'tags']]

# Converting list to string
new_df['tags']=new_df['tags'].apply(lambda x: " ".join(x))

# Converting to lowercase
new_df['tags']=new_df['tags'].apply(lambda x: x.lower())

# Vectorization
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors=cv.fit_transform(new_df['tags']).toarray()

# Cosine similarity
similarity=cosine_similarity(vectors)

# Recommendation function
def recommend(movie):
    movie_index=new_df[new_df['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

# Testing recommendation
recommend('Avatar')

# Saving model and data
pickle.dump(new_df, open('model/movies.pkl', 'wb'))
pickle.dump(similarity, open('model/similarity.pkl', 'wb'))