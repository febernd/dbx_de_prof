"""Integration test for taxi data ingestion."""
from dbx_prof_exam_prep.taxis import ingest_taxi_data

def test_ingest_taxi_data_integration(spark):
    """test the taxi data ingestion end-to-end."""
    # Use a fixture file and a temporary table in your dev schema
    input_path = "/Volumes/dbx/bernd_fellinghauer/test_fixtures/sample_taxis.parquet"
    output_table = "dbx.bernd_fellinghauer.test_taxis_output"

    # Run the integration logic
    ingest_taxi_data(input_path, output_table)

    # Verify the result in Delta
    result_df = spark.table(output_table)
    assert result_df.count() > 0
    assert "processed_at" in result_df.columns
    