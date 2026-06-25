# Week 1 - Day 0: Environment Setup (M1 Mac + VS Code / Antigravity)

## Objective
Establish a production-ready development environment using VS Code (or Antigravity IDE), Databricks CLI, and OAuth for Azure Databricks.

## 1. Local Tooling
### A. Databricks CLI (v0.200+)
- **Purpose:** Essential for managing Databricks Asset Bundles (DABs).
- **M1 Specifics:** Ensure you are using the native ARM64 version via Homebrew. 
	- `which brew` returns /opt/homebrew/bin/brew --> ok, this is new M1-world
    - install `Databricks CLI` from brew
        ```
        # Add the Databricks tap
        brew tap databricks/tap

        # Install the CLI
        brew install databricks

        # After running these, verify the installation with:
        databricks --version
        ```
    - install `Databricks`extension from VS Code extensions
    - need specific Python version
        ````
        brew update
        brew install pyenv

        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc

        echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc

        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        ````

        Then to install a particular version of Python
        ```
        pyenv install --list | grep "3.11"

        pyenv install 3.11.14

        pyenv global 3.11.14

        # open the VS Code terminal in the gemini project
        python -m venv .venv
        ```
 
        If no Unity Catalog is available, create one first, see the video [here](https://www.youtube.com/watch?v=f6Acij4hPqA)

        Then create the catalog within a Databricks notebook
        ````
        %sql
        CREATE CATALOG IF NOT EXISTS dbx;

        # if successful, the new UC will show up here
        SHOW CATALOGS;

        # Create a user schema within the dbx catalogue
        CREATE SCHEMA dbx.bernd_fellinghauer
        ```

### B. VS Code Extension
- **Features:** Syncing code, running notebooks as jobs, and Databricks Connect integration.

### C. Antigravity IDE (Alternative to VS Code)
- **Download URL:** [https://antigravity.google](https://antigravity.google)
- **Setup:** Open the `dbx_de_prof` workspace directory. Databricks CLI and `.venv` are automatically detected.

## 2. Authentication Patterns
- **User-to-Machine (U2M):** OAuth via browser login. Best for local development.
- **Machine-to-Machine (M2M):** OAuth via Client ID/Secret. Best for CI/CD and DABs.

## 3. Python Environment
- **Spark Stubs:** Always install `pyspark` and `delta-spark` locally to get IDE completion, even if not running Spark locally.
- **Architecture Note:** Be aware that M1 (ARM64) local builds may differ from Databricks (AMD64/X86_64) runtime environments.

## Action Items
1. [x] Install Databricks CLI.
2. [x] Authenticate using `azure-cli` or `oauth`.
3. [x] Install VS Code Extension (or Antigravity IDE) and connect to your workspace.
