from src.utils.arguments import arg_parser
from src.utils.settings import prom_info
from src.utils.log import logger
from pytimeparse2 import parse
import json

rule_path = arg_parser().get("rule.path")
prom_addr = arg_parser().get("prom.addr")
policies_data_file = ".policies.json"


def sync_to_file(data) -> None:
    """This function saves metrics lifecycle policies
    JSON object into file once it's updated"""
    global rule_path, policies_data_file
    with open(f"{rule_path}/{policies_data_file}", "w") as f:
        f.write(json.dumps(data))
    logger.debug(
        f"Policy has been updated in file {rule_path}/{policies_data_file}.")


def create_policy(name: str, match: str, keep_for: str,
                  description: str, data: dict) -> tuple[int, str, str]:
    """This function creates a new metrics lifecycle policy"""
    global rule_path, policies_data_file
    if name in data.keys():
        return 409, "error", "The requested policy already exists"
    try:
        data[name] = {
            "match": match,
            "keep_for": keep_for,
            "description": description
        }
        sync_to_file(data)
    except BaseException as e:
        return 500, "error", f"Failed to save policy. {e}"
    return 200, "success", "Policy created successfully"


def update_policy(name: str, data: dict,
                  policies: dict) -> tuple[int, str, str]:
    """This function updates the existing metrics lifecycle policy"""
    global rule_path, policies_data_file

    if name not in policies.keys():
        return 404, "error", "Policy not found"
    try:
        policies[name].update(data)
        sync_to_file(policies)
    except BaseException as e:
        return 500, "error", f"Failed to update policy. {e}"
    return 200, "success", "Policy updated successfully"


def delete_policy(name: str, policies: dict) -> tuple[int, str, str]:
    """This function deletes a metrics lifecycle policy"""
    global rule_path, policies_data_file

    if name not in policies.keys():
        return 404, "error", "Policy not found"
    try:
        del policies[name]
        sync_to_file(policies)
    except BaseException as e:
        return 500, "error", f"Failed to update policy. {e}"
    return 204, "success", "Policy deleted successfully"


def load_policies() -> dict:
    """This function loads metrics lifecycle policies
     object into memory at runtime of the application"""
    global rule_path, policies_data_file
    policies = dict()
    try:
        with open(f"{rule_path}/{policies_data_file}", "r") as f:
            policies = json.loads(f.read())
    except FileNotFoundError:
        logger.debug("No metrics lifecycle policies configured yet")
    except BaseException as e:
        logger.error(f"Failed to load metrics lifecycle policies. {e}")
    finally:
        return policies


def validate_duration(val) -> tuple[bool, int, str, str, int]:
    """
    This function compares the value of the 'keep_for'
    field with the retention time of the Prometheus server
    """
    prom_storage_retention_human = prom_info(
        prom_addr, "/runtimeinfo")["data"]["storageRetention"]
    prom_storage_retention_seconds = parse(prom_storage_retention_human)
    val_seconds = parse(val)
    if val_seconds >= prom_storage_retention_seconds:
        return False, 422, "error", f"Invalid duration: 'keep_for' must be less than Prometheus " \
            f"TSDB storage retention time, which is {prom_storage_retention_human}", 0
    return True, 200, "success", "Duration is valid", val_seconds


def validate_prom_admin_api() -> tuple[bool, int, str, str]:
    prom_admin_api_status = prom_info(
        prom_addr, "/flags")["data"]["web.enable-admin-api"]
    if prom_admin_api_status == "false":
        return False, 500, "error", "Metrics lifecycle policy API requires enabling Prometheus admin APIs. " \
                                    "For more information on configuration, check out this documentation " \
                                    "https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-admin-apis"
    return True, 200, "success", "Prometheus admin API is enabled"
