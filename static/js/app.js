// CinePick - Frontend Integration Script
// Handles all API interactions with the backend

document.addEventListener('DOMContentLoaded', function() {
    initializeUI();
    loadFavoritesCount();
    setupSearchBox();
    setupMenuNavigation();
    setupMovieCardButtons();
});

// ============ INITIALIZATION ============

function initializeUI() {
    console.log('CinePick initialized');
    // Load initial recommendations
    loadRecommendations();
}

function loadFavoritesCount() {
    fetch('/api/favorites')
        .then(response => response.json())
        .then(data => {
            const favCount = data.favorites ? data.favorites.length : 0;
            updateFavoritesStats(favCount);
        })
        .catch(error => console.error('Error loading favorites:', error));
}

function updateFavoritesStats(count) {
    // Update sidebar stats
    document.querySelectorAll('.stat-box').forEach((box, index) => {
        if (index === 0) {
            box.querySelector('h2').textContent = count;
        }
    });
    
    // Update overview cards
    document.querySelectorAll('.overview-card').forEach((card, index) => {
        if (index === 0) {
            card.querySelector('h2').textContent = count;
        }
    });
}

// ============ SEARCH & RECOMMENDATIONS ============

function setupSearchBox() {
    const searchInput = document.querySelector('.search-box input');
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const movieName = this.value.trim();
            if (movieName) {
                showMoodSelector(movieName);
            }
        }
    });
}

function showMoodSelector(movieName) {
    const moods = ['Happy', 'Sad', 'Romantic', 'Excited', 'Fear', 'Relaxed', 'Motivated', 'Curious', 'Lonely', 'Inspired'];
    
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'mood-modal';
    modal.innerHTML = `
        <div class="mood-modal-content">
            <h2>How are you feeling?</h2>
            <p>Select your mood for better recommendations</p>
            <div class="mood-grid">
                ${moods.map(mood => `
                    <button class="mood-btn" onclick="searchWithMood('${movieName}', '${mood}')">
                        ${getMoodEmoji(mood)} ${mood}
                    </button>
                `).join('')}
            </div>
            <button class="close-modal" onclick="this.parentElement.parentElement.remove()">✕</button>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function getMoodEmoji(mood) {
    const moodEmojis = {
        'Happy': '😊',
        'Sad': '😢',
        'Romantic': '❤️',
        'Excited': '⚡',
        'Fear': '😨',
        'Relaxed': '😌',
        'Motivated': '💪',
        'Curious': '🤔',
        'Lonely': '😔',
        'Inspired': '✨'
    };
    return moodEmojis[mood] || '🎬';
}

function searchWithMood(movieName, mood) {
    // Close modal
    document.querySelector('.mood-modal').remove();
    
    // Show loading state
    showLoadingState();
    
    // Call backend
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            movie: movieName,
            mood: mood
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'error') {
            alert('Error: ' + data.message);
            loadRecommendations();
        } else {
            displayRecommendations(data.recommendations, movieName, mood);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to get recommendations');
        loadRecommendations();
    });
}

function showLoadingState() {
    const sections = document.querySelectorAll('.movie-section');
    sections.forEach(section => {
        section.innerHTML = '<div class="loading">Loading recommendations...</div>';
    });
}

function loadRecommendations() {
    // Load trending and recommended movies
    fetch('/api/movies')
        .then(response => response.json())
        .then(data => {
            displayTrendingMovies(data.trending || []);
            displayRecommendedMovies(data.recommended || []);
        })
        .catch(error => console.error('Error loading recommendations:', error));
}

function displayRecommendations(recommendations, movieName, mood) {
    const sections = document.querySelectorAll('.movie-section');
    if (sections.length < 2) return;
    
    // Update first section to show search results
    const firstSection = sections[0];
    firstSection.innerHTML = `
        <div class="section-header">
            <h2><i class="fa-solid fa-sparkles"></i> Recommendations for "${movieName}" (${mood} mood)</h2>
            <a href="#" onclick="loadRecommendations(); return false;">Back to Trending</a>
        </div>
        <div class="movie-grid">
            ${recommendations.map(movie => createMovieCard(movie)).join('')}
        </div>
    `;
    
    setupMovieCardButtons();
}

function displayTrendingMovies(movies) {
    const sections = document.querySelectorAll('.movie-section');
    if (sections.length < 1) return;
    
    const firstSection = sections[0];
    if (!firstSection.querySelector('.section-header h2').textContent.includes('Recommendations')) {
        firstSection.querySelector('.movie-grid').innerHTML = movies.map(movie => createMovieCard(movie)).join('');
        setupMovieCardButtons();
    }
}

function displayRecommendedMovies(movies) {
    const sections = document.querySelectorAll('.movie-section');
    if (sections.length < 2) return;
    
    const secondSection = sections[1];
    secondSection.querySelector('.movie-grid').innerHTML = movies.map(movie => createMovieCard(movie)).join('');
    setupMovieCardButtons();
}

// ============ MOVIE CARDS ============

function createMovieCard(movie) {
    return `
        <div class="movie-card" data-movie-title="${movie.title || 'Unknown'}">
            <img src="${movie.poster || 'https://placehold.co/300x430?text=No+Image'}" 
                 alt="${movie.title}" 
                 onerror="this.src='https://placehold.co/300x430?text=No+Image'">
            <div class="movie-info">
                <h3>${movie.title || 'Unknown'}</h3>
                <p>${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'} • ${movie.genres || 'N/A'}</p>
                <div class="rating">
                    <span><i class="fa-solid fa-star"></i> ${movie.rating || 'N/A'}</span>
                    <button class="fav-btn" onclick="toggleFavorite(event, '${movie.title}')">
                        <i class="fa-regular fa-heart"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

function setupMovieCardButtons() {
    document.querySelectorAll('.fav-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
}

// ============ FAVORITES ============

function toggleFavorite(event, movieTitle) {
    const btn = event.currentTarget;
    const icon = btn.querySelector('i');
    
    if (!icon) {
        console.error('Icon not found in button');
        return;
    }
    
    if (icon.classList.contains('fa-regular')) {
        // Add to favorites
        addFavorite(movieTitle, btn);
    } else {
        // Remove from favorites
        removeFavorite(movieTitle, btn);
    }
}

function addFavorite(movieTitle, btn) {
    fetch('/favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ movie: movieTitle })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            if (btn) {
                btn.style.background = '#ff1744';
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-regular');
                    icon.classList.add('fa-solid');
                }
            }
            loadFavoritesCount();
        }
    })
    .catch(error => console.error('Error adding favorite:', error));
}

