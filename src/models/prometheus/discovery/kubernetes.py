from src.models.prometheus.misc.auth import BasicAuthConfig, AuthorizationConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class Namespace(BaseModel):
    own_namespace: Optional[bool] = Field(
        None,
        description="If true, only discover resources within the Prometheus pod's namespace.")
    names: Optional[List[str]] = Field(
        None, description="List of namespaces to discover resources from.")


class Selector(BaseModel):
    role: str = Field(...,
                      description="The Kubernetes role of entities to be discovered.")
    label: Optional[str] = Field(
        None, description="Label selector to limit discovery to a subset of resources.")
    field: Optional[str] = Field(
        None, description="Field selector to limit discovery to a subset of resources.")


class AttachMetadata(BaseModel):
    node: Optional[bool] = Field(
        False,
        description="Attach node metadata to discovered targets. Valid for roles: pod, endpoints, endpointslice.")


class KubernetesSDConfig(BaseModel):
    """
    Kubernetes SD configurations allow retrieving scrape targets from Kubernetes'
    REST API and always staying synchronized with the cluster state.
    """
    api_server: Optional[str] = Field(
        None,
        description="The API server addresses. If left empty, "
                    "Prometheus assumes it runs inside the cluster and will auto-discover the API server.")
    role: str = Field(..., description="The Kubernetes role of entities to be discovered. "
                                       "One of endpoints, endpointslice, service, pod, node, or ingress.")
    kubeconfig_file: Optional[str] = Field(
        None,
        description="Optional path to a kubeconfig file. Mutually exclusive with api_server.")
    basic_auth: Optional[BasicAuthConfig] = Field(
        None, description="Optional HTTP basic authentication information.")
    authorization: Optional[AuthorizationConfig] = Field(
        None, description="Optional Authorization header configuration.")
    oauth2: Optional[OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the "
                    "same time as basic_auth or authorization.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string of IPs, CIDR notation, or domain names to be excluded from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False,
        description="Use proxy URL indicated by environment variables. Default is false.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True,
        description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2. Default is true.")
    tls_config: Optional[TLSConfig] = Field(
        None, description="TLS configuration settings.")
    namespaces: Optional[Namespace] = Field(
        None,
        description="Optional namespace discovery. If omitted, all namespaces are used.")
    selectors: Optional[List[Selector]] = Field(
        None, description="Optional label and field selectors to limit the discovery "
                          "process to a subset of available resources.")
    attach_metadata: Optional[AttachMetadata] = Field(
        None,
        description="Optional metadata to attach to discovered targets. "
                    "If omitted, no additional metadata is attached.")
