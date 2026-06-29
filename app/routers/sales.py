from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate
from app.services.dependencies import get_sale_service
from app.services.exceptions import ConflictError, NotFoundError, ServiceError, ValidationError
from app.services.sale_service import SaleService

router = APIRouter(prefix="/sales", tags=["sales"])


def _raise_http_from_service_error(exc: Exception) -> None:
    if isinstance(exc, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if isinstance(exc, ValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc


@router.get("", response_model=list[SaleRead])
def list_sales(service: SaleService = Depends(get_sale_service)) -> list[SaleRead]:
    try:
        return service.list_sales()
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, service: SaleService = Depends(get_sale_service)) -> SaleRead:
    try:
        return service.get_sale(sale_id)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.post("", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(payload: SaleCreate, service: SaleService = Depends(get_sale_service)) -> SaleRead:
    try:
        return service.create_sale(payload)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)


@router.patch("/{sale_id}", response_model=SaleRead)
def update_sale(
    sale_id: int, payload: SaleUpdate, service: SaleService = Depends(get_sale_service)
) -> SaleRead:
    try:
        return service.update_sale(sale_id, payload)
    except ServiceError as exc:
        _raise_http_from_service_error(exc)
