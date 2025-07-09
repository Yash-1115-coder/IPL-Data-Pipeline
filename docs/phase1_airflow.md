# ⚡ Real-Time IPL Player Stats Pipeline — Phase 1

This project builds a real-time data pipeline to process IPL Player Stats using **Apache Kafka**, **Apache Airflow**, and **PostgreSQL**. It's designed to simulate ingestion, processing, and storage of structured streaming data — packaged with containerized microservices using **Docker**.

---

## 📦 Architecture (Phase 1)

IPL_Player_Stats.csv (Source)
↓
Python Kafka Producer
↓
Kafka Topic: airflow-topic
↓
Airflow DAG: kafka_to_postgres_dag
↓
PostgreSQL Table: ipl_stats

---

## 🛠️ Tech Stack

- **Apache Kafka** (Message Broker)  
- **Apache Airflow** (Workflow Orchestrator)  
- **PostgreSQL** (Relational DB)  
- **Python** (ETL + Kafka Producer)  
- **Docker + Docker Compose** (Containerization)  

---

## 🧠 What Phase 1 Covers

### ✅ Kafka Setup
- Created a Kafka topic called `airflow-topic`.
- Built a **Kafka Producer** script in Python using `kafka-python`.
- The script reads data from `IPL_Player_Stats.csv`, row by row, and pushes each as a **JSON message** into the Kafka topic.

### ✅ Airflow DAG
- DAG named `kafka_to_postgres_dag`.
- Uses `PythonOperator` to consume Kafka messages and insert them into a PostgreSQL table.
- Messages are stored as JSON in a single column named `message`.

### ✅ Postgres Setup
- Dockerized PostgreSQL service running on port 5432.
- Table created via DAG (if not exists):
```sql
CREATE TABLE IF NOT EXISTS ipl_stats (
    id SERIAL PRIMARY KEY,
    message JSON
);

---

⚠️ Data Fixes / Bug Solved

While inserting JSON data into Postgres, rows containing NaN caused the DAG to crash.
✅ Fixed by replacing NaN with valid null before insertion:

clean_msg = msg.value.replace("NaN", "null")
cursor.execute("INSERT INTO ipl_stats (message) VALUES (%s)", (clean_msg,))

---

📂 Project Structure

airflow_project/
├── dags/
│   └── kafka_to_postgres_dag.py        # Airflow DAG
├── kafka/
│   └── producer.py                     # Kafka Producer Script
├── IPL_Player_Stats.csv               # Input dataset (182 rows)
├── requirements.txt                   # Python deps
└── docker-compose.yml                 # Multi-service orchestration

---

🚀 How to Run (Phase 1)

1. Clone the Repo

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

2. Start All Services

docker-compose up --build

3. Push CSV Data to Kafka

docker exec -it airflow bash -c "python /opt/airflow/kafka/producer.py"

4. Trigger Airflow DAG

Go to http://localhost:8080

DAG ID: kafka_to_postgres_dag

Trigger → Monitor logs → Done

5. Check PostgreSQL

docker exec -it airflow bash
psql -h postgres -U postgres -d airflow
SELECT COUNT(*) FROM ipl_stats;
✅ Output:
 count
-------
 182
(1 row)

📊 Output Verification

Total Messages Pushed: 182
Total Messages Inserted into PostgreSQL: 182
Logs show:
📥 Message: {...}
✅ Inserted 182 messages.

🧪 Sample Log Messages to expect:
[2025-07-09, 11:48:52 UTC] {kafka_to_postgres_dag.py:29} INFO - ✅ Connected to Kafka
[2025-07-09, 11:48:52 UTC] {kafka_to_postgres_dag.py:35} INFO - ✅ Connected to Postgres
[2025-07-09, 11:48:57 UTC] {kafka_to_postgres_dag.py:39} INFO - 📥 Message: {"Player": "T Natarajan", "COUNTRY": "IND", "TEAM": "SRH", "AGE": 31, "CAPTAINCY EXP": 0, "Paying_Role": "Bowling", "Mat": 35, "Inns": null, "Runs": null, "BF": null, "HS": null, "Avg": null, "SR": null, "NO": null, "4s": null, "6s": null, "0s": null, "50s": null, "100s": null, "TMat": 4.0, "TInns": null, "TRuns": null, "TBF": null, "THS": null, "TAvg": null, "TSR": null, "TNO": null, "T4s": null, "T6s": null, "T0s": null, "T50s": null, "T100s": null, "B_Inns": 35.0, "B_Balls": 759.0, "B_Runs": 1094.0, "B_Maidens": 1.0, "B_Wkts": 38.0, "B_Avg": 28.79, "B_Econ": 8.65, "B_SR": 19.97, "B_4w": 0.0, "B_5w": 0.0, "B_TInns": 4.0, "B_TBalls": 96.0, "B_TRuns": 122.0, "B_TMaidens": 0.0, "B_TWkts": 7.0, "B_TAvg": 17.43, "B_TEcon": 7.62, "B_TSR": 13.71, "B_T4w": 0.0, "B_T5w": 0.0, "SOLD_PRICE": "4cr"}
[2025-07-09, 11:49:02 UTC] {kafka_to_postgres_dag.py:48} INFO - ✅ Inserted 182 messages.

# 🔚 Phase 1: ✅ COMPLETED
Real-time pipeline from CSV → Kafka → Airflow DAG → PostgreSQL is built, debugged, verified, and ready.