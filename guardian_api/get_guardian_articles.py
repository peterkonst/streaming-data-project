from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_guardian_articles(api_key, search_term, date_from=None):
    url = "https://content.guardianapis.com/search"
    params = {
        'q': search_term,
        'from-date': date_from,
        'api-key': api_key,
        'page-size': 10,
        'show-fields': 'body'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()['response']['results']
    for article in results:
        article['content_preview'] = article['fields']['body'][:1000]
    print(results)
    return results

api_key = os.getenv('GUARDIAN_API_KEY')

get_guardian_articles(api_key=api_key, search_term='learning', date_from=None )


