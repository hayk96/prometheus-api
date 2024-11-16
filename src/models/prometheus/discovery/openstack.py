from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional


class OpenStackSDConfig(BaseModel):
    """
    OpenStack SD configurations allow retrieving scrape targets from OpenStack Nova instances.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#openstack_sd_config
    """
    role: str = Field(...,
                      description="The OpenStack role of entities that should be discovered.")
    region: str = Field(..., description="The OpenStack region.")
    identity_endpoint: Optional[str] = Field(
        None, description="HTTP endpoint required to work with the Identity API.")
    username: Optional[str] = Field(
        None,
        description="Username for Identity V2 API. For V3, either userid or a combination of "
                    "username and domain_id or domain_name are needed.")
    userid: Optional[str] = Field(
        None, description="User ID for Identity V3 API.")
    password: Optional[SecretStr] = Field(
        None, description="Password for Identity V2 and V3 APIs.")
    domain_name: Optional[str] = Field(
        None, description="Domain name for Identity V3 API.")
    domain_id: Optional[str] = Field(
        None, description="Domain ID for Identity V3 API.")
    project_name: Optional[str] = Field(
        None, description="Project name for Identity V2 API.")
    project_id: Optional[str] = Field(
        None, description="Project ID for Identity V2 API.")
    application_credential_name: Optional[str] = Field(
        None, description="Application credential name for authentication.")
    application_credential_id: Optional[str] = Field(
        None, description="Application credential ID for authentication.")
    application_credential_secret: Optional[SecretStr] = Field(
        None, description="Application credential secret for authentication.")
    all_tenants: Optional[bool] = Field(
        False,
        description="Whether to list all instances for all projects. Relevant for 'instance' "
                    "role and usually requires admin permissions.")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="Refresh interval to re-read the instance list. Default is 60 seconds.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from. Default is 80.")
    availability: Optional[str] = Field(
        "public",
        description="The availability of the endpoint to connect to. Must be one of public, "
                    "admin or internal. Default is 'public'.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
