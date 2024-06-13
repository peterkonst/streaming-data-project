import os
import json
import pytest
from unittest.mock import patch, MagicMock
from producer_consumer.consumer import consume_from_kinesis
import boto3
from moto import mock_aws

from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv('AWS_REGION', 'eu-west-2')  

@mock_aws
def test_consume_from_kinesis(mock_env_variables):

    stream_name = 'test_stream'
    kinesis_client = boto3.client('kinesis', region_name='eu-west-2')
    kinesis_client.create_stream(StreamName=stream_name, ShardCount=1)

    records = [
        {
            'Data': json.dumps({'id': 'article-1', 'content_preview': 'Article 1 content'}),
            'PartitionKey': 'partition_key'
        },
        {
            'Data': json.dumps({'id': 'article-2', 'content_preview': 'Article 2 content'}),
            'PartitionKey': 'partition_key'
        }
    ]

    for record in records:
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=record['Data'],
            PartitionKey=record['PartitionKey']
        )

    with patch('builtins.print') as mock_print:
        consume_from_kinesis(stream_name)

        assert mock_print.call_count == 2
        assert json.loads(mock_print.call_args_list[0].args[0])['id'] == 'article-1'
        assert json.loads(mock_print.call_args_list[1].args[0])['id'] == 'article-2'
