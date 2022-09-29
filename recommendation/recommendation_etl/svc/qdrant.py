import backoff
import orjson
import requests
from core.config import config
from models.body import BatchQdrantPoints
from qdrant_client import QdrantClient
from qdrant_client.http import models


class QdrantProcessor:
    def __init__(self, client: QdrantClient):
        self.client = client
        try:
            self.client.get_collection(config.QDRANT_COLLECTION)
        except Exception:
            self.client.recreate_collection(
                collection_name=config.QDRANT_COLLECTION, distance="Cosine", vector_size=config.EMBEDDINGS_VECTOR_SIZE
            )

    def insert_points(self, points: BatchQdrantPoints):
        vector = self.get_embeddings(points)
        ids = [str(point.id) for point in points.qp_batch]
        payloads = [point.dict(exclude={"id"}) for point in points.qp_batch]
        self.client.upsert(
            collection_name=config.QDRANT_COLLECTION,
            points=models.Batch(
                ids=ids,
                payloads=payloads,
                vectors=vector,
            ),
        )

    @backoff.on_exception(backoff.expo, exception=Exception)
    def get_embeddings(self, points: BatchQdrantPoints):
        r = requests.post(config.EMBEDDINGS_GENERATOR_URL, json=orjson.loads(points.json()))
        r.raise_for_status()
        return r.json()
