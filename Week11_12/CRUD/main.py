from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import crud
from database import init_db
from models import Book

app = FastAPI(
    title="Book Library CRUD Demo",
    description="DEMO",
    version="1.0"
)

# Initialize DB on first start
@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "Book Library API - go to /docs for interactive demo"}

# GET all books
@app.get("/books", response_model=list[Book])
async def read_books():
    return crud.get_books()

# GET one book
@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int):
    book = crud.get_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book

# POST create book
@app.post("/books", response_model=Book, status_code=201)
async def create_new_book(book: Book):
    return crud.create_book(book.dict())

# PUT update book
@app.put("/books/{book_id}", response_model=Book)
async def update_existing_book(book_id: int, book: Book):
    if not crud.get_book(book_id):
        raise HTTPException(404, "Book not found")
    return crud.update_book(book_id, book.dict())

# DELETE book
@app.delete("/books/{book_id}")
async def delete_existing_book(book_id: int):
    if not crud.get_book(book_id):
        raise HTTPException(404, "Book not found")
    crud.delete_book(book_id)
    return {"detail": "Book deleted"}