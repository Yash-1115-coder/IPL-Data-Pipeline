#✅ PHASE 1 — Data Ingestion from Source using Kafka

---

##🧠 Objective
Simulate real-time data streaming by pushing IPL player stats from a CSV file into a Kafka topic using a Python producer.

---

##📌 Tools & Components Used
Apache Kafka

Apache Zookeeper

Docker Compose

kafka-python library (inside Python producer)

IPL CSV file (IPL_Player_Stats.csv)

---

##⚙️ SETUP STEPS
###🔸 1. Launch Kafka and Zookeeper using Docker
docker-compose up -d kafka zookeeper
✅ This brings up both Kafka and Zookeeper.

###🔸 2. Enter Kafka Container and Create Topic
docker exec -it kafka bash
kafka-topics.sh --bootstrap-server kafka:9092 --create --topic ipl_stats --partitions 1 --replication-factor 1
✅ This creates a Kafka topic called ipl_stats.
To verify topic creation:
kafka-topics.sh --bootstrap-server kafka:9092 --list

###🔸 3. Start the Python Producer
Make sure to install requirements if not already:
pip install pandas kafka-python
Then run:
cd kafka
python3 producer.py
✅ This starts sending records (one at a time with delay) from the CSV into the Kafka topic ipl_stats.

---

##⚠️ Important Notes
Data is streamed in a simulated real-time fashion (1 record per second).

Ensure the CSV file path and Kafka topic name inside producer.py are correctly set.

Kafka must be up before running the producer.

---

##✅ Completion Criteria
Kafka topic ipl_stats is successfully created.

Kafka and Zookeeper containers are running.

producer.py sends data without errors.

You see print logs for every record sent.