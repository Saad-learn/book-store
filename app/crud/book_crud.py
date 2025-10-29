from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import models, schemas

def create_book(db: Session, book_in: schemas.BookCreate):
    """Creates a new Book record, handling potential IntegrityErrors (e.g., duplicate ISBN or missing author)."""
    book = models.Book(**book_in.model_dump())
    db.add(book)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Database constraint error: {e.orig.pgerror}" if hasattr(e.orig, 'pgerror') else str(e.orig)
        )
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int):
    """Retrieves a single Book by ID."""
    return db.get(models.Book, book_id)


def list_books(db: Session, skip: int = 0, limit: int = 100):
    """Lists all Book records with pagination."""
    stmt = select(models.Book).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def update_book(db: Session, book: models.Book, changes: dict):
    """Updates an existing Book record, handling potential IntegrityErrors."""
    for k, v in changes.items():
        setattr(book, k, v)
    db.add(book)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Database constraint error: {e.orig.pgerror}" if hasattr(e.orig, 'pgerror') else str(e.orig)
        )
    db.refresh(book)
    return book


def delete_book(db: Session, book: models.Book):
    """Deletes a Book record."""
    db.delete(book)
    db.commit()
    return None