from os import remove, path
from .log import logger
from time import sleep
import requests


def check_prom_readiness(prometheus_address) -> bool:
    """Checks the connection to the Prometheus server over HTTP."""
    try:
        r = requests.get(f"{prometheus_address}/-/ready")
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
    else:
        if r.status_code == 200:
            logger.info(
                "The connection to the Prometheus server has been established successfully!")
            return True
        else:
            logger.error(
                "Please ensure that the Prometheus server is ready and able to receive connections.")
            return False


def establish_prom_connection(prometheus_address, retries=600) -> bool:
    """
    This function continuously checks the
    connection to the Prometheus server, waiting
    for it to establish. The total wait time is
    30 minutes (600 checks at 3-second intervals)
    """
    for i in range(retries):
        if check_prom_readiness(prometheus_address):
            return True
        sleep(3)
    logger.error(
        "Connection to Prometheus failed: Maximum retry attempts exceeded. The server has been shut down.")
    return False


def check_reload_api_status(prometheus_address) -> bool:
    """Checks the status of the Prometheus Management API."""
    try:
        r = requests.post(f"{prometheus_address}/-/reload")
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
    else:
        if r.status_code == 403:
            logger.error(
                f"{r.text} It's disabled by default and can be enabled via the --web.enable-lifecycle. "
                f"See https://prometheus.io/docs/prometheus/latest/management_api/#reload for more details.")
            return False
        return True


def check_rules_directory(prometheus_rules_dir) -> bool:
    """
    Checks the directory of the rule files. The provided
    directory must be accessible by the server.
    """
    if (not path.exists(prometheus_rules_dir)) or (
            not path.isdir(prometheus_rules_dir)):
        logger.error(
            f"{prometheus_rules_dir}: The directory you provided does not exist. "
            f"Please make sure it exists before proceeding.")
        return False
    return True


def check_fs_permissions(prometheus_rules_dir) -> bool:
    """
    Checks the necessary permissions for the server. The server should
    be able to create and delete files in the provided rules directory.
    """
    try:
        with open(f"{prometheus_rules_dir}/.test.yml", "w") as f:
            f.write("Do I have a write permission?")
        remove(f"{prometheus_rules_dir}/.test.yml")
    except OSError as e:
        logger.error(
            f"The temporary file could not be created or deleted for testing permissions. {e}")
        return False
    else:
        logger.debug(
            "The application has the necessary permissions to access the rule files directory.")
        return True


def prom_info(prometheus_address, sub_path) -> dict:
    """
    Returns various runtime, and configuration information properties
    about the Prometheus server based on the sub_path parameter
    """
    try:
        r = requests.get(f"{prometheus_address}/api/v1/status{sub_path}")
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return {}
    return r.json()
