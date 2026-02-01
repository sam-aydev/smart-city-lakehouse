from pyspark.sql.functions import *
from pyspark.sql.types import *


def standardize_schema(df):
    return df.select(
        col("sensor_id").cast("string"), 
        col("timestamp").cast("timestamp"), 
        col("temp_celsius").alias("temperature").cast("double"), 
        col("vibration_g").cast("double").alias("vibration"), 
        col("status").cast("string")
        )
    

def enrich_risk_level(df):
    return df.withColumn("risk_score", (col("temperature") * 0.5) + (col("vibration") * 2.0)).withColumn("risk_category", when(col("risk_score") > 50 , lit("HIGH")).when(col("risk_score") > 20, lit("MEDIUM")).otherwise(lit("LOW")))
