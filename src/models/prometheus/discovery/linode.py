from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class LinodeAPIConfig(BaseModel):
    """
    Linode SD configurations allow retrieving scrape targets from Linode's Linode APIv4.
    This service discovery uses the public IPv4 address by default, by that can be changed
    with relabeling, as demonstrated in the Prometheus linode-sd configuration file.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#linode_sd_config
    """
    basic_auth: Optional[BasicAuthConfig] = Field(
        None,
        description="Optional HTTP basic authentication information, not currently supported by Linode APIv4.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Optional Authorization header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.")
    region: Optional[str] = Field(
        None, description="Optional region to filter on.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string of IPs, CIDR notation, or domain names to be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False,
        description="Use proxy URL indicated by environment variables. Default is false.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True,
        description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2. Default is true.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from. Default is 80.")
    tag_separator: Optional[str] = Field(
        ",",
        description="The string by which Linode Instance tags are joined into the tag label. Default is ','.")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="The time after which the linode instances are refreshed. Default is 60 seconds.")
