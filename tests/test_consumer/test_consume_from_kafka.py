import os
import json
from unittest.mock import patch, MagicMock, ANY
from kafka import KafkaProducer
from producer_consumer.consumer import consume_from_kafka


def test_consume_from_kafka():
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('guardian_content', {'webPublicationDate': '2023-11-21T11:11:31Z',
                                       'webTitle': 'Test Article',
                                       'webUrl': 'https://example.com/test-article'})
    producer.flush()

    with patch('producer_consumer.consumer.KafkaConsumer') as mock_consumer:
        mock_consumer_instance = MagicMock()
        mock_consumer.return_value = mock_consumer_instance

        consume_from_kafka('guardian_content')

        mock_consumer.assert_called_once_with(
            'guardian_content',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=ANY
        )

        assert mock_consumer_instance.__iter__.called

