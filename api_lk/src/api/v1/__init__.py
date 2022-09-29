from fastapi import APIRouter

from .films import router as films_router
from .genres import router as genres_router
from .recommendations import router as recommendations_router

router = APIRouter(prefix="/v1")
router.include_router(films_router)
router.include_router(genres_router)
router.include_router(recommendations_router)
