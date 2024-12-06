from pydantic import BaseModel, Field
from typing import Optional, List


class DNSSDConfig(BaseModel):
    """
    A DNS-based service discovery configuration allows specifying a set
    of DNS domain names which are periodically queried to discover a list
    of targets. The DNS servers to be contacted are read from /etc/resolv.conf.

    This service discovery method only supports basic DNS A, AAAA, MX,
    NS and SRV record queries, but not the advanced DNS-SD approach
    specified in RFC6763.

    The following meta labels are available on targets during relabeling:

    __meta_dns_name: the record name that produced the discovered target.
    __meta_dns_srv_record_target: the target field of the SRV record
    __meta_dns_srv_record_port: the port field of the SRV record
    __meta_dns_mx_record_target: the target field of the MX record
    __meta_dns_ns_record_target: the target field of the NS record
    """
    names: List[str] = Field(...,
                             description="A list of DNS domain names to be queried.")
    type: Optional[str] = Field(
        "SRV",
        description="The type of DNS query to perform. One of SRV, A, AAAA, MX or NS.")
    port: Optional[int] = Field(
        None, description="The port number used if the query type is not SRV.")
    refresh_interval: Optional[str] = Field(
        "30s", description="The time after which the provided names are refreshed.")
