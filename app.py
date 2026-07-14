from flask import Flask, render_template, request
from src.recommender import recommend_hybrid
from src.tmdb_api import fetch_movie_details

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []

    if request.method == "POST":

        movie = request.form["movie"]

        mood = request.form["mood"]

        recommended_titles = recommend_hybrid(movie, mood)

        recommendations = []

        for title in recommended_titles:

            details = fetch_movie_details(title)

            if details:

                recommendations.append(details) 

    return render_template("index.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)