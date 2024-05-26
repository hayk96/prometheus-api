from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI


def openapi(app: FastAPI):
    """This function customizes the OpenAPI definition
    and adds a logo for the ReDoc API page. NOTE: this
    does not include a definition of the routes"""

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Prometheus API",
        summary="Extended HTTP API service for Prometheus",
        description="This project enhances the native Prometheus HTTP API by "
                    "providing additional features and addressing its limitations. "
                    "Running as a sidecar alongside the Prometheus server enables "
                    "users to extend the capabilities of the API.",
        version="0.2.2",
        contact={
            "name": "Hayk Davtyan",
            "url": "https://hayk96.github.io",
            "email": "hayko5999@gmail.com",
        },
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
            "url": "https://raw.githubusercontent.com/hayk96/prometheus-api/main/LICENSE"
        },
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://raw.githubusercontent.com/hayk96/prometheus-api/main/docs/images/logo.png",
        "href": "https://hayk96.github.io/prometheus-api",
        "altText": "Prometheus API"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema
