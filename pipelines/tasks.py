"""
Helper tasks that could fit any pipeline.
"""
from pathlib import Path
from typing import Union
from datetime import timedelta, date
import ruamel.yaml
from uuid import uuid4

import basedosdados as bd
import glob
import pandas as pd
from prefect import task

from pipelines.constants import constants
from pipelines.utils import log


###############
#
# Upload to GCS
#
###############
@task(
    max_retries=constants.TASK_MAX_RETRIES.value,
    retry_delay=timedelta(seconds=constants.TASK_RETRY_DELAY.value),
)
def dump_header_to_csv(data_path: Union[str, Path], wait=None):
    """
    Writes a header to a CSV file.
    """
    # Remove filename from path
    path = Path(data_path)
    if not path.is_dir():
        path = path.parent
    files = glob.glob(f"{path}/*")
    file = files[0] if files else ""

    # Read just first row
    dataframe = pd.read_csv(file, nrows=1)

    # Create directory if it doesn't exist
    save_header_path = Path(f"data/{uuid4()}/header.csv")
    save_header_path.parent.mkdir(parents=True, exist_ok=True)

    # Write dataframe to CSV
    dataframe.to_csv(save_header_path, index=False, encoding="utf-8")
    log(f"Wrote header CSV: {path}")

    return save_header_path


@task(
    max_retries=constants.TASK_MAX_RETRIES.value,
    retry_delay=timedelta(seconds=constants.TASK_RETRY_DELAY.value),
)
def create_bd_table(
    path: Union[str, Path],
    dataset_id: str,
    table_id: str,
    dump_type: str,
    wait=None,  # pylint: disable=unused-argument
) -> None:
    """
    Create table using BD+
    """
    # pylint: disable=C0103
    tb = bd.Table(dataset_id=dataset_id, table_id=table_id)

    # pylint: disable=C0103
    st = bd.Storage(dataset_id=dataset_id, table_id=table_id)

    # full dump
    if dump_type == "append":
        if tb.table_exists(mode="staging"):
            log(
                f"Mode append: Table {st.bucket_name}.{dataset_id}.{table_id} already exists"
            )
        else:
            tb.create(
                path=path,
                location="southamerica-east1",
            )
            log(
                f"Mode append: Sucessfully created a new table {st.bucket_name}.{dataset_id}.{table_id}"
            )  # pylint: disable=C0301

            st.delete_table(
                mode="staging", bucket_name=st.bucket_name, not_found_ok=True
            )
            log(
                f"Mode append: Sucessfully remove header data from {st.bucket_name}.{dataset_id}.{table_id}"
            )  # pylint: disable=C0301
    elif dump_type == "overwrite":
        if tb.table_exists(mode="staging"):
            log(
                f"Mode overwrite: Table {st.bucket_name}.{dataset_id}.{table_id} already exists, DELETING OLD DATA!"
            )  # pylint: disable=C0301
            st.delete_table(
                mode="staging", bucket_name=st.bucket_name, not_found_ok=True
            )
        # prod datasets is public if the project is datario. staging are private im both projects
        tb.create(
            path=path,
            if_storage_data_exists="replace",
            if_table_config_exists="replace",
            if_table_exists="replace",
        )

        log(
            f"Mode overwrite: Sucessfully created table {st.bucket_name}.{dataset_id}.{table_id}"
        )
        st.delete_table(mode="staging", bucket_name=st.bucket_name, not_found_ok=True)
        log(
            f"Mode overwrite: Sucessfully remove header data from {st.bucket_name}.{dataset_id}.{table_id}"
        )  # pylint: disable=C0301


@task(
    max_retries=constants.TASK_MAX_RETRIES.value,
    retry_delay=timedelta(seconds=constants.TASK_RETRY_DELAY.value),
)
def upload_to_gcs(
    path: Union[str, Path],
    dataset_id: str,
    table_id: str,
    wait=None,  # pylint: disable=unused-argument
) -> None:
    """
    Uploads a bunch of CSVs using BD+
    """
    # pylint: disable=C0103
    tb = bd.Table(dataset_id=dataset_id, table_id=table_id)
    # st = bd.Storage(dataset_id=dataset_id, table_id=table_id)

    if tb.table_exists(mode="staging"):
        # the name of the files need to be the same or the data doesn't get overwritten
        tb.append(
            filepath=path,
            if_exists="replace",
        )

        log(
            f"Successfully uploaded {path} to {tb.bucket_name}.staging.{dataset_id}.{table_id}"
        )

    else:
        # pylint: disable=C0301
        log(
            "Table does not exist in STAGING, need to create it in local first.\nCreate and publish the table in BigQuery first."
        )

@task
def update_metadata(dataset_id: str, table_id: str, fields_to_update: list) -> None:
    '''
    Update metadata for a selected table

    dataset_id: dataset_id, 
    table_id: table_id, 
    fields_to_update: list of dictionaries with key and values to be updated
    '''
    handle = bd.Metadata(dataset_id=dataset_id, table_id=table_id)
    handle.create(if_exists='replace')

    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=4, sequence=6, offset=4)

    config_file = handle.filepath.as_posix()

    with open(config_file) as fp:
        data = yaml.load(fp)
    
    # this is, of course, very slow but very few fields will be update each time, so the cubic algo will not have major performance consequences
    for field in fields_to_update:
        for k,v in field.items():
            if isinstance(v, dict):
                for i, j in v.items():
                    data[k][i] = j
            else:
                data[k] = v

    with open(config_file, 'w') as fp:
        yaml.dump(data, fp)
  
    if handle.validate():
        handle.publish(if_exists='replace')
        log(f"Metadata for {table_id} updated")
    else:
        log('Fail to validate metadata.')