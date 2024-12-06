from pydantic import BaseModel, Field, SecretStr
from typing import Optional


class TLSConfig(BaseModel):
    ca: Optional[str] = Field(
        None,
        description="CA certificate to validate API server certificate with. "
                    "At most one of ca and ca_file is allowed.")
    ca_file: Optional[str] = Field(
        None,
        description="CA certificate file to validate API server certificate with. "
                    "At most one of ca and ca_file is allowed.")
    cert: Optional[str] = Field(
        None,
        description="Certificate for client cert authentication to the server. "
                    "At most one of cert and cert_file is allowed.")
    cert_file: Optional[str] = Field(
        None,
        description="Certificate file for client cert authentication to the server. "
                    "At most one of cert and cert_file is allowed.")
    key: Optional[SecretStr] = Field(
        None,
        description="Key for client cert authentication to the server. "
                    "At most one of key and key_file is allowed.")
    key_file: Optional[str] = Field(
        None,
        description="Key file for client cert authentication to the server. "
                    "At most one of key and key_file is allowed.")
    server_name: Optional[str] = Field(
        None, description="ServerName extension to indicate the name of the server.")
    insecure_skip_verify: Optional[bool] = Field(
        None, description="Disable validation of the server certificate.")
    min_version: Optional[str] = Field(
        None, description="Minimum acceptable TLS version. "
        "Accepted values: TLS10 (TLS 1.0), TLS11 (TLS 1.1), TLS12 (TLS 1.2), TLS13 (TLS 1.3).")
    max_version: Optional[str] = Field(
        None, description="Maximum acceptable TLS version. "
        "Accepted values: TLS10 (TLS 1.0), TLS11 (TLS 1.1), TLS12 (TLS 1.2), TLS13 (TLS 1.3).")
