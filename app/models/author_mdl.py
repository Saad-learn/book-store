from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    bio = Column(Text, default="No bio provided")

    books = relationship("Book", back_populates="author")