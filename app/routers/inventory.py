from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.dependencies import get_product_service
from app.services.exceptions import ConflictError, NotFoundError, ServiceError, ValidationError
from app.services.product_service import ProductService

router = APIRouter(prefix="/inventory", tags=["inventory"])


def _raise_http_from_service_error(exc: Exception) -> None:
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if isinstance(exc, ValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc


@router.get("", response_model=list[ProductRead])
def list_items(service: ProductService = Depends(get_product_service)) -> list[ProductRead]:
    try:
        return service.list_products()
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.get("/{product_id}", response_model=ProductRead)
def get_item(product_id: int, service: ProductService = Depends(get_product_service)) -> ProductRead:
    try:
        return service.get_product(product_id)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ProductCreate, service: ProductService = Depends(get_product_service)
) -> ProductRead:
    try:
        return service.create_product(payload)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.patch("/{product_id}", response_model=ProductRead)
def update_item(
    product_id: int, payload: ProductUpdate, service: ProductService = Depends(get_product_service)
) -> ProductRead:
    try:
        return service.update_product(product_id, payload)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(product_id: int, service: ProductService = Depends(get_product_service)) -> Response:
    try:
        service.delete_product(product_id)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
