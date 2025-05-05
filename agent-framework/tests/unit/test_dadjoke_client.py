"""
Unit tests for the Dad Joke API Client.
"""

import pytest
import requests_mock
from prometheus_swarm.clients.dadjoke_client import DadJokeClient


@pytest.fixture
def dadjoke_client():
    """Fixture to create a DadJokeClient instance for testing."""
    return DadJokeClient()


def test_get_random_joke_success(dadjoke_client):
    """Test successful retrieval of a random joke."""
    with requests_mock.Mocker() as m:
        mock_joke = {"joke": "Why do programmers prefer dark mode? Because light attracts bugs!"}
        m.get("https://icanhazdadjoke.com/", json=mock_joke)

        joke = dadjoke_client.get_random_joke()
        assert joke == mock_joke["joke"]


def test_get_random_joke_api_error(dadjoke_client):
    """Test error handling when API request fails."""
    with requests_mock.Mocker() as m:
        m.get("https://icanhazdadjoke.com/", status_code=500)

        with pytest.raises(ValueError, match="Failed to fetch dad joke"):
            dadjoke_client.get_random_joke()


def test_get_random_joke_empty_response(dadjoke_client):
    """Test handling of empty API response."""
    with requests_mock.Mocker() as m:
        m.get("https://icanhazdadjoke.com/", json={})

        with pytest.raises(ValueError, match="No joke found in API response"):
            dadjoke_client.get_random_joke()


def test_get_joke_by_id_success(dadjoke_client):
    """Test successful retrieval of a joke by ID."""
    joke_id = "abc123"
    with requests_mock.Mocker() as m:
        mock_joke = {"id": joke_id, "joke": "Programmer's favorite dance? An algo-rhythm!"}
        m.get(f"https://icanhazdadjoke.com/j/{joke_id}", json=mock_joke)

        joke = dadjoke_client.get_joke_by_id(joke_id)
        assert joke == mock_joke["joke"]


def test_get_joke_by_id_empty_id(dadjoke_client):
    """Test error handling for empty joke ID."""
    with pytest.raises(ValueError, match="Joke ID cannot be empty"):
        dadjoke_client.get_joke_by_id("")


def test_search_jokes_success(dadjoke_client):
    """Test successful joke search."""
    search_term = "programmer"
    with requests_mock.Mocker() as m:
        mock_search_result = {
            "results": [
                {"joke": "Why do programmers prefer dark mode?"},
                {"joke": "Programming jokes are the best!"}
            ],
            "total_jokes": 2
        }
        m.get("https://icanhazdadjoke.com/search", json=mock_search_result)

        search_results = dadjoke_client.search_jokes(search_term)
        
        assert search_results["total_jokes"] == 2
        assert len(search_results["jokes"]) == 2
        assert all("programmer" in joke.lower() for joke in search_results["jokes"])


def test_search_jokes_empty_term(dadjoke_client):
    """Test error handling for empty search term."""
    with pytest.raises(ValueError, match="Search term cannot be empty"):
        dadjoke_client.search_jokes("")


def test_search_jokes_no_results(dadjoke_client):
    """Test handling of search with no results."""
    search_term = "nonexistent"
    with requests_mock.Mocker() as m:
        mock_search_result = {
            "results": [],
            "total_jokes": 0
        }
        m.get("https://icanhazdadjoke.com/search", json=mock_search_result)

        search_results = dadjoke_client.search_jokes(search_term)
        
        assert search_results["total_jokes"] == 0
        assert len(search_results["jokes"]) == 0