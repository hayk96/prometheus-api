from src.models.prometheus.discovery import \
    aws, azure, consul, digitalocean, dns, docker, eureka, file_sd, gce, hetzner, \
    http, ionos, kubernetes, lightsail, linode, marathon, nerve, nomad, openstack, \
    ovhcloud, puppetdb, scaleway, serverset, static, triton, uyuni, vultr
from src.models.prometheus.misc import auth, tls
from src.models.prometheus.configs import relabel
from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Dict, List


class AlertmanagerConfig(BaseModel):
    timeout: Optional[str] = Field(
        "10s", description="Per-target Alertmanager timeout when pushing alerts.")
    api_version: Optional[str] = Field(
        "v2", description="The API version of Alertmanager.")
    path_prefix: Optional[str] = Field(
        "/", description="Prefix for the HTTP path alerts are pushed to.")
    scheme: Optional[str] = Field(
        "http", description="Configures the protocol scheme used for requests.")
    basic_auth: Optional[auth.BasicAuthConfig] = Field(
        None,
        description="Sets the `Authorization` header on every request with the configured username and password.")
    authorization: Optional[auth.AuthorizationConfig] = Field(
        None, description="Optional `Authorization` header configuration.")
    sigv4: Optional[auth.Sigv4Config] = Field(
        None,
        description="Optionally configures AWS's Signature Verification 4 signing process to sign requests.")
    oauth2: Optional[auth.OAuth2Config] = Field(
        None, description="Optional OAuth 2.0 configuration.")
    tls_config: Optional[tls.TLSConfig] = Field(
        None, description="Configures the scrape request's TLS settings.")
    proxy_url: Optional[str] = Field(None, description="Optional proxy URL.")
    no_proxy: Optional[str] = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded "
                    "from proxying.")
    proxy_from_environment: Optional[bool] = Field(
        False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: Optional[Dict[str, List[SecretStr]]] = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests.")
    follow_redirects: Optional[bool] = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects.")
    enable_http2: Optional[bool] = Field(
        True, description="Whether to enable HTTP2.")
    azure_sd_configs: Optional[List[azure.AzureSDConfig]] = Field(
        None, description="List of Azure service discovery configurations.")
    consul_sd_configs: Optional[List[consul.ConsulSDConfig]] = Field(
        None, description="List of Consul service discovery configurations.")
    dns_sd_configs: Optional[List[dns.DNSSDConfig]] = Field(
        None, description="List of DNS service discovery configurations.")
    ec2_sd_configs: Optional[List[aws.EC2SDConfig]] = Field(
        None, description="List of EC2 service discovery configurations.")
    eureka_sd_configs: Optional[List[eureka.EurekaSDConfig]] = Field(
        None, description="List of Eureka service discovery configurations.")
    file_sd_configs: Optional[List[file_sd.FileSDConfig]] = Field(
        None, description="List of file service discovery configurations.")
    digitalocean_sd_configs: Optional[List[digitalocean.DigitalOceanSDConfig]] = Field(
        None, description="List of DigitalOcean service discovery configurations.")
    docker_sd_configs: Optional[List[docker.DockerSDConfig]] = Field(
        None, description="List of Docker service discovery configurations.")
    dockerswarm_sd_configs: Optional[List[docker.DockerSwarmSDConfig]] = Field(
        None, description="List of Docker Swarm service discovery configurations.")
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
    lightsail_sd_configs: Optional[List[lightsail.LightsailAPIConfig]] = Field(
        None, description="List of Lightsail service discovery configurations.")
    linode_sd_configs: Optional[List[List[linode.LinodeAPIConfig]]] = Field(
        None, description="List of Linode service discovery configurations.")
    marathon_sd_configs: Optional[List[List[marathon.MarathonConfig]]] = Field(
        None, description="List of Marathon service discovery configurations.")
    nerve_sd_configs: Optional[List[List[nerve.NerveSDConfig]]] = Field(
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
    vultr_sd_configs: Optional[List[vultr.VultrSDConfig]] = Field(
        None, description="List of Vultr service discovery configurations.")
    static_configs: Optional[List[static.StaticConfig]] = Field(
        None, description="List of labeled statically configured Alertmanagers.")
    relabel_configs: Optional[List[relabel.RelabelConfig]] = Field(
        None, description="List of Alertmanager relabel configurations.")
    alert_relabel_configs: Optional[List[relabel.RelabelConfig]] = Field(
        None, description="List of alert relabel configurations.")
