from src.utils.arguments import arg_parser
from src.utils.schemas import rule_schema
from jsonschema import exceptions
from pydantic import BaseModel
from typing import Optional
import requests
import yaml
import os


class Rule(BaseModel):
    data: Optional[dict] = dict()
    _prom_addr = arg_parser().get("prom.addr")
    _rule_path = arg_parser().get("rule.path")

    def validate_rule(self) -> tuple[bool, str, str]:
        """
        Validates the rule object provided by
        the user against the required schema.
        """
        try:
            rule_schema.validate(self.data)
        except exceptions.ValidationError as e:
            return False, "error", e.args[0]
        return True, "success", "Prometheus rule is valid"

    def create_rule(self, file) -> tuple[bool, str, str]:
        """Creates Prometheus rule file"""
        try:
            with open(f"{self._rule_path}/{file}", "w") as f:
                rule_as_yaml = yaml.dump(self.data)
                f.write(rule_as_yaml)
        except (IOError, yaml.YAMLError) as e:
            return False, "error", str(e)
        return True, "success", "The rule was created successfully"

    def delete_rule(self, file) -> tuple[bool, str, str]:
        """Deletes Prometheus rule file"""
        try:
            os.remove(f"{self._rule_path}/{file}")
        except OSError as e:
            return False, "error", str(e.strerror)
        return True, "success", "The rule was deleted successfully"

    def reload(self) -> tuple[int, str, str]:
        """Reloads the Prometheus configuration"""
        try:
            r = requests.post(f"{self._prom_addr}/-/reload")
        except requests.RequestException as e:
            return int(False), "error", str(e)
        return r.status_code, "success" if r.status_code == 200 else "error", r.text
