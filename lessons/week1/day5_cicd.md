# Week 1 - Day 5: CI/CD Integration

## Objective
Configure and integrate with Git-based CI/CD workflows using Databricks Git Folders and Databricks Asset Bundles (DABs). (Exam Section 9.2)

## 1. Databricks Git Folders (formerly Repos)
Git Folders allow you to sync your Databricks Workspace with a Git provider (GitHub, Azure DevOps, GitLab).

### Key Professional Concepts:
- **Repo-level Permissions:** Managing who can `CAN_READ`, `CAN_EDIT`, or `CAN_MANAGE` a Git Folder.
- **Branch Management:** You can programmatically switch branches using the Databricks API: `PATCH /api/2.0/repos/{repo_id}`.
- **Sparse Checkout:** (Advanced) Only pulling a subset of a repository into the workspace to save time and space.

## 2. Automating DABs with CI/CD
In a professional production environment, you never run `bundle deploy` from your laptop. You use a CI/CD runner (e.g., GitHub Actions or Azure Pipelines).

### A. The CI/CD Workflow
1.  **Checkout Code:** Pull the latest from Git.
2.  **Environment Setup:** Install `databricks` CLI and `uv`.
3.  **Authentication:** Use a **Service Principal** with **OAuth M2M**.
    - Set `DATABRICKS_HOST`, `DATABRICKS_CLIENT_ID`, and `DATABRICKS_CLIENT_SECRET`.
4.  **Validate:** `databricks bundle validate -t prod`.
5.  **Deploy:** `databricks bundle deploy -t prod`.

### B. Service Principals (Section 7.1)
The exam tests your knowledge of **Service Principals (SP)**.
- **Why:** SPs provide a non-human identity for automation.
- **UC Integration:** SPs must be granted `USE CATALOG` and `USE SCHEMA` permissions in Unity Catalog to run production jobs.

## 3. GitHub Actions Example
```yaml
name: Deploy DABs
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: databricks/setup-cli@v0.2
      - run: |
          databricks bundle deploy -t prod
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
```

## Rapid Fire Practice Questions

**Q1:** You are setting up a CI/CD pipeline for a Databricks project using Azure DevOps. To follow the principle of least privilege, which identity should be used by the pipeline to deploy resources into the production workspace?
- A) The personal access token (PAT) of the Lead Data Engineer.
- B) A Service Principal granted the `CAN_MANAGE` permission on the specific production folder.
- C) An Azure AD User account with Global Admin rights.
- D) The workspace administrator's credentials.
- **Answer: B**
- **Explanation:** Using a Service Principal ensures that the pipeline has a dedicated identity that can be audited and restricted to only the necessary permissions, avoiding dependency on human users.

**Q2:** When using Databricks Git Folders, you want to ensure that your production jobs always run using the code from the `main` branch. What is the most robust way to automate the update of the production Git Folder after a successful merge?
- A) Manually click "Pull" in the Databricks UI.
- B) Use a CI/CD step to call the Repos API `PATCH` endpoint to update the Git Folder to the latest commit on `main`.
- C) Rely on Databricks to automatically sync changes (Databricks does not auto-sync Git Folders).
- D) Delete and recreate the Git Folder on every run.
- **Answer: B**
- **Explanation:** The Repos API allows for programmatic branch updates, ensuring that your workspace always reflects the state of your Git repository without manual intervention.

**Q3:** Your `databricks bundle deploy` command fails in the CI/CD environment with a "401 Unauthorized" error, even though the same command works on your local machine. What is the most likely cause?
- A) The CI/CD runner is using an outdated version of the Databricks CLI.
- B) The `DATABRICKS_TOKEN` environment variable is either missing or has expired in the CI/CD secret store.
- C) DABs do not support deployment from Linux-based CI/CD runners.
- D) The bundle is missing a `uuid` in the `databricks.yml` file.
- **Answer: B**
- **Explanation:** 401 Unauthorized errors consistently indicate an authentication failure, usually due to an invalid or missing token in the environment variables of the CI/CD process.

## References
- [Databricks Documentation: Use Git with Databricks](https://docs.databricks.com/en/repos/index.html)
- [Databricks Documentation: CI/CD with DABs](https://docs.databricks.com/en/dev-tools/bundles/ci-cd.html)
