from jsonschema import validate, exceptions
from src.utils.arguments import arg_parser
import requests
import json
import copy
import csv
import os

prom_addr = arg_parser().get("prom.addr")


def prom_query(query, range_query=False, start="0", end="0",
               step="0", url=prom_addr) -> tuple[bool, int, dict]:
    """
    This function queries data from Prometheus
    based on the information provided by the
    user and returns the data as a dictionary.
    """
    try:
        r = requests.post(f"{url}/api/v1/{'query_range' if range_query else 'query'}",
                          data={
                              "query": query,
                              "start": start,
                              "end": end,
                              "step": step},
                          headers={"Content-Type": "application/x-www-form-urlencoded"})
    except BaseException as e:
        return False, 500, {"status": "error",
                            "error": f"Prometheus query has failed. {e}"}
    else:
        return True if r.status_code == 200 else False, r.status_code, r.json()


def data_processor(source_data: dict) -> tuple[list, list]:
    """
    This function preprocesses the results
    of the Prometheus query for future formatting.
    It returns all labels of the query result
    and the data of each time series.
    """
    data_raw = copy.deepcopy(source_data)
    data_processed, unique_labels = [], set()
    data_result = data_raw["data"]["result"]

    def vector_processor():
        for ts in data_result:
            ts_labels = set(ts["metric"].keys())
            unique_labels.update(ts_labels)
            series = ts["metric"]
            series["timestamp"] = ts["value"][0]
            series["value"] = ts["value"][1]
            data_processed.append(series)

    def matrix_processor():
        for ts in data_result:
            ts_labels = set(ts["metric"].keys())
            unique_labels.update(ts_labels)
            series = ts["metric"]
            for idx in range(len(ts["values"])):
                series_nested = copy.deepcopy(series)
                series_nested["timestamp"] = ts["values"][idx][0]
                series_nested["value"] = ts["values"][idx][1]
                data_processed.append(series_nested)
                del series_nested

    if data_raw["data"]["resultType"] == "vector":
        vector_processor()
    elif data_raw["data"]["resultType"] == "matrix":
        matrix_processor()

    unique_labels = sorted(unique_labels)
    unique_labels.extend(["timestamp", "value"])
    return unique_labels, data_processed


def validate_request(schema_file, data) -> tuple[bool, int, str, str]:
    """
    This function validates the request object
    provided by the user against the required schema.
    It will be moved into the utils package in the future.
    """
    schema_file = f"src/schemas/{schema_file}"
    with open(schema_file) as f:
        schema = json.load(f)
    try:
        validate(instance=data, schema=schema)
    except exceptions.ValidationError as e:
        return False, 400, "error", e.args[0]
    return True, 200, "success", "Request is valid"


def cleanup_files(file) -> tuple[True, str]:
    """
    This function removes the generated file
    once it sends a response to the user.
    """
    try:
        os.remove(file)
    except BaseException as e:
        return False, str(e)
    else:
        return True, "File has been removed successfully"


def csv_generator(data, fields, filename) -> tuple[bool, str, str]:
    """
    This function generates a CSV file
    based on the provided objects.
    """
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data)
    except BaseException as e:
        return False, "error", str(e)
    else:
        return True, "success", "CSV file has been generated successfully"
