"""
Main entry point for the dbx_prof_exam_prep Databricks job.
Handles job parameter parsing and integration test execution.
"""
import argparse
import sys
import pytest
from databricks.sdk.runtime import spark
from dbx_prof_exam_prep import taxis


def run_tests():
    """run pytest on the /tests directory and exit with its result code."""
    # Execute pytest on the /tests directory and exit with its result code
    # -v: verbose, -s: show output
    exit_code = pytest.main(["-v", "-s", "tests/"])
    sys.exit(exit_code)


def main():
    """
    Docstring for main
    """
    # Process command-line arguments
    parser = argparse.ArgumentParser(
        description="Databricks job with catalog and schema parameters",
    )
    # Make catalog and schema optional if --pytest is present
    parser.add_argument("--catalog", required="--pytest" not in sys.argv)
    parser.add_argument("--schema", required="--pytest" not in sys.argv)
    parser.add_argument("--pytest", action="store_true", help="Run integration tests")
    
    args = parser.parse_args()

    if args.pytest:
        run_tests()
        return

    # Set the default catalog and schema
    spark.sql(f"USE CATALOG {args.catalog}")
    spark.sql(f"USE SCHEMA {args.schema}")

    # Example: just find all taxis from a sample catalog
    taxis.find_all_taxis().show(5)


if __name__ == "__main__":
    main()
