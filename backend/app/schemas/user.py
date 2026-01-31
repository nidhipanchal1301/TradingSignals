from pydantic import BaseModel, EmailStr, Field

from typing import Annotated

from uuid import UUID

from datetime import datetime



class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=72)]

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_paid: bool
    created_at: datetime

    class Config:
        from_attributes = True
