from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class HttpSDConfig(BaseModel):
    """
    HTTP-based service discovery provides a more generic way to configure static targets
    and serves as an interface to plug in custom service discovery mechanisms.

    It fetches targets from an HTTP endpoint containing a list of zero or more
    <static_config>s. The target must reply with an HTTP 200 response. The HTTP header
    Content-Type must be application/json, and the body must be valid JSON.
    """
    url: str = Field(...,
                     description="URL from which the targets are fetched.")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="Refresh interval to re-query the endpoint. Default is 60 seconds.")
    basic_auth: Optional[BasicAuthConfig] = Field(
        None, description="Optional HTTP basic authentication information.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Optional Authorization header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None, description="Optional OAuth 2.0 configuration.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, "
                    "domain names that should be excluded from proxying.")
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
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
