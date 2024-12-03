from src.core.prometheus import PrometheusRequest


class PrometheusConfig(PrometheusRequest):
    def __init__(self):
        super().__init__()

    def partial_update(self, data: dict, user_data: dict):
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

    def rename_global_keyword(self, user_data) -> None:
        """"
        This function replaces the key 'global_' with 'global'
        from the user's input, since Python does not allow a
        key with the name 'global'
        """
        if "global_" in user_data:
            user_data["global"] = user_data["global_"]
            del user_data["global_"]
