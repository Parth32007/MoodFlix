"""
Unit tests for the recommendation engine.
Tests content-based, mood-based, and hybrid recommendation algorithms.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock


class TestRecommender:
    """Test suite for recommendation engine."""

    @pytest.fixture
    def mock_models(self):
        """Fixture for mocked model files."""
        # Create mock data
        movies_df = pd.DataFrame({
            'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
            'tags': ['action adventure', 'drama', 'action sci-fi', 'comedy', 'horror thriller']
        })

        similarity = np.array([
            [1.0, 0.2, 0.8, 0.1, 0.0],
            [0.2, 1.0, 0.1, 0.9, 0.3],
            [0.8, 0.1, 1.0, 0.0, 0.2],
            [0.1, 0.9, 0.0, 1.0, 0.4],
            [0.0, 0.3, 0.2, 0.4, 1.0]
        ])

        vectorizer = Mock()

        return movies_df, similarity, vectorizer

    @patch('src.recommender._load_models')
    def test_recommend_exact_match(self, mock_load, mock_models):
        """Test content-based recommendation with exact movie match."""
        from src.recommender import recommend

        mock_load.return_value = mock_models

        result = recommend("Movie A")

        assert result is not None
        assert len(result) > 0
        assert "Movie A" not in result  # Should not include input movie

    @patch('src.recommender._load_models')
    def test_recommend_movie_not_found(self, mock_load, mock_models):
        """Test recommendation when movie not found."""
        from src.recommender import recommend

        mock_load.return_value = mock_models

        result = recommend("Nonexistent Movie")

        assert result == []

    @patch('src.recommender._load_models')
    def test_recommend_by_mood_valid_mood(self, mock_load, mock_models):
        """Test mood-based recommendation with valid mood."""
        from src.recommender import recommend_by_mood

        mock_load.return_value = mock_models

        result = recommend_by_mood("Movie A", "Happy")

        # Should return recommendations or empty list
        assert isinstance(result, list)

    @patch('src.recommender._load_models')
    def test_recommend_by_mood_invalid_mood(self, mock_load, mock_models):
        """Test mood-based recommendation with invalid mood."""
        from src.recommender import recommend_by_mood

        mock_load.return_value = mock_models

        result = recommend_by_mood("Movie A", "InvalidMood123")

        assert result == []

    @patch('src.recommender._load_models')
    def test_recommend_hybrid_case_insensitive_match(self, mock_load, mock_models):
        """Test hybrid recommendation with case-insensitive matching."""
        from src.recommender import recommend_hybrid

        mock_load.return_value = mock_models

        result = recommend_hybrid("movie a", "Happy")

        assert isinstance(result, list)

    @patch('src.recommender._load_models')
    def test_recommend_hybrid_partial_match(self, mock_load, mock_models):
        """Test hybrid recommendation with partial movie name match."""
        from src.recommender import recommend_hybrid

        mock_load.return_value = mock_models

        result = recommend_hybrid("Movie", "Happy")

        # Should find partial matches
        assert isinstance(result, list)

    @patch('src.recommender._load_models')
    def test_recommend_hybrid_no_match(self, mock_load, mock_models):
        """Test hybrid recommendation when no movie found."""
        from src.recommender import recommend_hybrid

        mock_load.return_value = mock_models

        result = recommend_hybrid("xyz123nonexistent", "Happy")

        assert result == []

    @patch('src.recommender._load_models')
    def test_recommend_hybrid_invalid_mood(self, mock_load, mock_models):
        """Test hybrid recommendation with invalid mood."""
        from src.recommender import recommend_hybrid

        mock_load.return_value = mock_models

        result = recommend_hybrid("Movie A", "InvalidMood")

        assert result == []

    @patch('src.recommender._load_models')
    def test_recommend_hybrid_returns_top_n(self, mock_load, mock_models):
        """Test that hybrid recommendation returns correct number of results."""
        from src.recommender import recommend_hybrid
        from config import RECOMMENDATION_COUNT

        mock_load.return_value = mock_models

        result = recommend_hybrid("Movie A", "Happy")

        assert len(result) <= RECOMMENDATION_COUNT

    @patch('src.recommender._load_models')
    def test_models_load_failure(self, mock_load, mock_models):
        """Test behavior when model loading fails."""
        from src.recommender import recommend

        mock_load.return_value = (None, None, None)

        result = recommend("Movie A")

        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
