from pydantic import BaseModel, Extra
from typing import Optional


class MetricsLifecyclePolicyCreate(BaseModel, extra=Extra.allow):
    name: str
    match: str
    keep_for: str
    description: Optional[str] = None
    _request_body_examples = {
        "GoLang Metrics Lifecycle Policy": {
            "description": "Time-series matching with regex will be kept for 7 days",
            "value": {
                "name": "Example Policy",
                "match": "{__name__=~'go_.*'}",
                "keep_for": "7d",
                "description": "Time-series matching with regex will be kept for 7 days."
            }
        }
    }


class MetricsLifecyclePolicyUpdate(BaseModel, extra=Extra.allow):
    pattern: Optional[str]
    keep_for: Optional[str]
    description: Optional[str]
    _request_body_examples = {
        "Update retention time of series": {
            "description": "Updates `keep_for` setting only",
            "value": {
                "keep_for": "10d"
            }
        },
        "Update 'match' and 'description' fields": {
            "description": "Updates `match` and `description` fields of specific policy",
            "value": {
                "match": "{__name__='kube_pod_labels', job='kubernetes-service-endpoints'}",
                "description": "This policy deletes only 'kube_pod_labels' series of job 'kubernetes-service-endpoints'"
            }
        }
    }
