from pydantic import BaseModel
from typing import Optional


class MetricsLifecyclePolicy(BaseModel):
    name: str
    pattern: str
    delete_after: str
    description: Optional[str] = None
    _request_body_examples = {
        "GoLang Metrics Lifecycle Policy": {
            "description": "time-series matching with Regexp will be hold for 7 days",
            "value": {
                "name": "My Policy",
                "pattern": "go_.+",
                "delete_after": "7d",
                "description": "time-series matching with Regexp will be hold for 7 days"
            }
        }
    }
