from fastapi import APIRouter

from .endpoints.notes import router as note_router
from .endpoints.category import router as category_router

router = APIRouter(prefix="/v1")

router.include_router(note_router, prefix="/note", tags=["Notes"])
router.include_router(category_router, prefix="/category", tags=["Category"])
