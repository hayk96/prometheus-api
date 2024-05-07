# Changelog

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