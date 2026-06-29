from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.category_service import CategoryService
from app.services.product_service import ProductService
from app.services.sale_service import SaleService


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    """Dependency provider for category service."""
    return CategoryService(db)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency provider for product service."""
    return ProductService(db)


def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    """Dependency provider for sale service."""
    return SaleService(db)
