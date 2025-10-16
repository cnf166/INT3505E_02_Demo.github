from main.models import Borrow, Copy
from .extensions import db
from datetime import datetime

class BorrowService:
    @staticmethod
    def borrow_copy(user_id, book_id):
        # Find an available copy for the book
        copy = Copy.query.filter_by(book_id=book_id, status="Available").first()
        if not copy:
            return None, "No available copies"

        # Create borrow record
        borrow = Borrow(user_id=user_id, copy_id=copy.id)
        copy.status = "Borrowed"

        db.session.add(borrow)
        db.session.commit()
        return borrow, None

    @staticmethod
    def return_copy(borrow_id):
        borrow = Borrow.query.get(borrow_id)
        if not borrow:
            return None, "Borrow record not found"
        if borrow.return_date:
            return None, "Copy already returned"

        borrow.return_date = datetime.utcnow()
        borrow.copy.status = "Available"

        db.session.commit()
        return borrow, None
    
    @staticmethod
    def valid_user(borrow_id, user_id):
        borrow = Borrow.query.get(borrow_id)
        if not borrow:
            return None, "Borrow record not found"
        if borrow.user_id == user_id:
            return True
        return False

    @staticmethod
    def list_borrows(user_id=None):
        query = Borrow.query
        if user_id:
            query = query.filter(Borrow.user_id == user_id)
        return query.all()

    @staticmethod
    def admin_update_borrow(borrow_id, user_id=None, copy_id=None, return_date=None):
        borrow = Borrow.query.get(borrow_id)
        if not borrow:
            return None

        # Update user
        if user_id is not None:
            borrow.user_id = user_id

        # Update copy
        if copy_id is not None:
            old_copy = borrow.copy
            new_copy = Copy.query.get(copy_id)
            if not new_copy:
                return None
            # Update copy status if changed
            if old_copy.id != new_copy.id:
                if old_copy.status == "Borrowed":
                    old_copy.status = "Available"
                if new_copy.status != "Available":
                    return None  # cannot assign borrowed copy
                new_copy.status = "Borrowed"
                borrow.copy_id = copy_id

        # Update return date
        if return_date is not None:
            borrow.return_date = return_date
            if borrow.copy:
                borrow.copy.status = "Available" if return_date else "Borrowed"

        db.session.commit()
        return borrow
    
    @staticmethod
    def delete_borrow(borrow_id):
        borrow = Borrow.query.get(borrow_id)
        if not borrow:
            return False

        # If the borrow was still active, mark copy as available
        if borrow.return_date is None and borrow.copy:
            borrow.copy.status = "Available"

        db.session.delete(borrow)
        db.session.commit()
        return True