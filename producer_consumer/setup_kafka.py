from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import os

def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = KafkaAdminClient(
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        client_id='kafka-admin'
    )
    
    topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print(f"Topic '{topic_name}' created successfully")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists")

if __name__ == "__main__":
    topic = 'guardian_content'
    create_kafka_topic(topic)

