from src.utils.settings import check_prom_readiness
from fastapi import APIRouter, Response, status
from src.utils.arguments import arg_parser

router = APIRouter()
rule_path = arg_parser().get("rule.path")
prom_addr = arg_parser().get("prom.addr")


@router.get("/health",
            name="Get system health",
            description="Returns a 200 status when the prometheus-api is able to connect to the Prometheus server",
            status_code=status.HTTP_200_OK,
            tags=["health"],
            responses={
                200: {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "success",
                                    "message": "Service is up and running"
                                }
                            ]
                        }
                    }
                },
                503: {
                    "description": "Service Unavailable",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "status": "error",
                                    "message": "Service is unavailable due to a health-check failure"
                                }
                            ]
                        }
                    }
                }
            })
async def health(response: Response):
    global prom_addr
    if not check_prom_readiness(prom_addr):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error",
                "message": "Service is unavailable due to a health-check failure"}
    return {"status": "success",
            "message": "Service is up and running"}
