from src.models.prometheus.misc import alertmanager
from src.models.prometheus.configs import relabel
from pydantic import BaseModel, Field
from typing import Optional, List


class AlertingConfig(BaseModel):
    alert_relabel_configs: Optional[List[relabel.RelabelConfig]] = Field(
        None,
        description="Dynamically rewrite the label set of a target before it gets scraped. Multiple relabeling "
                    "steps can be configured per scrape configuration")
    alertmanagers: Optional[List[alertmanager.AlertmanagerConfig]] = Field(
        None, description="specifies Alertmanager instances the Prometheus server sends alerts to.")
