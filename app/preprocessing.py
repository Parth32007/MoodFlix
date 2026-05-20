import numpy as np
import pandas as pd
import ast

movies=pd.read_csv('data/tmdb_5000_movies.csv')
credits=pd.read_csv('data/tmdb_5000_credits.csv')
movies=movies.merge(credits, on='title')

print(movies.head())

movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

def convert(text):
    L=[]
    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)