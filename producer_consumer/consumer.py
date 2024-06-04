import os
import json
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

def consume_from_kafka(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    for message in consumer:
        print(f"Received message: {message.value}")

if __name__ == "__main__":
    topic = 'guardian_content'
    consume_from_kafka(topic)

