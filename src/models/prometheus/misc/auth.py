from pydantic import BaseModel, Field, SecretStr
from src.models.prometheus.misc import tls
from typing import Optional, Dict, List


class BasicAuthConfig(BaseModel):
    username: Optional[str] = Field(None)
    password: Optional[SecretStr] = Field(None)
    password_file: Optional[str] = Field(None)


class AuthorizationConfig(BaseModel):
    type: Optional[str] = Field("Bearer")
    credentials: Optional[SecretStr] = Field(None)
    credentials_file: Optional[str] = Field(None)


class OAuth2Config(BaseModel):
    client_id: str = Field(..., description="The client ID.")
    client_secret: Optional[SecretStr] = Field(
        None, description="The client secret.")
    client_secret_file: Optional[str] = Field(
        None,
        description="The client secret file. It is mutually exclusive with `client_secret`.")
    scopes: Optional[List[str]] = Field(
        None, description="Scopes for the token request.")
    token_url: str = Field(..., description="The URL to fetch the token from.")
    endpoint_params: Optional[Dict[str, str]] = Field(
        None, description="Optional parameters to append to the token URL.")
    tls_config: Optional[tls.TLSConfig] = Field(
        None, description="Configures the token request's TLS settings.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be "
                    "excluded from proxying. IP and domain names can contain port numbers.")
    proxy_from_environment: Optional[bool] = Field(
        False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")


class Sigv4Config(BaseModel):
    region: Optional[str] = Field(None)
    access_key: Optional[str] = Field(None)
    secret_key: Optional[SecretStr] = Field(None)
    profile: Optional[str] = Field(None)
    role_arn: Optional[str] = Field(None)


class ManagedIdentityConfig(BaseModel):
    client_id: Optional[str] = Field(None)


class AzureOAuthConfig(BaseModel):
    client_id: Optional[str] = Field(None)
    client_secret: Optional[SecretStr] = Field(None)
    tenant_id: Optional[str] = Field(None)


class AzureSDKConfig(BaseModel):
    tenant_id: Optional[str] = Field(None)


class AzureADConfig(BaseModel):
    cloud: Optional[str] = Field("AzurePublic")
    managed_identity: Optional[ManagedIdentityConfig] = Field(None)
    oauth: Optional[AzureOAuthConfig] = Field(None)
    sdk: Optional[AzureSDKConfig] = Field(None)
