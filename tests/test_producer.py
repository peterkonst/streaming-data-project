import os
import json
import requests
import pytest
from unittest.mock import patch, MagicMock
from producer_consumer.producer import get_guardian_articles, publish_to_kinesis
import boto3
from moto import mock_aws

from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv('GUARDIAN_API_KEY', 'test_api_key')

@patch('requests.get')
def test_get_guardian_articles_success(mock_get, mock_env_variables):

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'response': {
            'results': [
                {
                    'id': 'article-1',
                    'fields': {'body': 'This is the body of the article 1'}
                },
                {
                    'id': 'article-2',
                    'fields': {'body': 'This is the body of the article 2'}
                }
            ]
        }
    }
    mock_get.return_value = mock_response

    api_key = os.getenv('GUARDIAN_API_KEY')
    articles = get_guardian_articles(api_key, 'machine learning', '2023-01-01')

    assert len(articles) == 2
    assert articles[0]['id'] == 'article-1'
    assert 'content_preview' in articles[0]
    assert articles[0]['content_preview'] == 'This is the body of the article 1'

@patch('requests.get')
def test_get_guardian_articles_failure(mock_get, mock_env_variables):
    # Mock a failed API response
    mock_get.side_effect = requests.RequestException("API request failed")

    api_key = os.getenv('GUARDIAN_API_KEY')
    articles = get_guardian_articles(api_key, 'machine learning', '2023-01-01')

    assert len(articles) == 0

@mock_aws
def test_publish_to_kinesis(mock_env_variables):
    
    stream_name = 'test_stream'
    kinesis_client = boto3.client('kinesis', region_name='eu-west-2')
    kinesis_client.create_stream(StreamName=stream_name, ShardCount=1)

    articles = [
        {
            'id': 'article-1',
            'content_preview': 'This is the body of the article 1'
        },
        {
            'id': 'article-2',
            'content_preview': 'This is the body of the article 2'
        }
    ]

    publish_to_kinesis(stream_name, articles)

    response = kinesis_client.describe_stream(StreamName=stream_name)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']
    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )['ShardIterator']
    records_response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)

    assert len(records_response['Records']) == 2
    record_data_1 = json.loads(records_response['Records'][0]['Data'])
    assert record_data_1['id'] == 'article-1'
    record_data_2 = json.loads(records_response['Records'][1]['Data'])
    assert record_data_2['id'] == 'article-2'

