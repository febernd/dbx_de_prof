"""This module contains functions to work with taxi data in Databricks."""
from databricks.sdk.runtime import spark
from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp


def find_all_taxis() -> DataFrame:
    """Find all taxi data."""
    return spark.read.table("samples.nyctaxi.trips")

def ingest_taxi_data(input_path, output_table):
    """Ingest taxi data from a parquet file and save it as a table."""
    df = spark.read.parquet(input_path)
    # perform some transformation
    df_transformed = df.withColumn("processed_at", current_timestamp())
    df_transformed.write.mode("overwrite").saveAsTable(output_table)
    