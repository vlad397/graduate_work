from fastapi import APIRouter

from .recommendation import router as recommendation_router

router = APIRouter(prefix="/v1")
router.include_router(recommendation_router)
