from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class HetznerSDConfig(BaseModel):
    """
    Hetzner SD configurations allow retrieving scrape targets from Hetzner Cloud API and Robot API.
    This service discovery uses the public IPv4 address by default, but that can be changed with
    relabeling, as demonstrated in the Prometheus hetzner-sd configuration file.

    The following meta labels are available on all targets during relabeling:

    __meta_hetzner_server_id: the ID of the server
    __meta_hetzner_server_name: the name of the server
    __meta_hetzner_server_status: the status of the server
    __meta_hetzner_public_ipv4: the public ipv4 address of the server
    __meta_hetzner_public_ipv6_network: the public ipv6 network (/64) of the server
    __meta_hetzner_datacenter: the datacenter of the server
    The labels below are only available for targets with role set to hcloud:

    __meta_hetzner_hcloud_image_name: the image name of the server
    __meta_hetzner_hcloud_image_description: the description of the server image
    __meta_hetzner_hcloud_image_os_flavor: the OS flavor of the server image
    __meta_hetzner_hcloud_image_os_version: the OS version of the server image
    __meta_hetzner_hcloud_datacenter_location: the location of the server
    __meta_hetzner_hcloud_datacenter_location_network_zone: the network zone of the server
    __meta_hetzner_hcloud_server_type: the type of the server
    __meta_hetzner_hcloud_cpu_cores: the CPU cores count of the server
    __meta_hetzner_hcloud_cpu_type: the CPU type of the server (shared or dedicated)
    __meta_hetzner_hcloud_memory_size_gb: the amount of memory of the server (in GB)
    __meta_hetzner_hcloud_disk_size_gb: the disk size of the server (in GB)
    __meta_hetzner_hcloud_private_ipv4_<networkname>: the private ipv4 address of the server within a given network
    __meta_hetzner_hcloud_label_<labelname>: each label of the server, with any unsupported characters converted
    to an underscore
    __meta_hetzner_hcloud_labelpresent_<labelname>: true for each label of the server, with any unsupported
    characters converted to an underscore
    The labels below are only available for targets with role set to robot:

    __meta_hetzner_robot_product: the product of the server
    __meta_hetzner_robot_cancelled: the server cancellation status
    """
    role: str = Field(
        ..., description="The Hetzner role of entities that should be discovered. One of robot or hcloud.")
    basic_auth: Optional[BasicAuthConfig] = Field(
        None,
        description="Optional HTTP basic authentication information, required when role is robot. "
                    "Role hcloud does not support basic auth.")
    authorization: Optional[AuthorizationConfig] = Field(
        None,
        description="Optional Authorization header configuration, required when role is hcloud. "
                    "Role robot does not support bearer token authentication.")
    oauth2: Optional[OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same "
                    "time as basic_auth or authorization.")
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
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from. Default is 80.")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="The time after which the servers are refreshed. Default is 60 seconds.")
