# Week 1 - Day 3: Advanced UDFs (Pandas/Python UDFs)

## Objective
Develop User-Defined Functions (UDFs) using Pandas/Python UDF to extend Spark's functionality while maintaining performance. (Exam Section 1.1)

## 1. Why Pandas UDFs?
Standard Python UDFs (row-by-row) are slow because they require:
1.  **Serialization:** Moving data from the JVM (Spark) to the Python process.
2.  **Row-level execution:** Processing one row at a time.
3.  **Deserialization:** Moving data back to the JVM.

**Pandas UDFs (Vectorized UDFs)** use **Apache Arrow** to transfer data efficiently in batches, allowing for vectorized operations using Pandas/NumPy.

## 2. Types of Pandas UDFs
For the exam, you must distinguish between these three main types:

### A. Series to Series
Processes a batch of rows. Used for scalar transformations.
```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def multiply_by_two(s: pd.Series) -> pd.Series:
    return s * 2
```

### B. Iterator of Series to Iterator of Series
Ideal for pre-fetching data or initializing heavy state (e.g., loading a machine learning model) once per batch instead of once per row.
```python
@pandas_udf("double")
def model_inference(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    model = load_model() # Load once per executor/batch
    for s in iterator:
        yield model.predict(s)
```

### C. Map (Grouped Map)
Used with `groupBy().applyInPandas()`. Allows you to apply a function to an entire group as a Pandas DataFrame.
```python
def subtract_mean(pdf: pd.DataFrame) -> pd.DataFrame:
    return pdf.assign(v = pdf.v - pdf.v.mean())

df.groupBy("id").applyInPandas(subtract_mean, schema="id int, v double")
```

### D. Syntax Comparison: Standard vs. Pandas UDFs
The syntax difference highlights the shift from row-level Python primitives to batch-level Pandas objects.

#### Standard Python UDF (Row-by-Row)
Processes one Python primitive at a time (e.g., `float`, `str`).
```python
from pyspark.sql.functions import udf

@udf("double")
def multiply_by_two_standard(n: float) -> float:
    # Processes a single scalar value
    return n * 2
```

#### Pandas UDF (Vectorized)
Processes a `pandas.Series` object using high-performance C/C++ backends.
```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def multiply_by_two_pandas(s: pd.Series) -> pd.Series:
    # Processes an entire batch (Series) at once
    return s * 2
```

### E. Standard vs. Pandas UDF Comparison
The Professional-tier exam requires you to know which to choose based on performance.

| Feature | Standard UDF (`@udf`) | Pandas UDF (`@pandas_udf`) |
| :--- | :--- | :--- |
| **Execution** | Row-by-row | Batch (Vectorized) |
| **Data Format** | Python primitives | Pandas Series/DataFrames |
| **Transport** | High overhead (JVM <-> Python) | Low overhead (**Apache Arrow**) |
| **Best Use Case** | Simple logic, very small datasets | Complex math, large datasets, ML inference |
| **Risk** | Slow performance, executor bottlenecks | OOM errors if batch size/data skew is too high |

**Pro Tip:** For the exam, always prioritize **Native Functions** (Spark SQL/PySpark) first. Only use a UDF when native functions are not available.

## 3. Professional Best Practices
*   **Prefer Native Functions:** If a native `pyspark.sql.functions` exists (e.g., `when()`, `regexp_replace()`), use it. It runs directly in the JVM and is always faster than a UDF.
*   **Arrow Execution:** Ensure `spark.sql.execution.arrow.pyspark.enabled` is set to `true` (default in modern DBR).
*   **Memory Management:** Large batches in Pandas UDFs can lead to OOM (Out of Memory) errors on executors. Tune `spark.sql.execution.arrow.maxRecordsPerBatch`.

## Rapid Fire Practice Questions

**Q1:** You need to perform a complex mathematical calculation that is not available in standard PySpark functions. The calculation requires high performance and involves millions of rows. Which UDF type should you choose?
- A) Standard Python UDF (`udf`)
- B) Pandas UDF (Vectorized UDF)
- C) Scala UDF
- D) Hive UDF
- **Answer: B**
- **Explanation:** Pandas UDFs use Apache Arrow for efficient data transfer and vectorized processing, making them significantly faster than standard Python UDFs for bulk operations.

**Q2:** When using `applyInPandas` for grouped operations, what is a primary risk that a Data Engineer must manage to ensure cluster stability?
- A) Network latency between executors.
- B) Data skew leading to an OOM error on a single executor.
- C) JVM heap size limitations.
- D) SQL syntax errors in the transformation logic.
- **Answer: B**
- **Explanation:** `applyInPandas` loads the entire group into memory as a Pandas DataFrame. If a group is too large (due to data skew), it can easily exceed the executor's memory and cause an Out of Memory error.

**Q3:** You are implementing a Pandas UDF that needs to load a 500MB lookup table from cloud storage. Which Pandas UDF pattern should you use to ensure the table is only loaded once per batch of data processed by an executor?
- A) Series to Series
- B) Scalar Iter
- C) Iterator of Series to Iterator of Series
- D) Grouped Aggregate
- **Answer: C**
- **Explanation:** The "Iterator to Iterator" pattern allows for setup logic (like loading a model or lookup table) to be performed once at the start of the iterator, rather than for every batch or row.

## References
- [Databricks Documentation: Pandas UDFs](https://docs.databricks.com/en/udf/pandas.html)
- [Apache Spark Documentation: Pandas User-Defined Functions](https://spark.apache.org/docs/latest/api/python/user_guide/sql/queries/pandas_udfs.html)
