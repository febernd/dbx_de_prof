from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual
import pytest


@pytest.fixture(scope="session")
def local_spark():
    """Provides a fully local Spark session for testing without Databricks."""
    # .master("local[*]") tells Spark to use all available CPU cores on your laptop
    return SparkSession.builder.master("local[*]").appName("LocalTest").getOrCreate()


def test_local_filter_logic(local_spark):
    """A purely local test that doesn't touch Databricks or Unity Catalog."""
    # 1. Create local test data
    data = [
        (1, "valid", 100),
        (2, "invalid", 50),
        (3, "valid", 200)
    ]
    df = local_spark.createDataFrame(data, ["id", "status", "amount"])

    # 2. Apply a filter (this is the logic we are testing)
    result_df = df.filter(df.status == "valid")

    # 3. Define the expected output
    expected_data = [
        (1, "valid", 100),
        (3, "valid", 200)
    ]
    expected_df = local_spark.createDataFrame(expected_data, ["id", "status", "amount"])

    # 4. Use Spark's built-in testing utility to assert equality
    assertDataFrameEqual(result_df, expected_df)
