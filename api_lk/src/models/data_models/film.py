from models.base import DefaultModel
from models.data_models.genre import Genre


class Film(DefaultModel):
    id: str
    title: str | None
    description: str | None
    imdb_rating: float | None = None
    genre: list[Genre] | None = None
