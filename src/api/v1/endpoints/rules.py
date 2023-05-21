from fastapi import APIRouter, Response, Request, status
from src.utils.arguments import arg_parser
from string import ascii_lowercase
from src.models.rule import Rule
from src.utils.log import logger
from random import choices
import time
import os

router = APIRouter()


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
        validation_status, sts, msg = rule.validate_rule()
        if not validation_status:
            response.status_code = status.HTTP_400_BAD_REQUEST
            break
        create_rule_status, sts, msg = rule.create_rule(file)
        if not create_rule_status:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            break
        time.sleep(0.1)
        response.status_code, sts, msg = rule.reload()
        if response.status_code != 200:
            rule.delete_rule(file)
            break
        msg = "The rule was created successfully"
        response.status_code = status.HTTP_201_CREATED
        break

    logger.info(
        msg=msg,
        extra={
            "status": response.status_code,
            "method": request.method,
            "path": request.url.path})

    resp = {"status": sts, "message": msg}
    if request.method == "POST":
        resp.update({"file": file})
    return resp


@router.post("/rules", status_code=status.HTTP_201_CREATED)
async def create(rule: Rule, request: Request, response: Response):
    r = Rule(data=rule.data)
    file_prefix = f"{arg_parser().get('file.prefix')}-" if arg_parser().get('file.prefix') else ""
    file_suffix = arg_parser().get('file.extension')

    while True:
        file = f"{file_prefix}{''.join(choices(ascii_lowercase, k=15))}{file_suffix}"
        if os.path.exists(f"{Rule._rule_path}/{file}"):
            continue
        break
    return create_prometheus_rule(r, request, response, file)


@router.put("/rules/{file}", status_code=status.HTTP_201_CREATED)
async def update(file: str, rule: Rule, request: Request, response: Response):
    r = Rule(data=rule.data)

    if file and os.path.exists(f"{Rule._rule_path}/{file}"):
        response.status_code = status.HTTP_409_CONFLICT
        msg = f"The requested file already exists."
        logger.info(
            msg=msg,
            extra={
                "status": response.status_code,
                "method": request.method,
                "path": request.url.path})
        return {"status": "error", "message": msg}
    return create_prometheus_rule(r, request, response, file)


@router.delete("/rules/{file}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(file, request: Request, response: Response):
    r = Rule()

    while True:
        if not os.path.exists(f"{Rule._rule_path}/{file}"):
            response.status_code, sts, msg = status.HTTP_404_NOT_FOUND, "error", "File not found"
            break
        delete_rule_status, sts, msg = r.delete_rule(file)
        if not delete_rule_status:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            break
        reload_status, sts, msg = r.reload()
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
            "path": request.url.path})
    return {
        "status": sts,
        "message": msg} if response.status_code != 204 else response.status_code
