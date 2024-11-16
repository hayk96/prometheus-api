from src.utils.arguments import arg_parser
import requests
import yaml

prom_addr = arg_parser().get("prom.addr")


def get_prometheus_config(prometheus_addr=prom_addr) -> tuple[bool, int, dict]:
    try:
        r = requests.request(method="GET", url=f"{prometheus_addr}/api/v1/status/config")
    except BaseException as e:
        return False, 500, {"status": "error",
                            "error": f"Failed to connect to Prometheus. {e}"}
    else:
        if r.status_code == 200:
            data_raw = r.json().get("data")
            data = yaml.load(data_raw.get("yaml"), Loader=yaml.SafeLoader)
            return True, r.status_code, data
        return False, r.status_code, {"status": "error", "error": r.reason}


def partial_update(user_data: dict, data: dict):
    for k in user_data.keys():
        if isinstance(user_data[k], list) and isinstance(data[k], list):
            data[k].extend(user_data[k])
        elif isinstance(user_data[k], dict) and isinstance(data[k], dict):
            data[k].update(user_data[k])
        elif isinstance(user_data[k], str) and isinstance(data[k], str):
            data[k] = user_data[k]