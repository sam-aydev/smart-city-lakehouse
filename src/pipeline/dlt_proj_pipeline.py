import dlt

from pyspark.sql.functions import *
from transformations import standardize_schema, enrich_risk_level





volume_path = spark.conf.get("my.project.volume_path")


## The Bronze Layer(Ingestion Layer)

@dlt.table(
    comment="Our raw ingestion layer using autoloader",
    table_properties={"quality": "bronze"}
)

def bronze_layer():
    return spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").option("cloudFiles.inferColumnTypes", "true").load(volume_path)




@dlt.table(
    comment="Cleaned telemetry with Risk Scores",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_sensor", "sensor_id IS NOT NULL")
@dlt.expect("reasonable_temp", "temperature > -50 AND temperature < 200")
def silver_layer():
    bronze_data = dlt.read("bronze_layer")
    standardized_data = standardize_schema(bronze_data)
    df = enrich_risk_level(standardized_data)
    return df



@dlt.table(
    comment="Hourly Sensor Summary with AI Analysis",
    cluster_by=["sensor_id"] 
)
def gold_layer():
    df = dlt.read("silver_layer")
    
    agg_df = df.groupBy("sensor_id").agg(
        expr("avg(temperature)").alias("avg_temp"),
        expr("max(risk_score)").alias("max_risk"),
        expr("count(*)").alias("reading_count")
    )
    
    # AI Query: Use DBRX to explain the risk
    prompt = """
        concat(
            'Sensor ', sensor_id, ' has a max risk score of ', cast(max_risk as string), 
            '. The average temp is ', cast(avg_temp as string), '. Briefly analyze the health of this machine.'
        )
    """

    return agg_df.withColumn(
        "ai_analysis",
        expr(f"ai_query('databricks-meta-llama-3-3-70b-instruct', {prompt})")
    )