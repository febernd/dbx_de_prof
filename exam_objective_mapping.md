# Databricks Data Engineer Professional: Full Objective Mapping (Sept 2025)

This document is the "Source of Truth" ensuring 100% coverage of the Databricks Certified Data Engineer Professional exam.

## Section 1: Developing Code for Data Processing
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **1.1.1** | Scalable Python project structure for DABs | W1 D1 |
| **1.1.2** | Manage third-party libraries (PyPI, Wheels, Source Archives) | W1 D2 |
| **1.1.3** | Develop Pandas/Python UDFs | W1 D3 |
| **1.2.1** | Build pipelines with Lakeflow & Auto Loader | W2 D1 |
| **1.2.2** | Automate ETL via Jobs UI/APIs/CLI | W1 D2 |
| **1.2.3** | Streaming Tables vs. Materialized Views | W2 D2 |
| **1.2.4** | APPLY CHANGES API for CDC | W2 D3 |
| **1.2.5** | Compare Spark Structured Streaming vs. Lakeflow | W2 D5 |
| **1.2.6** | Control Flow operators (if/else, for/each) | W2 D4 |
| **1.2.7** | Choose appropriate configs (high-memory, auto-opt) | W1 D1, D5 |
| **1.2.8** | Testing: `assertDataFrameEqual`, `assertSchemaEqual` | W1 D4 |

## Section 2: Data Ingestion & Acquisition
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **2.1** | Ingest formats: Delta, Parquet, ORC, AVRO, JSON, CSV, XML, Text, Binary | W2 D4 |
| **2.2** | Create append-only pipelines (Batch & Streaming) | W2 D1 |

## Section 3: Data Transformation, Cleansing, and Quality
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **3.1** | Efficient Spark SQL/PySpark (Window functions, Joins, Aggs) | W5 D2 |
| **3.2** | Quarantining process for bad data (Lakeflow/Auto Loader) | W2 D1 |

## Section 4: Data Sharing and Federation
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **4.1** | Delta Sharing (D2D and D2O) | W3 D2 |
| **4.2** | Lakehouse Federation governance | W3 D3 |
| **4.3** | Share live data to any computing platform | W3 D2 |

## Section 5: Monitoring and Alerting
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **5.1.1** | System tables for cost, auditing, resource utilization | W4 D3 |
| **5.1.2** | Query Profiler UI and Spark UI | W4 D3, D5 |
| **5.1.3** | REST APIs/CLI for monitoring jobs/pipelines | W1 D2 |
| **5.1.4** | Lakeflow Event Logs for monitoring | W4 D3 |
| **5.2.1** | SQL Alerts for data quality | W4 D4 |
| **5.2.2** | Job status and performance issue notifications | W1 D2 |

## Section 6: Cost & Performance Optimisation
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **6.1** | Unity Catalog managed tables for operational efficiency | W3 D1 |
| **6.2** | Delta optimization: Deletion Vectors & Liquid Clustering | W4 D1 |
| **6.3** | Optimization: Data skipping, file pruning | W4 D2 |
| **6.4** | Change Data Feed (CDF) for latency/streaming limits | W4 D2 |
| **6.5** | Analyze Query Profile for bottlenecks (Shuffling, Joins) | W4 D5 |

## Section 7: Ensuring Data Security and Compliance
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **7.1.1** | Workspace Object ACLs (Least Privilege) | W3 D4 |
| **7.1.2** | Row filters and column masks | W3 D4 |
| **7.1.3** | Anonymization (Hashing, Tokenization, Suppression) | W3 D5 |
| **7.2.1** | PII masking in batch/streaming pipelines | W3 D5 |
| **7.2.2** | Data purging for compliance/retention policies | W3 D5 |

## Section 8: Data Governance
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **8.1** | Create metadata/descriptions for discoverability | W3 D1 |
| **8.2** | Unity Catalog permission inheritance model | W3 D1 |

## Section 9: Debugging and Deploying
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **9.1.1** | Use UI/Logs/Tables to troubleshoot errors | W4 D5 |
| **9.1.2** | Remediate failed jobs (repairs, parameter overrides) | W4 D5 |
| **9.1.3** | Debug Lakeflow via event logs & Spark UI | W4 D5 |
| **9.2.1** | Build and deploy resources using DABs | W1 D1 |
| **9.2.2** | Git-based CI/CD and Git Folders | W1 D5 |

## Section 10: Data Modelling
| ID | Objective | Study Day |
| :--- | :--- | :--- |
| **10.1** | Scalable data models using Delta Lake | W5 D1 |
| **10.2** | Optimize performance using Liquid Clustering | W4 D1 |
| **10.3** | Benefits of Liquid Clustering over Partitioning/Z-Order | W4 D1 |
| **10.4** | Dimensional Models for analytical workloads | W5 D2 |
