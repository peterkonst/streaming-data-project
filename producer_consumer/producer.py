import os
import requests
import json
import logging
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError, BotoCoreError

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


def get_guardian_articles(api_key, search_term, date_from=None):
    """
    Fetches articles from The Guardian API based on their search criteria.

    Args:
    - api_key(str): API key for accessing The Guardian API.
    - search_term (str): Term to search for in article content.
    - date_from (str, optional): Start date for filtering articles.

    Returns:
    - list: List of articles fetched from the API.
    Each article is a dictionary.

    Raises:
    - requests.RequestsException: If an occurs during the API request.

    Notes:
    - Retrieves up to 10 articles per request.
    - Adds a 'content_preview' field to each article containing
    the first 1000 characters of the article body.
    """

    url = "https://content.guardianapis.com/search"
    params = {
        'q': search_term,
        'from-date': date_from,
        'api-key': api_key,
        'page-size': 10,
        'show-fields': 'body'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()['response']['results']
        for article in results:
            article['content_preview'] = article['fields']['body'][:1000]
        return results
    except requests.RequestException as e:
        logging.error(f"Error fetching articles: {e}")
        return []


def publish_to_kinesis(stream_name, articles):
    kinesis_client = boto3.client('kinesis')
    for article in articles:
        try:
            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(article),
                PartitionKey="partition_key"
            )
            logging.info(f"Published article to Kinesis: {article['id']}")
        except (ClientError, BotoCoreError) as e:
            logging.error(f"Error publishing to Kinesis: {e}")


def main():
    stream_name = 'guardian_content'
    api_key = os.getenv('GUARDIAN_API_KEY')

    if not api_key:
        logging.error("""Guardian API key is not set.
                      Please set the GUARDIAN_API_KEY environment variable.""")
        return

    articles = get_guardian_articles(api_key=api_key,
                                     search_term='machine learning',
                                     date_from='2023-01-01')
    if articles:
        publish_to_kinesis(stream_name, articles)
    else:
        logging.warning("No articles retrieved or failed to fetch articles.")


if __name__ == "__main__":
    main()
