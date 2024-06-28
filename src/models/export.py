from pydantic import BaseModel, Extra
from typing import Optional


class ExportData(BaseModel, extra=Extra.allow):
    expr: str
    start: Optional[str] = None
    end: Optional[str] = None
    step: Optional[str] = None
    replace_fields: Optional[dict] = dict()
    _request_body_examples = {
        "Count of successful logins by users per hour in a day": {
            "description": "Count of successful logins by users per hour in a day",
            "value": {
                "expr": "users_login_count{status='success'}",
                "start": "2024-01-30T00:00:00Z",
                "end": "2024-01-31T23:59:59Z",
                "step": "1h",
                "replace_fields": {
                    "__name__": "Name",
                    "timestamp": "Time"
                }
            }
        }
    }
