# PHASE 3 - GCS Bucket Integration for Spark Sink

## 🎯 Objective:
Stream the processed data from Spark into a Google Cloud Storage (GCS) bucket in CSV format using Spark Structured Streaming.

---

## ⚙️ Tools Used:
- Apache Spark (inside Docker container)
- Google Cloud Platform (GCS Bucket)
- GCP Service Account JSON Key
- spark-submit with GCS configs

---

## 🛠️ Steps Followed:

### ✅ 1. Created GCS Bucket

- Bucket name: `ipl-stream-output`
- Structure was created by Spark automatically:
```
ipl-stream-output/
 └── ipl_stream_output/
     ├── part-xxxxx.csv
     └── _spark_metadata/
```

---

### ✅ 2. Uploaded GCP Key to Spark container

- Service account key: `ipl-streaming-project-<...>.json`
- Dockerfile.spark included:
```dockerfile
COPY ./ipl-streaming-project-*.json /app/
```

---

### ✅ 3. Edited `spark_stream.py` to use GCS Sink

```python
df.writeStream \
  .format("csv") \
  .option("path", "gs://ipl-stream-output/ipl_stream_output/") \
  .option("checkpointLocation", "gs://ipl-stream-output/checkpoint") \
  .outputMode("append") \
  .start()
```

---

### ✅ 4. Launched Spark Streaming Job

```bash
docker exec -it spark bash

spark-submit \
  --conf spark.hadoop.google.cloud.auth.service.account.enable=true \
  --conf spark.hadoop.google.cloud.auth.service.account.json.keyfile=/app/ipl-streaming-project-<...>.json \
  spark_stream.py
```

---

## ✅ Verification:

- `part-xxxxx.csv` files started appearing in GCS
- Checkpoint folder also created for maintaining state

---

### 🚨 Troubleshooting Faced:
| Issue | Fix |
|------|-----|
| GCS write permission denied | Checked service account IAM permissions |
| Files not appearing | Spark wasn't streaming; checked logs |
| Metadata empty | Normal for first few batches |

---

## 💡 Outcome:
Structured streaming successfully wrote the processed IPL player data to the GCS bucket in real-time.
