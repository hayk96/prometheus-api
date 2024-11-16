from pydantic import BaseModel, Field, SecretStr
from typing import Optional, List, Dict


class UyuniSDConfig(BaseModel):
    """
    Uyuni SD configurations allow retrieving scrape targets from managed systems via Uyuni API.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#uyuni_sd_config
    """
    server: str = Field(
        ..., description="The URL to connect to the Uyuni server.")
    username: str = Field(
        ..., description="Username to authenticate the requests to Uyuni API.")
    password: SecretStr = Field(
        ..., description="Password to authenticate the requests to Uyuni API.")
    entitlement: Optional[str] = Field(
        "monitoring_entitled", description="The entitlement string to filter eligible systems. "
                                           "Default is 'monitoring_entitled'.")
    separator: Optional[str] = Field(
        ",", description="The string by which Uyuni group names are joined into the groups label. Default is ','.")
    refresh_interval: Optional[str] = Field(
        "60s", description="Refresh interval to re-read the managed targets list. Default is 60 seconds.")
    basic_auth: Optional[Dict[str, Optional[SecretStr]]] = Field(
        None, description="Optional HTTP basic authentication information, currently not supported by Uyuni.")
    authorization: Optional[Dict[str, Optional[SecretStr]]] = Field(
        None, description="Optional `Authorization` header configuration, currently not supported by Uyuni.")
    oauth2: Optional[Dict[str, Optional[str]]] = Field(
        None, description="Optional OAuth 2.0 configuration, currently not supported by Uyuni. "
                          "Cannot be used at the same time as basic_auth or authorization.")
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
