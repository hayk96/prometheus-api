from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse, Response
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

router = APIRouter()

homepage = "ui/homepage"
rules_management = "ui/rules-management"

@router.get("/", response_class=HTMLResponse)
async def home_page():
    with open(f"{homepage}/index.html", "r") as html:
        return html.read()

@router.get("/script.js", response_class=Response)
async def rules_management_page():
    with open(f"{rules_management}/script.js", "r") as html:
        return html.read()

@router.get("/style.css", response_class=Response)
async def rules_management_page():
    with open(f"{rules_management}/style.css", "r") as html:
        return html.read()

@router.get("/rules-management")
async def rules_management_page():
    return FileResponse(f"{rules_management}/index.html")