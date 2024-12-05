from pydantic import BaseModel
from typing import Optional


class Rule(BaseModel):
    file: Optional[str] = str()
    data: Optional[dict] = dict()
    _request_body_examples = {
        "Prometheus Recording Rule": {
            "description": "Creates Prometheus recording rule with the name **ExampleRecordingRule**",
            "value": {
                "data": {
                    "groups": [
                        {
                            "name": "ExampleRecordingRule",
                            "rules": [
                                {
                                    "record": "code:prometheus_http_requests_total:sum",
                                    "expr": "sum by (code) (prometheus_http_requests_total)"
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "Prometheus Alerting Rule": {
            "description": "Creates Prometheus alerting rule with the name **ServiceHealthAlerts**",
            "value": {
                "data": {
                    "groups": [
                        {
                            "name": "ServiceHealthAlerts",
                            "rules": [
                                {
                                    "alert": "HighCPUUsage",
                                    "expr": "sum(rate(cpu_usage{job=\"webserver\"}[5m])) > 0.8",
                                    "for": "5m",
                                    "labels": {
                                        "severity": "warning"
                                    },
                                    "annotations": {
                                        "summary": "High CPU Usage Detected",
                                        "description": "The CPU usage for the web server is {{ $value }}% for the last 5 minutes."
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
