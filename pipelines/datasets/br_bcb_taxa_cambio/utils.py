# -*- coding: utf-8 -*-
"""
General purpose functions for the br_bcb_indicadores project
"""
import requests
import pandas as pd
import datetime
import pytz
from datetime import timedelta
import os
from io import StringIO
import time as tm
from pipelines.datasets.br_bcb_taxa_cambio.constants import constants as bcb_constants
from pipelines.utils.utils import (
    connect_to_endpoint_json,
    log,
)
from pipelines.utils.apply_architecture_to_dataframe.utils import apply_architecture_to_dataframe

###############################################################################
#
# Esse é um arquivo onde podem ser declaratas funções que serão usadas
# pelo projeto br_bcb_indicadores.
#
# Por ser um arquivo opcional, pode ser removido sem prejuízo ao funcionamento
# do projeto, caos não esteja em uso.
#
# Para declarar funções, basta fazer em código Python comum, como abaixo:
#
# ```
# def foo():
#     """
#     Function foo
#     """
#     print("foo")
# ```
#
# Para usá-las, basta fazer conforme o exemplo abaixo:
#
# ```py
# from pipelines.datasets.br_bcb_indicadores.utils import foo
# foo()
# ```
#
###############################################################################


def available_currencies() -> dict:
    """
    Return available currencies from api
    """
    url = bcb_constants.API_URL.value["taxa_cambio_moedas"]
    json_response = connect_to_endpoint_json(url)
    log(f"available currencies:{json_response['value']}")
    return json_response["value"]


def create_url_currency(start_date: str, end_date: str, moeda="USD") -> str:
    """
    Creates parameterized url
    """
    search_url = bcb_constants.API_URL.value["taxa_cambio"].format(
        moeda, start_date, end_date
    )
    log(search_url)
    return search_url


def get_currency_data(currency: dict) -> pd.DataFrame:
    """
    Retrieves currency data for a specific currency from an API endpoint.

    Args:
        currency (dict): A dictionary containing information about the currency.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the retrieved currency data.

    Raises:
        requests.exceptions.Timeout: If the connection to the API endpoint times out.

    """

    # Get the start date as 14 days before the current date
    start_day = datetime.datetime.now(tz=pytz.UTC) - timedelta(days=14)
    start_day = start_day.strftime("%m-%d-%Y")

    # Log the start day
    log(f"start day: {start_day}")

    # Calculate the end date as 7 days before the current date
    now = datetime.datetime.now(tz=pytz.UTC) - timedelta(days=7)
    end_day = now.strftime("%m-%d-%Y")

    # Log the end day
    log(f"end day: {end_day}")

    # Get the currency code for the current currency
    currency_code = currency["simbolo"]

    # Create the URL for retrieving data using the start and end dates and currency code
    log("creating_url")
    url = create_url_currency(start_day, end_day, currency_code)

    # Connect to the API endpoint and retrieve the JSON response
    attempts = 0
    while attempts < 3:
        attempts += 1
        log(f"tentativa {attempts}")
        try:
            log("connecting to endpoint")
            json_response = connect_to_endpoint_json(url)
            break
        except requests.exceptions.Timeout:
            tm.sleep(3)

    # Extract the currency data from the JSON response
    data = json_response["value"]

    # Convert the data into a DataFrame
    log("transform json into df")
    df = pd.DataFrame(data)

    # Add columns about the currency code to the DataFrame
    log("Add columns about the currency code")
    df["moeda"] = currency["simbolo"]
    df["tipo_moeda"] = currency["tipoMoeda"]

    return df


def treat_currency_df(df: pd.DataFrame, table_id: str) -> pd.DataFrame:
    """
    Performs data treatment on the currency DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame containing currency data.
        table_id (str): The identifier for the architecture table.
    Returns:
        pd.DataFrame: The treated DataFrame with renamed and reordered columns.
    """

    # Convert the 'dataHoraCotacao' column in 'df' to datetime format
    log("Convert the 'dataHoraCotacao' column in 'df' to datetime format")
    df["dataHoraCotacao"] = pd.to_datetime(
        df["dataHoraCotacao"], format="%Y-%m-%d %H:%M:%S.%f"
    )

    # Extract the date and time components from 'dataHoraCotacao' column and create new columns 'data_cotacao' and 'hora_cotacao'
    log(
        "Extract the date and time components from 'dataHoraCotacao' column and create new columns 'data_cotacao' and 'hora_cotacao'"
    )
    df["data_cotacao"] = df["dataHoraCotacao"].dt.date
    df["hora_cotacao"] = df["dataHoraCotacao"].dt.time

    df = apply_architecture_to_dataframe(
        df,
        url_architecture=bcb_constants.ARCHITECTURE_URL.value["taxa_cambio"],
        apply_include_missing_columns=False,
    )

    return df


def save_input(df: pd.DataFrame, table_id: str) -> str:
    """
    Saves a DataFrame as a CSV file in the input folder.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        table_id (str): The identifier for the table.

    Returns:
        str: The full file path of the saved CSV file.

    """

    # Define the folder path for storing the file
    folder = f"tmp/{table_id}/input/"
    # Create the folder if it doesn't exist
    os.system(f"mkdir -p {folder}")
    # Define the full file path for the CSV file
    full_filepath = f"{folder}/{table_id}.csv"
    # Save the DataFrame as a CSV file
    df.to_csv(full_filepath, index=False)
    log("save_input")
    return full_filepath


def save_output(df: pd.DataFrame, table_id: str) -> str:
    """
    Saves a DataFrame as a CSV file in the output folder.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        table_id (str): The identifier for the table.

    Returns:
        str: The full file path of the saved CSV file.

    """

    # Define the folder path for storing the file
    folder = f"tmp/{table_id}/output/"
    # Create the folder if it doesn't exist
    os.system(f"mkdir -p {folder}")
    # Define the full file path for the CSV file
    full_filepath = f"{folder}/{table_id}.csv"
    # Save the DataFrame as a CSV file
    df.to_csv(full_filepath, index=False)
    log("save_output")
    return full_filepath


def read_input_csv(table_id: str):
    """
    Reads and returns the input CSV file as a DataFrame.

    Args:
        table_id (str): The identifier for the table.

    Returns:
        pd.DataFrame: The DataFrame read from the input CSV file.

    """

    # Define the path of the input CSV file
    path = f"tmp/{table_id}/input/{table_id}.csv"
    log("read input")
    # Read the CSV file as a DataFrame
    return pd.read_csv(path)
