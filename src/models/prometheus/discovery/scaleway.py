from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, List, Dict


class ScalewaySDConfig(BaseModel):
    """
    Scaleway SD configurations allow retrieving scrape targets from Scaleway instances and baremetal services.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scaleway_sd_config
    """
    access_key: str = Field(
        ...,
        description="Access key to use. https://console.scaleway.com/project/credentials")
    secret_key: Optional[SecretStr] = Field(
        None,
        description="Secret key to use when listing targets. Mutually exclusive with secret_key_file.")
    secret_key_file: Optional[str] = Field(
        None,
        description="File containing the secret key. Mutually exclusive with secret_key.")
    project_id: str = Field(..., description="Project ID of the targets.")
    role: str = Field(...,
                      description="Role of the targets to retrieve. Must be 'instance' or 'baremetal'.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from. Default is 80.")
    api_url: Optional[str] = Field(
        "https://api.scaleway.com",
        description="API URL to use when doing the server listing requests. Default is 'https://api.scaleway.com'.")
    zone: Optional[str] = Field(
        "fr-par-1",
        description="Zone is the availability zone of your targets (e.g. fr-par-1). Default is 'fr-par-1'.")
    name_filter: Optional[str] = Field(
        None,
        description="Name filter (works as a LIKE) to apply on the server listing request.")
    tags_filter: Optional[List[str]] = Field(
        None, description="Tag filter (a server needs to have all defined tags to be listed) to apply on the server listing request.")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="Refresh interval to re-read the targets list. Default is 60 seconds.")
    follow_redirects: Optional[bool] = Field(
        True,
        description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2. Default is true.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False,
        description="Use proxy URL indicated by environment variables. Default is false.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Headers to send to proxies during CONNECT requests.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
