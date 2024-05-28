from guardian_api.get_guardian_articles import get_guardian_articles
import os
from dotenv import load_dotenv
import pytest
from requests.exceptions import HTTPError


# Load environment variables from .env file
load_dotenv()

@pytest.mark.parametrize("search_term, date_from, expected_count", [
    ("machine learning", "2023-01-01", 10),  # Example parameters and expected count
    # Add more parameter sets and expected counts as needed
])
def test_get_guardian_articles(search_term, date_from, expected_count):
    # Get API key from environment variable
    api_key = os.getenv('GUARDIAN_API_KEY')

    # Call the function with the actual API key
    articles = get_guardian_articles(api_key=api_key, search_term=search_term, date_from=date_from)
    
    # Assert that the number of articles returned matches the expected count
    assert len(articles) == expected_count

def test_invalid_api_key():
    invalid_api_key = "key"
    with pytest.raises(HTTPError):
        get_guardian_articles(api_key=invalid_api_key, search_term='machine learning')

def test_returns_no_valid_search_results():
    api_key = os.getenv('GUARDIAN_API_KEY')
    articles = get_guardian_articles(api_key=api_key, search_term='shouldnevereverreturnaresponse12345')
    assert len(articles) == 0

def test_raises_error_when_invalid_date_is_passes():
    api_key = os.getenv('GUARDIAN_API_KEY')
    with pytest.raises(HTTPError):
        get_guardian_articles(api_key=api_key, search_term='learning', date_from='1223445')
    