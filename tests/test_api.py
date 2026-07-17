"""
Unit tests for the TMDB API module.
Tests API key validation, error handling, and response parsing.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.tmdb_api import fetch_movie_details


class TestTMDBApi:
    """Test suite for TMDB API functions."""

    @patch('src.tmdb_api.API_KEY', 'test-api-key')
    @patch('src.tmdb_api.session.get')
    def test_fetch_movie_details_success(self, mock_get):
        """Test successful movie details fetch."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{
                "title": "The Matrix",
                "poster_path": "/path/to/poster.jpg",
                "vote_average": 8.7,
                "release_date": "1999-03-31",
                "overview": "A hacker learns about the true nature of reality."
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_movie_details("The Matrix")

        assert result is not None
        assert result["title"] == "The Matrix"
        assert result["rating"] == 8.7
        assert result["release_date"] == "1999-03-31"
        assert result["poster"] == "https://image.tmdb.org/t/p/w500/path/to/poster.jpg"

    @patch('src.tmdb_api.session.get')
    def test_fetch_movie_details_not_found(self, mock_get):
        """Test movie not found."""
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_movie_details("NonexistentMovie12345")

        assert result is None

    def test_fetch_movie_details_invalid_input(self):
        """Test invalid movie name input."""
        result = fetch_movie_details("")
        assert result is None

        result = fetch_movie_details(None)
        assert result is None

        result = fetch_movie_details(123)
        assert result is None

    @patch('src.tmdb_api.API_KEY', '')
    def test_fetch_movie_details_no_api_key(self):
        """Test behavior when API key is not configured."""
        result = fetch_movie_details("The Matrix")
        assert result is None

    @patch('src.tmdb_api.session.get')
    def test_fetch_movie_details_network_error(self, mock_get):
        """Test network error handling."""
        mock_get.side_effect = Exception("Network error")

        result = fetch_movie_details("The Matrix")

        assert result is None

    @patch('src.tmdb_api.session.get')
    def test_fetch_movie_details_invalid_json(self, mock_get):
        """Test invalid JSON response handling."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_movie_details("The Matrix")

        assert result is None

    @patch('src.tmdb_api.API_KEY', 'test-api-key')
    @patch('src.tmdb_api.session.get')
    def test_fetch_movie_details_missing_fields(self, mock_get):
        """Test handling of missing optional fields."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{
                "title": "Minimal Movie"
                # Missing: poster_path, vote_average, etc.
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_movie_details("Minimal Movie")

        assert result is not None
        assert result["title"] == "Minimal Movie"
        assert result["poster"] == ""
        assert result["rating"] == "N/A"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
