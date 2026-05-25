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

# 📂 Project Structure

# 📁 Project Structure

```bash
MoodFlix/
│
├── app/
│   └── preprocessing.py          # Data preprocessing and recommendation engine
│
├── assets/                       # Images, logos, and UI assets
│
├── data/
│   ├── tmdb_5000_movies.csv      # TMDB movies dataset
│   └── tmdb_5000_credits.csv     # TMDB credits dataset
│
├── model/
│   └── movies.pkl                # Processed movie dataframe
│
├── notebooks/                    # Jupyter notebooks for experimentation
│
├── screenshots/                  # Project screenshots and demo images
│
├── .gitignore                    # Ignored files and folders
├── README.md                     # Project documentation
└── requirements.txt              # Required Python libraries