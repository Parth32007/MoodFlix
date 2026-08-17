document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const views = document.querySelectorAll('.view');
  const viewLanding = document.getElementById('view-landing');
  const viewLoading = document.getElementById('view-loading');
  const viewRecommendations = document.getElementById('view-recommendations');
  
  const moodPills = document.querySelectorAll('.mood-pill');
  const customInput = document.getElementById('custom-mood-input');
  const referenceMovieInput = document.getElementById('reference-movie-input');
  const findMovieBtn = document.getElementById('find-movie-btn');
  const changeMoodBtn = document.getElementById('change-mood-btn');
  
  const displayDetectedMood = document.getElementById('display-detected-mood');
  const recommendationsGrid = document.getElementById('recommendations-grid');
  
  const topSearchBtn = document.getElementById('top-search-btn');
  const searchOverlay = document.getElementById('search-overlay');
  const closeSearchBtn = document.getElementById('close-search');
  
  const movieModal = document.getElementById('movie-modal');
  const closeModalBtn = document.getElementById('close-modal');
  const modalLayoutContent = document.getElementById('modal-layout-content');

  // State
  let selectedMoods = [];

  // Mock Movie Data
  const mockMovies = [
    {
      id: 1,
      title: 'Interstellar',
      year: 2014,
      rating: 8.7,
      genres: 'Sci-Fi • Drama • Adventure',
      overview: 'An emotional journey through space, time, and human connection. A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
      poster: 'https://placehold.co/300x450/0f0f19/ec4899?text=Interstellar',
      backdrop: 'https://placehold.co/900x300/0f0f19/3b82f6?text=Interstellar+Backdrop',
      match: 94
    },
    {
      id: 2,
      title: 'The Secret Life of Walter Mitty',
      year: 2013,
      rating: 7.3,
      genres: 'Adventure • Comedy • Drama',
      overview: 'When his job along with that of his co-worker are threatened, Walter takes action in the real world embarking on a global journey that turns into an adventure more extraordinary than anything he could have ever imagined.',
      poster: 'https://placehold.co/300x450/0f0f19/a855f7?text=Walter+Mitty',
      backdrop: 'https://placehold.co/900x300/0f0f19/ec4899?text=Walter+Mitty+Backdrop',
      match: 88
    },
    {
      id: 3,
      title: 'Everything Everywhere All at Once',
      year: 2022,
      rating: 7.8,
      genres: 'Action • Adventure • Comedy',
      overview: 'A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save existence by exploring other universes and connecting with the lives she could have led.',
      poster: 'https://placehold.co/300x450/0f0f19/3b82f6?text=EEAAO',
      backdrop: 'https://placehold.co/900x300/0f0f19/a855f7?text=EEAAO+Backdrop',
      match: 91
    },
    {
      id: 4,
      title: 'Arrival',
      year: 2016,
      rating: 7.9,
      genres: 'Drama • Sci-Fi • Mystery',
      overview: 'A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.',
      poster: 'https://placehold.co/300x450/0f0f19/ec4899?text=Arrival',
      backdrop: 'https://placehold.co/900x300/0f0f19/3b82f6?text=Arrival+Backdrop',
      match: 85
    }
  ];

  // --- MOOD SELECTION ---
  moodPills.forEach(pill => {
    pill.addEventListener('click', () => {
      // Toggle selection
      if (pill.classList.contains('selected')) {
        pill.classList.remove('selected');
        selectedMoods = selectedMoods.filter(m => m !== pill.dataset.mood);
      } else {
        pill.classList.add('selected');
        selectedMoods.push(pill.dataset.mood);
      }
    });
  });

  // --- NAVIGATION FLOW ---
  function switchView(targetViewId) {
    views.forEach(view => {
      view.classList.remove('active-view');
    });
    document.getElementById(targetViewId).classList.add('active-view');
  }

  findMovieBtn.addEventListener('click', () => {
    const customText = customInput.value.trim();
    const referenceMovie = referenceMovieInput.value.trim();
    if (selectedMoods.length === 0 && customText === '' && referenceMovie === '') {
      // Small shake animation if nothing is selected
      findMovieBtn.style.transform = 'translateX(-10px)';
      setTimeout(() => findMovieBtn.style.transform = 'translateX(10px)', 100);
      setTimeout(() => findMovieBtn.style.transform = 'translateX(0)', 200);
      return;
    }

    // Determine display mood
    let displayMood = '';
    if (customText) {
      displayMood = `"${customText}"`;
    } else if (selectedMoods.length > 0) {
      displayMood = selectedMoods.join(', ');
    } else {
      displayMood = 'Any mood';
    }
    
    if (referenceMovie) {
      displayMood += ` | Similar to: ${referenceMovie}`;
    }
    
    displayDetectedMood.textContent = displayMood;

    // Transition to Loading
    switchView('view-loading');

    // The backend ONLY accepts exactly one of 10 specific mood strings.
    const validBackendMoods = ["Happy", "Sad", "Romantic", "Excited", "Fear", "Relaxed", "Motivated", "Curious", "Lonely", "Inspired"];
    let backendMood = "Happy"; // Fallback
    
    // Find the first selected mood that is valid
    if (selectedMoods.length > 0) {
      backendMood = selectedMoods[0];
    } else if (customText) {
      // If user typed custom text, try to find a valid mood keyword in it
      const match = validBackendMoods.find(m => customText.toLowerCase().includes(m.toLowerCase()));
      if (match) backendMood = match;
    }

    // Fetch recommendations from real API
    fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // The API requires both. If user left referenceMovie empty, use a fallback like "Inception"
        movie: referenceMovie || 'Inception', 
        mood: backendMood
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success' && data.recommendations) {
        renderRecommendations(data.recommendations);
        switchView('view-recommendations');
      } else {
        alert("Error: " + (data.message || "Failed to find recommendations"));
        switchView('view-landing');
      }
    })
    .catch(err => {
      console.error(err);
      alert("Error connecting to AI engine.");
      switchView('view-landing');
    });
  });

  changeMoodBtn.addEventListener('click', () => {
    switchView('view-landing');
  });

  // --- RENDER RECOMMENDATIONS ---
  function renderRecommendations(movies = []) {
    recommendationsGrid.innerHTML = '';
    
    // If empty array passed, fallback to mockMovies for safety
    const moviesToRender = movies.length > 0 ? movies : mockMovies;
    
    moviesToRender.forEach((apiMovie, index) => {
      // Map API TMDB data to our frontend format
      const movie = {
        title: apiMovie.title || 'Unknown',
        year: apiMovie.release_date ? apiMovie.release_date.substring(0, 4) : 'N/A',
        rating: apiMovie.vote_average ? parseFloat(apiMovie.vote_average).toFixed(1) : 'N/A',
        genres: Array.isArray(apiMovie.genres) ? apiMovie.genres.join(' • ') : (apiMovie.genres || 'Film'),
        overview: apiMovie.overview || 'No description available.',
        poster: apiMovie.poster || (apiMovie.poster_path ? `https://image.tmdb.org/t/p/w500${apiMovie.poster_path}` : ''),
        backdrop: apiMovie.backdrop_path ? `https://image.tmdb.org/t/p/original${apiMovie.backdrop_path}` : '',
        match: 99 - (index * 2) // mock match percentage for visual flair
      };
      const card = document.createElement('div');
      card.className = 'movie-card';
      card.onclick = () => openModal(movie);

      let posterHtml = '';
      let badgeHtml = `<div class="match-badge" style="position:relative; top:auto; right:auto; align-self: flex-end; margin-bottom: 10px;">${movie.match}% Match</div>`;
      
      if (movie.poster) {
        posterHtml = `
        <div class="poster-container">
          <img src="${movie.poster}" alt="${movie.title}">
          <div class="match-badge">${movie.match}% Match</div>
        </div>`;
        badgeHtml = '';
      }

      card.innerHTML = `
        ${posterHtml}
        <div class="card-info" style="${!movie.poster ? 'padding-top: 15px;' : ''}">
          ${badgeHtml}
          <h3 class="card-title">${movie.title}</h3>
          <div class="card-meta">
            <span>${movie.year}</span>
            <span class="rating">⭐ ${movie.rating}</span>
          </div>
          <div class="card-genres">${movie.genres}</div>
          <p class="card-desc">${movie.overview}</p>
        </div>
      `;
      recommendationsGrid.appendChild(card);
    });
  }

  // --- MODAL & DETAILS ---
  function openModal(movie) {
    const activeMoods = selectedMoods.length > 0 ? selectedMoods.join(', ') : 'your mood';
    
    modalLayoutContent.innerHTML = `
      <div class="modal-backdrop" style="${movie.backdrop ? `background-image: url('${movie.backdrop}')` : 'display:none;'}"></div>
      <div class="modal-details" style="${!movie.backdrop ? 'margin-top: 2rem;' : ''}">
        ${movie.poster ? `<img src="${movie.poster}" alt="${movie.title}" class="modal-poster">` : ''}
        <div class="modal-info">
          <h2 class="modal-title">${movie.title}</h2>
          <div class="modal-tags">
            <span>${movie.year}</span>
            <span style="color: #fbbf24">⭐ ${movie.rating}/10</span>
            <span>${movie.genres}</span>
          </div>
          <p class="modal-overview">${movie.overview}</p>
          
          <div class="why-match-box">
            <h4>Why we recommend this</h4>
            <p>"Based on ${activeMoods}, we prioritized this film for its perfect blend of emotional storytelling and immersive visuals, matching your vibe at a ${movie.match}% level."</p>
          </div>

          <div class="modal-actions">
            <button class="neon-btn">
              <i class="fa-solid fa-play"></i> Watch Trailer
            </button>
            <button class="btn-secondary" onclick="document.getElementById('movie-modal').classList.remove('active')">
              Back to Recommendations
            </button>
          </div>
        </div>
      </div>
    `;
    movieModal.classList.add('active');
  }

  closeModalBtn.addEventListener('click', () => {
    movieModal.classList.remove('active');
  });

  // --- SEARCH OVERLAY ---
  topSearchBtn.addEventListener('click', (e) => {
    e.preventDefault();
    searchOverlay.classList.add('active');
    document.getElementById('global-search-input').focus();
  });

  closeSearchBtn.addEventListener('click', () => {
    searchOverlay.classList.remove('active');
  });

});
