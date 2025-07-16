# 🧪 Optional Flow: Kafka → Airflow DAG → PostgreSQL → Spark (via JDBC)

This document explains how to complete the **JDBC-based Spark streaming from PostgreSQL**, after data has already been ingested from Kafka via Airflow.

---

## ✅ Objective

Use Spark to read the data stored in PostgreSQL using JDBC and proceed with processing.

---

## 🧱 Setup Requirements

- PostgreSQL running in Docker (named `airflow_postgres`)
- Table: `ipl_players` already filled via Kafka + Airflow
- Spark container up and running
- PostgreSQL JDBC `.jar` driver added to the Spark container

---

## 📁 Step 1: Ensure PostgreSQL Table Exists

```sql
-- Connect to PostgreSQL inside Docker
docker exec -it airflow_postgres psql -U airflow -d ipl

-- Run this in psql
SELECT * FROM ipl_players LIMIT 5;

## 🛠️ Step 2: Place PostgreSQL JDBC .jar in Spark
###Place the driver .jar (e.g. postgresql-42.5.0.jar) in the local jars/ folder

###Ensure your Dockerfile.spark has this line:

dockerfile
COPY ./jars/*.jar /opt/spark/jars/
Rebuild Spark:
docker-compose build spark


##🚀 Step 3: Spark Code to Read from PostgreSQL
Create a Python script (e.g. read_postgres.py) in your /spark/ folder:


from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Postgres to Spark") \
    .config("spark.jars", "/opt/spark/jars/postgresql-42.5.0.jar") \
    .getOrCreate()

jdbc_url = "jdbc:postgresql://airflow_postgres:5432/ipl"
table_name = "ipl_players"
properties = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(
    url=jdbc_url,
    table=table_name,
    properties=properties
)

df.show()


## 💻 Step 4: Run the Spark Job
### Step inside Spark container
docker exec -it spark bash

### Run the script
spark-submit read_postgres.py
You’ll see the output from PostgreSQL loaded directly into Spark.

---

##🧠 Why This Matters
This approach gives you:

Structured ingestion via Airflow

Storage in PostgreSQL for audit or backups

Flexibility to read and process in Spark

✅ Perfect for batch processing or hybrid setups

---

##💬 Summary
1️⃣	Kafka - produces data
2️⃣	Airflow DAG - reads Kafka & inserts into PostgreSQL
3️⃣	Spark - connects to PostgreSQL using JDBC
4️⃣	Spark - reads data → transforms or stores it

