from src.models.prometheus.misc import auth, tls
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class DigitalOceanSDConfig(BaseModel):
    """
    DigitalOcean SD configurations allow retrieving scrape targets from DigitalOcean's Droplets API.
    This service discovery uses the public IPv4 address by default, by that can be changed with
    relabeling, as demonstrated in the Prometheus digitalocean-sd configuration file.

    The following meta labels are available on targets during relabeling:

    __meta_digitalocean_droplet_id: the id of the droplet
    __meta_digitalocean_droplet_name: the name of the droplet
    __meta_digitalocean_image: the slug of the droplet's image
    __meta_digitalocean_image_name: the display name of the droplet's image
    __meta_digitalocean_private_ipv4: the private IPv4 of the droplet
    __meta_digitalocean_public_ipv4: the public IPv4 of the droplet
    __meta_digitalocean_public_ipv6: the public IPv6 of the droplet
    __meta_digitalocean_region: the region of the droplet
    __meta_digitalocean_size: the size of the droplet
    __meta_digitalocean_status: the status of the droplet
    __meta_digitalocean_features: the comma-separated list of features of the droplet
    __meta_digitalocean_tags: the comma-separated list of tags of the droplet
    __meta_digitalocean_vpc: the id of the droplet's VPC
    """
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None,
        description="Optional HTTP basic authentication information, not currently supported by DigitalOcean.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None, description="Optional OAuth 2.0 configuration.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names "
                    "that should be excluded from proxying.")
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
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from.")
    refresh_interval: Optional[str] = Field(
        "60s", description="The time after which the droplets are refreshed.")
