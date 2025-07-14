from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType

# ✅ Schema definition
schema = (
    StructType()
    .add("Player", StringType())
    .add("COUNTRY", StringType())
    .add("TEAM", StringType())
    .add("AGE", IntegerType())
    .add("CAPTAINCY EXP", IntegerType())
    .add("Paying_Role", StringType())
    .add("Mat", IntegerType())
    .add("Inns", FloatType())
    .add("Runs", FloatType())
    .add("BF", FloatType())
    .add("HS", FloatType())
    .add("Avg", StringType())
    .add("SR", FloatType())
    .add("NO", FloatType())
    .add("4s", FloatType())
    .add("6s", FloatType())
    .add("0s", FloatType())
    .add("50s", FloatType())
    .add("100s", FloatType())
    .add("TMat", FloatType())
    .add("TInns", FloatType())
    .add("TRuns", FloatType())
    .add("TBF", FloatType())
    .add("THS", FloatType())
    .add("TAvg", FloatType())
    .add("TSR", FloatType())
    .add("TNO", FloatType())
    .add("T4s", FloatType())
    .add("T6s", FloatType())
    .add("T0s", FloatType())
    .add("T50s", FloatType())
    .add("T100s", FloatType())
    .add("B_Inns", FloatType())
    .add("B_Balls", FloatType())
    .add("B_Runs", FloatType())
    .add("B_Maidens", FloatType())
    .add("B_Wkts", FloatType())
    .add("B_Avg", FloatType())
    .add("B_Econ", FloatType())
    .add("B_SR", FloatType())
    .add("B_4w", FloatType())
    .add("B_5w", FloatType())
    .add("B_TInns", FloatType())
    .add("B_TBalls", FloatType())
    .add("B_TRuns", FloatType())
    .add("B_TMaidens", FloatType())
    .add("B_TWkts", FloatType())
    .add("B_TAvg", FloatType())
    .add("B_TEcon", FloatType())
    .add("B_TSR", FloatType())
    .add("B_T4w", FloatType())
    .add("B_T5w", FloatType())
    .add("SOLD_PRICE", StringType())
)

# ✅ Spark session
spark = SparkSession.builder.appName("KafkaSparkStreaming").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# ✅ Read from Kafka
df_raw = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "airflow-topic")
    .option("startingOffsets", "earliest")
    .load()
)

# ✅ Parse and extract data
df_parsed = (
    df_raw.selectExpr("CAST(value AS STRING) as json_value")
    .select(from_json(col("json_value"), schema).alias("data"))
    .select("data.*")
)

# ✅ Write to CSV under artifacts/ipl_stream_output
query = (
    df_parsed.writeStream
    .outputMode("append")
    .format("csv")
    .option("header", "true")
    .option("path", "/app/artifacts/ipl_stream_output")
    .option("checkpointLocation", "/app/artifacts/checkpoint")
    .start()
)

query.awaitTermination()
