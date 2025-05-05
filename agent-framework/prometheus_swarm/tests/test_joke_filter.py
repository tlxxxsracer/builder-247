"""
Test suite for the JokeFilter utility.
"""
import pytest
from prometheus_swarm.utils.joke_filter import JokeFilter

@pytest.fixture
def sample_jokes():
    """Provide a standard set of sample jokes for testing."""
    return [
        {"text": "Why did the scarecrow win an award? Because he was outstanding in his field!"},
        {"text": "I told my wife she was drawing her eyebrows too high. She looked surprised."},
        {"text": "Why don't scientists trust atoms? Because they make up everything!"},
        {"text": "Short joke."},
        {"text": "Very long joke that goes on and on and on about something completely ridiculous and might bore you to tears before getting to any actual punchline."}
    ]

def test_filter_max_length(sample_jokes):
    """Test filtering jokes by maximum length."""
    filtered = JokeFilter.filter_jokes(sample_jokes, max_length=30)
    assert len(filtered) == 2
    assert all(len(joke['text']) <= 30 for joke in filtered)

def test_filter_min_length(sample_jokes):
    """Test filtering jokes by minimum length."""
    filtered = JokeFilter.filter_jokes(sample_jokes, min_length=20)
    assert len(filtered) == 4
    assert all(len(joke['text']) >= 20 for joke in filtered)

def test_exclude_keywords(sample_jokes):
    """Test filtering out jokes with specific keywords."""
    filtered = JokeFilter.filter_jokes(sample_jokes, exclude_keywords=['award', 'atoms'])
    assert len(filtered) == 3
    assert all('award' not in joke['text'].lower() and 'atoms' not in joke['text'].lower() for joke in filtered)

def test_include_keywords(sample_jokes):
    """Test filtering to include only jokes with specific keywords."""
    filtered = JokeFilter.filter_jokes(sample_jokes, include_keywords=['why'])
    assert len(filtered) == 2
    assert all('why' in joke['text'].lower() for joke in filtered)

def test_combine_filters(sample_jokes):
    """Test combining multiple filtering criteria."""
    filtered = JokeFilter.filter_jokes(
        sample_jokes, 
        max_length=50, 
        min_length=10, 
        exclude_keywords=['surprised'],
        include_keywords=['why']
    )
    assert len(filtered) == 1
    assert 'why don\'t scientists trust atoms' in filtered[0]['text'].lower()

def test_empty_input():
    """Test that an empty list returns an empty list."""
    assert JokeFilter.filter_jokes([]) == []

def test_no_filters(sample_jokes):
    """Test that without any filters, all jokes are returned."""
    filtered = JokeFilter.filter_jokes(sample_jokes)
    assert len(filtered) == len(sample_jokes)

def test_case_insensitivity(sample_jokes):
    """Test that keyword filtering is case-insensitive."""
    filtered = JokeFilter.filter_jokes(sample_jokes, include_keywords=['JOKE'])
    assert len(filtered) == 2
    assert all('joke' in joke['text'].lower() for joke in filtered)