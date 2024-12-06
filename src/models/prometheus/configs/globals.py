from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class GlobalConfig(BaseModel):
    scrape_interval: Optional[str] = Field(
        "1m", description="How frequently to scrape targets by default.")
    scrape_timeout: Optional[str] = Field(
        "10s", description="How long until a scrape request times out.")
    scrape_protocols: Optional[List[str]] = Field(
        ["OpenMetricsText1.0.0", "OpenMetricsText0.0.1", "PrometheusText0.0.4"],
        description="The protocols to negotiate during a scrape with the client."
    )
    evaluation_interval: Optional[str] = Field(
        "1m", description="How frequently to evaluate rules.")
    rule_query_offset: Optional[str] = Field(
        "0s",
        description="Offset the rule evaluation timestamp of this particular group by the specified duration into the "
                    "past to ensure the underlying metrics have been received.")
    external_labels: Optional[Dict[str, str]] = Field(
        None, description="The labels to add to any time series or alerts when communicating with external systems "
                          "(federation, remote storage, Alertmanager).")
    query_log_file: Optional[str] = Field(
        None,
        description="File to which PromQL queries are logged. Reloading the configuration will reopen the file.")
    body_size_limit: Optional[str] = Field(
        "0",
        description="An uncompressed response body larger than this many bytes will cause the scrape to fail. 0 means "
                    "no limit. Example: 100MB. This is an experimental feature, this behaviour could change or be "
                    "removed in the future.")
    sample_limit: Optional[int] = Field(
        0,
        description="Per-scrape limit on number of scraped samples that will be accepted. If more than this number of "
                    "samples are present after metric relabeling the entire scrape will be treated as failed. "
                    "0 means no limit.")
    label_limit: Optional[int] = Field(
        0,
        description="Per-scrape limit on number of labels that will be accepted for a sample. If more than this number "
                    "of labels are present post metric-relabeling, the entire scrape will be treated as failed. "
                    "0 means no limit.")
    label_name_length_limit: Optional[int] = Field(
        0,
        description="Per-scrape limit on length of labels name that will be accepted for a sample. If a label name "
        "is longer than this number post metric-relabeling, the entire scrape will be treated as failed. "
        "0 means no limit.")
    label_value_length_limit: Optional[int] = Field(
        0, description="Per-scrape limit on length of labels value that will be accepted for a sample. If a label "
                       "value is longer than this number post metric-relabeling, the entire scrape will be treated "
                       "as failed. 0 means no limit.")
    target_limit: Optional[int] = Field(
        0, description="Per-scrape config limit on number of unique targets that will be accepted. If more than this "
        "number of targets are present after target relabeling, Prometheus will mark the targets as "
        "failed without scraping them. 0 means no limit. This is an experimental feature, this behaviour "
        "could change in the future.")
    keep_dropped_targets: Optional[int] = Field(
        0, description="Limit per scrape config on the number of targets dropped by relabeling that will be kept in "
                       "memory. 0 means no limit.")
