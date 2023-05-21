from .. v1.endpoints import reverse_proxy, rules
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(rules.router, prefix="/api/v1")
api_router.add_route("/{path:path}", reverse_proxy._reverse_proxy, ["GET", "POST", "PUT"])
