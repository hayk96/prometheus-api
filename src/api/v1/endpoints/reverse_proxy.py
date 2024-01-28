from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask
from src.utils.arguments import arg_parser
from src.utils.log import logger
from fastapi import Request
import httpx

prom_addr = arg_parser().get("prom.addr")
client = httpx.AsyncClient(base_url=prom_addr)


async def _reverse_proxy(request: Request):
    """
    This function implements as a reverse proxy to the Prometheus HTTP API
    ref: https://github.com/tiangolo/fastapi/issues/1788#issuecomment-1071222163
    """
    url = httpx.URL(path=request.url.path,
                    query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(request.method, url,
                                  headers=request.headers.raw,
                                  content=await request.body())
    rp_resp = await client.send(rp_req, stream=True)
    logger.info(
        msg="-",
        extra={
            "status": rp_resp.status_code,
            "method": request.method,
            "request_path": rp_resp.url.path})
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )
