# Week 1 - Day 2: Dependency Management & CLI/REST APIs

## Objective
Manage and troubleshoot external third-party library installations and dependencies in Databricks. Automate ETL workloads and monitor them using the Databricks CLI and REST APIs. (Exam Section 1.1, 1.2, 5.1)

## 1. Professional Dependency Management
Your `dbx_prof_exam_prep` project uses `uv` and `pyproject.toml` to manage libraries.

### A. The `pyproject.toml` Strategy
- **`dependencies` section:** This is where you list libraries required for your production jobs (e.g., `pandas`, `scikit-learn`). When you run `uv build --wheel`, these are NOT bundled into the wheel itself; instead, the wheel's metadata lists them as requirements.
- **`dependency-groups.dev`:** These are for your local machine and VS Code (e.g., `pytest`, `ruff`, `databricks-connect`). They are **not** deployed to the Databricks cluster.

### B. Installing on the Cluster
For the Professional exam, you must know how Databricks installs these libraries:
1.  **Jobs:** In `resources/sample_job.job.yml`, your task references `../dist/*.whl`. Databricks installs the wheel and then uses `pip` to resolve and install any dependencies listed in your `pyproject.toml` from PyPI.
2.  **Pipelines (DLT):** Your `dbx_prof_exam_prep_etl.pipeline.yml` uses `- --editable ${workspace.file_path}`. This is a "Developer Mode" feature that allows DLT to use your source code directly without a full build/deploy cycle.

### C. The "M1 Problem" (Architecture Mismatch)
**Critical for M1 Mac Users:** If you add a library with C-extensions (e.g., `psycopg2`, `confluent-kafka`) to your `dependencies`, you must ensure the wheel is built for the cluster's architecture (X86_64), not your Mac's (ARM64). DABs handle this by allowing you to define a build step that can run in a compatible environment.

### D. Source Archives (.tar.gz) and Private Repositories
The exam expects you to know how to install libraries from non-PyPI sources:
- **Source Archives:** You can reference `.tar.gz` files stored in a workspace folder or cloud storage directly in your `libraries` list.
- **Private Repos:** Use `--extra-index-url` in your `pyproject.toml` or as a Spark environment variable (`PIP_EXTRA_INDEX_URL`) to allow clusters to authenticate against private Artifactory or Azure DevOps feeds.

## 2. Automating with CLI & REST API
The Professional exam focuses on using the CLI (v0.200+) to interact with Jobs and Pipelines.

### A. Monitoring Commands
```bash
# Get the status of a specific job run
databricks jobs get-run --run-id <run-id>

# List all updates for a DLT pipeline
databricks pipelines list-updates --pipeline-id <pipeline-id>
```

### B. REST API Integration
Sometimes the CLI isn't enough. You might use `curl` or a Python script to call the REST API for advanced monitoring:
- **Endpoint:** `GET /api/2.1/jobs/runs/get-output` (Retrieves logs and error messages from a failed run).
- **Full Call Example:**
  ```bash
  curl -X GET "https://${DATABRICKS_HOST}/api/2.1/jobs/runs/get-output?run_id=123456" \
  -H "Authorization: Bearer ${DATABRICKS_TOKEN}"
  ```
- **Professional Insight:** Use this endpoint in automated CI/CD pipelines to scrape error messages and include them in Slack/Teams notifications upon failure.

### C. Job Status & Performance Notifications (Section 5.2.2)
The Professional exam focuses on configuring monitoring for job health. 
1. **Email Notifications:** Configurable in the `email_notifications` block in YAML.
2. **Webhooks:** For Slack/Teams via Databricks SQL or Job Webhooks.
3. **Event Notification Types:**
   - `on_start`
   - `on_success`
   - `on_failure`
   - `on_duration_warning_threshold_exceeded`: Crucial for performance monitoring.

**DABs Implementation Example:**
```yaml
resources:
  jobs:
    sample_job:
      email_notifications:
        on_failure: ["bernd.fellinghauer@data-fittery.ch"]
      health:
        rules:
          - metric: RUN_DURATION_SECONDS
            op: GREATER_THAN
            value: 3600
```

## 3. Practical Exercise: Add a Dependency
1.  Open `dbx/dbx_prof_exam_prep/pyproject.toml`.
2.  Add `requests` to the `dependencies` list.
3.  Run the build and validation:
    ```bash
    cd dbx/dbx_prof_exam_prep
    uv build --wheel
    databricks bundle validate
    ```

## Rapid Fire Practice Questions

**Q1:** You are deploying a Databricks Job that requires a specific version of the `scikit-learn` library. What is the most robust way to ensure this dependency is consistently installed on the job's cluster across all environments (dev/prod)?
- A) Run `%pip install scikit-learn==x.y.z` in the first cell of every notebook.
- B) Add `scikit-learn==x.y.z` to the `dependencies` list in `pyproject.toml` and reference the built wheel in the Job's `libraries` section.
- C) Manually install the library on the cluster via the Databricks UI.
- D) Use a Cluster Init Script to download the library from a private S3 bucket.
- **Answer: B**
- **Explanation:** Using `pyproject.toml` to define dependencies and including the resulting wheel in the bundle ensures that Databricks manages the lifecycle and versioning of the library automatically via its integrated package manager.

**Q2:** A production job fails with a `ModuleNotFoundError` for a library you just added to your `pyproject.toml`. You suspect the wheel file in the workspace is outdated. Which CLI command should you use to force a rebuild and redeployment of the latest code and dependencies?
- A) `databricks bundle deploy --force`
- B) `databricks bundle run --rebuild`
- C) `databricks bundle deploy` (DABs automatically detect changes and rebuild/redeploy artifacts)
- D) `databricks fs cp dist/*.whl dbfs:/FileStore/wheels/`
- **Answer: C**
- **Explanation:** The Databricks CLI is "artifact-aware." When you run `deploy`, it checks for changes in your `src/` directory, triggers the build command (like `uv build`), and uploads the new artifact if changes are detected.

**Q3:** You need to programmatically retrieve the error message from a failed Databricks Job task for inclusion in a custom Slack notification. Which REST API endpoint is best suited for this?
- A) `GET /api/2.1/jobs/get`
- B) `GET /api/2.1/jobs/runs/get-output`
- C) `GET /api/2.0/clusters/get`
- D) `GET /api/2.1/pipelines/get`
- **Answer: B**
- **Explanation:** The `get-output` endpoint retrieves the standard output, standard error, and any error message associated with a specific task run, making it the primary source for diagnostic information.

## References
- [Databricks Documentation: Manage Libraries with DABs](https://docs.databricks.com/en/dev-tools/bundles/library-dependencies.html)
- [Databricks Jobs REST API Reference](https://docs.databricks.com/api/workspace/jobs)
