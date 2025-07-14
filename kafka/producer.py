import pandas as pd
import json
from kafka import KafkaProducer
import numpy as np

df = pd.read_csv("/home/yash/airflow_project/IPL_Player_Stats.csv")
df = df.replace({np.nan: None})

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

for _, row in df.iterrows():
    producer.send("airflow-topic", value=row.to_dict())

producer.flush()
print("✅ All records sent to Kafka.")