function removeFavorite(movieTitle, btn) {
    fetch(`/favorite/${encodeURIComponent(movieTitle)}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            if (btn) {
                btn.style.background = '#ff8c1a';
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-regular');
                    icon.classList.remove('fa-solid');
                }
            }
            loadFavoritesCount();
        }
    })
    .catch(error => console.error('Error removing favorite:', error));
}

// ============ SIDEBAR MENU NAVIGATION ============

function setupMenuNavigation() {
    const menuItems = document.querySelectorAll('.menu li');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const text = this.querySelector('span').textContent;
            handleMenuClick(text);
        });
    });
}

function handleMenuClick(menuItem) {
    const mainContent = document.querySelector('.main');
    
    switch(menuItem) {
        case 'Home':
            location.reload();
            break;
        case 'Favorites':
            showFavoritesPage();
            break;
        case 'Watchlist':
            alert('Watchlist feature coming soon!');
            break;
        case 'Recent Searches':
            alert('Recent Searches feature coming soon!');
            break;
        case 'Dashboard':
            alert('Dashboard feature coming soon!');
            break;
    }
}

function showFavoritesPage() {
    fetch('/api/favorites')
        .then(response => response.json())
        .then(data => {
            const movies = data.favorites || [];
            
            const mainContent = document.querySelector('.main');
            mainContent.innerHTML = `
                <header class="hero">
                    <div class="hero-left">
                        <h1>❤️ Your Favorites</h1>
                        <p>All your saved movies in one place.</p>
                    </div>
                </header>
                
                <section class="movie-section">
                    <div class="section-header">
                        <h2>Saved Movies (${movies.length})</h2>
                        <a href="#" onclick="location.reload(); return false;">Back to Home</a>
                    </div>
                    <div class="movie-grid">
                        ${movies.length > 0 ? movies.map(movie => createMovieCard(movie)).join('') : '<p>No favorites yet!</p>'}
                    </div>
                </section>
            `;
            
            setupMovieCardButtons();
        })
        .catch(error => console.error('Error loading favorites:', error));
}

// ============ STYLING FOR MODALS ============

const styles = `
.mood-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.mood-modal-content {
    background: #101827;
    border-radius: 22px;
    padding: 40px;
    max-width: 500px;
    width: 90%;
    position: relative;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.mood-modal-content h2 {
    font-size: 28px;
    margin-bottom: 10px;
    color: #fff;
}

.mood-modal-content p {
    color: #9aa5ba;
    margin-bottom: 25px;
}

.mood-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}

.mood-btn {
    background: #1a2540;
    border: 1px solid #2a3d5a;
    color: #fff;
    padding: 15px;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.3s;
    font-size: 14px;
}

.mood-btn:hover {
    background: #ff8c1a;
    border-color: #ff8c1a;
    transform: scale(1.05);
}

.close-modal {
    position: absolute;
    top: 15px;
    right: 15px;
    background: none;
    border: none;
    color: #9aa5ba;
    font-size: 24px;
    cursor: pointer;
}

.loading {
    text-align: center;
    padding: 40px;
    color: #9aa5ba;
    font-size: 18px;
}

.fav-btn {
    background: #ff8c1a;
}

.fav-btn i.fa-solid {
    color: #ff1744;
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);
