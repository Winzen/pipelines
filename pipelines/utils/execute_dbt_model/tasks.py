# -*- coding: utf-8 -*-
"""
Tasks related to DBT flows.
"""
# pylint: disable=unused-argument

from datetime import timedelta

from dbt_client import DbtClient
from prefect import task
from pipelines.utils.utils import log

from pipelines.utils.execute_dbt_model.utils import (
    get_dbt_client,
    parse_dbt_logs,
)
from pipelines.constants import constants


@task(
    checkpoint=False,
    max_retries=constants.TASK_MAX_RETRIES.value,
    retry_delay=timedelta(seconds=constants.TASK_RETRY_DELAY.value),
)
def get_k8s_dbt_client(
    mode: str = "dev",
    wait=None,
) -> DbtClient:
    """
    Get a DBT client for the Kubernetes cluster.
    """
    if mode not in ["dev", "prod"]:
        raise ValueError(f"Invalid mode: {mode}")
    return get_dbt_client(
        host=f"dbt-rpc-{mode}",
    )


@task(
    checkpoint=False,
    max_retries=constants.TASK_MAX_RETRIES.value,
    retry_delay=timedelta(seconds=constants.TASK_RETRY_DELAY.value),
)
def run_dbt_model(
    dbt_client: DbtClient,
    dataset_id: str,
    table_id: str,
    dbt_alias: bool,
    dbt_test: bool,
    sync: bool = True,
):
    """
    Run a DBT model.
    """
    if dbt_alias:
        table_id = f"{dataset_id}__{table_id}"

    # dbt_client.cli(
    #     f"run --models {dataset_id}.{table_id}",
    #     sync=sync,
    #     logs=True,
    # )

    if dbt_test:
        log(f"test --models {dataset_id}.{table_id}  --store-failures")
        logs_dict  = dbt_client.cli(
            f"test --models {dataset_id}.{table_id}  --store-failures",
            sync=sync,
            logs=True,
        )
        for event in logs_dict["result"]["logs"]:
            if event["levelname"] == "INFO" or event["levelname"] == "ERROR":
                log(f"#####{event['levelname']}#####")
                log(event["message"])
            if event["levelname"] == "DEBUG":
                if "On model" in event["message"]:
                    log(event["message"])