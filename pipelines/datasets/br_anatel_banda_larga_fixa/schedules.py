# -*- coding: utf-8 -*-
"""
Schedules for dataset br_anatel_banda_larga_fixa
"""

from datetime import datetime

from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock, IntervalClock

from pipelines.constants import constants

anatel_microdados = Schedule(
    clocks=[
        CronClock(
            cron="0 15 * * *",  # ! goes execute every day 12 pm
            start_date=datetime(2023, 4, 3, 7, 5, 0),  # ! first date that the pipeline executed
            labels=[
                constants.BASEDOSDADOS_PROD_AGENT_LABEL.value,  # ! label of identify (ex: basedosdados-dev)
            ],
            parameter_defaults={
                "dataset_id": "br_anatel_banda_larga_fixa",
                "table_id": "microdados",
                "materialization_mode": "prod",
                "materialize_after_dump": True,
                "dbt_alias": True,
                "update_metadata": True,
            },
        ),
    ]
)

anatel_densidade_municipio = Schedule(
    clocks=[
        CronClock(
            cron="0 16 * * *",  # ! goes execute every day 12 pm
            start_date=datetime(2023, 4, 3, 7, 5, 0),  # ! first date that the pipeline executed
            labels=[
                constants.BASEDOSDADOS_PROD_AGENT_LABEL.value,  # ! label of identify (ex: basedosdados-dev)
            ],
            parameter_defaults={
                "dataset_id": "br_anatel_banda_larga_fixa",
                "table_id": "densidade_municipio",
                "materialization_mode": "prod",
                "materialize_after_dump": True,
                "dbt_alias": True,
                "update_metadata": True,
            },
        ),
    ]
)

anatel_densidade_brasil = Schedule(
    clocks=[
        CronClock(
            cron="0 17 * * *",  # ! goes execute every day 12 pm
            start_date=datetime(2023, 4, 3, 7, 5, 0),  # ! first date that the pipeline executed
            labels=[
                constants.BASEDOSDADOS_PROD_AGENT_LABEL.value,  # ! label of identify (ex: basedosdados-dev)
            ],
            parameter_defaults={
                "dataset_id": "br_anatel_banda_larga_fixa",
                "table_id": "densidade_brasil",
                "materialization_mode": "prod",
                "materialize_after_dump": True,
                "dbt_alias": True,
                "update_metadata": True,
            },
        ),
    ]
)

anatel_densidade_uf = Schedule(
    clocks=[
        CronClock(
            cron="0 18 * * *",  # ! goes execute every day 12 pm
            start_date=datetime(2023, 4, 3, 7, 5, 0),  # ! first date that the pipeline executed
            labels=[
                constants.BASEDOSDADOS_PROD_AGENT_LABEL.value,  # ! label of identify (ex: basedosdados-dev)
            ],
            parameter_defaults={
                "dataset_id": "br_anatel_banda_larga_fixa",
                "table_id": "densidade_uf",
                "materialization_mode": "prod",
                "materialize_after_dump": True,
                "dbt_alias": True,
                "update_metadata": True,
            },
        ),
    ]
)
