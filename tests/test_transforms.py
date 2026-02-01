import pytest 
from pyspark.sql import SparkSession
from src.pipeline.transformations import standardize_schema, enrich_risk_level

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("Test").getOrCreate()

def test_enrich_risk_level(spark):
    data = [(100.0, 10.0)] 
    schema = ["temperature", "vibration"]
    df = spark.createDataFrame(data, schema)
    
    
    result = enrich_risk_level(df)
    

    row = result.collect()[0]
    expected_score = (100.0 * 0.5) + (10.0 * 2.0) 
    
    assert row["risk_score"] == 70.0
    assert row["risk_category"] == "HIGH"