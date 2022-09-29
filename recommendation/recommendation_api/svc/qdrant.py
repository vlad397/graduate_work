import asyncio
import functools
import uuid
from typing import List, Optional

import numpy as np
from core import config
from models.body import FilmBasedRecommendation
from qdrant_client import QdrantClient


class QdrantProcess:
    def __init__(self, client: QdrantClient):
        self.client = client

    async def get_vectors(self, ids: List[uuid.UUID]):
        loop = asyncio.get_running_loop()
        return [
            rec.vector
            for rec in await loop.run_in_executor(
                None,
                functools.partial(
                    self.client.retrieve,
                    collection_name=config.QDRANT_COLLECTION,
                    ids=[str(fid) for fid in ids],
                    with_vector=True,
                ),
            )
        ]

    async def get_recommendation_by_vector(self, vector: List[float]):
        loop = asyncio.get_running_loop()
        return [
            qp.id
            for qp in await loop.run_in_executor(
                None,
                functools.partial(
                    self.client.search,
                    collection_name=config.QDRANT_COLLECTION,
                    query_vector=vector,
                    limit=10,
                ),
            )
        ]

    @staticmethod
    def map_recommendation(ids: List) -> FilmBasedRecommendation:
        el, count = np.unique(ids, return_counts=True)
        count_sort_ind = np.argsort(-count)
        return FilmBasedRecommendation(ids=el[count_sort_ind][:10].tolist())

    async def get_all_candidates(self, vectors: List[List[float]]) -> List:
        futures = []
        for vector in vectors:
            futures.append(self.get_recommendation_by_vector(vector=vector))
        results = await asyncio.gather(*futures)
        return [fid for res in results for fid in res]

    async def recommendation_process(self, ids: List) -> FilmBasedRecommendation:
        vectors = await self.get_vectors(ids=ids)
        ids_c = await self.get_all_candidates(vectors=vectors)
        return self.map_recommendation(ids_c)


qdrant_process: Optional[QdrantProcess] = None


def get_qdrant_process() -> Optional[QdrantProcess]:
    return qdrant_process
