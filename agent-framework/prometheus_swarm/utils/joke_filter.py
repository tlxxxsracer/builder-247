"""
Module for filtering and managing jokes based on various criteria.
"""
from typing import List, Dict, Optional

class JokeFilter:
    """
    A utility class for filtering jokes based on specific criteria.
    """
    
    @staticmethod
    def filter_jokes(
        jokes: List[Dict[str, str]], 
        max_length: Optional[int] = None, 
        min_length: Optional[int] = None, 
        exclude_keywords: Optional[List[str]] = None,
        include_keywords: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """
        Filter jokes based on multiple optional criteria.
        
        Args:
            jokes (List[Dict[str, str]]): List of joke dictionaries
            max_length (Optional[int]): Maximum allowed joke length
            min_length (Optional[int]): Minimum allowed joke length
            exclude_keywords (Optional[List[str]]): Keywords to exclude
            include_keywords (Optional[List[str]]): Keywords that must be present
        
        Returns:
            List[Dict[str, str]]: Filtered list of jokes
        """
        if not jokes:
            return []
        
        exclude_keywords = exclude_keywords or []
        include_keywords = include_keywords or []
        
        # Convert all keywords to lowercase for case-insensitive matching
        exclude_keywords = [kw.lower() for kw in exclude_keywords]
        include_keywords = [kw.lower() for kw in include_keywords]
        
        filtered_jokes = []
        
        for joke in jokes:
            # Check joke text for each criterion
            joke_text = joke.get('text', '').lower()
            
            # Length checks
            if max_length is not None and len(joke_text) > max_length:
                continue
            
            if min_length is not None and len(joke_text) < min_length:
                continue
            
            # Exclude keywords check
            if any(kw in joke_text for kw in exclude_keywords):
                continue
            
            # Include keywords check
            if include_keywords and not any(kw in joke_text for kw in include_keywords):
                continue
            
            filtered_jokes.append(joke)
        
        return filtered_jokes