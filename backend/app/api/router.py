from fastapi import APIRouter

from app.features.base.routes import router as base_router
from app.features.cargo_allocation.routes import router as cargo_allocation_router
from app.features.health.routes import router as health_router

api_router = APIRouter()
api_router.include_router(base_router)
api_router.include_router(
    cargo_allocation_router,
    prefix="/cargo-allocation",
    tags=["cargo allocation"],
)
api_router.include_router(health_router, prefix="/health", tags=["health"])
