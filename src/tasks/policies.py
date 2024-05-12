from src.core.policies import load_policies
from src.utils.arguments import arg_parser
from src.utils.log import logger
from pytimeparse2 import parse
import requests
import time

prom_addr = arg_parser().get("prom.addr")


def delete_series(policy_name: str, policy: dict) -> None:
    """
    This function calls two Prometheus endpoints:
    * POST /api/v1/admin/tsdb/delete_series
    * POST /api/v1/admin/tsdb/clean_tombstones
    User-defined policies passed to this function
    perform cleanup based on the specified policy settings.
    """
    time_range = time.time() - parse(policy["keep_for"])
    start_time = time.time()
    try:
        r = requests.post(
            f'{prom_addr}/api/v1/admin/tsdb/delete_series?match[]={policy["match"]}&end={time_range}')
    except BaseException as e:
        logger.error(e, extra={"policy_name": policy_name})
    else:
        if r.status_code != 204:
            logger.error(f"Failed to delete series, {r.json().get('error')}", extra={
                         "status": r.status_code, "policy_name": policy_name})
            return
        try:
            r = requests.post(
                f'{prom_addr}/api/v1/admin/tsdb/clean_tombstones')
        except BaseException as e:
            logger.error(e, extra={"policy_name": policy_name})
            return
        else:
            if r.status_code != 204:
                logger.error(f"Failed to clean tombstones, {r.json().get('error')}", extra={
                             "status": r.status_code, "policy_name": policy_name})
                return
        exec_time = float("{:.2f}".format(time.time() - start_time))
        logger.debug("Task cleanup time-series has been successfully completed",
                     extra={"policy_name": policy_name, "exec_time": exec_time})
        return


def task_run_policies():
    """
    This function loops over user-defined metrics lifecycle
    policies and executes the cleanup job one by one
    """
    policies = load_policies()
    if policies:
        logger.debug(
            f"Found {len(policies)} metrics lifecycle {'policies' if len(policies) > 1 else 'policy'}. "
            f"Starting job to cleanup time-series.")
        for p in policies:
            logger.debug(
                f"Task cleanup time-series is in progress", extra={
                    "policy_name": p, "match": policies[p]["match"],
                    "keep_for": policies[p]["keep_for"]})
            delete_series(policy_name=p, policy=policies[p])
