from starlette.responses import FileResponse
from src.utils.arguments import arg_parser
from fastapi.responses import HTMLResponse
from src.utils.log import logger
from fastapi import APIRouter
from fastapi import Request

router = APIRouter()

if arg_parser().get("web.enable_ui") == "true":
    rules_management = "ui/rules-management"
    logger.info("Starting web management UI")

    @router.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def homepage():
        return FileResponse("ui/homepage/index.html")

    @router.get("/rules-management", include_in_schema=False)
    async def rules_management_page():
        return FileResponse(f"{rules_management}/index.html")

    @router.get("/rules-management/{path}", include_in_schema=False)
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
