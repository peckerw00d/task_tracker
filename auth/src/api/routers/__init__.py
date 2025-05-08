from fastapi import APIRouter

from .auth_router import router as auth_router


router = APIRouter(
    prefix="/auth",
    tags=[
        "Auth",
    ],
)

router.include_router(auth_router)
