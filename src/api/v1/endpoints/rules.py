from fastapi import APIRouter, Response, Request, Body, status
from src.utils.arguments import arg_parser
from string import ascii_lowercase
from src.models.rule import Rule
from src.utils.log import logger
from src.core.base import validate_schema
from typing import Annotated
from random import choices
from shutil import copy
import time
import os
from src.core.prometheus import PrometheusRequest

router = APIRouter()
prom = PrometheusRequest()

rule_path = arg_parser().get('rule.path')


def create_prometheus_rule(
        rule: Rule,
        request: Request,
        response: Response,
        file: str) -> dict:
    """
    A common function for the /rules API
    is used in the POST and PUT routes.
    """

    while True:
        validation_status, response.status_code, sts, msg = validate_schema("rules.json", rule.data)
        if not validation_status:
            response.status_code = status.HTTP_400_BAD_REQUEST
            break
        create_rule_status, sts, msg = prom.create_rule(file, data=rule.data)
        if not create_rule_status:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            break
        time.sleep(0.1)
        response.status_code, sts, msg = prom.reload()
        if response.status_code != 200:
            prom.delete_rule(file)
            break
        msg = "The rule was created successfully"
        response.status_code = status.HTTP_201_CREATED
        break

    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})

    resp = {"status": sts, "message": msg}
    if request.method == "POST":
        resp.update({"file": file})
    return resp


@router.post("/rules",
             name="Create Rule",
             description="Creates a new rule with a randomly generated filename",
             status_code=status.HTTP_201_CREATED,
             tags=["rules"],
             responses={
                 201: {
                     "description": "Created",
                     "content": {
                         "application/json": {
                             "example": [
                                {
                                    "status": "success",
                                    "file": "example-rule.yml",
                                    "message": "The rule was created successfully"
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
                                     "message": "Additional properties are not allowed ('rule' was unexpected)"
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
                                     "message": "failed to reload config: one or more errors occurred while applying the new configuration (--config.file=\"/etc/prometheus/prometheus.yml\")\n"
                                 }
                             ]
                         }
                     }
                 }
             }
             )
async def create(
        request: Request,
        response: Response,
        rule: Annotated[
            Rule,
            Body(
                openapi_examples=Rule._request_body_examples,
            )
        ]
):
    r = Rule(data=rule.data)
    file_prefix = f"{arg_parser().get('file.prefix')}-" if arg_parser().get('file.prefix') else ""
    file_suffix = arg_parser().get('file.extension')

    while True:
        file = f"{file_prefix}{''.join(choices(ascii_lowercase, k=15))}{file_suffix}"
        if os.path.exists(f"{rule_path}/{file}"):
            continue
        break
    return create_prometheus_rule(r, request, response, file)


@router.put("/rules/{file}",
            name="Create Rule",
            description="Creates a new rule file with the provided filename",
            status_code=status.HTTP_201_CREATED,
            tags=["rules"],
            responses={
                201: {
                    "description": "Created",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "success",
                                    "message": "The rule was created successfully"
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
                                    "message": "Additional properties are not allowed ('rule' was unexpected)"
                                }
                            ]
                        }
                    }
                },
                409: {
                    "description": "Conflict",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "error",
                                    "message": "The requested file already exists"
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
                                    "message": "failed to reload config: one or more errors occurred while applying the new configuration (--config.file=\"/etc/prometheus/prometheus.yml\")\n"
                                }
                            ]
                        }
                    }
                }
            }
            )
async def update(
    file: str,
    request: Request,
    response: Response,
    rule: Annotated[
        Rule,
        Body(
            openapi_examples=Rule._request_body_examples,
        )
    ],
    recreate: str = "false"
):
    r = Rule(data=rule.data)

    if file and os.path.exists(f"{rule_path}/{file}"):
        if recreate.lower() == "true":
            orig_file, temp_file = f"{rule_path}/{file}", f"{rule_path}/{file}.temp"
            copy(orig_file, temp_file)
            resp = create_prometheus_rule(r, request, response, file)
            if resp.get("status") == "success":
                os.remove(temp_file)
                return resp
            os.rename(temp_file, orig_file)
            return resp

        response.status_code = status.HTTP_409_CONFLICT
        msg = "The requested file already exists."
        logger.info(
            msg=msg,
            extra={
                "status": response.status_code,
                "method": request.method,
                "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})
        return {"status": "error", "message": msg}
    return create_prometheus_rule(r, request, response, file)


@router.delete("/rules/{file}",
               name="Delete Rule",
               description="Deletes a rule that matches to the provided parameter",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["rules"],
               responses={
                   204: {
                       "description": "No Content",
                   },
                   404: {
                       "description": "Not Found",
                       "content": {
                           "application/json": {
                               "example": [
                                   {
                                      "status": "error",
                                      "message": "File not found"
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
                                       "message": "failed to reload config: one or more errors occurred while applying the new configuration (--config.file=\"/etc/prometheus/prometheus.yml\")\n"
                                   }
                               ]
                           }
                       }
                   }
               }
               )
async def delete(file, request: Request, response: Response):

    while True:
        if not os.path.exists(f"{rule_path}/{file}"):
            response.status_code, sts, msg = status.HTTP_404_NOT_FOUND, "error", "File not found"
            break
        delete_rule_status, sts, msg = prom.delete_rule(file)
        if not delete_rule_status:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            break
        reload_status, sts, msg = prom.reload()
        if reload_status != 200:
            response.status_code = reload_status
            break
        msg = "The rule was deleted successfully"
        response.status_code = status.HTTP_204_NO_CONTENT
        break

    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})
    return {
        "status": sts,
        "message": msg} if response.status_code != 204 else response.status_code
