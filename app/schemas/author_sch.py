from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None

class AuthorDTO(AuthorBase):
    id: int

    class Config:
        from_attributes = True

