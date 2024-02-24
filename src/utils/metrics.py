from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator
from fastapi import FastAPI
from .log import logger
from sys import modules


def metrics(app: FastAPI):
    """
    This function exposes Prometheus
    metrics for prometheus-api service
    """
    metrics_path = "/api-metrics"
    try:
        instrumentator = PrometheusFastApiInstrumentator(
            should_group_status_codes=False,
            excluded_handlers=["/{path:path}", "/.*metrics"]
        )
        instrumentator.instrument(app)
        instrumentator.expose(app, endpoint=metrics_path)
    except BaseException as e:
        logger.error(f"{modules[__name__], e}")
    else:
        logger.info(f"Successfully started metrics endpoint at {metrics_path} path")
