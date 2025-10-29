from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    publication_date = Column(Date, nullable=False)
    description = Column(String)
    isbn = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")