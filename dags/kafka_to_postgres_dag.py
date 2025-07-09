from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import psycopg2
import json


def consume_and_insert():
    import logging
    import psycopg2
    from kafka import KafkaConsumer
    import json

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    try:
        log.info("Connecting to Kafka...")
        consumer = KafkaConsumer(
            "airflow-topic",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="airflow-pg-group-new-final",  # 🔁 change this every run to force reconsume
            value_deserializer=lambda x: x.decode("utf-8", errors="replace"),
            consumer_timeout_ms=5000,
        )
        log.info("✅ Connected to Kafka")

        conn = psycopg2.connect(
            host="postgres", database="airflow", user="postgres", password="virat"
        )
        cursor = conn.cursor()
        log.info("✅ Connected to Postgres")

        inserted = 0
        for msg in consumer:
            log.info("📥 Message: %s", msg.value)

            # ✅ CRITICAL LINE HERE
            clean_msg = msg.value.replace("NaN", "null")

            cursor.execute("INSERT INTO ipl_stats (message) VALUES (%s)", (clean_msg,))
            conn.commit()
            inserted += 1

        log.info("✅ Inserted %d messages.", inserted)
        cursor.close()
        conn.close()
        consumer.close()

    except Exception as e:
        log.error("❌ DAG crashed hard: %s", str(e))
        raise


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 7, 1),
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="kafka_to_postgres_dag",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id="consume_and_store", python_callable=consume_and_insert)
