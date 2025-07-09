import pandas as pd
import json
from kafka import KafkaProducer
import numpy as np

# ✅ Read and sanitize
df = pd.read_csv("/opt/airflow/IPL_Player_Stats.csv")
df = df.replace({np.nan: None})  # ← THIS is critical

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

for _, row in df.iterrows():
    message = row.to_dict()
    producer.send("airflow-topic", value=message)

producer.flush()
print("✅ All records sent to Kafka.")
