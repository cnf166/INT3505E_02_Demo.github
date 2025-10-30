import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from library_api.models.book_create import BookCreate  # noqa: E501
from library_api.models.book_search_response import BookSearchResponse  # noqa: E501
from library_api.models.book_update import BookUpdate  # noqa: E501
from library_api.models.create_book201_response import CreateBook201Response  # noqa: E501
from library_api.models.delete_book200_response import DeleteBook200Response  # noqa: E501
from library_api.models.error import Error  # noqa: E501
from library_api.models.get_books200_response import GetBooks200Response  # noqa: E501
from library_api import util


def get_books():
    """Get all books
    
    :rtype: dict
    """
    try:
        books = BookDB.query.all()
        books_list = [book.to_dict() for book in books]
        return {'books': books_list}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def create_book(body):
    """Create a new book
    
    :param body: Book data
    :type body: dict | bytes
    
    :rtype: dict
    """
    try:
        if isinstance(body, dict):
            title = body.get('title')
            author = body.get('author')
        else:
            title = body.title
            author = body.author
        
        if not title or not author:
            return {'message': 'Title and author are required'}, 400
        
        new_book = BookDB(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        
        return {'book': new_book.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}, 500


def get_book_by_id(id):
    """Get a book by id
    
    :param id: Book ID
    :type id: int
    
    :rtype: dict
    """
    try:
        book = BookDB.query.get(id)
        if not book:
            return {'message': 'Book not found'}, 404
        
        return {'book': book.to_dict()}, 200
    except Exception as e:
        return {'message': str(e)}, 500


def update_book(id, body):
    """Update a book
    
    :param id: Book ID
    :type id: int
    :param body: Updated book data
    :type body: dict | bytes
    
    :rtype: dict
    """
    try:
        book = BookDB.query.get(id)
        if not book:
            return {'message': 'Book not found'}, 404
        
        if isinstance(body, dict):
            title = body.get('title')
            author = body.get('author')
        else:
            title = body.title
            author = body.author
        
        if title:
            book.title = title
        if author:
            book.author = author
        
        db.session.commit()
        return {'book': book.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}, 500


def delete_book(id):
    """Delete a book
    
    :param id: Book ID
    :type id: int
    
    :rtype: dict
    """
    try:
        book = BookDB.query.get(id)
        if not book:
            return {'message': 'Book not found'}, 404
        
        book_dict = book.to_dict()
        db.session.delete(book)
        db.session.commit()
        
        return {'book_deleted': book_dict}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}, 500


def search_books(q=None, page=None, per_page=None):
    """Search books by title or author with pagination
    
    :param q: Search query for title or author
    :type q: str
    :param page: Page number
    :type page: int
    :param per_page: Number of items per page
    :type per_page: int
    
    :rtype: BookSearchResponse
    """
    try:
        # Default values
        search_query = q if q else ''
        page = page if page else 1
        per_page = per_page if per_page else 10
        
        query = BookDB.query
        
        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                db.or_(
                    BookDB.title.ilike(search_pattern),
                    BookDB.author.ilike(search_pattern)
                )
            )
        
        paginated_books = query.paginate(page=page, per_page=per_page, error_out=False)
        
        books_list = [book.to_dict() for book in paginated_books.items]
        
        response = {
            'books': books_list,
            'total': paginated_books.total,
            'pages': paginated_books.pages,
            'current_page': paginated_books.page
        }
        
        return response, 200
    except Exception as e:
        return {'message': str(e)}, 500