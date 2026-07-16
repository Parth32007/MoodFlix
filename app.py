from flask import Flask, render_template, request
from src.recommender import recommend_hybrid
from src.metadata import get_movie_details
import time
from flask import redirect, url_for
from src.favorites import add_favorite
from flask import jsonify

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

            print("Found:", details is not None)

            if details:
                recommendations.append(details) 

            time.sleep(0.3)

    return render_template("index.html", recommendations=recommendations)

@app.route("/favorite", methods=["POST"])
def favorite():

    data = request.get_json()

    movie_title = data.get("movie")

    add_favorite(movie_title)

    return jsonify({

        "status": "success",

        "message": f"{movie_title} added to favorites"

    })

if __name__ == "__main__":
    app.run(debug=True)