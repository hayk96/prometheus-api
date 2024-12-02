from src.utils.arguments import arg_parser
from src.utils.log import logger
import requests
import yaml
import os


class PrometheusRequest:

    def __init__(self,
                 prom_addr=arg_parser().get("prom.addr"),
                 prom_config_file=arg_parser().get("config.file"),
                 prom_rule_path=arg_parser().get("rule.path")):
        self.prom_addr = prom_addr
        self.prom_rule_path = prom_rule_path
        self.prom_config_file = prom_config_file

    def get_prometheus_config(self) -> tuple[bool, int, dict]:
        """
        This function returns current configuration
        of Prometheus as a dictionary object
        """
        try:
            r = requests.request(method="GET",
                                 url=f"{self.prom_addr}/api/v1/status/config")
        except BaseException as e:
            return False, 500, {"status": "error",
                                "error": f"Failed to connect to Prometheus. {e}"}
        else:
            if r.status_code == 200:
                data_raw = r.json().get("data")
                data = yaml.load(data_raw.get("yaml"), Loader=yaml.SafeLoader)
                return True, r.status_code, data
            return False, r.status_code, {"status": "error", "error": r.reason}

    def update_prometheus_yml(self, data: str) -> tuple[bool, str]:
        """
        This function updates Prometheus
        configuration file (prometheus.yml)
        """
        try:
            with open(self.prom_config_file, "w") as f:
                f.write(data)
        except BaseException as e:
            logger.error(
                f"Failed to update Prometheus configuration file. {e}")
            return False, str(e)
        else:
            logger.debug(
                f"Successfully updated Prometheus configuration file: {self.prom_config_file}")
            return True, "success"

    def create_rule(self, file, data) -> tuple[bool, str, str]:
        """Creates Prometheus rule file"""
        try:
            with open(f"{self.prom_rule_path}/{file}", "w") as f:
                rule_as_yaml = yaml.dump(data)
                f.write(rule_as_yaml)
        except (IOError, yaml.YAMLError) as e:
            return False, "error", str(e)
        return True, "success", "The rule was created successfully"

    def delete_rule(self, file) -> tuple[bool, str, str]:
        """Deletes Prometheus rule file"""
        try:
            os.remove(f"{self.prom_rule_path}/{file}")
        except OSError as e:
            return False, "error", str(e.strerror)
        return True, "success", "The rule was deleted successfully"

    def reload(self) -> tuple[int, str, str]:
        """Reloads the Prometheus configuration"""
        try:
            r = requests.post(f"{self.prom_addr}/-/reload")
        except requests.RequestException as e:
            return 500, "error", str(e)
        return r.status_code, "success" if r.status_code == 200 else "error", r.text



