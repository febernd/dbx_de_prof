# Week 1 - Day 4: Unit Testing & Integration Testing

## Objective
Develop unit and integration tests using `assertDataFrameEqual`, `assertSchemaEqual`, and `pytest` to ensure code correctness and facilitate CI/CD. (Exam Section 1.2.8)

## 1. Modern Spark Testing (`pyspark.testing`)
Prior to Databricks Runtime 14.x (Spark 3.5), testing Spark DataFrames was painful (often involving `toPandas()` and `pandas.testing`).
The Professional exam expects you to use the built-in, scalable testing utilities.

### A. `assertDataFrameEqual`
Validates that two DataFrames share the same schema and data.
```python
from pyspark.testing.utils import assertDataFrameEqual

def test_transformation(spark):
    input_data = [("A", 10), ("B", 20)]
    expected_data = [("A", 20), ("B", 40)]
    
    df = spark.createDataFrame(input_data, ["id", "val"])
    # Assume 'transform_func' doubles the value
    result_df = transform_func(df)
    expected_df = spark.createDataFrame(expected_data, ["id", "val"])
    
    # Assert equality (handles nulls, tolerance, and schema)
    assertDataFrameEqual(result_df, expected_df)
```

### B. `assertSchemaEqual`
Validates only the structure (column names, types, nullability), ignoring data. Useful for ensuring interface contracts between pipeline steps.
```python
from pyspark.testing.utils import assertSchemaEqual
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def test_schema_contract(spark):
    df = spark.table("my_table")
    expected_schema = StructType([
        StructField("id", StringType(), True),
        StructField("val", IntegerType(), True)
    ])
    assertSchemaEqual(df.schema, expected_schema)
```

## 2. Integration Testing with DABs
Unit tests check logic in isolation. Integration tests check how that logic interacts with the Databricks environment (e.g., writing to Delta, reading from Unity Catalog).

### Reproducible Example: Testing a Delta Write
To implement this in VS Code, you need three components:

#### 1. Setup of Test Fixtures (UC Volumes)
The Professional exam emphasizes **Unity Catalog Volumes** for managing non-tabular data (like Parquet files used for ingestion).

**A. Create the Managed Volume:**
```bash
# Syntax: databricks volumes create <catalog> <schema> <name> <type>
databricks volumes create dbx bernd_fellinghauer test_fixtures MANAGED
```

**B. Generate Local Parquet Data:**
Use Python locally to create a minimal valid schema in your `fixtures/` directory:
```python
import pandas as pd
df = pd.DataFrame({
    'tpep_pickup_datetime': ['2023-01-01 00:00:00'], 
    'tpep_dropoff_datetime': ['2023-01-01 00:10:00'], 
    'trip_distance': [1.5]
})
df.to_parquet('dbx/dbx_prof_exam_prep/fixtures/sample_taxis.parquet')
```

**C. Upload to Volume:**
```bash
databricks fs cp dbx/dbx_prof_exam_prep/fixtures/sample_taxis.parquet \
  dbfs:/Volumes/dbx/bernd_fellinghauer/test_fixtures/sample_taxis.parquet \
  --overwrite
```

#### 2. The Source Logic (`src/dbx_prof_exam_prep/taxis.py`)
```python
def ingest_taxi_data(spark, input_path, output_table):
    df = spark.read.parquet(input_path)
    # Perform some transformation
    df_transformed = df.withColumn("processed_at", current_timestamp())
    df_transformed.write.mode("overwrite").saveAsTable(output_table)
```

#### 3. The Integration Test (`tests/test_integration.py`)
```python
import pytest
from dbx_prof_exam_prep.taxis import ingest_taxi_data

def test_ingest_taxi_data_integration(spark):
    # Point to the Volume path instead of legacy DBFS
    input_path = "/Volumes/dbx/bernd_fellinghauer/test_fixtures/sample_taxis.parquet"
    output_table = "dbx.bernd_fellinghauer.test_taxis_output"
    
    # Run the integration logic
    ingest_taxi_data(input_path, output_table)
    
    # Verify the result in Delta
    result_df = spark.table(output_table)
    assert result_df.count() > 0
    assert "processed_at" in result_df.columns
```

#### 4. The Bundle Configuration (`resources/test_job.job.yml`)
Define a job that runs your tests in the remote workspace:
```yaml
resources:
  jobs:
    run_integration_tests:
      name: "[${bundle.target}] Integration Tests"
      tasks:
        - task_key: run_pytest
          job_cluster_key: test_cluster
          spark_python_task:
            python_file: ../src/dbx_prof_exam_prep/main.py # Or a dedicated test runner
            parameters: ["--pytest"]
      job_clusters:
        - job_cluster_key: test_cluster
          new_cluster:
            spark_version: "14.3.x-scala2.12"
            node_type_id: "Standard_DS3_v2"
            num_workers: 1
```

