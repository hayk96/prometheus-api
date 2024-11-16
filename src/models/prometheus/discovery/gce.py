from pydantic import BaseModel, Field
from typing import Optional


class GCESDConfig(BaseModel):
    """
    GCE SD configurations allow retrieving scrape targets from GCP GCE instances.
    The private IP address is used by default, but may be changed to the public
    IP address with relabeling. The following meta labels are available on
    targets during relabeling:

    __meta_gce_instance_id: the numeric id of the instance
    __meta_gce_instance_name: the name of the instance
    __meta_gce_label_<labelname>: each GCE label of the instance, with any unsupported
    characters converted to an underscore
    __meta_gce_machine_type: full or partial URL of the machine type of the instance
    __meta_gce_metadata_<name>: each metadata item of the instance
    __meta_gce_network: the network URL of the instance
    __meta_gce_private_ip: the private IP address of the instance
    __meta_gce_interface_ipv4_<name>: IPv4 address of each named interface
    __meta_gce_project: the GCP project in which the instance is running
    __meta_gce_public_ip: the public IP address of the instance, if present
    __meta_gce_subnetwork: the subnetwork URL of the instance
    __meta_gce_tags: comma separated list of instance tags
    __meta_gce_zone: the GCE zone URL in which the instance is running
    """
    project: str = Field(
        ..., description="The GCP Project.")
    zone: str = Field(
        ..., description="The zone of the scrape targets. If you need multiple zones, use multiple gce_sd_configs.")
    filter: Optional[str] = Field(
        None,
        description="Filter to optionally filter the instance list by other criteria. "
                    "Syntax of this filter string is described here in the filter query "
                    "parameter section: https://cloud.google.com/compute/docs/reference/latest/instances/list")
    refresh_interval: Optional[str] = Field(
        "60s",
        description="Refresh interval to re-read the instance list. Default is 60 seconds.")
    port: Optional[int] = Field(
        80,
        description="The port to scrape metrics from. If using the public IP address, this must "
                    "instead be specified in the relabeling rule. Default is 80.")
    tag_separator: Optional[str] = Field(
        ",",
        description="The tag separator used to separate the tags on concatenation. Default is ','.")
