import os
import json
import ast
import pytest
from unittest.mock import patch, MagicMock
from producer_consumer.consumer import consume_from_kinesis
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError, BotoCoreError

from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv('AWS_REGION', 'eu-west-2')

@mock_aws
def test_main_functionality_of_consumer(mock_env_variables):
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

    with patch('logging.info') as mock_info:
        consume_from_kinesis(stream_name, max_records=2)

        assert mock_info.call_count == 2

        
        first_call_arg = mock_info.call_args_list[0][0][0]
        second_call_arg = mock_info.call_args_list[1][0][0]


        first_record = ast.literal_eval(first_call_arg.split("Received record: ")[1])
        second_record = ast.literal_eval(second_call_arg.split("Received record: ")[1])

        assert first_record['id'] == 'article-1'
        assert second_record['id'] == 'article-2'


@mock_aws
def test_consume_from_kinesis_exceeding_max_records(mock_env_variables):
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
        },
        {
            'Data': json.dumps({'id': 'article-3', 'content_preview': 'Article 3 content'}),
            'PartitionKey': 'partition_key'
        }
    ]

    for record in records:
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=record['Data'],
            PartitionKey=record['PartitionKey']
        )

    with patch('logging.info') as mock_info, patch('time.sleep', return_value=None):
        consume_from_kinesis(stream_name, max_records=2)

        assert mock_info.call_count == 2
        first_call_arg = mock_info.call_args_list[0][0][0]
        second_call_arg = mock_info.call_args_list[1][0][0]
        first_record = ast.literal_eval(first_call_arg.split("Received record: ")[1])
        second_record = ast.literal_eval(second_call_arg.split("Received record: ")[1])
        assert first_record['id'] == 'article-1'
        assert second_record['id'] == 'article-2'


