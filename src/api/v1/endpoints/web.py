from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from src.utils.arguments import arg_parser
from src.utils.log import logger
from fastapi import APIRouter
from fastapi import Request
from os.path import exists

router = APIRouter()

if arg_parser().get("web.enable_ui") == "true":
    rules_management = "ui/pages/rules-management"
    metrics_management = "ui/pages/metrics-management"
    reports = "ui/pages/reports"
    logger.info("Starting web management UI")

    @router.get("/", response_class=HTMLResponse,
                description="Renders home page of this application",
                include_in_schema=False)
    async def homepage():
        return FileResponse("ui/pages/homepage/index.html")

    @router.get(
        "/images/{path}",
        description="Returns common image resources for web UI",
        include_in_schema=False)
    async def images(path, request: Request):
        assets_images = "ui/assets/images"
        if exists(f"{assets_images}/{path}"):
            return FileResponse(f"{assets_images}/{path}")
        sts, msg = "404", "Not Found"
        logger.info(
            msg=msg,
            extra={
                "status": sts,
                "method": request.method,
                "request_path": request.url.path})
        return f"{sts} {msg}"

    @router.get("/rules-management",
                description="Renders rules management HTML page of this application",
                include_in_schema=False)
    async def rules_management_page():
        return FileResponse(f"{rules_management}/index.html")

    @router.get(
        "/rules-management/{path}",
        description="Returns JavaScript and CSS files of the rules management page",
        include_in_schema=False)
    async def rules_management_files(path, request: Request):
        if path in ["script.js", "style.css"]:
            return FileResponse(f"{rules_management}/{path}")
        sts, msg = "404", "Not Found"
        logger.info(
            msg=msg,
            extra={
                "status": sts,
                "method": request.method,
                "request_path": request.url.path})
        return f"{sts} {msg}"

    @router.get("/metrics-management",
                description="Renders metrics management HTML page of this application",
                include_in_schema=False)
    async def metrics_management_page():
        return FileResponse(f"{metrics_management}/index.html")

    @router.get(
        "/metrics-management/{path}",
        description="Returns JavaScript and CSS files of the metrics management page",
        include_in_schema=False)
    async def metrics_management_files(path, request: Request):
        if path in ["script.js", "style.css"]:
            return FileResponse(f"{metrics_management}/{path}")
        sts, msg = "404", "Not Found"
        logger.info(
            msg=msg,
            extra={
                "status": sts,
                "method": request.method,
                "request_path": request.url.path})
        return f"{sts} {msg}"

    @router.get("/reports",
                description="Renders Reports HTML page of this application",
                include_in_schema=False)
    async def reports_page():
        return FileResponse(f"{reports}/index.html")

    @router.get(
        "/reports/{path}",
        description="Returns JavaScript and CSS files of the Reports",
        include_in_schema=False)
    async def reports_files(path, request: Request):
        if path in ["script.js", "style.css"]:
            return FileResponse(f"{reports}/{path}")
        sts, msg = "404", "Not Found"
        logger.info(
            msg=msg,
            extra={
                "status": sts,
                "method": request.method,
                "request_path": request.url.path})
        return f"{sts} {msg}"
