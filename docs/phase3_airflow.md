# 📦 Phase 3 – Kafka to Spark Streaming Pipeline

## ✅ Objective
Stream the IPL data from Kafka to Apache Spark, transform and clean it, then write to CSV format in real-time.

---

## 🔧 Components Used
- **Apache Kafka**: Data Source (Kafka Topic: `airflow-topic`)
- **Apache Spark (Structured Streaming)**: Streaming processor
- **Docker**: Environment for Kafka, Spark
- **CSV Output**: Saved to `/app/artifacts/ipl_stream_output`
- **Checkpointing**: Managed in `/app/artifacts/checkpoint`

---

## ⚙️ Spark Streaming Logic

```python
# spark_stream.py
spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "airflow-topic") \
    .option("startingOffsets", "earliest") \
    .load() \
    ...
    .writeStream \
    .format("csv") \
    .option("path", "/app/artifacts/ipl_stream_output") \
    .option("checkpointLocation", "/app/artifacts/checkpoint") \
    .start()


📁 Output Example

Output folder: /app/artifacts/ipl_stream_output
CSV Files: part-*.csv
Number of records: 182 (excluding headers)
Header: Only present in one file

🧹 Clean-Up Before Each Run
bash
Copy code
# Inside spark container:
rm -rf /app/artifacts/ipl_stream_output/*
rm -rf /app/artifacts/checkpoint/*

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