# MoodFlix
MoodFlix is an emotion-aware movie recommendation system that suggests movies based on user mood and preferences using Machine Learning and NLP. It is built with Python, Streamlit, and TMDB (The Movie Database) API providing personalized recommendations with posters, ratings, and trailers.

# 🚀 Features

- 🎭 Emotion-aware movie recommendation concept
- 🎬 Content-based movie recommendation engine
- 📊 Cosine similarity-based recommendations
- 🧠 NLP preprocessing pipeline
- 🎥 TMDB movie dataset integration
- ⭐ Top 5 similar movie recommendations
- 🏗 Clean and scalable project structure
- 💻 Built using Python and Scikit-learn

# 🛠 Tech Stack

- **Language:** Python  
- **Machine Learning:** Scikit-learn  
- **Data Processing:** Pandas, NumPy  
- **NLP:** NLTK  
- **Recommendation Algorithm:** Content-Based Filtering  
- **Similarity Metric:** Cosine Similarity  
- **Dataset:** TMDB 5000 Movie Dataset  
- **IDE:** VS Code  
- **Version Control:** Git & GitHub  

# 📁 Project Structure

```bash
MoodFlix/
│
├── app/
│   ├── preprocessing.py          # Data preprocessing and recommendation engine
│   └── app.py                    # Streamlit web application
│
├── assets/                       # Images, logos and UI assets
│
├── data/
│   ├── tmdb_5000_movies.csv      # TMDB movies dataset
│   └── tmdb_5000_credits.csv     # TMDB credits dataset
│
├── model/
│   ├── movies.pkl                # Processed movie dataset
│   └── vectorizer.pkl            # Trained CountVectorizer model
│
├── notebooks/                    # Jupyter notebooks for experimentation
│
├── screenshots/                  # Application screenshots
│
├── .venv/                        # Python virtual environment
│
├── .gitignore                    # Ignored files and folders
│
├── requirements.txt              # Project dependencies
│
└── README.md                     # Project documentation