import streamlit as st
import pickle
from sklearn.metrics.pairwise import cosine_similarity

movies=pickle.load(open('model/movies.pkl','rb'))
cv=pickle.load(open('model/vectorizer.pkl','rb'))

vectors=cv.transform(movies['tags']).toarray()
similarity=cosine_similarity(vectors)

st.title("MoodFlix")
st.write("Emotion-based Movie Recommendation System")

movie_list=movies['title'].values

selected_movie=st.selectbox("Select Movie",movie_list)

moods=["Happy","Sad","Excited","Romantic","Motivational","Curious","Scared"]

selected_mood=st.selectbox("Select Mood",moods)

def recommend(movie):

    movie_index=movies[movies['title']==movie].index[0]

    distances=similarity[movie_index]

    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    recommended_movies=[]

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

if st.button("Recommend"):

    recommendations=recommend(selected_movie)

    st.subheader("🎥 Recommended Movies")

    for movie in recommendations:
        st.write(movie)

    st.success(f"Mood Selected: {selected_mood}")