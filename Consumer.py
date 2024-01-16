
#                       Received Data from Kafka
from confluent_kafka import Consumer, KafkaException
import json
import time

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'measurements'

# Consume and display weather measurements
def consume_and_display_measurements(consumer):
    consumer.subscribe([topic_name])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    # End of partition event (not an error)
                    continue
                else:
                    print(f'Error: {msg.error()}')
                    break
            else:
                try:
                    # Attempt to parse the JSON message
                    raw_message = msg.value().decode('utf-8').replace("'", '"')
                    # Parse the JSON message
                    data = json.loads(raw_message)
                    # Process and display the JSON message
                    print("\nReceived Heart Rate Measurement:")
                    print(f"Desired Training Intensity: {data.get('Desired Training Intensity', 'N/A')}")
                    print(f"Estimated Heart Rate: {data.get('Estimated Heart Rate', 'N/A')}")
                    print(f"Minimum Heart Rate: {data.get('Minimum Heart Rate', 'N/A')}")
                    print(f"Maximum Heart Rate: {data.get('Maximum Heart Rate', 'N/A')}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON message: {e}")
                    continue

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

# Main function to periodically or event-driven consume and display measurements
def main():
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'heartrate-consumer',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)

    try:
        consume_and_display_measurements_periodic(consumer)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def consume_and_display_measurements_periodic(consumer):
    while True:
        consume_and_display_measurements(consumer)
        # Sleep for 10 seconds (adjust as needed)
        time.sleep(10)

if __name__ == "__main__":
    main()
