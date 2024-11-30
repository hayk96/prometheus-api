from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class KumaControlPlaneConfig(BaseModel):
    """
    Kuma SD configurations allow retrieving scrape target from the Kuma control plane.

    This SD discovers "monitoring assignments" based on Kuma Dataplane Proxies,
    via the MADS v1 (Monitoring Assignment Discovery Service) xDS API, and will create
    a target for each proxy inside a Prometheus-enabled mesh.

    The following meta labels are available for each target:

    __meta_kuma_mesh: the name of the proxy's Mesh
    __meta_kuma_dataplane: the name of the proxy
    __meta_kuma_service: the name of the proxy's associated Service
    __meta_kuma_label_<tagname>: each tag of the proxy
    """
    server: str = Field(...,
                        description="Address of the Kuma Control Plane's MADS xDS server.")
    client_id: Optional[str] = Field(
        None,
        description="Client id used by Kuma Control Plane to compute Monitoring Assignment for "
                    "specific Prometheus backend. Default is system hostname/fqdn or 'prometheus'.")
    refresh_interval: Optional[str] = Field(
        "30s",
        description="The time to wait between polling update requests. Default is 30 seconds.")
    fetch_timeout: Optional[str] = Field(
        "2m",
        description="The time after which the monitoring assignments are refreshed. Default is 2 minutes.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string of IPs, CIDR notation, or domain names to be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False,
        description="Use proxy URL indicated by environment variables. Default is false.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Headers to send to proxies during CONNECT requests.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
    basic_auth: Optional[BasicAuthConfig] = Field(
        None, description="Optional HTTP basic authentication information.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Optional Authorization header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same "
                    "time as basic_auth or authorization.")
    follow_redirects: Optional[bool] = Field(
        True,
        description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2. Default is true.")
