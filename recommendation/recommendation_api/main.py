import db.qdrant
import svc.qdrant
from api import v1
from core import config
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from qdrant_client import QdrantClient
from svc import embedder
from svc.embedder import Transformer
from svc.qdrant import QdrantProcess

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/docs.json",
    default_response_class=ORJSONResponse,
    debug=config.DEBUG,
)


@app.on_event("startup")
async def startup():
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    db.qdrant.client = client
    embedder.transformer = Transformer()
    svc.qdrant.qdrant_process = QdrantProcess(db.qdrant.client)


app.include_router(v1.router, prefix="/api", tags=["recommendation"])
