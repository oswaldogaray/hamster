from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import TokenResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin) -> TokenResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication is scaffolded for future implementation.",
    )
