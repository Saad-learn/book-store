from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    title: str
    description: str
    price: float
    author_id: int
    isbn: str = Field(..., pattern=r"^\d{3}-\d{10}$", description="Format: 123-1234567890")

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: str | None = None
    publication_date: Optional[date] = None
    isbn: Optional[str] = None
    price: Optional[float] = None
    author_id: Optional[int] = None

class Book(BookBase):
    id: int
    
    class Config:
        from_attributes = True
