# Week 1 - Day 1: Python Project Structure & Databricks Asset Bundles (DABs)

## Objective
Design and implement a scalable Python project structure optimized for Databricks Asset Bundles (DABs), specifically analyzing the `dbx_prof_exam_prep` project structure. (Exam Section 1.1)

## 1. Professional Project Structure Analysis
Your current bundle `dbx_prof_exam_prep` follows the Databricks-recommended modular structure:

1.  **`src/dbx_prof_exam_prep/` (Python Code Layer):**
    - `main.py`: Entry point for Spark logic.
    - `taxis.py`: Likely contains transformation logic (modularized).
    - **Pro Tip:** For the exam, know that logic in `src/` is built into a **Python Wheel (`.whl`)** using `uv build` in your specific setup.
2.  **`resources/` (Infrastructure Layer):**
    - `sample_job.job.yml`: Defines standard Spark Jobs.
    - `dbx_prof_exam_prep_etl.pipeline.yml`: Defines **Delta Live Tables (DLT)** pipelines.
    - **Exam Focus:** The `include` directive in `databricks.yml` (`resources/*.yml`) is what pulls these modular configurations into the bundle.
3.  **`tests/` (QA Layer):**
    - Contains `pytest` files to verify `src/` logic. This is critical for Section 1.1.2 (CI/CD integration).

4.  **`fixtures/` (Test Data Layer):**
    - **Purpose:** Stores static data files (e.g., CSV, JSON, Parquet) used during unit and integration tests.
    - **Professional Tier Insight:** In a CI/CD pipeline, you want to test your transformations against **known data** (fixtures) rather than live production data. This ensures your tests are deterministic and fast.
    - **Example:** A small sample of NYC Taxi data used to verify your `taxis.py` logic.

5.  **`dist/` (Distribution Layer):**
    - **Purpose:** This folder is automatically generated when you run your build command (in your case, `uv build`). It contains the compiled **Python Wheel (`.whl`)**.
    - **How it works:** When you run `databricks bundle deploy`, the CLI looks in `dist/` for your wheel file and uploads it to the workspace so your clusters can install it as a library.
    - **Note:** This folder is usually excluded from Git via `.gitignore` because it is a "derived" artifact.

6.  **`.databricks/` (Internal Metadata):**
    - **Purpose:** A hidden folder that stores the bundle's local state, including the `bundle.uuid` and information about your active targets.
    - **Warning:** Do not delete or manually edit files in here, as it can break the link between your local bundle and the deployed resources in Azure.

## 2. Deep-Dive: Your `databricks.yml`
Your file uses advanced features that are common on the Professional-tier exam:

### A. Dynamic Variables
```yaml
variables:
  catalog:
    description: The catalog to use
  schema:
    description: The schema to use
```
**Exam Insight:** Variables allow the same code to run in `dev` and `prod` without hardcoded paths. You use `${workspace.current_user.short_name}` in `dev` for user-isolated testing.

### B. Deployment Modes (Dev vs. Prod)
Your `dev` target uses `mode: development`, which:
- Prefixes resources with `[dev <user>]`.
- Pauses schedules by default to avoid accidental costs.
Your `prod` target uses `mode: production`, which:
- Enforces strict resource locking.
- Requires explicit `root_path` definitions (as seen in your file) to ensure stability.

### C. Permissions
```yaml
permissions:
  - user_name: bernd.fellinghauer@data-fittery.ch
    level: CAN_MANAGE
```
**Exam Focus:** Section 7 of the guide (Security) covers workspace object permissions. DABs are the standard way to deploy these permissions as part of your Infrastructure as Code (IaC).

### D. Target-Specific Configuration Overrides
The exam specifically mentions choosing appropriate configs for `high-memory` and `auto-optimization` (Section 1.2.7). 
- **Auto-Optimization:** Consists of two features:
    1. **Optimized Writes:** Spark dynamically optimizes the size of Delta files as they are written to disk.
    2. **Auto-Compaction:** Automatically checks if files can be compacted into larger, more efficient sizes after a write operation.
- **DABs Implementation:**
```yaml
targets:
  prod:
    mode: production
    resources:
      jobs:
        sample_job:
          tasks:
            - task_key: python_wheel_task
              new_cluster:
                spark_conf:
                  spark.databricks.delta.optimizeWrite.enabled: "true"
                  spark.databricks.delta.autoCompact.enabled: "true"
                node_type_id: "Standard_DS4_v2" # High-memory node
```

## 3. Practical Exercise: Local Validation
Since you are on an M1 Mac, run this to ensure your local environment and architecture are correctly communicating with Azure:

```bash
cd dbx/dbx_prof_exam_prep
databricks bundle validate
```

## Rapid Fire Practice Questions

**Q1:** You have defined a variable `catalog: dbx` in your `databricks.yml`. How should you reference this variable within a SQL task defined in `resources/sample_job.job.yml` to ensure it is correctly substituted during deployment?
- A) `${var.catalog}`
- B) `${bundle.variables.catalog}`
- C) `{{catalog}}`
- D) `${catalog}`
- **Answer: A**
- **Explanation:** In Databricks Asset Bundles, variables declared in the `variables` block are referenced using the `${var.<variable_name>}` syntax within resource configuration files.

**Q2:** Your `dbx_prof_exam_prep` bundle contains a DLT pipeline. You want to ensure that when deploying to the `dev` target, the pipeline uses a smaller cluster size than in `prod`. Where is the most appropriate place to define this override?
- A) In the `src/main.py` using Spark configurations.
- B) In the `targets.dev` section of `databricks.yml` under resource overrides.
- C) By creating a separate `resources/dev_pipeline.yml` file.
- D) In the `pyproject.toml` file.
- **Answer: B**
- **Explanation:** The `targets` section in `databricks.yml` is specifically designed for environment-specific overrides. You can redefine any property of a resource (like `clusters` or `spark_conf`) within a target to differentiate between development and production environments.

**Q3:** You run `databricks bundle deploy -t prod`. The deployment fails because a resource with the same name already exists and is managed by another bundle. Which feature of DABs prevents this conflict?
- A) `bundle.uuid`
- B) `mode: production`
- C) `workspace.root_path`
- D) `artifacts.python_artifact.type`
- **Answer: A**
- **Explanation:** The `bundle.uuid` is a unique identifier generated when the bundle is initialized. Databricks uses this UUID to track ownership of resources in the workspace. If you try to deploy a bundle with a different UUID that contains resources with names identical to those managed by an existing bundle, the CLI will block the deployment to prevent accidental overwriting or deletion.

## References
- [Databricks Documentation: Use Variables in Bundles](https://docs.databricks.com/en/dev-tools/bundles/variables.html)
- [Databricks Documentation: Bundle Deployment Modes](https://docs.databricks.com/en/dev-tools/bundles/deployment-modes.html)
