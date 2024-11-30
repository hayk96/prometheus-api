from src.models.prometheus.misc import auth, tls
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class AzureSDConfig(BaseModel):
    """
    Azure SD configurations allow retrieving scrape targets from Azure VMs.

    The following meta labels are available on targets during relabeling:

    __meta_azure_machine_id: the machine ID
    __meta_azure_machine_location: the location the machine runs in
    __meta_azure_machine_name: the machine name
    __meta_azure_machine_computer_name: the machine computer name
    __meta_azure_machine_os_type: the machine operating system
    __meta_azure_machine_private_ip: the machine's private IP
    __meta_azure_machine_public_ip: the machine's public IP if it exists
    __meta_azure_machine_resource_group: the machine's resource group
    __meta_azure_machine_tag_<tagname>: each tag value of the machine
    __meta_azure_machine_scale_set: the name of the scale set which the
    vm is part of (this value is only set if you are using a scale set)
    __meta_azure_machine_size: the machine size
    __meta_azure_subscription_id: the subscription ID
    __meta_azure_tenant_id: the tenant ID
    """
    environment: Optional[str] = Field(
        "AzurePublicCloud",
        description="The Azure environment.")
    authentication_method: Optional[str] = Field(
        "OAuth",
        description="The authentication method, either OAuth, ManagedIdentity or SDK.")
    subscription_id: str = Field(...,
                                 description="The subscription ID. Always required.")
    tenant_id: Optional[str] = Field(
        None,
        description="Optional tenant ID. Only required with authentication_method OAuth.")
    client_id: Optional[str] = Field(
        None,
        description="Optional client ID. Only required with authentication_method OAuth.")
    client_secret: Optional[SecretStr] = Field(
        None,
        description="Optional client secret. Only required with authentication_method OAuth.")
    resource_group: Optional[str] = Field(
        None,
        description="Optional resource group name. Limits discovery to this resource group.")
    refresh_interval: Optional[str] = Field(
        "300s", description="Refresh interval to re-read the instance list.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from.")
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None,
        description="Optional HTTP basic authentication information, currently not support by Azure.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration, currently not supported by Azure.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration, currently not supported by Azure.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that "
                    "should be excluded from proxying.")
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
