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

### 🛠 File: `spark/spark_stream.py`

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# Define schema
schema = StructType() \
    .add("Player", StringType()) \
    .add("COUNTRY", StringType()) \
    .add("TEAM", StringType()) \
    .add("AGE", IntegerType()) \
    .add("SOLD_PRICE", StringType())

# Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read Kafka Stream
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "airflow-topic") \
    .option("startingOffsets", "earliest") \
    .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json(col("json_value"), schema).alias("data")) \
    .select("data.*")

# Write stream to CSV
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", "/app/artifacts/ipl_stream_output") \
    .option("checkpointLocation", "/app/checkpoint/ipl") \
    .start()

query.awaitTermination()


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


💪 Result
You now have a realtime pipeline from Kafka → Spark → CSV ✅
Structured, checkpointed, and fault-tolerant
Sets up perfectly for Airflow orchestration in Phase 3