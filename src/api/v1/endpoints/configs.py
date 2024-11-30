from fastapi import APIRouter, Response, Request, Body, status
from fastapi.responses import PlainTextResponse
from src.core.export import validate_request
from src.models.config import UpdateConfig
from src.core import configs as cfg
from src.models.rule import Rule
from src.utils.log import logger
from typing import Annotated
import yaml

router = APIRouter()
prometheus = Rule()


@router.get("/configs",
            name="Get Prometheus configuration",
            description="Get Prometheus configuration in various formats depending on the `Content-Type` request header",
            status_code=status.HTTP_200_OK,
            tags=["configs"],
            responses={
                200: {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "example": {
                                "global": {
                                    "scrape_interval": "15s",
                                    "scrape_timeout": "10s",
                                    "evaluation_interval": "30s"
                                },
                                "scrape_configs": [
                                    {
                                        "job_name": "prometheus",
                                        "scrape_interval": "15s",
                                        "scrape_timeout": "10s",
                                        "metrics_path": "/metrics",
                                        "scheme": "http",
                                        "static_configs": [
                                            {
                                                "targets": [
                                                    "localhost:9090"
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        "application/yaml": {
                            "example": """
                                global:
                                  scrape_interval: 15s
                                  scrape_timeout: 10s
                                  evaluation_interval: 30s
                                scrape_configs:
                                - job_name: prometheus
                                  scrape_interval: 15s
                                  scrape_timeout: 10s
                                  metrics_path: "/metrics"
                                  scheme: http
                                  static_configs:
                                  - targets:
                                    - localhost:9090
                            """
                        }
                    }
                },
                500: {
                    "description": "Internal Server Error",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "error",
                                    "message": "Failed to connect to Prometheus. Max retries exceeded with url: /api/v1/status/config"
                                }
                            ]
                        }
                    }
                }
            }
            )
async def get_config(
        request: Request,
        response: (Response or PlainTextResponse)
):
    cfg_status, response.status_code, cfg_dict = cfg.get_prometheus_config()
    if cfg_status:
        if request.headers.get("content-type") == "application/yaml":
            data_yaml = yaml.dump(
                cfg_dict,
                Dumper=yaml.SafeDumper,
                sort_keys=False)
            cfg_dict = PlainTextResponse(data_yaml)

    logger.info(
        msg="Prometheus configuration provided successfully" if cfg_status else cfg_dict.get(
            "error"),
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": request.url.path})
    return cfg_dict


@router.put("/configs",
            name="Update Prometheus configuration",
            description="Update entire Prometheus configuration file",
            status_code=status.HTTP_200_OK,
            tags=["configs"],
            responses={
                200: {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "success",
                                    "message": "Configuration updated successfully"
                                }
                            ]
                        }
                    }
                },
                400: {
                    "description": "Bad Request",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "error",
                                    "message": "Additional properties are not allowed (globals was unexpected)"
                                }
                            ]
                        }
                    }
                },
                500: {
                    "description": "Internal Server Error",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "error",
                                    "message": "failed to reload config: couldn't load configuration (--config.file=\"/etc/prometheus/prometheus.yml\"): parsing YAML file /etc/prometheus/prometheus.yml: global scrape timeout greater than scrape interval\n"
                                }
                            ]
                        }
                    }
                }
            }
            )
async def update_config(
        request: Request,
        response: Response,
        data: Annotated[
            UpdateConfig,
            Body(
                openapi_examples={
                    "Update Prometheus configuration": {
                        "description": "Update entire Prometheus configuration file",
                        "value": {
                            "global": {
                                "scrape_interval": "30s",
                                "scrape_timeout": "30s",
                                "evaluation_interval": "1m"
                            },
                            "scrape_configs": [
                                {
                                    "job_name": "prometheus",
                                    "metrics_path": "/metrics",
                                    "scheme": "http",
                                    "static_configs": [
                                        {
                                            "targets": [
                                                "localhost:9090"
                                            ],
                                            "labels": {
                                                "instance": "prometheus-server",
                                                "env:": "production"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            )
        ],
):
    user_data = data.dict(exclude_unset=True)
    cfg.rename_global_keyword(user_data)
    validation_status, response.status_code, sts, msg = \
        validate_request("configs.json", user_data)
    if validation_status:
        data_yaml = yaml.dump(
            user_data,
            Dumper=yaml.SafeDumper,
            sort_keys=False)
        config_update_status, msg = cfg.update_prometheus_yml(data=data_yaml)
        if config_update_status:
            response.status_code, sts, msg = prometheus.reload()
            msg = "Configuration updated successfully" if sts == "success" else msg
        else:
            response.status_code, sts = 500, "error"
    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": request.url.path})

    return {"status": sts, "message": msg}


@router.patch("/configs",
              name="Update part of Prometheus configuration",
              description="Update specific part of Prometheus configuration file",
              status_code=status.HTTP_200_OK,
              tags=["configs"],
              responses={
                  200: {
                      "description": "OK",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "success",
                                      "message": "Configuration updated successfully"
                                  }
                              ]
                          }
                      }
                  },
                  400: {
                      "description": "Bad Request",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "error",
                                      "message": "Additional properties are not allowed (globals was unexpected)"
                                  }
                              ]
                          }
                      }
                  },
                  500: {
                      "description": "Internal Server Error",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "error",
                                      "message": "failed to reload config: couldn't load configuration (--config.file=\"/etc/prometheus/prometheus.yml\"): parsing YAML file /etc/prometheus/prometheus.yml: global scrape timeout greater than scrape interval\n"
                                  }
                              ]
                          }
                      }
                  }
              }
              )
async def partial_update(
        request: Request,
        response: Response,
        data: Annotated[
            UpdateConfig,
            Body(
                openapi_examples={
                    "Update Alertmanager configuration": {
                        "description": "Update Alertmanager configuration settings",
                        "value": {
                            "alerting": {
                                "alertmanagers": [
                                    {
                                        "scheme": "https",
                                        "static_configs": [
                                            {
                                                "targets": [
                                                    "example-alertmanager.com"
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            )
        ],
):
    user_data = data.dict(exclude_unset=True)
    cfg.rename_global_keyword(user_data)
    validation_status, response.status_code, sts, msg = \
        validate_request("configs.json", user_data)
    if validation_status:
        cfg_status, response.status_code, cfg_dict = cfg.get_prometheus_config()
        if cfg_status:
            cfg.partial_update(user_data, cfg_dict)
            data_yaml = yaml.dump(
                user_data,
                Dumper=yaml.SafeDumper,
                sort_keys=False)
            config_update_status, msg = cfg.update_prometheus_yml(
                data=data_yaml)
            if config_update_status:
                response.status_code, sts, msg = prometheus.reload()
                msg = "Configuration updated successfully" if sts == "success" else msg
            else:
                response.status_code, sts = 500, "error"
        else:
            msg = "error"
    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": request.url.path})

    return {"status": sts, "message": msg}
