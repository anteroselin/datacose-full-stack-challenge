from fastapi import APIRouter

from api.auth import router as auth_router
from api.authors import router as authors_router
from api.books import router as books_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(authors_router, prefix="/authors", tags=["Authors"])
router.include_router(books_router, prefix="/books", tags=["Books"])
