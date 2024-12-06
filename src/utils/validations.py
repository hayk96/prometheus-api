from jsonschema import validate, exceptions
import json


def validate_schema(schema_file, data) -> tuple[bool, int, str, str]:
    """
    This function validates the passed object
    provided by the user against the required schema.
    """
    schema_file = f"src/schemas/{schema_file}"
    with open(schema_file) as f:
        schema = json.load(f)
    try:
        validate(instance=data, schema=schema)
    except exceptions.ValidationError as e:
        return False, 400, "error", e.args[0]
    return True, 200, "success", "Data is valid"

