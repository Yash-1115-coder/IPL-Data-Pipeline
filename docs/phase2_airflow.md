## ✅ Phase 2: Real-time Spark Streaming from Kafka to Console


## 🔥 Phase 2: Real-Time Streaming with Spark + Kafka

This phase establishes a robust data pipeline using **Apache Kafka** and **Apache Spark Structured Streaming**. It consumes IPL player data, processes it using Spark, and stores the streaming results to disk.

---

### ✅ Objectives
- Consume real-time data from Kafka topic: `airflow-topic`
- Parse JSON messages into structured format using Spark
- Stream the data into `.csv` files (local storage)
- Enable checkpointing for fault-tolerance

---

### 🧪 Prerequisites
- Docker & Docker Compose installed
- Apache Kafka container running (included in Phase 1)
- Spark image: `bitnami/spark:3.4.1`
- Required Kafka JARs + commons-pool2 jar in `./spark/jars/`:
  - `spark-sql-kafka-0-10_2.12-3.4.1.jar`
  - `spark-token-provider-kafka-0-10_2.12-3.4.1.jar`
  - `kafka-clients-3.4.0.jar`
  - `commons-pool2-2.11.1.jar`

---

### 🛠 File Architecture: `spark/spark_stream.py`


# Define schema
# Spark Session
# Read Kafka Stream
# Write stream to CSV


📦 Docker Compose Spark Block
Make sure your docker-compose.yaml includes this:
  spark:
    image: bitnami/spark:3.4.1
    container_name: spark
    environment:
      - SPARK_MODE=master
      - SPARK_EXTRA_CLASSPATH=/app/jars/*
    volumes:
      - ./spark:/app
    ports:
      - "4040:4040"
    networks:
      - airflow_net


🚀 Run Commands
# Inside project root
docker-compose up -d spark
docker exec -it spark bash
cd /app
spark-submit spark_stream.py


📂 Output Location
After running, the streamed CSVs will appear in:
./spark/artifacts/ipl_stream_output/


🛑 Known Issues / Fixes
NoClassDefFoundError for GenericKeyedObjectPoolConfig → FIXED by downloading commons-pool2 jar manually:
wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar -P ./spark/jars

Must --no-cache rebuild spark if any jars were added.
docker-compose build --no-cache spark
docker-compose up -d spark


🚫 Common Errors & Fixes
Error: Duplicate records
Cause: Kafka re-read old offsets
Fix: Clean the Kafka topic and the checkpoint folder before streaming again.

Error: Folder permission error
Cause: Docker folder access issues
Fix: Use mkdir -p to create folders, then run chmod -R 777 on them to grant permissions.

Error: UnknownTopicOrPartition
Cause: Topic was recreated but not yet fully initialized
Fix: Wait a few seconds after creating the topic before producing or consuming.

Error: Metadata file exists
Cause: .crc or temp files not cleaned inside the checkpoint directory
Fix: Delete all hidden files (.*) inside the checkpoint directory using:
rm -rf /path/to/checkpoint/* /path/to/checkpoint/.* 2>/dev/null



✅ Final Result
182 messages streamed to Kafka

Processed by Spark

Written to clean CSV files

No duplicates

Output ready for GCP ingestion