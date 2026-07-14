from flask import Flask, render_template, request
from src.recommender import recommend_hybrid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []

    if request.method == "POST":

        movie = request.form["movie"]

        mood = request.form["mood"]

        recommendations = recommend_hybrid(movie, mood)

        print(recommendations) 

    return render_template("index.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)