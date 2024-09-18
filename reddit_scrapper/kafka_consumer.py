"""Create a Kafka consumer that stores Reddit comments in a database."""

import json  # Standard library import
from kafka import KafkaConsumer  # Third-party import
from setup_database import create_connection, insert_comment  # Local imports

def consume_messages():
    """
    Consume messages from a Kafka topic and store them in a database.

    The consumer listens to the 'reddit_comments' topic, deserializes the
    messages, and inserts the comment data into the database.
    """
    consumer = KafkaConsumer(
        'reddit_comments',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='comment_storage_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    conn = create_connection()
    if conn is None:
        return

    try:
        for message in consumer:
            comment = message.value
            comment_data = (
                comment['id'],
                comment['body'],
                comment.get('created_utc', None),
                comment.get('score', None)
            )
            insert_comment(conn, comment_data)
            print(f"Stored comment {comment['id']} in database")
    except KeyboardInterrupt:
        print("Stopping the consumer...")
    finally:
        consumer.close()
        conn.close()

if __name__ == "__main__":
    consume_messages()
