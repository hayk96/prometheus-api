from src.services.mlp import MetricsLifecyclePolicyService, load_policies
from fastapi import APIRouter, Response, Request, Body, status
from src.utils.log import logger
from typing import Annotated

router = APIRouter()
data = load_policies()


@router.get("/metrics-lifecycle-policy/{name}",
            name="Returns requested lifecycle policy",
            description="Returns requested lifecycle policy",
            status_code=status.HTTP_200_OK,
            tags=["metrics-lifecycle-policy"],
            responses={
                 200: {
                     "description": "OK",
                     "content": {
                         "application/json": {
                             "example": [
                                {
                                    "pattern": "go_.+",
                                    "delete_after": "7d",
                                    "description": "This is 7d metric lifecycle policy"
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
                 }
            }
            )
async def get_policy(
        name: str,
        request: Request,
        response: Response,
):
    resp = {
        200: {"status": "success", "msg": "Successfully returned requested metric lifecycle policy."},
        404: {"status": "error", "msg": "Policy not found"}
    }
    response.status_code = 200 if data.get(name) else 404
    logger.info(
        msg=resp[response.status_code],
        extra={
            "status": response.status_code,
            "policy_name": name,
            "method": request.method,
            "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})
    return data.get(name) or resp[response.status_code]


@router.get("/metrics-lifecycle-policy",
            name="List all metric lifecycle policies",
            description="Lists all metric lifecycle policies",
            status_code=status.HTTP_200_OK,
            tags=["metrics-lifecycle-policy"],
            responses={
                 200: {
                     "description": "OK",
                     "content": {
                         "application/json": {
                             "example": [
                                {
                                    "GoLang Policy": {
                                        "pattern": "go_+",
                                        "delete_after": "7d",
                                        "message": "Policy for GoLang metrics"
                                    },
                                    "Kubernetes Policy": {
                                        "pattern": "kube_+",
                                        "delete_after": "10d",
                                        "message": "Policy for Kubernetes metrics"
                                    }
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
                                    "message": "Failed to list metric lifecycle policy"
                                }
                            ]
                        }
                    }
                 }
            }
            )
async def get_all_policies(
        request: Request,
        response: Response,
):
    response.status_code = 200
    logger.info(
        msg="Successfully returned .....",
        extra={
            "status": response.status_code,
            "method": request.method,
            "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})
    return data


@router.post("/metrics-lifecycle-policy",
             name="Create Metric Lifecycle Policy",
             description="Creates a new metric lifecycle policy",
             status_code=status.HTTP_201_CREATED,
             tags=["metrics-lifecycle-policy"],
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
            MetricsLifecyclePolicyService,
            Body(
                openapi_examples=MetricsLifecyclePolicyService._request_body_examples,
            )
        ]
):
    p = MetricsLifecyclePolicyService(**policy.dict())
    response.status_code, sts, msg = p.create_policy(data)
    logger.info(
        msg=msg,
        extra={
            "status": sts,
            "policy_name": p.name,
            "method": request.method,
            "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})
    return {
        "status": sts,
        "policy_name": p.name,
        "message": msg
    }


@router.put("/metrics-lifecycle-policy/{name}",
             name="Update Metrics Lifecycle Policy",
             description="Updates the specific metrics lifecycle policy",
             status_code=status.HTTP_200_OK,
             tags=["metrics-lifecycle-policy"],
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
                                     "message": "Additional properties are not allowed ('rule' was unexpected)"
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
            MetricsLifecyclePolicyService,
            Body(
                openapi_examples=MetricsLifecyclePolicyService._request_body_examples,
            )
        ]
):
    p = MetricsLifecyclePolicyService(**policy.dict())
    response.status_code, sts, msg = p.create_policy(data)
    if data.get(name):
        data[name].update()