from src.models.mlp import MetricsLifecyclePolicy
from src.utils.arguments import arg_parser
from src.utils.log import logger
import json


class MetricsLifecyclePolicyService(MetricsLifecyclePolicy):
    _prom_addr = arg_parser().get("prom.addr")
    _rule_path = arg_parser().get("rule.path")
    _mlp_data_file = ".mlp-data.json"

    def create_policy(self, data: dict) -> tuple[int, str, str]:
        if self.name in data.keys():
            return 409, "error", "The requested policy already exists"
        try:
            data[self.name] = {
                "pattern": self.pattern,
                "delete_after": self.delete_after,
                "description": self.description
            }
            with open(f"{self._rule_path}/{self._mlp_data_file}", "w") as f:
                f.write(json.dumps(data))
                logger.debug(
                    f"MLP data has been successfully saved in {self._rule_path}/{self._mlp_data_file}")
        except BaseException as e:
            return 500, "error", f"Failed to save policy. {e}"
        return 200, "success", "Policy created successfully"

    def update_policy(self, data: dict, **kwargs) -> tuple[int, str, str]:
        if self.name not in data.keys():
            return 404, "error", "Policy not found"
        try:
            data[self.name].update(**kwargs)
            with open(f"{self._rule_path}/{self._mlp_data_file}", "w") as f:
                f.write(json.dumps(data))
                logger.debug(
                    f"MLP data has been successfully updated in {self._rule_path}/{self._mlp_data_file}")
        except BaseException as e:
            return 500, "error", f"Failed to update policy. {e}"
        return 200, "success", "Policy updated successfully"


def load_policies() -> dict:
    _rule_path = arg_parser().get("rule.path")
    _mlp_data_file = ".mlp-data.json"
    policies = dict()
    try:
        with open(f"{_rule_path}/{_mlp_data_file}", "r") as f:
            policies = f.read()
            policies = json.loads(policies)
    except FileNotFoundError:
        logger.debug(f"MLP data does not exist yet")
    except BaseException as e:
        logger.error(f"Somthing went wrong. {e}")
    finally:
        return policies
