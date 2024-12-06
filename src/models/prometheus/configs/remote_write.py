from src.models.prometheus.misc import auth, tls
from src.models.prometheus.configs import relabel
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class QueueConfig(BaseModel):
    capacity: Optional[int] = Field(10000)
    max_shards: Optional[int] = Field(50)
    min_shards: Optional[int] = Field(1)
    max_samples_per_send: Optional[int] = Field(2000)
    batch_send_deadline: Optional[str] = Field("5s")
    min_backoff: Optional[str] = Field("30ms")
    max_backoff: Optional[str] = Field("5s")
    retry_on_http_429: Optional[bool] = Field(False)
    sample_age_limit: Optional[str] = Field("0s")


class MetadataConfig(BaseModel):
    send: Optional[bool] = Field(True)
    send_interval: Optional[str] = Field("1m")
    max_samples_per_send: Optional[int] = Field(500)


class RemoteWriteConfig(BaseModel):
    url: str = Field(...,
                     description="The URL of the endpoint to send samples to.")
    remote_timeout: Optional[str] = Field(
        "30s", description="Timeout for requests to the remote write endpoint.")
    headers: Optional[Dict[str, str]] = Field(
        None, description="Custom HTTP headers to be sent along with each remote write request. Be aware that headers "
                          "that are set by Prometheus itself can't be overwritten.")
    write_relabel_configs: Optional[List[relabel.RelabelConfig]] = Field(
        None, description="List of remote write relabel configurations.")
    name: Optional[str] = Field(
        None,
        description="Name of the remote write config, which if specified must be unique among remote write configs. "
                    "The name will be used in metrics and logging in place of a generated value to help users "
                    "distinguish between remote write configs.")
    send_exemplars: Optional[bool] = Field(
        False,
        description="Enables sending of exemplars over remote write. Note that exemplar storage itself must be enabled "
                    "for exemplars to be scraped in the first place.")
    send_native_histograms: Optional[bool] = Field(
        False,
        description="Enables sending of native histograms, also known as sparse histograms, over remote write.")
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None,
        description="Sets the `Authorization` header on every remote write request with the configured username and "
                    "password. password and password_file are mutually exclusive.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration.")
    sigv4: Optional[auth.Sigv4Config] = Field(
        None,
        description="Optionally configures AWS's Signature Verification 4 signing process to sign requests. "
                    "Cannot be set at the same time as basic_auth, authorization, oauth2, or azuread. To use the "
                    "default credentials from the AWS SDK, use `sigv4: {}`.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth, authorization, "
                    "sigv4, or azuread.")
    azuread: Optional[auth.AzureADConfig] = Field(
        None,
        description="Optional AzureAD configuration. Cannot be used at the same time as basic_auth, authorization, "
                    "oauth2, or sigv4.")
    tls_config: Optional[tls.TLSConfig] = Field(
        None, description="Configures the remote write request's TLS settings.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be "
                    "excluded from proxying. IP and domain names can contain port numbers.")
    proxy_from_environment: Optional[bool] = Field(
        False,
        description="Use proxy URL indicated by environment variables (HTTP_PROXY, https_proxy, HTTPs_PROXY, "
                    "https_proxy, and no_proxy).")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2.")
    queue_config: Optional[QueueConfig] = Field(
        None, description="Configures the queue used to write to remote storage.")
    metadata_config: Optional[MetadataConfig] = Field(
        None,
        description="Configures the sending of series metadata to remote storage. Metadata configuration is subject "
                    "to change at any point or be removed in future releases.")
