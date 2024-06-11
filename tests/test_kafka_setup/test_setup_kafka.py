import os
from unittest.mock import patch, MagicMock
from kafka.errors import TopicAlreadyExistsError
import pytest
from producer_consumer.setup_kafka import create_kafka_topic

@patch('producer_consumer.setup_kafka.KafkaAdminClient')
def test_create_kafka_topic_success(mock_kafka_admin_client):
    mock_admin_instance = MagicMock()
    mock_kafka_admin_client.return_value = mock_admin_instance

    create_kafka_topic('test_topic')

    mock_admin_instance.create_topics.assert_called_once()
    args, kwargs = mock_admin_instance.create_topics.call_args
    assert kwargs['new_topics'][0].name == 'test_topic'

@patch('producer_consumer.setup_kafka.KafkaAdminClient')
def test_create_kafka_topic_already_exists(mock_kafka_admin_client):
    mock_admin_instance = MagicMock()
    mock_admin_instance.create_topics.side_effect = TopicAlreadyExistsError
    mock_kafka_admin_client.return_value = mock_admin_instance

    create_kafka_topic('test_topic')

    mock_admin_instance.create_topics.assert_called_once()


