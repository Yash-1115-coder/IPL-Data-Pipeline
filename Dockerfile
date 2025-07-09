FROM apache/airflow:2.6.3-python3.8

COPY requirements.txt /

USER airflow

RUN pip install --no-cache-dir --user -r /requirements.txt
