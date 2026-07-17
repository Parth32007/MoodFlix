"""
MoodFlix Flask application.
Emotion-aware movie recommendation system.
"""

from flask import Flask, render_template, request, jsonify
from config import DEBUG, SECRET_KEY, TMDB_DELAY_BETWEEN_REQUESTS, RECOMMENDATION_COUNT
from src.recommender import recommend_hybrid
from src.metadata import get_movie_details
from src.favorites import add_favorite, get_favorites, remove_favorite
from src.logger import get_logger
import time

logger = get_logger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JSON_SORT_KEYS'] = False


def validate_input(data_dict, required_fields):
    """
    Validate that required fields are present and non-empty.
    
    Args:
        data_dict (dict): Dictionary to validate
        required_fields (list): List of required field names
        
    Returns:
        tuple: (is_valid, error_message)
    """
    for field in required_fields:
        if not data_dict.get(field) or not str(data_dict.get(field)).strip():
            return False, f"Missing required field: {field}"
    return True, None


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page with recommendation form. Supports both form-data and JSON."""
    recommendations = []
    error_message = None

    if request.method == "POST":
        try:
            # Handle both form data and JSON
            if request.is_json:
                data = request.get_json()
                movie = data.get("movie", "").strip()
                mood = data.get("mood", "").strip()
                is_json_request = True
            else:
                movie = request.form.get("movie", "").strip()
                mood = request.form.get("mood", "").strip()
                is_json_request = False

            # Validate input
            is_valid, error = validate_input(
                {"movie": movie, "mood": mood},
                ["movie", "mood"]
            )
            if not is_valid:
                error_message = error
                logger.warning(f"Validation failed in home(): {error}")
                if is_json_request:
                    return jsonify({"status": "error", "message": error_message}), 400
            else:
                logger.info(f"Processing recommendation request: movie='{movie}', mood='{mood}'")
                
                # Get recommendations
                recommended_titles = recommend_hybrid(movie, mood)

                if not recommended_titles:
                    error_message = f"Could not find recommendations for '{movie}' with mood '{mood}'"
                    logger.info(error_message)
                    if is_json_request:
                        return jsonify({"status": "error", "message": error_message}), 404
                else:
                    logger.debug(f"Received {len(recommended_titles)} recommendations")

                    # Fetch movie details for each recommendation
                    for title in recommended_titles:
                        try:
                            details = get_movie_details(title)
                            if details:
                                recommendations.append(details)
                                logger.debug(f"Added recommendation: {title}")
                            time.sleep(TMDB_DELAY_BETWEEN_REQUESTS)
                        except Exception as e:
                            logger.error(f"Error fetching details for '{title}': {e}")
                            continue

                    if not recommendations:
                        error_message = "Could not fetch details for recommended movies"
                        logger.warning(error_message)
                        if is_json_request:
                            return jsonify({"status": "error", "message": error_message}), 500

                    # Return JSON if requested
                    if is_json_request:
                        return jsonify({
                            "status": "success",
                            "recommendations": recommendations
                        }), 200

        except Exception as e:
            error_message = "An error occurred while processing your request"
            logger.exception(f"Error in home() POST: {e}")
            if request.is_json:
                return jsonify({"status": "error", "message": error_message}), 500

    return render_template(
        "index.html",
        recommendations=recommendations,
        error_message=error_message
    )


@app.route("/favorite", methods=["POST"])
def favorite():
    """Add a movie to favorites."""
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body must be JSON"
            }), 400

        movie_title = data.get("movie", "").strip()

        if not movie_title:
            return jsonify({
                "status": "error",
                "message": "Movie title is required"
            }), 400

        add_favorite(movie_title)
        logger.info(f"Added to favorites: {movie_title}")

        return jsonify({
            "status": "success",
            "message": f"'{movie_title}' added to favorites"
        }), 200

    except Exception as e:
        logger.exception(f"Error in favorite(): {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to add favorite"
        }), 400


@app.route("/favorites", methods=["GET"])
def get_user_favorites():
    """Retrieve all user favorites."""
    try:
        favorites = get_favorites()
        logger.debug(f"Retrieved {len(favorites)} favorites")
        return jsonify({
            "status": "success",
            "favorites": favorites
        }), 200
    except Exception as e:
        logger.exception(f"Error retrieving favorites: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve favorites"
        }), 500


@app.route("/favorite/<movie_title>", methods=["DELETE"])
def delete_favorite(movie_title):
    """Remove a movie from favorites."""
    try:
        if not movie_title or not movie_title.strip():
            return jsonify({
                "status": "error",
                "message": "Movie title is required"
            }), 400

        remove_favorite(movie_title)
        logger.info(f"Removed from favorites: {movie_title}")

        return jsonify({
            "status": "success",
            "message": f"'{movie_title}' removed from favorites"
        }), 200

    except Exception as e:
        logger.exception(f"Error deleting favorite: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to remove favorite"
        }), 500


# API Endpoints for Dashboard
@app.route("/api/favorites", methods=["GET"])
def api_get_favorites():
    """Get all favorites with details."""
    try:
        favorite_titles = get_favorites()
        logger.debug(f"Retrieved {len(favorite_titles)} favorite titles")
        
        # Fetch details for each favorite
        favorites_with_details = []
        for title in favorite_titles:
            try:
                details = get_movie_details(title)
                if details:
                    favorites_with_details.append(details)
                time.sleep(0.1)  # Small delay to avoid rate limiting
            except Exception as e:
                logger.error(f"Error fetching details for favorite '{title}': {e}")
                # Still add it with minimal info
                favorites_with_details.append({"title": title})
        
        return jsonify({
            "status": "success",
            "favorites": favorites_with_details
        }), 200
    except Exception as e:
        logger.exception(f"Error in api_get_favorites(): {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve favorites"
        }), 500


@app.route("/api/movies", methods=["GET"])
def api_get_movies():
    """Get trending and recommended movies for dashboard."""
    try:
        # For now, return the first few movies from the dataset
        # In a real app, this could be based on trending/popular metrics
        
        # Sample movies for demo (in production, fetch from database)
        from src.metadata import _load_metadata
        
        try:
            metadata = _load_metadata()
            if metadata is not None and len(metadata) > 0:
                # Get first 6 movies as trending
                trending = []
                recommended = []
                
                for i, (idx, row) in enumerate(metadata.iterrows()):
                    if i < 6:
                        movie = {
                            "title": row.get("title", "Unknown"),
                            "rating": row.get("vote_average", "N/A"),
                            "release_date": str(row.get("release_date", "N/A"))[:10],
                            "genres": str(row.get("genres", "Unknown"))[:50],
                            "poster": ""
                        }
                        trending.append(movie)
                    elif i < 12:
                        movie = {
                            "title": row.get("title", "Unknown"),
                            "rating": row.get("vote_average", "N/A"),
                            "release_date": str(row.get("release_date", "N/A"))[:10],
                            "genres": str(row.get("genres", "Unknown"))[:50],
                            "poster": ""
                        }
                        recommended.append(movie)
                    else:
                        break
                
                return jsonify({
                    "status": "success",
                    "trending": trending,
                    "recommended": recommended
                }), 200
        except Exception as e:
            logger.warning(f"Could not load metadata: {e}")
        
        # Fallback: return empty lists
        return jsonify({
            "status": "success",
            "trending": [],
            "recommended": []
        }), 200
        
    except Exception as e:
        logger.exception(f"Error in api_get_movies(): {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve movies"
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.url}")
    return jsonify({
        "status": "error",
        "message": "Page not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.exception(f"500 error: {error}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {error}")
    return jsonify({
        "status": "error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == "__main__":
    logger.info(f"Starting MoodFlix application (debug={DEBUG})")
    app.run(debug=DEBUG)