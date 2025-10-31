from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import Author
from app.database import get_db
from app.schemas.author_sch import AuthorDTO, AuthorCreate


router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.post("/", response_model=AuthorDTO, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author."""
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/", response_model=List[AuthorDTO])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of all authors."""
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors

@router.get("/{author_id}", response_model=AuthorDTO)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Retrieve a single author by ID."""
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=AuthorDTO)
def update_author(author_id: int, author_update: AuthorDTO, db: Session = Depends(get_db)):
    """Update an existing author's details."""
    db_author = read_author(author_id=author_id, db=db) # Reuses the read logic for existence check

    update_data = author_update.model_dump(exclude_unset=True)
    if not update_data:
        return db_author 

    for key, value in update_data.items():
        setattr(db_author, key, value)
    
    db.commit()
    db.refresh(db_author)
    return db_author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author by ID."""
    db_author = read_author(author_id=author_id, db=db)
    
    db.delete(db_author)
    db.commit()
    return {"ok": True}