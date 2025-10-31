from fastapi import FastAPI
from app.database import Base, engine
from app.routes import authors_route, books_route

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app = FastAPI(
    title="Bookstore API")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Bookstore."}

app.include_router(authors_route.router)
app.include_router(books_route.router)

