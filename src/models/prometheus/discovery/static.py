from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class StaticConfig(BaseModel):
    """
    A static_config allows specifying a list of targets and a common label set for them.
    It is the canonical way to specify static targets in a scrape configuration.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#static_config
    """
    targets: List[str] = Field(
        ..., description="The targets specified by the static config.")
    labels: Optional[Dict[str, str]] = Field(
        None, description="Labels assigned to all metrics scraped from the targets.")
