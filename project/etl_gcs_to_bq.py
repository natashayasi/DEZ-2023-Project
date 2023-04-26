from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(log_prints=True,retries=3)
def extract_from_gcs(table: str) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{table}.parquet"
    gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")
    gcp_cloud_storage_bucket_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")

@task(log_prints=True)
def fetch_data(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    print(f"rows: {len(df)}")
    return df

@task(log_prints=True,retries=3)
def transform_data(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df

@task(log_prints=True,retries=3)
def write_bq(df: pd.DataFrame, table: str) -> None:
    """Write DataFram to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")


    df.to_gbq(
        destination_table = f"project.{table}",
        project_id = "vast-signifier-375221",
        credentials = gcp_credentials_block.get_credentials_from_service_account(),
        chunksize = 500_000,
        if_exists="append",

    )

@flow()
def etl_gcs_to_bq(table: str) -> None:
    """Main ETL flow to load data into Big Query"""

    path = extract_from_gcs(table)
    df = fetch_data(path)
    write_bq(df, table)


@flow()
def etl_parent_flow(tableList: list[str]) -> None:
    for table in tableList:
        etl_gcs_to_bq(table)

if __name__ == '__main__':
    tableList = ["geometries","simulations"]
    etl_parent_flow(tableList)