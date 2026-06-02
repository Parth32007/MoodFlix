import streamlit as st
import pickle 

movies=pickle.load(open('model/movies.pkl','rb'))
st.title("MoodFlix")

st.write("Emotion-based Movie Recommendation System")

movie_list=movies['title'].values
selected_movie=st.selectbox("Select Movie",movie_list)

moods=["Happy","Sad","Excited","Romantic","Motivational","Curious","Scared"]
selected_mood=st.selectbox("Select Mood",moods)

def recommend(movie):
    return ["Movie 1","Movie 2","Movie 3","Movie 4","Movie 5"]

if st.button("Recommend"):
    recommendations=recommend(selected_movie)
    st.subheader("Recommended Movies:")
    for movie in recommendations:
        st.write(movie)
