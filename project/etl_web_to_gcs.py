from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
#from random import randint

@task(log_prints=True)
def fetch_data(dataset_url: str) -> pd.DataFrame:
    """Read data from web into panda Dataframe"""

    #if randint(0,1) > 0:
    #    raise Exception

    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean_data(df = pd.DataFrame) -> pd.DataFrame:
    return df

@task(log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write dataframe out as a parquet file"""
    path = Path(f"data/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Uploading local parquet file to GCS"""

    gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=f"{path}",to_path=path)
    return

@flow
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    geometries_file = "geometries"
    geometries_url = "https://zenodo.org/record/7070952/files/geometries.csv?download=1"
    simulations_file = "simulations"
    simulations_url = "https://zenodo.org/record/7070952/files/simulations.csv?download=1"

    df = fetch_data(geometries_url)
    df_clean = clean_data(df)
    path = write_local(df_clean, geometries_file)
    write_gcs(path)
    
    df = fetch_data(simulations_url)
    df_clean = clean_data(df)
    path = write_local(df_clean, simulations_file)
    write_gcs(path)

if __name__ == '__main__':
    etl_web_to_gcs()