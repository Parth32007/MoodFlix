"""
Configuration management for MoodFlix application.
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path

# Application settings
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
FLASK_ENV = os.getenv("FLASK_ENV", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# API settings
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_REQUEST_TIMEOUT = int(os.getenv("TMDB_TIMEOUT", "10"))
TMDB_DELAY_BETWEEN_REQUESTS = float(os.getenv("TMDB_DELAY", "0.3"))

# Recommendation settings
RECOMMENDATION_COUNT = int(os.getenv("RECOMMENDATION_COUNT", "5"))
MOOD_WEIGHT = float(os.getenv("MOOD_WEIGHT", "0.7"))
CONTENT_WEIGHT = float(os.getenv("CONTENT_WEIGHT", "0.3"))

# File paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
CACHE_DIR = BASE_DIR / "cache"

# Ensure directories exist
STORAGE_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "moodflix.log"))

# Feature flags
ENABLE_CACHING = os.getenv("ENABLE_CACHING", "True").lower() == "true"
ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "True").lower() == "true"
