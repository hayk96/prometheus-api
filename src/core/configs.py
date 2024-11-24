from src.utils.arguments import arg_parser
from src.utils.log import logger
import requests
import yaml

prom_addr = arg_parser().get("prom.addr")
prom_config_file = arg_parser().get("config.file")


def get_prometheus_config(prometheus_addr=prom_addr) -> tuple[bool, int, dict]:
    """
    This function returns current configuration
    of Prometheus as a dictionary object
    """
    try:
        r = requests.request(method="GET",
                             url=f"{prometheus_addr}/api/v1/status/config")
    except BaseException as e:
        return False, 500, {"status": "error",
                            "error": f"Failed to connect to Prometheus. {e}"}
    else:
        if r.status_code == 200:
            data_raw = r.json().get("data")
            data = yaml.load(data_raw.get("yaml"), Loader=yaml.SafeLoader)
            return True, r.status_code, data
        return False, r.status_code, {"status": "error", "error": r.reason}


def update_prometheus_yml(data: str) -> tuple[bool, str]:
    """
    This function updates Prometheus
    configuration file (prometheus.yml)
    """
    try:
        with open(prom_config_file, "w") as f:
            f.write(data)
    except BaseException as e:
        logger.error(
            f"Failed to update Prometheus configuration file: {prom_config_file}. {e}")
        return False, str(e)
    else:
        logger.debug(
            f"Successfully updated Prometheus configuration file: {prom_config_file}")
        return True, "success"


def partial_update(user_data: dict, data: dict):
    """
    This function updates objects depending on their types
    """
    for k in user_data.keys():
        if isinstance(user_data[k], list) and isinstance(data[k], list):
            data[k].extend(user_data[k])
        elif isinstance(user_data[k], dict) and isinstance(data[k], dict):
            data[k].update(user_data[k])
        elif isinstance(user_data[k], str) and isinstance(data[k], str):
            data[k] = user_data[k]
