from pydantic import BaseModel, Field, SecretStr
from typing import Optional


class OVHcloudSDConfig(BaseModel):
    """
    OVHcloud SD configurations allow retrieving scrape targets from OVHcloud's
    dedicated servers and VPS using their API. Prometheus will periodically check
    the REST endpoint and create a target for every discovered server. The role
    will try to use the public IPv4 address as default address, if there's none it
    will try to use the IPv6 one. This may be changed with relabeling. For OVHcloud's
    public cloud instances you can use the openstacksdconfig.
    """
    application_key: str = Field(
        ..., description="Access key to use. https://api.ovh.com")
    application_secret: SecretStr = Field(
        ..., description="Secret for the application key.")
    consumer_key: SecretStr = Field(
        ..., description="Consumer key.")
    service: str = Field(
        ..., description="Service of the targets to retrieve. Must be `vps` or `dedicated_server`.")
    endpoint: Optional[str] = Field(
        "ovh-eu", description="API endpoint. Default is 'ovh-eu'. https://github.com/ovh/go-ovh#supported-apis")
    refresh_interval: Optional[str] = Field(
        "60s", description="Refresh interval to re-read the resources list. Default is 60 seconds.")
