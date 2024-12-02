from src.models.policy import MetricsLifecyclePolicyCreate, MetricsLifecyclePolicyUpdate
from fastapi import APIRouter, Response, Request, Body, status
from apscheduler.triggers.date import DateTrigger
from src.core.base import validate_schema
from src.utils.scheduler import schedule
from src.core import policies as mlp
from src.utils.log import logger
from datetime import datetime
from typing import Annotated

router = APIRouter()
policies = mlp.load_policies()


@router.get("/metrics-lifecycle-policies/{name}",
            name="Get metrics lifecycle policy by name",
            description="Returns metrics lifecycle policy that match the provided name parameter",
            status_code=status.HTTP_200_OK,
            tags=["metrics-lifecycle-policies"],
            responses={
                200: {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "match": "{__name__=~'go_.*'}",
                                    "keep_for": "7d",
                                    "description": "This metrics lifecycle policy keeps GoLang metrics for 7 days"
                                }
                            ]
                        }
                    }
                },
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "error",
                                    "message": "Policy not found"}
                            ]
                        }
                    }
                }
            }
            )
async def get_policy(
        name: str,
        request: Request,
        response: Response,
):
    resp = {
        200: {
            "status": "success",
            "message": "Successfully returned the requested metric lifecycle policy"},
        404: {
            "status": "error",
            "message": "Policy not found"}}
    response.status_code = 200 if policies.get(name) else 404
    logger.info(
        msg=resp[response.status_code]["message"],
        extra={
            "status": response.status_code,
            "policy_name": name,
            "method": request.method,
            "request_path": request.url.path})
    return policies.get(name) or resp[response.status_code]


@router.get("/metrics-lifecycle-policies",
            name="Get all metrics lifecycle policies",
            description="Returns all metrics lifecycle policies",
            status_code=status.HTTP_200_OK,
            tags=["metrics-lifecycle-policies"],
            responses={
                200: {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "GoLang Policy": {
                                        "match": "{__name__=~'go_.*'}",
                                        "keep_for": "7d",
                                        "message": "This policy keeps GoLang metrics for 7 days"
                                    },
                                    "Kubernetes Policy": {
                                        "match": "{job='kubernetes-pods'}",
                                        "keep_for": "10d",
                                        "message": "This policy keeps series of job 'kubernetes-pods' for 10 days"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
            )
async def get_policies(
        request: Request,
        response: Response,
):
    response.status_code = 200
    logger.info(
        msg="Successfully returned all metrics lifecycle policies",
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": request.url.path})
    return policies


@router.post("/metrics-lifecycle-policies",
             name="Create metrics lifecycle policy",
             description="Creates a new metrics lifecycle policy",
             status_code=status.HTTP_201_CREATED,
             tags=["metrics-lifecycle-policies"],
             responses={
                  201: {
                      "description": "Created",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "success",
                                      "policy_name": "GoLang Metrics Policy",
                                      "message": "Policy created successfully"
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
                                      "message": "Additional properties are not allowed (time was unexpected)"
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
                                      "message": "The requested policy already exists"
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
                                      "message": "Failed to create metric lifecycle policy"
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
        policy: Annotated[
            MetricsLifecyclePolicyCreate,
            Body(
                openapi_examples=MetricsLifecyclePolicyCreate._request_body_examples,
            )
        ]
):
    data = policy.dict()
    validation_status, response.status_code, sts, msg = mlp.validate_prom_admin_api()
    if validation_status:
        validation_status, response.status_code, sts, msg = validate_schema(
            "policies_create.json", data)
        if validation_status:
            validation_status, response.status_code, sts, msg, val = mlp.validate_duration(
                data.get("keep_for"))
            if validation_status:
                response.status_code, sts, msg = mlp.create_policy(
                    **policy.dict(), data=policies)
    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "policy_name": policy.dict().get("name"),
            "method": request.method,
            "request_path": request.url.path})
    return {
        "status": sts,
        "policy_name": policy.dict().get("name"),
        "message": msg
    }


@router.patch("/metrics-lifecycle-policies/{name}",
              name="Update metrics lifecycle policy by name",
              description="Updates specific metrics lifecycle policy",
              status_code=status.HTTP_200_OK,
              tags=["metrics-lifecycle-policies"],
              responses={
                  200: {
                      "description": "OK",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "success",
                                      "message": "Policy updated successfully"
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
                                      "message": "Additional properties are not allowed ('name' was unexpected)"
                                  }
                              ]
                          }
                      }
                  },
                  404: {
                      "description": "Not Found",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "error",
                                      "message": "Policy not found"
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
                                      "message": "Failed to create metric lifecycle policy"
                                  }
                              ]
                          }
                      }
                  }
              }
              )
async def update(
        name: str,
        request: Request,
        response: Response,
        policy: Annotated[
            MetricsLifecyclePolicyUpdate,
            Body(
                openapi_examples=MetricsLifecyclePolicyUpdate._request_body_examples,
            )
        ]
):
    data = policy.dict(exclude_unset=True)
    validation_status, response.status_code, sts, msg = mlp.validate_prom_admin_api()
    if validation_status:
        validation_status, response.status_code, sts, msg = validate_schema(
            "policies_update.json", data)
        if validation_status:
            validation_status, response.status_code, sts, msg, val = mlp.validate_duration(
                data.get("keep_for"))
            if validation_status:
                response.status_code, sts, msg = mlp.update_policy(
                    name=name, data=data, policies=policies)
    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "policy_name": name,
            "method": request.method,
            "request_path": request.url.path})
    return {
        "status": sts,
        "policy_name": name,
        "message": msg
    }


@router.delete("/metrics-lifecycle-policies/{name}",
               name="Delete metrics lifecycle policy",
               description="Deletes specific metrics lifecycle policy",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["metrics-lifecycle-policies"],
               responses={
                   204: {
                    "description": "No Content"
                   },
                   404: {
                       "description": "Not Found",
                       "content": {
                           "application/json": {
                               "example": [
                                   {
                                       "status": "error",
                                       "message": "Policy not found"
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
                                       "message": "Failed to delete metrics lifecycle policy"
                                   }
                               ]
                           }
                       }
                   }
               }
               )
async def delete(
        name: str,
        request: Request,
        response: Response
):

    response.status_code, sts, msg = mlp.delete_policy(
        name=name, policies=policies)
    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": request.url.path})
    return {
        "status": sts,
        "message": msg} if response.status_code != 204 else response.status_code


@router.post("/metrics-lifecycle-policies/trigger",
             name="Trigger metrics lifecycle policies",
             description="Force triggers all new metrics lifecycle policies",
             status_code=status.HTTP_202_ACCEPTED,
             tags=["metrics-lifecycle-policies"],
             responses={
                  202: {
                      "description": "Accepted",
                      "content": {
                          "application/json": {
                              "example": [
                                  {
                                      "status": "success",
                                      "message": "Your request has been accepted for processing"
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
                                     "message": "Cannot create a new task. Server is currently processing another task"
                                 }
                             ]
                         }
                     }
                  },
             }
             )
async def trigger(request: Request, response: Response):
    from src.tasks.policies import running_tasks
    if not running_tasks:
        schedule(trigger=DateTrigger(run_date=datetime.now()))
        response.status_code, sts, msg = 202, "success", "Request has been accepted for processing"
    else:
        response.status_code, sts, msg = 409, "error", \
            "Cannot create a new task. Server is currently processing another task"
    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": request.url.path})
    return {
        "status": sts,
        "message": msg
    }
