from flask import Flask, render_template, request
from src.recommender import recommend_hybrid
from src.metadata import get_movie_details
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []

    if request.method == "POST":

        movie = request.form["movie"]

        mood = request.form["mood"]

        recommended_titles = recommend_hybrid(movie, mood)

        print("=" * 50)
        print("Recommended Titles:")
        print(recommended_titles)
        print("=" * 50)

        recommendations = []

        for title in recommended_titles:

            print("Searching:", title)

            details = get_movie_details(title)

            print(details)

            if details:
                recommendations.append(details) 

            time.sleep(0.3)

    return render_template("index.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)