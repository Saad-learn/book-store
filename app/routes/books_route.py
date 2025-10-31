from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.schemas import BookDTO
from app.models import Author, Book

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

def check_author_exists(db: Session, author_id: int):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Author with id {author_id} does not exist."
        )

@router.post("/", response_model=BookDTO, status_code=status.HTTP_201_CREATED)
def create_book(book: BookDTO, db: Session = Depends(get_db)):
    """Create a new book, ensuring the author_id is valid."""
    check_author_exists(db, book.author_id)
    
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookDTO])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of all books, including author details."""
    books = db.query(Book).options(joinedload(Book.author)).offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookDTO)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a single book by ID, including author details."""
    book = db.query(Book).options(joinedload(Book.author)).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookDTO)
def update_book(book_id: int, book_update:BookDTO, db: Session = Depends(get_db)):
    """Update an existing book's details."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
    update_data = book_update.model_dump(exclude_unset=True)
    
    if 'author_id' in update_data:
        check_author_exists(db, update_data['author_id'])

    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book by ID."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"ok": True}