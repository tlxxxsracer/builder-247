"""
Dad Joke API Client Module

This module provides a client for fetching dad jokes from the icanhazdadjoke.com API.
"""

import requests
from typing import Dict, Optional
from .base_client import BaseClient


class DadJokeClient(BaseClient):
    """
    A client for interacting with the icanhazdadjoke.com API.

    Attributes:
        BASE_URL (str): The base URL for the Dad Joke API.
        HEADERS (Dict[str, str]): Standard headers for the API requests.
    """

    BASE_URL = "https://icanhazdadjoke.com"
    HEADERS = {
        "Accept": "application/json",
        "User-Agent": "Prometheus Swarm Dad Joke Client (https://github.com/your-repo)"
    }

    def get_random_joke(self) -> str:
        """
        Fetch a random dad joke from the API.

        Returns:
            str: A random dad joke text.

        Raises:
            requests.RequestException: If there's a network or API error.
            ValueError: If the joke cannot be retrieved.
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/",
                headers=self.HEADERS
            )
            response.raise_for_status()
            joke_data = response.json()
            
            if not joke_data or 'joke' not in joke_data:
                raise ValueError("No joke found in API response")
            
            return joke_data['joke']
        
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch dad joke: {str(e)}")

    def get_joke_by_id(self, joke_id: str) -> Optional[str]:
        """
        Fetch a specific dad joke by its ID.

        Args:
            joke_id (str): The unique identifier of the joke.

        Returns:
            Optional[str]: The joke text if found, None otherwise.

        Raises:
            requests.RequestException: If there's a network or API error.
            ValueError: If the joke ID is invalid.
        """
        if not joke_id:
            raise ValueError("Joke ID cannot be empty")

        try:
            response = requests.get(
                f"{self.BASE_URL}/j/{joke_id}",
                headers=self.HEADERS
            )
            response.raise_for_status()
            joke_data = response.json()
            
            return joke_data.get('joke')
        
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch joke with ID {joke_id}: {str(e)}")

    def search_jokes(self, term: str, limit: int = 30) -> Dict[str, list]:
        """
        Search for dad jokes containing a specific term.

        Args:
            term (str): The search term to find jokes.
            limit (int, optional): Maximum number of jokes to return. Defaults to 30.

        Returns:
            Dict[str, list]: A dictionary containing search results.

        Raises:
            requests.RequestException: If there's a network or API error.
            ValueError: If the search term is invalid.
        """
        if not term:
            raise ValueError("Search term cannot be empty")

        try:
            response = requests.get(
                f"{self.BASE_URL}/search",
                headers=self.HEADERS,
                params={"term": term, "limit": limit}
            )
            response.raise_for_status()
            search_data = response.json()
            
            return {
                "total_jokes": search_data.get('total_jokes', 0),
                "jokes": [joke['joke'] for joke in search_data.get('results', [])]
            }
        
        except requests.RequestException as e:
            raise ValueError(f"Failed to search jokes with term '{term}': {str(e)}")