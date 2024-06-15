import json
import boto3
import time
import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError, BotoCoreError

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


def consume_from_kinesis(stream_name, max_records=float('inf')):
    """
    This function consumes records from a Kinesis stream and
    logs the received records.

    It continously fetches records from the specified Kinesis stream
    and logs each received records until a specified maximum number
    of records is reached or there are no more records to fecth

    Args:
        stream_name(str): The name of the Kinesis stream to
        consume records from.
        max_records (int, optional): The maximum number of records to process.
            Defaults to float ('inf'),
            which means there is no limit (for testing purposes)

    Returns:
        None

    Raises:
        botocore.exceptions.ClientError:
        If an error occurs while fetching records from Kinesis
        botocore.exceptions.BotoCoreError:
        If a low-level error occurs in the boto3 client.

    """
    kinesis_client = boto3.client('kinesis')
    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId='shardId-000000000000',
        ShardIteratorType='TRIM_HORIZON'
    )['ShardIterator']

    records_processed = 0

    while True:
        try:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=10
            )
            for record in response['Records']:
                data = json.loads(record['Data'])
                logging.info(f"Received record: {data}")
                records_processed += 1
                if max_records and records_processed >= max_records:
                    return

            shard_iterator = response['NextShardIterator']
            if not shard_iterator:
                logging.warning("Shard iterator is None. Exiting...")
                break

            # Sleep for a short interval before fetching more records
            time.sleep(1)

        except (ClientError, BotoCoreError) as e:
            logging.error(f"Error fetching records: {e}")
            time.sleep(5)
        except KeyboardInterrupt:
            logging.info("Consumer interrupted. Exiting...")
            break


def main():
    stream_name = 'guardian_content'
    consume_from_kinesis(stream_name)


if __name__ == "__main__":
    main()
