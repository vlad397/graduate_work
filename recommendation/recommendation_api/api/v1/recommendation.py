from http import HTTPStatus

from fastapi import APIRouter, Depends
from models.body import BatchQdrantPoints, FilmBasedRecommendation
from svc.embedder import Transformer, get_transformer
from svc.qdrant import QdrantProcess, get_qdrant_process

router = APIRouter(prefix="/recommendation")


@router.post("/film-personal-top/", status_code=HTTPStatus.OK)
async def get_recommendation_by_films(
    fids: FilmBasedRecommendation, qp: QdrantProcess = Depends(get_qdrant_process)
) -> FilmBasedRecommendation:
    return await qp.recommendation_process(fids.ids)


@router.post("/generate-embeddings/", status_code=HTTPStatus.OK)
async def get_embeddings(
    qp: BatchQdrantPoints, transformer: Transformer = Depends(get_transformer)
) -> list[list[float]]:
    return transformer.processing(qp)
