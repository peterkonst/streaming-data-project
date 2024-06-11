import json
from unittest.mock import patch, MagicMock
import pytest
from producer_consumer.producer import publish_to_kafka

@pytest.fixture
def articles():
    return [
        {"webPublicationDate": "2023-01-01T00:00:00Z", "webTitle": "Article 1", "webUrl": "http://example.com/1"},
        {"webPublicationDate": "2023-01-02T00:00:00Z", "webTitle": "Article 2", "webUrl": "http://example.com/2"},
    ]

@patch('producer_consumer.producer.KafkaProducer')
def test_publish_to_kafka(mock_kafka_producer, articles):
    mock_producer_instance = MagicMock()
    mock_kafka_producer.return_value = mock_producer_instance

    publish_to_kafka('test_topic', articles)

    args, kwargs = mock_kafka_producer.call_args
    assert kwargs['bootstrap_servers'] == 'localhost:9092'
    assert callable(kwargs['value_serializer'])

    for article in articles:
        mock_producer_instance.send.assert_any_call('test_topic', article)

    mock_producer_instance.flush.assert_called_once()

if __name__ == "__main__":
    pytest.main()
