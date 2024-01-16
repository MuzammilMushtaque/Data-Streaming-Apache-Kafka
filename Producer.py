#                      Send Message to Kafka
import random
import time
from confluent_kafka import Producer, KafkaException

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'measurements'

#                      Develop Python Application to Calculate the Target Heart Rate of Human being
# Reference: https://www.heartonline.org.au/resources/calculators/target-heart-rate-calculator


def Target_Heart_Rate(age, HR_rest):
    '''
    Target Heart Rate (THR) range values are often calculated to ensure exercise intensity is 
    maintained at a desired level. This calculator automatically calculates THR ranges.
    The Karvonen formula is often used for this purpose and calculates results as a function of 
    heart rate reserve (HRR) and maximum heart rate (HRmax).
    '''
    desired_training_intensity_ranges = {
        'Very Light': (1.0, 19.0),
        'Light': (20.0, 39.0),
        'Moderate': (40.0, 59.0),
        'Hard': (60.0, 84.0),
        'Very Hard': (85.0, 100.0)
    }

    desired_training_intensity = random.choice(list(desired_training_intensity_ranges.keys()))
    desired_training_intensity_min, desired_training_intensity_max = desired_training_intensity_ranges[desired_training_intensity]
    desired_training_intensity_current = random.uniform(desired_training_intensity_min, desired_training_intensity_max)

    HRmax = 220. - age
    HRR = HRmax - HR_rest
    
    '''
    Target HR range is calculated as follows:
    '''
    THRR_current = (HRR * desired_training_intensity_current/100) + HR_rest
    THRR_min = (HRR * desired_training_intensity_min/100) + HR_rest
    THRR_max = (HRR * desired_training_intensity_max/100) + HR_rest
    
    return [desired_training_intensity, THRR_current, THRR_min, THRR_max]

# Produce a Heart Rate Data to the Kafka topic
def produce_HeartRate_measurement(producer):
    data = Target_Heart_Rate(32, 60.)

    # Construct a JSON message with weather data
    message = {
        "Desired Training Intensity": data[0],
        "Estimated Heart Rate": data[1],
        "Minimum Heart Rate": data[2],
        "Maximum Heart Rate": data[3]
    }

    try:
        producer.produce(topic=topic_name, value=str(message))
        producer.flush()
        print(f"Produced message: {message}")
    except KafkaException as e:
        print(f"Error producing message: {e}")

# Main function to periodically produce Heart Rate measurements
def main():
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': 'heartrate-producer'
    }

    producer = Producer(producer_conf)

    try:
        while True:
            # Produce a Heart Rate measurement every 30 sec interval
            produce_HeartRate_measurement(producer)
            time.sleep(30)

    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main()
