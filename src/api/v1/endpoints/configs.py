from fastapi import APIRouter, Response, Request, Body, status
from fastapi.responses import FileResponse, PlainTextResponse
from src.core.export import validate_request
from src.models.config import UpdateConfig
from src.core import configs as cfg
from src.utils.log import logger
from typing import Annotated
import yaml


router = APIRouter()


@router.get("/configs",
            name="Get Prometheus configuration",
            description="Get Prometheus configuration in various formats depending on the request header",
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
async def configs(
        request: Request,
        response: (Response or PlainTextResponse)
):
    cfg_status, response.status_code, cfg_dict = cfg.get_prometheus_config()
    if cfg_status:
        if request.headers.get("content-type") == "application/yaml":
            data_yaml = yaml.dump(cfg_dict, Dumper=yaml.SafeDumper, sort_keys=False)
            cfg_dict = PlainTextResponse(data_yaml)
            # return FileResponse("/tmp/prom.yml")

    logger.info(
        msg="Prometheus configuration provided successfully" if cfg_status else cfg_dict.get("error"),
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
            responses={}
            )
async def update(
        request: Request,
        response: Response,
        data: Annotated[
            UpdateConfig,
            Body(
                openapi_examples={},
            )
        ],
):
    user_data = data.__str__()
    data_yaml = yaml.dump(user_data, Dumper=yaml.SafeDumper, sort_keys=False)
    with open("/Users/hayk/Projects/Personal/Github/hayk96/prometheus-api/docs/examples/docker/prometheus.yml", "w") as f:
        f.write(data_yaml)
    return PlainTextResponse(data_yaml)


@router.patch("/configs",
              name="Get Prometheus configuration",
              description="",
              status_code=status.HTTP_200_OK,
              tags=["configs"],
              responses={}
              )
async def partial_update(
        request: Request,
        response: Response,
        data: Annotated[
            UpdateConfig,
            Body(
                openapi_examples={},
            )
        ],
):
    user_data = data.__dict__
    print(validate_request("configs.json", user_data))
    cfg_status, response.status_code, cfg_dict = cfg.get_prometheus_config()
    if cfg_status:
        cfg.partial_update(user_data, cfg_dict)
        return cfg_dict
