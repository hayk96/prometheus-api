from fastapi.middleware.cors import CORSMiddleware
from src.utils.arguments import arg_parser
from src.utils.scheduler import schedule
from src.api.v1.api import api_router
from src.utils.openapi import openapi
from src.utils.metrics import metrics
from src.utils.log import logger
from src.utils import settings
from fastapi import FastAPI
import uvicorn
import sys


args = arg_parser()
prom_addr, rule_path = args.get("prom.addr"), args.get("rule.path")
host, port = args.get("web.listen_address").split(":")

if not all([settings.check_rules_directory(rule_path),
            settings.check_fs_permissions(rule_path),
            settings.establish_prom_connection(prom_addr),
            settings.check_reload_api_status(prom_addr)]):
    sys.exit()


def custom_openapi_wrapper():
    return openapi(app)


app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
app.openapi = custom_openapi_wrapper
metrics(app)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


def main():
    config = uvicorn.Config(
        app,
        host=host,
        port=int(port),
        server_header=False,
        date_header=False,
        log_config=None)
    server = uvicorn.Server(config)
    try:
        logger.info(f"Server listening on {host}:{port}")
        server.run()
    except BaseException as e:
        logger.error(e)


if __name__ == "__main__":
    schedule()
    main()
