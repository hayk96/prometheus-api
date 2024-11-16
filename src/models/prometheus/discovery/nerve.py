from pydantic import BaseModel, Field
from typing import Optional, List


class NerveSDConfig(BaseModel):
    """
    Nerve SD configurations allow retrieving scrape targets from AirBnB's Nerve which are stored in Zookeeper.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#nerve_sd_config
    """
    servers: List[str] = Field(
        ..., description="The Zookeeper servers.")
    paths: List[str] = Field(
        ..., description="Paths can point to a single service, or the root of a tree of services.")
    timeout: Optional[str] = Field(
        "10s", description="Timeout for connections to Zookeeper servers. Default is 10 seconds.")
