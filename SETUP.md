# MoodFlix - Setup & Development Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MoodFlix
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example configuration
   cp .env.example .env

   # Edit .env and add your TMDB API key
   # Get one from: https://www.themoviedb.org/settings/api
   ```

5. **Prepare data (first time only)**
   ```bash
   # This trains the recommendation model
   python -c "from src.preprocessing import main; main()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The app will be available at `http://localhost:5000`

---

## 📋 Configuration

### Environment Variables (.env file)

```env
# Flask Configuration
FLASK_DEBUG=False
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# TMDB API Configuration
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_TIMEOUT=10
TMDB_DELAY=0.3

# Recommendation Engine Settings
RECOMMENDATION_COUNT=5
MOOD_WEIGHT=0.7
CONTENT_WEIGHT=0.3

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=moodflix.log
ENABLE_LOGGING=True

# Feature Flags
ENABLE_CACHING=True
```

### Getting a TMDB API Key

1. Visit [TMDB API Settings](https://www.themoviedb.org/settings/api)
2. Create an account if you don't have one
3. Request an API key
4. Copy the key to your `.env` file

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
```

### Run Tests with Coverage
```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

### Run Only Unit Tests
```bash
pytest tests/ -m unit -v
```

### Run Only Integration Tests
```bash
pytest tests/ -m integration -v
```

---

## 🛠️ Development

### Project Structure
```
MoodFlix/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── src/                        # Source code
│   ├── recommender.py         # Core recommendation engine
│   ├── mood_engine.py         # Mood-to-genre mapping
│   ├── metadata.py            # Movie metadata extraction
│   ├── tmdb_api.py            # TMDB API client
│   ├── favorites.py           # User favorites management
│   ├── preprocessing.py       # Data preprocessing pipeline
│   ├── utils.py               # Utility functions
│   └── logger.py              # Logging configuration
│
├── templates/                  # HTML templates
│   ├── index.html             # Home page
│   ├── movie.html             # Movie details page
│   ├── recommendations.html   # Recommendations page
│   └── error.html             # Error page
│
├── static/                     # Static files
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   └── images/                # Image assets
│
├── tests/                      # Test suite
│   ├── conftest.py            # pytest configuration
│   ├── test_api.py            # TMDB API tests
│   ├── test_recommender.py    # Recommendation engine tests
│   └── test_flask_integration.py  # Flask route tests
│
├── data/                       # Data files
│   ├── raw/                   # Original TMDB datasets
│   └── processed/             # Processed data
│
└── model/                      # Trained models
    ├── movies.pkl             # Movie dataset
    ├── similarity.pkl         # Similarity matrix
    └── vectorizer.pkl         # Text vectorizer
```

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where possible
- Add docstrings to all functions
- Keep functions focused and reusable

### Adding Features

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests first** (TDD approach)
   ```bash
   # Add tests in tests/test_*.py
   pytest tests/test_*.py -v
   ```

3. **Implement feature**
   ```bash
   # Write code in src/
   ```

4. **Verify tests pass**
   ```bash
   pytest tests/ -v
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

---

## 🐛 Debugging

### Enable Debug Mode
```bash
# In .env
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

### View Logs
```bash
# Real-time log viewing
tail -f moodflix.log

# View recent logs
cat moodflix.log | tail -100
```

### Debug a Specific Module
```python
# In your code
from src.logger import get_logger
logger = get_logger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

---

## 📊 Performance Optimization

### Model Caching
The recommendation models are lazy-loaded on first request for better startup time.

### Request Caching
Enable response caching in `.env`:
```env
ENABLE_CACHING=True
```

### TMDB API Delays
Adjust delays between API calls to respect rate limits:
```env
TMDB_DELAY=0.3  # seconds between requests
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `FLASK_DEBUG=False`
- [ ] Set `FLASK_ENV=production`
- [ ] Generate a secure `SECRET_KEY`
- [ ] Configure TMDB API key
- [ ] Set up logging to file
- [ ] Configure data backup
- [ ] Test all endpoints

### Using Gunicorn (Production Server)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 📚 API Endpoints

### GET /
Home page with recommendation form.

### POST /
Submit movie and mood for recommendations.

### POST /favorite
Add a movie to favorites.
```json
{
  "movie": "Movie Title"
}
```

### GET /favorites
Get all favorite movies.

### DELETE /favorite/<movie_title>
Remove a movie from favorites.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🆘 Troubleshooting

### Issue: TMDB API Key Error
**Solution**: Make sure the API key is correctly set in `.env`

### Issue: Model Files Not Found
**Solution**: Run preprocessing script first
```bash
python -c "from src.preprocessing import main; main()"
```

### Issue: Port Already in Use
**Solution**: Use a different port
```bash
python app.py --port 5001
```

### Issue: Module Import Errors
**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
pip install -r requirements.txt
```

---

## 📞 Support

For issues or questions, please create an issue on the repository.

---

**Last Updated**: 2024
**Maintainers**: MoodFlix Team
