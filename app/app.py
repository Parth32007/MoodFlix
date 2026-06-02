import streamlit as st

st.title("MoodFlix")

st.write("Emotion-based Movie Recommendation System")

movies=["Avatar","Titanic","Interstellar","The dark knight"]
selected_movie=st.selectbox("Select Movie",movies)

moods=["Happy","Sad","Excited","Romantic","Motivational","Curious","Scared"]
selected_mood=st.selectbox("Select Mood",moods)

if st.button("Recommend"):
    st.write("Movie:",selected_movie)
    st.write("Mood:",selected_mood)