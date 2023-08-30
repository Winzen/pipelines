# -*- coding: utf-8 -*-
"""
Flows for br_poder360_pesquisas
"""

from datetime import datetime, timedelta

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefect import Parameter, case
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run

from pipelines.utils.execute_dbt_model.constants import constants as dump_db_constants
from pipelines.utils.constants import constants as utils_constants
from pipelines.constants import constants
from pipelines.datasets.br_poder360_pesquisas.tasks import crawler
from pipelines.utils.decorators import Flow
from pipelines.utils.tasks import (
    create_table_and_upload_to_gcs,
    get_temporal_coverage,
    update_metadata,
    rename_current_flow_run_dataset_table,
    get_current_flow_labels,
)
from pipelines.datasets.br_poder360_pesquisas.schedules import every_monday_thursday

# pylint: disable=C0103
with Flow(
    name="br_poder360_pesquisas.microdados", code_owners=["lucas_cr"]
) as br_poder360:
    # Parameters
    dataset_id = Parameter("dataset_id", default="br_poder360_pesquisas", required=True)
    table_id = Parameter("table_id", default="microdados", required=True)
    materialization_mode = Parameter(
        "materialization_mode", default="prod", required=False
    )
    materialize_after_dump = Parameter(
        "materialize after dump", default=True, required=False
    )
    dbt_alias = Parameter("dbt_alias", default=False, required=False)

    rename_flow_run = rename_current_flow_run_dataset_table(
        prefix="Dump: ", dataset_id=dataset_id, table_id=table_id, wait=table_id
    )

    filepath = crawler()

    wait_upload_table = create_table_and_upload_to_gcs(
        data_path=filepath,
        dataset_id=dataset_id,
        table_id=table_id,
        dump_mode="append",
        wait=filepath,
    )

    temporal_coverage = get_temporal_coverage(
        filepath=filepath,
        date_cols=["data"],
        time_unit="year",
        interval="1",
        upstream_tasks=[wait_upload_table],
    )

    # wait_update_metadata = update_metadata(
    #     dataset_id=dataset_id,
    #     table_id=table_id,
    #     fields_to_update=[
    #         {"last_updated": {"data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}},
    #         {"temporal_coverage": [temporal_coverage]},
    #     ],
    #     upstream_tasks=[temporal_coverage],
    # )

    with case(materialize_after_dump, True):
        # Trigger DBT flow run
        current_flow_labels = get_current_flow_labels()
        materialization_flow = create_flow_run(
            flow_name=utils_constants.FLOW_EXECUTE_DBT_MODEL_NAME.value,
            project_name=constants.PREFECT_DEFAULT_PROJECT.value,
            parameters={
                "dataset_id": dataset_id,
                "table_id": table_id,
                "mode": materialization_mode,
                "dbt_alias": dbt_alias,
            },
            labels=current_flow_labels,
            run_name=f"Materialize {dataset_id}.{table_id}",
        )

        wait_for_materialization = wait_for_flow_run(
            materialization_flow,
            stream_states=True,
            stream_logs=True,
            raise_final_state=True,
        )
        wait_for_materialization.max_retries = (
            dump_db_constants.WAIT_FOR_MATERIALIZATION_RETRY_ATTEMPTS.value
        )
        wait_for_materialization.retry_delay = timedelta(
            seconds=dump_db_constants.WAIT_FOR_MATERIALIZATION_RETRY_INTERVAL.value
        )

br_poder360.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
br_poder360.run_config = KubernetesRun(image=constants.DOCKER_IMAGE.value)
br_poder360.schedule = every_monday_thursday
