from fastapi import APIRouter, Response, Request, Body, status
from starlette.background import BackgroundTask
from fastapi.responses import FileResponse
from src.models.export import ExportData
from src.core import export as exp
from src.utils.log import logger
from typing import Annotated
from src.core import base

router = APIRouter()


@router.post("/export",
             name="Export data from Prometheus",
             description="Exports data from Prometheus based on the provided PromQL",
             status_code=status.HTTP_200_OK,
             tags=["export"],
             responses={
                 200: {
                     "description": "OK",
                     "content": {
                         "text/csv; charset=utf-8": {
                             "example": "__name__,instance,job,timestamp,value\n"
                                        "up,prometheus-api:5000,prometheus-api,1719131438.585,1\n"
                                        "up,localhost:9090,prometheus,1719131438.585,1"
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
                                    "query": "sum by (instance) (prometheus_build_info",
                                    "message": "invalid parameter 'query': 1:41: parse error: unclosed left parenthesis"

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
                                     "query": "sum by (instance) (prometheus_build_info)",
                                     "message": "Prometheus query has failed. HTTPConnectionPool(host='localhost', port=9090)"
                                 }
                             ]
                         }
                     }
                 }
             }
             )
async def export(
        request: Request,
        response: FileResponse or Response,
        data: Annotated[
            ExportData,
            Body(
                openapi_examples=ExportData._request_body_examples,
            )
        ],
        format: str = "csv"
):
    data = data.dict()
    expr, start = data.get("expr"), data.get("start")
    end, step = data.get("end"), data.get("step")
    file, file_format = None, format.lower()
    custom_fields, timestamp_format = data.get(
        "replace_fields"), data.get("timestamp_format")
    validation_status, response.status_code, sts, msg = base.validate_schema(
        "export.json", data)
    if validation_status:
        range_query = True if all([start, end, step]) else False
        resp_status, response.status_code, resp_data = exp.prom_query(
            range_query=range_query,
            query=expr, start=start,
            end=end, step=step)
        if resp_status:
            labels, data_processed = exp.data_processor(
                source_data=resp_data, custom_fields=custom_fields, timestamp_format=timestamp_format)
            file_generator_status, sts, response.status_code, file, msg = exp.file_generator(
                file_format=file_format, data=data_processed, fields=labels)
        else:
            sts, msg = resp_data.get("status"), resp_data.get("error")

    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "query": expr,
            "method": request.method,
            "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})
    if sts == "success":
        return FileResponse(path=file,
                            background=BackgroundTask(exp.cleanup_files, file))
    return {"status": sts, "query": expr, "message": msg}
