from models.base import DefaultModel


class Genre(DefaultModel):
    id: str
    name: str | None
