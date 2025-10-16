"""
Version 1: Client-Server Architecture
"""

from flask import Flask, request
from flask_restx import Api, Resource, fields
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Library Management API',
          description='Version 1: Client-Server Architecture Demo')

ns = api.namespace('books', description='Book operations')

book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description='Book identifier'),
    'title': fields.String(required=True, description='Book title'),
    'author': fields.String(required=True, description='Book author'),
    'isbn': fields.String(required=True, description='ISBN number'),
    'available': fields.Boolean(description='Availability status')
})

class BookDatabase:
    """Server-side data storage and business logic"""
    def __init__(self):
        self.books = {}
        self.counter = 1
        # Dữ liệu mẫu
        self._init_data()
    
    def _init_data(self):
        sample_books = [
            {'title': 'Clean Code', 'author': 'Robert Martin', 'isbn': '978-0132350884'},
            {'title': 'Design Patterns', 'author': 'Gang of Four', 'isbn': '978-0201633610'}
        ]
        for book in sample_books:
            self.create_book(book)
    
    def create_book(self, data):
        book = {
            'id': self.counter,
            'title': data['title'],
            'author': data['author'],
            'isbn': data['isbn'],
            'available': True
        }
        self.books[self.counter] = book
        self.counter += 1
        return book
    
    def get_all_books(self):
        return list(self.books.values())
    
    def get_book(self, book_id):
        return self.books.get(book_id)
    
    def update_book(self, book_id, data):
        if book_id in self.books:
            self.books[book_id].update(data)
            return self.books[book_id]
        return None
    
    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
            return True
        return False

# Server instance
db = BookDatabase()

# API ENDPOINTS: Interface giữa Client và Server
@ns.route('/')
class BookList(Resource):
    """Client giao tiếp với Server thông qua HTTP requests"""
    
    @ns.doc('list_books')
    @ns.marshal_list_with(book_model)
    def get(self):
        """Lấy danh sách tất cả sách (Client request → Server response)"""
        return db.get_all_books()
    
    @ns.doc('create_book')
    @ns.expect(book_model)
    @ns.marshal_with(book_model, code=201)
    def post(self):
        """Tạo sách mới (Client gửi data → Server xử lý)"""
        return db.create_book(api.payload), 201

@ns.route('/<int:id>')
@ns.response(404, 'Book not found')
class Book(Resource):
    @ns.doc('get_book')
    @ns.marshal_with(book_model)
    def get(self, id):
        """Lấy thông tin một quyển sách"""
        book = db.get_book(id)
        if book is None:
            api.abort(404, f"Book {id} doesn't exist")
        return book
    
    @ns.doc('update_book')
    @ns.expect(book_model)
    @ns.marshal_with(book_model)
    def put(self, id):
        """Cập nhật thông tin sách"""
        book = db.update_book(id, api.payload)
        if book is None:
            api.abort(404, f"Book {id} doesn't exist")
        return book
    
    @ns.doc('delete_book')
    @ns.response(204, 'Book deleted')
    def delete(self, id):
        """Xóa sách"""
        if not db.delete_book(id):
            api.abort(404, f"Book {id} doesn't exist")
        return '', 204
