FROM apache/airflow:2.6.3-python3.8

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt
