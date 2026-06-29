from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ORMModel


class UserBase(BaseModel):
    email: EmailStr
    role: str = Field(min_length=1, max_length=64, default="user")


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=255)
    role: str | None = Field(default=None, min_length=1, max_length=64)


class UserRead(ORMModel):
    id: int
    email: EmailStr
    role: str
