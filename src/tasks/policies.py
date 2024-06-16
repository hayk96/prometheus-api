from src.core.policies import load_policies
from src.utils.arguments import arg_parser
from src.utils.log import logger
from pytimeparse2 import parse
from time import time
import requests


prom_addr = arg_parser().get("prom.addr")
running_tasks = False


def delete_series(policy_name: str, policy: dict) -> bool:
    """
    This function calls following Prometheus endpoint:
    POST /api/v1/admin/tsdb/delete_series
    User-defined policies passed to this function
    perform clean-up based on the specified policy settings.
    """
    time_range = time() - parse(policy["keep_for"])
    try:
        r = requests.post(
            f'{prom_addr}/api/v1/admin/tsdb/delete_series?match[]={policy["match"]}&end={time_range}')
    except BaseException as e:
        logger.error(e, extra={"policy_name": policy_name})
    else:
        if r.status_code == 204:
            logger.debug("Task clean-up time-series has been successfully completed",
                         extra={"policy_name": policy_name})
            return True
        logger.error(f"Failed to delete series, {r.json().get('error')}", extra={
                     "status": r.status_code, "policy_name": policy_name})
    return False


def clean_tombstones() -> bool:
    """
    This function calls following Prometheus endpoint:
    POST /api/v1/admin/tsdb/clean_tombstones
    Removes the deleted data from disk and
    cleans up the existing tombstones
    """
    try:
        r = requests.post(
            f'{prom_addr}/api/v1/admin/tsdb/clean_tombstones')
    except BaseException as e:
        logger.error(e)
    else:
        if r.status_code == 204:
            return True
        logger.error(f"Failed to clean tombstones, {r.json().get('error')}", extra={
            "status": r.status_code})
    return False


def run_policies() -> bool:
    """
    This function loops over user-defined metrics lifecycle
    policies and executes the clean-up job one by one
    """
    global running_tasks
    if running_tasks:
        logger.warning(
            "Cannot create a new task. Server is currently processing another task")
        return False

    policies = load_policies()
    if policies:
        logger.debug(
            f"Found {len(policies)} metrics lifecycle {'policies' if len(policies) > 1 else 'policy'}. "
            f"Starting job to clean-up time-series.")
        running_tasks = True
        start_time = time()
        for p in policies:
            logger.debug(
                "Task clean-up series is in progress", extra={
                    "policy_name": p, "match": policies[p]["match"],
                    "keep_for": policies[p]["keep_for"]})
            delete_series(policy_name=p, policy=policies[p])
        clean_tombstones()
        exec_time = float("{:.2f}".format(time() - start_time))
        running_tasks = False
        logger.debug(
            "Task clean-up series has been completed", extra={
                "duration": exec_time})
    return True
