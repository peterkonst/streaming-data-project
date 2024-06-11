import os
import requests
import json
from dotenv import load_dotenv
from kafka import KafkaProducer
from producer_consumer.setup_kafka import create_kafka_topic

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
    return results

def publish_to_kafka(topic, articles):
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    for article in articles:
        producer.send(topic, article)
    producer.flush()

if __name__ == "__main__":
    topic = 'guardian_content'
    create_kafka_topic(topic)

    api_key = os.getenv('GUARDIAN_API_KEY')
    articles = get_guardian_articles(api_key=api_key, search_term='machine learning', date_from='2023-01-01')
    publish_to_kafka(topic, articles)




