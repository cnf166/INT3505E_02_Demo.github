from main.models import Book
from .extensions import db

class BookFeature:
    @staticmethod
    def add_book(title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author)
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def get_all_books(book_id: int) -> list[Book]:
        return Book.query.all()
    
    @staticmethod
    def get_book_by_id(book_id: int) -> Book:
        return Book.query.get(book_id)

    @staticmethod
    def update_book(book_id: int, title: str = None, author: str = None, year: int = None) -> Book:
        book = Book.query.get(book_id)
        if title:
            book.title = title
        if author:
            book.author = author
        db.session.commit()
        return book
        
    @staticmethod
    def delete_book(book_id: int) -> None:
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()


    
    