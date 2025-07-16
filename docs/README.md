# 🏏 IPL Data Engineering Pipeline Project

A complete end-to-end real-time data engineering pipeline to stream IPL player statistics from Kafka, process it with Spark, store it in BigQuery, and visualize it on Looker Studio.

---

## 📌 Project Overview

This project simulates a real-time data pipeline using IPL players’ data. It follows a production-grade stack using message queues, stream processing, cloud storage, transformation layers, and dashboarding — all automated and scalable.

---

## 🔧 Tech Stack Used

- **Kafka** - Stream data from a Python producer
- **Spark Structured Streaming** - Consume Kafka streams and process
- **Google Cloud Storage (GCS)** - Data lake (CSV landing zone)
- **BigQuery** - Data warehouse
- **dbt (Data Build Tool)** - Transform and model data
- **Looker Studio** - Visualization and dashboard
- **Docker & Docker Compose** - Containerization
- **Python (pandas, faker)** - Data generation
- **GitHub** - Version control and documentation

---

## ⚙️ Pipeline Architecture

Kafka Producer → Kafka → Spark Structured 
↓
Streaming → GCS (CSV)
↓
↓——→ BigQuery via dbt
↓
Looker Studio

---

## 🚀 Pipeline Phases

📁 All documentation for each phase is available in the [`docs/`](./docs/) folder:

| Phase | Description |
|-------|-------------|
| Phase 1 | Setup Kafka, Producer, and Docker environment |
| Phase 2 | Stream IPL data via Kafka to Spark |
| Phase 3 | Store processed data in GCS |
| Phase 4 | Load GCS data to BigQuery |
| Phase 5 | Data modeling using dbt |
| Phase 6 | Dashboarding using Looker Studio |
| Bonus | Optional Flow with Airflow → PostgreSQL → JDBC → Spark |

---

## 📂 Folder Structure

airflow_project/
│
├── kafka/ # Kafka producer setup
├── spark/ # Spark docker & script
├── dbt_venv/ # dbt virtualenv (not pushed)
├── ipl_dbt_project/ # dbt models & configs
├── docs/ # All documentation phase-wise
├── dags/ # Airflow DAGs (optional)
├── logs/ # Spark & Airflow logs
├── jars/ # Spark GCS connectors
├── ipl-streaming-*.json # GCP credentials

---

## 🛠️ How to Run This Project Locally

> Make sure Docker, Python 3.8+, and a GCP project are configured

### Step 1: Clone the Repo

```bash
git clone https://github.com/Yash-1115-coder/IPL-Data-Pipeline.git
cd IPL-Data-Pipeline

### Step 2: Start All Services

docker-compose up -d --build

### Step 3: Run Kafka Producer

cd kafka
python3 producer.py

### Step 4: Run Spark Streaming

docker exec -it spark bash
spark-submit --conf spark.hadoop.google.cloud.auth.service.account.enable=true \
             --conf spark.hadoop.google.cloud.auth.service.account.json.keyfile=/app/ipl-streaming-project-xxxxxx.json \
             spark_stream.py


### Step 5: Setup dbt and Transform Data

cd ipl_dbt_project
dbt run

### Step 6: Connect to Looker Studio and Visualize

Connect BigQuery table ipl_dbt_dataset.stg_ipl_stats to Looker Studio and create charts.

---

## 🌟 Key Highlights
✅ Real-time streaming via Kafka & Spark

✅ GCS integration without cloud SDK on WSL

✅ BigQuery modeling with dbt

✅ Fully functional dashboard with filters

✅ Complete documentation of all phases

---

## 📚 Credits
Course Inspiration: DataTalksClub’s DE Zoomcamp

Built & implemented by Yashas Rajesh

---
