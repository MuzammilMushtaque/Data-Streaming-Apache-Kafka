# Kafka and Python Application

This repository provides a simple guide to set up Apache Kafka using Docker Compose and demonstrates a basic Python application for producing and consuming heart rate data using Kafka.

## Installation

### Step 1: Install Docker and Docker Compose
Make sure you have Docker and Docker Compose installed on your system. You can follow the official documentation for [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) to install these tools.

### Step 2: Set up Kafka and Zookeeper

1. Start Kafka and Zookeeper services:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

6. Open new terminal, verify that the containers are running:
   ```bash
   docker ps
   ```

### Step 3: Configure Kafka Topics
1. Access the Kafka container's shell:
   ```bash
   docker exec -it kafka /bin/sh
   ```

2. Navigate to Kafka's bin directory:
   ```bash
   cd /opt/kafka/bin/
   ```

3. Create a Kafka topic named "measurements":
   ```bash
   ./kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic measurements
   ```

4. List the created Kafka topics:
   ```bash
   ./kafka-topics.sh --list --zookeeper zookeeper:2181
   ```

## Programming with Kafka

### Overview of Kafka APIs

Kafka provides APIs for both producers and consumers to interact with the messaging system. Key APIs include the Producer API for sending messages and the Consumer API for subscribing to and processing messages.

### Python Application

The repository includes a Python application that generates simulated human heartbeat data and sends it to the Kafka topic "measurements". Additionally, there is a separate Python script to consume and process the heartbeat data from the Kafka topic.

1. Producer: `producer.py`
   - Generates simulated heartbeat data and sends it to the Kafka topic.

2. Consumer: `consumer.py`
   - Connects to the Kafka topic and processes the received heartbeat data.

Feel free to explore and modify these Python scripts according to your requirements.

## Running the Python Application

Run the producer script to generate and send heartbeat data:
```bash
python producer.py
```

In a separate terminal, run the consumer script to receive and process the heartbeat data:
```bash
python consumer.py
```

Now, you should see the simulated heartbeat data being produced and consumed by the respective scripts.

Feel free to customize the scripts and experiment with different scenarios based on your use case.

**Note:** Make sure your Kafka and Zookeeper containers are still running before executing the Python scripts. You can cross check it if you have installed `Docker Desktop`.

