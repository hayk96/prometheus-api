from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class VultrSDConfig(BaseModel):
    """
    Vultr SD configurations allow retrieving scrape targets from Vultr.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#vultr_sd_config
    """
    basic_auth: Optional[BasicAuthConfig] = Field(
        None, description="Optional HTTP basic authentication information, not currently supported by Vultr.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None, description="Optional OAuth 2.0 configuration. Cannot be used at the same "
                          "time as basic_auth or authorization.")
    proxy_url: Optional[str] = Field(
        None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None, description="Comma-separated string that can contain IPs, CIDR notation, domain "
                          "names that should be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False, description="Use proxy URL indicated by environment variables. Default is false.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2. Default is true.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from. Default is 80.")
    refresh_interval: Optional[str] = Field(
        "60s", description="The time after which the instances are refreshed. Default is 60 seconds.")
