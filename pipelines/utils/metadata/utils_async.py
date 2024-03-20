# -*- coding: utf-8 -*-

###
## Módulo de funções para fazer interagir de forma assíncrona com a api.
###

import asyncio
import aiohttp
import json
import re
from pipelines.utils.metadata.utils import get_id, get_token
#from pipelines.utils.metadata.utils import create_quality_check_async
from pipelines.utils.utils import get_credentials_from_secret, log, get_credentials_utils
import pandas as pd

# async def get_id_async(
#     query_class,
#     query_parameters,
#     email,
#     password,
#     api_mode: str = "prod",
#     cloud_table: bool = True,
# ):
#     token = await get_token_async(email, password, api_mode)
#     header = {
#         "Authorization": f"Bearer {token}",
#     }
#     _filter = ", ".join(list(query_parameters.keys()))

#     keys = [
#         parameter.replace("$", "").split(":")[0]
#         for parameter in list(query_parameters.keys())
#     ]

#     values = list(query_parameters.values())

#     _input = ", ".join([f"${key}:{key}" for key in keys])

#     if cloud_table:
#         query = f"""query({_filter}) {{
#                             {query_class}({_input}){{
#                             edges{{
#                                 node{{
#                                 id,
#                                 table{{
#                                     _id
#                                     }}
#                                 }}
#                             }}
#                             }}
#                         }}"""

#     else:
#         query = f"""query({_filter}) {{
#                             {query_class}({_input}){{
#                             edges{{
#                                 node{{
#                                 id,
#                                 }}
#                             }}
#                             }}
#                         }}"""

#     if api_mode == "staging":
#         url = "https://staging.api.basedosdados.org/api/v1/graphql"
#     elif api_mode == "prod":
#         url = "https://api.basedosdados.org/api/v1/graphql"

#     async with aiohttp.ClientSession() as session:
#         async with session.post(
#             url=url,
#             json={"query": query, "variables": dict(zip(keys, values))},
#             headers=header,
#         ) as response:
#             data = await response.json()

#             if "data" in data and data is not None:
#                 if data.get("data", {}).get(query_class, {}).get("edges") == []:
#                     id = None
#                     # print(f"get: not found {query_class}", dict(zip(keys, values)))
#                 else:
#                     id = data["data"][query_class]["edges"][0]["node"]["id"]
#                     # print(f"get: found {id}")
#                     id = id.split(":")[1]

#                 return data, id
#             else:
#                 log(data)
#                 raise Exception(
#                     f"Error: the executed query did not return a data json.\nExecuted query:\n{query} \nVariables: {dict(zip(keys, values))}"
#                 )

# async def get_token_async(email, password, api_mode: str = "prod"):
#     """
#     Get api token asynchronously.
#     """
#     if api_mode == "prod":
#         url = "http://api.basedosdados.org/api/v1/graphql"
#     elif api_mode == "staging":
#         url = "http://staging.api.basedosdados.org/api/v1/graphql"

#     async with aiohttp.ClientSession() as session:
#         async with session.post(
#             url=url,
#             headers={"Content-Type": "application/json"},
#             json={
#                 "query": """
#             mutation ($email: String!, $password: String!) {
#                 tokenAuth(email: $email, password: $password) {
#                     token
#                 }
#             }
#         """,
#                 "variables": {"email": email, "password": password},
#             },
#         ) as response:
#             response.raise_for_status()
#             data = await response.json()
#             return data["data"]["tokenAuth"]["token"]

async def create_update_async(
    email,
    password,
    mutation_class,
    mutation_parameters,
    query_class,
    query_parameters,
    update=True,
    api_mode: str = "prod",
):
    token = get_token(
        email=email,
        password=password,
        api_mode=api_mode,
    )

    header = {
        "Authorization": f"Bearer {token}",
    }

    r, id = get_id(
        query_class=query_class,
        query_parameters=query_parameters,
        email=email,
        password=password,
        cloud_table=False,
        api_mode=api_mode,
    )
    if id is not None:
        r["r"] = "query"
        if update is False:
            print(r, id)

    _classe = mutation_class.replace("CreateUpdate", "").lower()
    query = f"""
                mutation($input:{mutation_class}Input!){{
                    {mutation_class}(input: $input){{
                    errors {{
                        field,
                        messages
                    }},
                    clientMutationId,
                    {_classe} {{
                        id,
                    }}
                }}
                }}
            """

    if update is True and id is not None:
        mutation_parameters["id"] = id

    if api_mode == "prod":
        url = "https://api.basedosdados.org/api/v1/graphql"
    elif api_mode == "staging":
        url = "https://staging.api.basedosdados.org/api/v1/graphql"

    async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={"query": query, "variables": {"input": mutation_parameters}},
                headers=header,
            ) as response:
                r = await response.json()
                log(f"Response: {r}")

            r["r"] = "mutation"
            if "data" in r and r is not None:
                if r.get("data", {}).get(mutation_class, {}).get("errors", []) != []:
                    print(f"create: not found {mutation_class}", mutation_parameters)
                    print("create: error\n", json.dumps(r, indent=4, ensure_ascii=False), "\n")
                    id = None
                    raise Exception("create: Error")
                else:
                    id = r["data"][mutation_class][_classe]["id"]
                    id = id.split(":")[1]

                    return r, id
            else:
                print("\n", "create: query\n", query, "\n")
                print(
                    "create: input\n",
                    json.dumps(mutation_parameters, indent=4, ensure_ascii=False),
                    "\n",
                )
                print("create: error\n", json.dumps(r, indent=4, ensure_ascii=False), "\n")
                raise Exception("create: Error")



async def create_quality_check_async(email:str, password:str, name:str, description:str, passed:str, dataset_id:str, table_id:str,api_mode:str = "prod", ):
    table_result, id = get_id(
        email=email,
        password=password,
        query_class="allCloudtable",
        query_parameters={
            "$gcpDatasetId: String": dataset_id,
            "$gcpTableId: String": table_id,
        },
        cloud_table=True,
        api_mode=api_mode,
    )

    result_id = table_result["data"]["allCloudtable"]["edges"][0]["node"][
        "table"
    ].get("_id")

    quality_check, quality_check_id = get_id(
        email=email,
        password=password,
        query_class="allQualitycheck",
        query_parameters={
            "$name: String": name,
            "$table_Id: ID": result_id,

        },
        cloud_table=False,
        api_mode=api_mode,
    )

    if not id:
        raise ValueError("Table ID not found.")

    parameters = {
                            "name": name,
                            "description": description,
                            "passed": True if passed == 'pass' else False,
                            "table": result_id
        }

    await create_update_async(
        query_class="allQualitycheck",
        query_parameters={"$id: ID": quality_check_id},
        mutation_class="CreateUpdateQualityCheck",
        mutation_parameters=parameters,
        update=True,
        email=email,
        password=password,
        api_mode=api_mode,
)



async def create_update_quality_checks_async(tests_results: pd.DataFrame, api_mode: str = "prod"):
    (email, password) = get_credentials_utils(secret_path=f"api_user_{api_mode}")
    semaphore = asyncio.Semaphore(16)
    async with semaphore:
        tasks = [create_quality_check_async(email = email, password = password, name =row['name'],description= row['description'], passed =row['status'], dataset_id = row['dataset_id'], table_id= row['table_id']) for index, row in tests_results.iterrows() ]
        await asyncio.gather(*tasks)