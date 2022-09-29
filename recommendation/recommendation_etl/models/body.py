import uuid
from typing import Optional

from models.base import BasePModel


class QdrantPoint(BasePModel):
    id: uuid.UUID
    film_title: str
    film_description: Optional[str]


class BatchQdrantPoints(BasePModel):
    qp_batch: list[QdrantPoint]
