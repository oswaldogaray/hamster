from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.health import router as health_router
from app.routers.inventory import router as inventory_router
from app.routers.products import router as products_router
from app.routers.sales import router as sales_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(categories_router)
api_router.include_router(inventory_router)
api_router.include_router(products_router)
api_router.include_router(sales_router)
api_router.include_router(auth_router)
