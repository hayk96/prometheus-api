# Changelog

## 0.3.3 / 2024-06-16

* [ENHANCEMENT] Added a new endpoint: `/metrics-lifecycle-policies/trigger` for force-triggering all Metrics Lifecycle Policies. #29
* [CHANGE] Changed the execution interval of the task "Clean-up Prometheus series" by the scheduler to 2 hours (previously 20 minutes).
* [BUGFIX] Prevented the execution of more than one task at the same time, as tasks can remain in the running state for longer than their execution interval.

## 0.3.2 / 2024-06-08

* [ENHANCEMENT] Added a new endpoint: `/health` for retrieving system health. #28
* [ENHANCEMENT] Added a new function that continuously checks (600 checks at 3-second intervals) for establishing a connection to Prometheus.
* [BUGFIX] The Prometheus /runtimeinfo API call check has been moved under the validation function.
* [BUGFIX] Added proper exception handling while checking the status of the reload API of Prometheus at runtime.

## 0.3.1 / 2024-06-01

* [ENHANCEMENT] Added a new webpage, Metrics Management, based on the `/metrics-lifecycle-policies` API. This feature allows 
for directly defining and managing policies for retaining Prometheus metrics. #23
* [ENHANCEMENT] Added support for dark mode on the Rules Management page. #16
* [ENHANCEMENT] Added support of filtering of rules by their type from the UI. #15

## 0.3.0 / 2024-05-26

* [ENHANCEMENT] 
Introduced a new API `/metrics-lifecycle-policies` for managing metrics lifecycle in the Prometheus ecosystem. This 
flexible API allows users to define policies that specify which time-series should be retained and for how long in the 
Prometheus TSDB storage.
* [BUGFIX] fixed description of 404 status code of the `DELETE /api/v1/rules` API in the Redocli page.

## 0.2.2 / 2024-05-12

* [REVERT] Reverted schema validation mechanism of rules API. Use local schema validation instead of remote which was introduces in [v0.1.2](https://github.com/hayk96/prometheus-api/releases/tag/v0.1.2). #18

## 0.2.1 / 2024-05-07

* [CHANGE] Serve remote JS script through Cloudflare CDN. No API changes.  #17

## 0.2.0 / 2024-05-02

* [ENHANCEMENT] Added support of Web UI for better management of the Prometheus rules through UI. #14 
* [CHANGE] Updated documentation

## 0.1.5 / 2024-02-25

* [ENHANCEMENT] Added support for exposing Prometheus metrics. The corresponding metrics are available under the path 
`/api-metrics`. The `/metrics` endpoint is also accessible for exposing the metrics of the Prometheus server.
* [BUGFIX] Fixed startup check of filesystem permissions in case of OSError.  

## 0.1.4 / 2024-01-28

* [ENHANCEMENT] Added HTTP query string: `recreate=true|false` for `PUT /api/v1/rules/{file}` endpoint.
* [CHANGE] Log format includes HTTP query strings passed by user.

## 0.1.3 / 2024-01-21

* [CHANGE] Upgraded FastAPI module from `0.95.1` to `0.109.0`.
* [ENHANCEMENT] Updated OpenAPI reference
* [ENHANCEMENT] Support auto-generation of OpenAPI specification
* [ENHANCEMENT] Added API documentation page (powered by Redocly) which is available here: https://hayk96.github.io/prometheus-api.

## 0.1.2 / 2023-11-18

* [ENHANCEMENT] Use remote schema for Prometheus rule #7

## 0.1.1 / 2023-10-27

* [CHANGE] Upgraded PyYAML module from `5.4.1` to `6.0.1` due to the following [issue](https://github.com/yaml/pyyaml/issues/724).
* [ENHANCEMENT] Updated README.md.
* [ENHANCEMENT] Added a new stage for vulnerability scanning of Docker images.