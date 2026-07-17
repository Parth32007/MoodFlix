# 🎬 MoodFlix

## Emotion-Aware Movie Recommendation System

MoodFlix is an AI-powered movie recommendation system that suggests movies based on the user's emotions, natural language preferences, and movie similarity.

Unlike traditional recommendation systems that rely only on watch history, MoodFlix focuses on understanding how the user feels to provide more personalized recommendations.

---

## 🚀 Features

- **Emotion-based recommendations** - Get movies tailored to your current mood
- **Hybrid recommendation engine** - Combines content-based filtering with mood-based preferences
- **Natural language input** - Search for movies naturally
- **Explainable recommendations** - Understand why each movie was recommended
- **User favorites** - Save and manage your favorite movies
- **Netflix-inspired UI** - Modern, responsive design
- **Movie details** - Access comprehensive movie information using TMDB API
- **Mood mapping** - Intelligent mapping between emotions and movie genres
- **Lazy-loaded models** - Optimized startup time with on-demand model loading
- **Comprehensive logging** - Full request/error tracking for debugging
- **Thread-safe operations** - Concurrent request handling

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, Sentence Transformers
- **Text Processing**: NLTK
- **API**: TMDB API
- **Testing**: pytest
- **Logging**: Python logging module

---

## 📋 Quick Start

For detailed setup instructions, see [SETUP.md](SETUP.md)

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. **Clone & Setup**
   ```bash
   git clone <repository-url>
   cd MoodFlix
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your TMDB API key
   ```

4. **Prepare Data**
   ```bash
   python -c "from src.preprocessing import main; main()"
   ```

5. **Run Application**
   ```bash
   python app.py
   ```

   Visit: `http://localhost:5000`

---

## 🎯 How It Works

### Recommendation Algorithm

MoodFlix uses a **hybrid recommendation approach**:

1. **Content-Based Filtering** (70% weight)
   - Analyzes movie features: genres, keywords, cast, crew, plot overview
   - Uses TF-IDF vectorization and cosine similarity
   - Finds movies most similar to user's selected movie

2. **Mood-Based Filtering** (30% weight)
   - Maps user emotions to genre preferences
   - Example: "Happy" mood → Comedy, Family, Adventure genres
   - Scores movies based on mood-genre overlap

3. **Hybrid Score**
   ```
   Final Score = 0.7 × Similarity Score + 0.3 × Mood Score
   ```

### Supported Moods

- 😊 Happy
- 😢 Sad
- 💕 Romantic
- 🤩 Excited
- 😨 Fear
- 😌 Relaxed
- 💪 Motivated
- 🤔 Curious
- 😔 Lonely
- ✨ Inspired

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_recommender.py -v
```

**Test Coverage**:
- ✅ TMDB API client with error handling
- ✅ Recommendation engine (content, mood, hybrid)
- ✅ Flask routes and endpoints
- ✅ Input validation and sanitization
- ✅ Favorites management
- ✅ Error handling and logging

---

## 📁 Project Structure

```
MoodFlix/
├── app.py                    # Flask application
├── config.py                 # Configuration management
├── SETUP.md                  # Setup guide
├── requirements.txt          # Dependencies
│
├── src/                      # Source code
│   ├── recommender.py        # Recommendation engine
│   ├── mood_engine.py        # Mood-genre mapping
│   ├── metadata.py           # Movie metadata
│   ├── tmdb_api.py           # TMDB API client
│   ├── favorites.py          # Favorites management
│   ├── preprocessing.py      # Data preprocessing
│   ├── utils.py              # Utilities
│   └── logger.py             # Logging setup
│
├── tests/                    # Test suite
│   ├── conftest.py           # pytest configuration
│   ├── test_api.py           # API tests
│   ├── test_recommender.py   # Engine tests
│   └── test_flask_integration.py  # Route tests
│
├── templates/                # HTML templates
│   ├── index.html            # Home page
│   ├── movie.html            # Movie details
│   └── recommendations.html  # Recommendations page
│
└── static/                   # CSS, JS, Images
    ├── css/
    ├── js/
    └── images/
```

---

## 🔒 Security Features

- ✅ **Environment-based configuration** - API keys in .env
- ✅ **Input validation** - All user inputs sanitized
- ✅ **Error handling** - Comprehensive exception handling
- ✅ **Logging** - Request/error audit trail
- ✅ **Thread-safe operations** - Concurrent request handling
- ✅ **Debug mode disabled in production** - Flask debug disabled by default

---

## 🚀 Deployment

### Production Configuration

Edit `.env`:
```env
FLASK_DEBUG=False
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```bash
docker build -t moodflix .
docker run -p 5000:5000 --env-file .env moodflix
```

---

## 📊 Performance

- **Model Loading**: Lazy-loaded on first request (~2-3 seconds)
- **Recommendation Time**: ~100-500ms for hybrid recommendations
- **API Response**: ~1-2 seconds including TMDB API calls
- **Memory Usage**: ~500MB with loaded models

### Optimization Tips

1. **Enable Caching**: Set `ENABLE_CACHING=True` in .env
2. **Adjust TMDB Delays**: Balance rate limits vs. responsiveness
3. **Use Gunicorn workers**: Increase `-w` parameter for concurrent requests
4. **Monitor Logs**: Check `moodflix.log` for performance issues

---

## 🐛 Debugging

### Enable Debug Logging

```env
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

### View Logs

```bash
tail -f moodflix.log
```

### Test Specific Component

```python
from src.recommender import recommend_hybrid
results = recommend_hybrid("Inception", "Excited")
print(results)
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Write tests for new features
4. Commit your changes (`git commit -am 'Add feature'`)
5. Push to the branch (`git push origin feature/name`)
6. Open a Pull Request

### Code Style
- Follow PEP 8
- Add docstrings to functions
- Use type hints
- Write tests

---

## 📚 API Documentation

### GET /
Home page with recommendation form

### POST /
Submit movie and mood
```python
{
    "movie": "Inception",
    "mood": "Excited"
}
```

### POST /favorite
Add to favorites
```python
{
    "movie": "Inception"
}
```

### GET /favorites
Get all favorites

### DELETE /favorite/<movie_title>
Remove from favorites

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| TMDB API Key Error | Verify key in `.env` |
| Model Files Not Found | Run preprocessing script |
| Port Already in Use | Change port in app.py |
| Import Errors | Reinstall dependencies |
| Slow Recommendations | Check TMDB API delays |

See [SETUP.md](SETUP.md) for more help.

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👥 Team

- **Lead Developer**: [Your Name]
- **Data Scientist**: [Your Name]
- **UI/UX Designer**: [Your Name]

---

## 🙏 Acknowledgments

- **TMDB** - For providing comprehensive movie data API
- **Scikit-learn** - For ML algorithms
- **Flask** - For web framework
- **The Python Community** - For amazing libraries

---

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Email**: support@moodflix.com
- **Documentation**: [SETUP.md](SETUP.md)

---

## 🎯 Roadmap

- [ ] User authentication & profiles
- [ ] Watch history tracking
- [ ] Social recommendations
- [ ] Mobile app
- [ ] Advanced mood detection (sentiment analysis)
- [ ] Real-time collaboration
- [ ] Recommendation explanations
- [ ] Multi-language support

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅
