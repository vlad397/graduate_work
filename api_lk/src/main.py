from api import v1
from core import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.config.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/docs.json",
    default_response_class=ORJSONResponse,
    debug=config.config.DEBUG,
)


app.include_router(v1.router, prefix="/api", tags=["lk"])
