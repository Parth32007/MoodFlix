"""
Flask integration tests for MoodFlix application.
Tests all routes, error handling, and request/response validation.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def app():
    """Create Flask app for testing."""
    from app import app
    
    # Create temporary storage directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Patch the storage directory
        with patch('src.favorites.FAVORITES_FILE', Path(tmpdir) / 'favorites.json'):
            app.config['TESTING'] = True
            yield app


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


class TestFlaskRoutes:
    """Test suite for Flask routes."""

    def test_home_get(self, client):
        """Test GET request to home page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'MoodFlix' in response.data or b'recommendations' in response.data

    @patch('app.recommend_hybrid')
    @patch('app.get_movie_details')
    def test_home_post_success(self, mock_get_details, mock_recommend, client):
        """Test successful POST request to home page."""
        mock_recommend.return_value = ['Movie A', 'Movie B']
        mock_get_details.return_value = {
            'title': 'Movie A',
            'poster': 'url',
            'rating': 8.0,
            'release_date': '2020-01-01',
            'overview': 'Test'
        }

        response = client.post('/', data={
            'movie': 'Test Movie',
            'mood': 'Happy'
        })

        assert response.status_code == 200

    def test_home_post_missing_fields(self, client):
        """Test POST request with missing required fields."""
        response = client.post('/', data={
            'movie': 'Test Movie'
            # Missing 'mood' field
        })

        assert response.status_code == 200

    def test_home_post_empty_fields(self, client):
        """Test POST request with empty fields."""
        response = client.post('/', data={
            'movie': '',
            'mood': ''
        })

        assert response.status_code == 200

    def test_favorite_post_success(self, client):
        """Test successful POST to /favorite endpoint."""
        response = client.post('/favorite',
            data=json.dumps({'movie': 'Test Movie'}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'

    def test_favorite_post_missing_json(self, client):
        """Test POST to /favorite without JSON body."""
        response = client.post('/favorite',
            data='not json',
            content_type='application/json'
        )

        assert response.status_code in [200, 400]

    def test_favorite_post_missing_movie_title(self, client):
        """Test POST to /favorite without movie title."""
        response = client.post('/favorite',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    def test_favorite_post_empty_movie_title(self, client):
        """Test POST to /favorite with empty movie title."""
        response = client.post('/favorite',
            data=json.dumps({'movie': ''}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    def test_get_favorites_success(self, client):
        """Test GET /favorites endpoint."""
        response = client.get('/favorites')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert isinstance(data['favorites'], list)

    def test_delete_favorite_success(self, client):
        """Test DELETE /favorite/<movie> endpoint."""
        # First add a favorite
        client.post('/favorite',
            data=json.dumps({'movie': 'Test Movie'}),
            content_type='application/json'
        )

        # Then delete it
        response = client.delete('/favorite/Test Movie')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'

    def test_delete_favorite_missing_title(self, client):
        """Test DELETE /favorite/ without title."""
        response = client.delete('/favorite/')

        assert response.status_code in [400, 404, 405]

    def test_delete_favorite_empty_title(self, client):
        """Test DELETE /favorite with empty title."""
        response = client.delete('/favorite/ ')

        assert response.status_code == 400

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent-route')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'

    @patch('app.home')
    def test_500_error(self, mock_home, client):
        """Test 500 error handling."""
        mock_home.side_effect = Exception("Test error")

        response = client.get('/')

        # Should handle the error gracefully
        assert response.status_code in [200, 500]


class TestInputValidation:
    """Test input validation and sanitization."""

    def test_validate_input_valid(self, client):
        """Test validation of valid input."""
        from app import validate_input

        is_valid, error = validate_input(
            {'field1': 'value1', 'field2': 'value2'},
            ['field1', 'field2']
        )

        assert is_valid is True
        assert error is None

    def test_validate_input_missing_field(self, client):
        """Test validation with missing required field."""
        from app import validate_input

        is_valid, error = validate_input(
            {'field1': 'value1'},
            ['field1', 'field2']
        )

        assert is_valid is False
        assert error is not None

    def test_validate_input_empty_field(self, client):
        """Test validation with empty required field."""
        from app import validate_input

        is_valid, error = validate_input(
            {'field1': '', 'field2': 'value2'},
            ['field1', 'field2']
        )

        assert is_valid is False
        assert error is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
