from main.models import Copy, Book
from .extensions import db

class CopyService:
    @staticmethod
    def create_copy(book_id, status="Available"):
        book = Book.query.get(book_id)
        if not book:
            return None
        copy = Copy(book_id=book_id, status=status)
        db.session.add(copy)
        db.session.commit()
        return copy

    @staticmethod
    def get_copies_by_book(book_id):
        return Copy.query.filter_by(book_id=book_id).all()

    @staticmethod
    def update_copy(copy_id, status=None):
        copy = Copy.query.get(copy_id)
        if not copy:
            return None
        if status:
            copy.status = status
        db.session.commit()
        return copy

    @staticmethod
    def delete_copy(copy_id):
        copy = Copy.query.get(copy_id)
        if not copy:
            return False
        db.session.delete(copy)
        db.session.commit()
        return True