from src.models.prometheus.misc import auth, tls
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class ConsulSDConfig(BaseModel):
    """
    Consul SD configurations allow retrieving scrape targets from Consul's Catalog API.

    The following meta labels are available on targets during relabeling:

    __meta_consul_address: the address of the target
    __meta_consul_dc: the datacenter name for the target
    __meta_consul_health: the health status of the service
    __meta_consul_partition: the admin partition name where the service is registered
    __meta_consul_metadata_<key>: each node metadata key value of the target
    __meta_consul_node: the node name defined for the target
    __meta_consul_service_address: the service address of the target
    __meta_consul_service_id: the service ID of the target
    __meta_consul_service_metadata_<key>: each service metadata key value of the target
    __meta_consul_service_port: the service port of the target
    __meta_consul_service: the name of the service the target belongs to
    __meta_consul_tagged_address_<key>: each node tagged address key value of the target
    __meta_consul_tags: the list of tags of the target joined by the tag separator
    """
    server: Optional[str] = Field(
        "localhost:8500",
        description="The Consul server address.")
    path_prefix: Optional[str] = Field(
        None,
        description="Prefix for URIs when Consul is behind an API gateway (reverse proxy).")
    token: Optional[SecretStr] = Field(
        None, description="The token for accessing Consul API.")
    datacenter: Optional[str] = Field(
        None, description="The datacenter to use.")
    namespace: Optional[str] = Field(
        None, description="Namespace for Consul Enterprise.")
    partition: Optional[str] = Field(
        None, description="Admin partition for Consul Enterprise.")
    scheme: Optional[str] = Field(
        "http", description="The scheme to use for requests (http or https).")
    username: Optional[str] = Field(
        None, description="Deprecated: Use basic_auth instead.")
    password: Optional[SecretStr] = Field(
        None, description="Deprecated: Use basic_auth instead.")
    services: Optional[List[str]] = Field(
        None, description="A list of services for which targets are retrieved. If omitted, all services are scraped.")
    tags: Optional[List[str]] = Field(
        None, description="An optional list of tags used to filter nodes for a given service. "
                          "Services must contain all tags in the list.")
    node_meta: Optional[Dict[str, str]] = Field(
        None, description="Node metadata key/value pairs to filter nodes for a given service.")
    tag_separator: Optional[str] = Field(
        ",", description="The string by which Consul tags are joined into the tag label.")
    allow_stale: Optional[bool] = Field(
        True, description="Allow stale Consul results.")
    refresh_interval: Optional[str] = Field(
        "30s", description="The time after which the provided names are refreshed.")
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None, description="Optional HTTP basic authentication information.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None, description="Optional OAuth 2.0 configuration.")
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
    tls_config: Optional[tls.TLSConfig] = Field(
        None, description="TLS configuration.")