### Execution Modes: Local vs. Remote (DABs)

| Mode | Context | Command / Tool | Execution Environment | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Local** | Unit Tests | `pytest tests/unit` | Local Laptop (No Spark) | Testing pure Python logic, regex, or math. |
| **Local (DB Connect)** | Integration | VS Code Test Explorer | Local Laptop -> Remote Cluster | Rapid dev cycle; testing against live UC data/volumes. |
| **Remote (Dev)** | DABs Job | `databricks bundle run` | Databricks Job Cluster | CI/CD validation; verifying DABs resources and permissions. |
| **Remote (Prod)** | DABs Job | CI/CD Pipeline | Databricks Job Cluster (Isolated) | Final validation before release; strictly controlled schema. |

### 3. Comparison: Local vs. Hybrid vs. Remote

| Feature | **Fully Local** | **Hybrid (DB Connect)** | **Remote (DABs Job)** |
| :--- | :--- | :--- | :--- |
| **Connection** | ❌ None (Offline) | ✅ Live to Workspace | ✅ Runs inside Workspace |
| **Compute** | Your Laptop CPU | **Databricks Serverless** | **Job Cluster** |
| **Data Access** | Local files only | **Unity Catalog / Volumes** | **Unity Catalog / Volumes** |
| **UC Support** | ❌ No (no `CATALOG.SCHEMA`) | ✅ Yes | ✅ Yes |
| **Best For** | Logic & Unit Tests | Dev & Integration Tests | Final CI/CD Validation |

## 4. Debugging Techniques (Section 9.1)
*   **`display()` vs. `show()`:** `display()` is a Databricks-specific command for the UI; `show()` is standard Spark (stdout).
*   **Spark UI:** Use the "SQL" tab to visualize the DAG (Directed Acyclic Graph) and identify bottlenecks (e.g., excessive shuffling).
*   **pdb/ipdb:** In Databricks Connect v2 (VS Code), you can use standard Python debuggers to step through execution.

## Rapid Fire Practice Questions

**Q1:** You are writing a unit test for a transformation function that calculates financial metrics. You want to ensure the result is correct within a tolerance of 0.001 to account for floating-point precision differences between your local machine and the Spark cluster. Which function is best suited for this?
- A) `pandas.testing.assert_frame_equal`
- B) `assertDataFrameEqual(..., rtol=0.001)`
- C) `assert(df.collect() == expected_df.collect())`
- D) `df.subtract(expected_df).count() == 0`
- **Answer: B**
- **Explanation:** `pyspark.testing.assertDataFrameEqual` supports a `rtol` (relative tolerance) parameter specifically for fuzzy matching of floating-point numbers, avoiding brittle tests that fail on minor precision mismatches.

**Q2:** You have a CI/CD pipeline using Databricks Asset Bundles (DABs). You want to run integration tests automatically whenever a Pull Request is opened, but you want to ensure these tests do not affect production data in Unity Catalog. What is the recommended architecture?
- A) Use the `prod` target but delete the data after the test finishes.
- B) Use a `staging` target that writes to a dedicated `test_schema` (e.g., `catalog.test_schema`) using variable overrides in `databricks.yml`.
- C) Mock the `spark.write` operation using `unittest.mock`.
- D) Run the tests on a local Spark instance instead of Databricks.
- **Answer: B**
- **Explanation:** Integration tests should run in a real environment. Using a separate `staging` target with a dedicated schema (isolated via variables) ensures safety while verifying actual interactions with the platform.

**Q3:** A DLT pipeline is failing with a generic "AnalysisException". You need to inspect the exact query plan that Spark is generating to understand the error. Which tool provides the visual representation of the Logical and Physical plans?
- A) Driver Logs (log4j)
- B) Ganglia Metrics
- C) Spark UI > SQL Tab
- D) Databricks CLI `bundle validate`
- **Answer: C**
- **Explanation:** The Spark UI's SQL Tab provides the "Details" view, which shows the Parsed, Analyzed, Optimized, and Physical plans, allowing you to pinpoint exactly where the analysis is failing.

## References
- [PySpark Testing Utils](https://spark.apache.org/docs/latest/api/python/reference/pyspark.testing.html)
- [Databricks Documentation: CI/CD with DABs](https://docs.databricks.com/en/dev-tools/bundles/ci-cd.html)
