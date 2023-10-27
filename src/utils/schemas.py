from jsonschema import Draft202012Validator
from .log import logger


def fetch_rule_schema(url) -> (bool, str):
    """
    Fetch schema of Prometheus rule from the https://schemastore.org
    """
    try:
        logger.info(f"Downloading {url} from SchemaStore")
        schema = Draft202012Validator(
            {"$ref": f"{url}"})
        schema.validate({})
    except Exception as e:
        logger.error(e)
        return False, "error"
    else:
        logger.info(
            "Successfully downloaded the schema for Prometheus rules from SchemaStore")
        return True, schema


rule_schema_status, rule_schema = fetch_rule_schema(
    "https://json.schemastore.org/prometheus.rules.json")
