from src.models.prometheus.misc import auth, tls
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class EC2SDConfig(BaseModel):
    """
    EC2 SD configurations allow retrieving scrape targets from AWS EC2 instances.
    The private IP address is used by default, but may be changed to the public
    IP address with relabeling.

    The IAM credentials used must have the ec2:DescribeInstances permission to
    discover scrape targets, and may optionally have the ec2:DescribeAvailabilityZones
    permission if you want the availability zone ID available as a label (see below).

    The following meta labels are available on targets during relabeling:

    __meta_ec2_ami: the EC2 Amazon Machine Image
    __meta_ec2_architecture: the architecture of the instance
    __meta_ec2_availability_zone: the availability zone in which the instance is running
    __meta_ec2_availability_zone_id: the availability zone ID in which the instance
    is running (requires ec2:DescribeAvailabilityZones)
    __meta_ec2_instance_id: the EC2 instance ID
    __meta_ec2_instance_lifecycle: the lifecycle of the EC2 instance, set only for
    'spot' or 'scheduled' instances, absent otherwise
    __meta_ec2_instance_state: the state of the EC2 instance
    __meta_ec2_instance_type: the type of the EC2 instance
    __meta_ec2_ipv6_addresses: comma separated list of IPv6 addresses assigned to the
    instance's network interfaces, if present
    __meta_ec2_owner_id: the ID of the AWS account that owns the EC2 instance
    __meta_ec2_platform: the Operating System platform, set to 'windows' on Windows
    servers, absent otherwise
    __meta_ec2_primary_subnet_id: the subnet ID of the primary network interface, if available
    __meta_ec2_private_dns_name: the private DNS name of the instance, if available
    __meta_ec2_private_ip: the private IP address of the instance, if present
    __meta_ec2_public_dns_name: the public DNS name of the instance, if available
    __meta_ec2_public_ip: the public IP address of the instance, if available
    __meta_ec2_region: the region of the instance
    __meta_ec2_subnet_id: comma separated list of subnets IDs in which the instance
    is running, if available
    __meta_ec2_tag_<tagkey>: each tag value of the instance
    __meta_ec2_vpc_id: the ID of the VPC in which the instance is running, if available
    """
    region: Optional[str] = Field(
        None,
        description="The AWS region. If blank, the region from the instance metadata is used.")
    endpoint: Optional[str] = Field(
        None, description="Custom endpoint to be used.")
    access_key: Optional[str] = Field(None, description="The AWS access key.")
    secret_key: Optional[SecretStr] = Field(
        None, description="The AWS secret key.")
    profile: Optional[str] = Field(
        None, description="Named AWS profile used to connect to the API.")
    role_arn: Optional[str] = Field(
        None, description="AWS Role ARN, an alternative to using AWS API keys.")
    refresh_interval: Optional[str] = Field(
        "60s", description="Refresh interval to re-read the instance list.")
    port: Optional[int] = Field(
        80, description="The port to scrape metrics from.")
    filters: Optional[List[Dict[str, List[str]]]] = Field(
        None, description="Filters to limit the discovery process to a subset of available resources.")
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None,
        description="Optional HTTP basic authentication information, currently not supported by AWS.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration, currently not supported by AWS.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration, currently not supported by AWS.")
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
