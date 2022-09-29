import uuid
from typing import Optional

from models.base import BasePModel
from pydantic import validator


class QdrantPoint(BasePModel):
    id: uuid.UUID
    film_title: Optional[str]
    film_description: Optional[str]

    @validator("film_description")
    def prevent_none_film_title(cls, v):
        if v is None:
            return "ups_desc"

    @validator("film_title")
    def prevent_none_film_description(cls, v):
        if v is None:
            return "ups"


class BatchQdrantPoints(BasePModel):
    qp_batch: list[QdrantPoint]


class FilmBasedRecommendation(BasePModel):
    ids: list[uuid.UUID]
