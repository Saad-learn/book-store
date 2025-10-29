from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import models, schemas

def create_author(db: Session, author_in: schemas.AuthorCreate):
    """Creates a new Author record in the database."""
    author = models.Author(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def get_author(db: Session, author_id: int):
    """Retrieves a single Author by ID using Session.get (SQLAlchemy 2.0 style)."""
    return db.get(models.Author, author_id)


def list_authors(db: Session, skip: int = 0, limit: int = 100):
    """Lists all Author records with pagination."""
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def update_author(db: Session, author: models.Author, changes: dict):
    """Updates an existing Author record with the given changes."""
    for k, v in changes.items():
        setattr(author, k, v)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author: models.Author):
    """Deletes an Author record."""
    db.delete(author)
    db.commit()
    return None