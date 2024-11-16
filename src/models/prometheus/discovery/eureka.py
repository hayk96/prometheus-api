from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class EurekaSDConfig(BaseModel):
    """
    Eureka SD configurations allow retrieving scrape targets using the Eureka REST API.
    Prometheus will periodically check the REST endpoint and create a target for every
    app instance. The following meta labels are available on targets during relabeling:

    __meta_eureka_app_name: the name of the app
    __meta_eureka_app_instance_id: the ID of the app instance
    __meta_eureka_app_instance_hostname: the hostname of the instance
    __meta_eureka_app_instance_homepage_url: the homepage url of the app instance
    __meta_eureka_app_instance_statuspage_url: the status page url of the app instance
    __meta_eureka_app_instance_healthcheck_url: the health check url of the app instance
    __meta_eureka_app_instance_ip_addr: the IP address of the app instance
    __meta_eureka_app_instance_vip_address: the VIP address of the app instance
    __meta_eureka_app_instance_secure_vip_address: the secure VIP address of the app instance
    __meta_eureka_app_instance_status: the status of the app instance
    __meta_eureka_app_instance_port: the port of the app instance
    __meta_eureka_app_instance_port_enabled: the port enabled of the app instance
    __meta_eureka_app_instance_secure_port: the secure port address of the app instance
    __meta_eureka_app_instance_secure_port_enabled: the secure port of the app instance
    __meta_eureka_app_instance_country_id: the country ID of the app instance
    __meta_eureka_app_instance_metadata_<metadataname>: app instance metadata
    __meta_eureka_app_instance_datacenterinfo_name: the datacenter name of the app instance
    __meta_eureka_app_instance_datacenterinfo_<metadataname>: the datacenter metadata
    """
    server: str = Field(...,
                        description="The URL to connect to the Eureka server.")
    basic_auth: Optional[BasicAuthConfig] = Field(
        None, description="Basic authentication configuration.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Optional Authorization header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used "
                    "at the same time as basic_auth or authorization.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="Configures the scrape request's TLS settings.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, "
                    "domain names that should be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2.")
    refresh_interval: Optional[str] = Field(
        "30s", description="Refresh interval to re-read the app instance list.")
