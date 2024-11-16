from src.models.prometheus.discovery import \
    aws, azure, consul, digitalocean, dns, docker, eureka, file_sd, gce, hetzner, \
    http, ionos, kubernetes, kuma, lightsail, linode, marathon, nerve, nomad, \
    openstack, ovhcloud, puppetdb, scaleway, serverset, triton, uyuni, static
from src.models.prometheus.misc import auth, tls
from src.models.prometheus.configs import globals
from src.models.prometheus.configs import relabel
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class ScrapeConfig(BaseModel):
    job_name: str = Field(...,
                          description="The job name assigned to scraped metrics by default.")
    scrape_interval: Optional[str] = Field(
        globals.GlobalConfig.__getattribute__(
            globals.GlobalConfig(),
            "scrape_interval"),
        description="How frequently to scrape targets from this job.")
    scrape_timeout: Optional[str] = Field(
        globals.GlobalConfig.__getattribute__(
            globals.GlobalConfig(),
            "scrape_timeout"),
        description="Per-scrape timeout when scraping this job.")
    scrape_protocols: Optional[List[str]] = Field(globals.GlobalConfig.__getattribute__(globals.GlobalConfig(
    ), "scrape_protocols"), description="The protocols to negotiate during a scrape with the client.")
    scrape_classic_histograms: Optional[bool] = Field(
        False,
        description="Whether to scrape a classic histogram that is also exposed as a native histogram. "
                    "(has no effect without --enable-feature=native-histograms)")
    metrics_path: Optional[str] = Field(
        "/metrics",
        description="The HTTP resource path on which to fetch metrics from targets.")
    honor_labels: Optional[bool] = Field(
        False,
        description="Controls how Prometheus handles conflicts between labels that are already present in "
                    "scraped data and labels that Prometheus would attach server-side.")
    honor_timestamps: Optional[bool] = Field(
        True,
        description="Controls whether Prometheus respects the timestamps present in scraped data.")
    track_timestamps_staleness: Optional[bool] = Field(
        False,
        description="Controls whether Prometheus tracks staleness of the metrics that have explicit timestamps "
                    "present in scraped data.")
    scheme: Optional[str] = Field(
        "http", description="Configures the protocol scheme used for requests.")
    params: Optional[Dict[str, List[str]]] = Field(
        None, description="Optional HTTP URL parameters.")
    enable_compression: Optional[bool] = Field(
        True,
        description="If set to false, Prometheus will request uncompressed response from the scraped target.")
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None,
        description="Sets the `Authorization` header on every scrape request with the "
                    "configured username and password.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Sets the `Authorization` header on every scrape request with the configured credentials.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.")
    follow_redirects: Optional[bool] = Field(
        True, description="Configure whether scrape requests follow HTTP 3xx redirects.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2.")
    tls_config: Optional[tls.TLSConfig] = Field(
        None, description="Configures the scrape request's TLS settings.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded "
                    "from proxying. IP and domain names can contain port numbers.")
    proxy_from_environment: Optional[bool] = Field(
        False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")
    azure_sd_configs: Optional[List[azure.AzureSDConfig]] = Field(
        None, description="List of Azure service discovery configurations.")
    consul_sd_configs: Optional[List[consul.ConsulSDConfig]] = Field(
        None, description="List of Consul service discovery configurations.")
    digitalocean_sd_configs: Optional[List[digitalocean.DigitalOceanSDConfig]] = Field(
        None, description="List of DigitalOcean service discovery configurations.")
    docker_sd_configs: Optional[List[docker.DockerSDConfig]] = Field(
        None, description="List of Docker service discovery configurations.")
    dockerswarm_sd_configs: Optional[List[docker.DockerSwarmSDConfig]] = Field(
        None, description="List of Docker Swarm service discovery configurations.")
    dns_sd_configs: Optional[List[dns.DNSSDConfig]] = Field(
        None, description="List of DNS service discovery configurations.")
    ec2_sd_configs: Optional[List[aws.EC2SDConfig]] = Field(
        None, description="List of EC2 service discovery configurations.")
    eureka_sd_configs: Optional[List[eureka.EurekaSDConfig]] = Field(
        None, description="List of Eureka service discovery configurations.")
    file_sd_configs: Optional[List[file_sd.FileSDConfig]] = Field(
        None, description="List of file service discovery configurations.")
    gce_sd_configs: Optional[List[gce.GCESDConfig]] = Field(
        None, description="List of GCE service discovery configurations.")
    hetzner_sd_configs: Optional[List[hetzner.HetznerSDConfig]] = Field(
        None, description="List of Hetzner service discovery configurations.")
    http_sd_configs: Optional[List[http.HttpSDConfig]] = Field(
        None, description="List of HTTP service discovery configurations.")
    ionos_sd_configs: Optional[List[ionos.IONOSCloudConfig]] = Field(
        None, description="List of IONOS service discovery configurations.")
    kubernetes_sd_configs: Optional[List[kubernetes.KubernetesSDConfig]] = Field(
        None, description="List of Kubernetes service discovery configurations.")
    kuma_sd_configs: Optional[List[kuma.KumaControlPlaneConfig]] = Field(
        None, description="List of Kuma service discovery configurations.")
    lightsail_sd_configs: Optional[List[lightsail.LightsailAPIConfig]] = Field(
        None, description="List of Lightsail service discovery configurations.")
    linode_sd_configs: Optional[List[linode.LinodeAPIConfig]] = Field(
        None, description="List of Linode service discovery configurations.")
    marathon_sd_configs: Optional[List[marathon.MarathonConfig]] = Field(
        None, description="List of Marathon service discovery configurations.")
    nerve_sd_configs: Optional[List[nerve.NerveSDConfig]] = Field(
        None, description="List of AirBnB's Nerve service discovery configurations.")
    nomad_sd_configs: Optional[List[nomad.NomadSDConfig]] = Field(
        None, description="List of Nomad service discovery configurations.")
    openstack_sd_configs: Optional[List[openstack.OpenStackSDConfig]] = Field(
        None, description="List of OpenStack service discovery configurations.")
    ovhcloud_sd_configs: Optional[List[ovhcloud.OVHcloudSDConfig]] = Field(
        None, description="List of OVHcloud service discovery configurations.")
    puppetdb_sd_configs: Optional[List[puppetdb.PuppetDBSDConfig]] = Field(
        None, description="List of PuppetDB service discovery configurations.")
    scaleway_sd_configs: Optional[List[scaleway.ScalewaySDConfig]] = Field(
        None, description="List of Scaleway service discovery configurations.")
    serverset_sd_configs: Optional[List[serverset.ServersetSDConfig]] = Field(
        None, description="List of Zookeeper Serverset service discovery configurations.")
    triton_sd_configs: Optional[List[triton.TritonSDConfig]] = Field(
        None, description="List of Triton service discovery configurations.")
    uyuni_sd_configs: Optional[List[uyuni.UyuniSDConfig]] = Field(
        None, description="List of Uyuni service discovery configurations.")
    static_configs: Optional[List[static.StaticConfig]] = Field(
        None, description="List of labeled statically configured targets for this job.")
    relabel_configs: Optional[List[relabel.RelabelConfig]] = Field(
        None, description="List of target relabel configurations.")
    metric_relabel_configs: Optional[List[relabel.RelabelConfig]] = Field(
        None, description="List of metric relabel configurations.")
    body_size_limit: Optional[str] = Field(
        "0",
        description="An uncompressed response body larger than this many bytes will cause the scrape to fail.")
    sample_limit: Optional[int] = Field(
        0, description="Per-scrape limit on number of scraped samples that will be accepted.")
    label_limit: Optional[int] = Field(
        0, description="Per-scrape limit on number of labels that will be accepted for a sample.")
    label_name_length_limit: Optional[int] = Field(
        0, description="Per-scrape limit on length of labels name that will be accepted for a sample.")
    label_value_length_limit: Optional[int] = Field(
        0, description="Per-scrape limit on length of labels value that will be accepted for a sample.")
    target_limit: Optional[int] = Field(
        0, description="Per-scrape config limit on number of unique targets that will be accepted.")
    keep_dropped_targets: Optional[int] = Field(
        0, description="Per-job limit on the number of targets dropped by relabeling that will be kept in memory.")
    native_histogram_bucket_limit: Optional[int] = Field(
        0, description="Limit on total number of positive and negative buckets allowed in a single native histogram.")
    native_histogram_min_bucket_factor: Optional[float] = Field(
        0, description="Lower limit for the growth factor of one bucket to the next in each native histogram.")
