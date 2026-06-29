from sqlalchemy.orm import Session

from app.schemas.auth import UserLogin


class AuthService:
    """Authentication service placeholder for future implementation."""

    def __init__(self, db: Session):
        self.db = db

    def login(self, payload: UserLogin) -> dict:
        raise NotImplementedError("Authentication service is not implemented yet.")
