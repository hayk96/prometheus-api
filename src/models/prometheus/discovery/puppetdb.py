from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class PuppetDBSDConfig(BaseModel):
    """
    PuppetDB SD configurations allow retrieving scrape targets from PuppetDB resources.
    This SD discovers resources and will create a target for each resource returned by the API.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#puppetdb_sd_config
    """
    url: str = Field(...,
                     description="The URL of the PuppetDB root query endpoint.")
    query: str = Field(..., description="Puppet Query Language (PQL) query. Only resources are supported. "
                                        "https://puppet.com/docs/puppetdb/latest/api/query/v4/pql.html")
    include_parameters: Optional[bool] = Field(
        False,
        description="Whether to include the parameters as meta labels. Note: Enabling this exposes "
                    "parameters in the Prometheus UI and API.")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="Refresh interval to re-read the resources list. Default is 60 seconds.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from. Default is 80.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration to connect to the PuppetDB.")
    basic_auth: Optional[BasicAuthConfig] = Field(
        None, description="Optional HTTP basic authentication information.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Authorization HTTP header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as "
                    "basic_auth or authorization.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names "
                    "that should be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False,
        description="Use proxy URL indicated by environment variables. Default is false.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True,
        description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2. Default is true.")
