"""
Version 2: Uniform Interface
"""

from flask import Flask, request, make_response
from flask_restx import Api, Resource, fields
import json

app = Flask(__name__)
api = Api(app, version='2.0', title='Library Management API',
          description='Version 2: Uniform Interface Demo')

books_ns = api.namespace('books', description='Book operations', path='/api/v2/books')
authors_ns = api.namespace('authors', description='Author operations', path='/api/v2/authors')

book_model = api.model('Book', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True, min_length=1),
    'author': fields.String(required=True),
    'isbn': fields.String(required=True, pattern=r'^\d{3}-\d{10}$'),
    'year': fields.Integer(required=True),
    'available': fields.Boolean(default=True)
})

author_model = api.model('Author', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'nationality': fields.String(required=True),
    'birth_year': fields.Integer()
})

# Response wrapper nhất quán
response_model = api.model('Response', {
    'status': fields.String(description='success or error'),
    'message': fields.String(description='Response message'),
    'data': fields.Raw(description='Response data')
})

class DataStore:
    def __init__(self):
        self.books = {
            1: {'id': 1, 'title': 'Clean Architecture', 'author': 'Robert Martin', 
                'isbn': '978-0134494166', 'year': 2017, 'available': True},
            2: {'id': 2, 'title': 'Refactoring', 'author': 'Martin Fowler',
                'isbn': '978-0134757599', 'year': 2018, 'available': True}
        }
        self.authors = {
            1: {'id': 1, 'name': 'Robert Martin', 'nationality': 'American', 'birth_year': 1952},
            2: {'id': 2, 'name': 'Martin Fowler', 'nationality': 'British', 'birth_year': 1963}
        }
        self.book_counter = 3
        self.author_counter = 3

db = DataStore()

@books_ns.route('/')
class BookList(Resource):
    @books_ns.doc('list_all_books', 
                  params={'available': 'Filter by availability (true/false)'})
    @books_ns.marshal_list_with(book_model)
    def get(self):
        """GET method - Lấy danh sách sách (Idempotent & Safe)"""
        available = request.args.get('available')
        books = list(db.books.values())
        
        if available is not None:
            available_bool = available.lower() == 'true'
            books = [b for b in books if b['available'] == available_bool]
        
        return books, 200  # HTTP 200 OK (Chuẩn)
    
    @books_ns.doc('create_book')
    @books_ns.expect(book_model, validate=True)
    @books_ns.marshal_with(book_model, code=201)
    @books_ns.response(400, 'Validation Error')
    def post(self):
        """POST method - Tạo resource mới (Not Idempotent)"""
        data = api.payload
        book = {
            'id': db.book_counter,
            **data
        }
        db.books[db.book_counter] = book
        db.book_counter += 1
        
        return book, 201  # HTTP 201 Created (Chuẩn)

@books_ns.route('/<int:id>')
@books_ns.param('id', 'Book identifier')
@books_ns.response(404, 'Book not found')
class BookResource(Resource):
    @books_ns.doc('get_book')
    @books_ns.marshal_with(book_model)
    def get(self, id):
        """GET method - Lấy một resource (Safe & Idempotent)"""
        if id not in db.books:
            api.abort(404, f"Book {id} not found")  # HTTP 404 (Chuẩn)
        return db.books[id], 200
    
    @books_ns.doc('update_book')
    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model)
    def put(self, id):
        """PUT method - Update toàn bộ resource (Idempotent)"""
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        
        data = api.payload
        db.books[id] = {'id': id, **data}
        return db.books[id], 200  # HTTP 200 OK
    
    @books_ns.doc('patch_book')
    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model)
    def patch(self, id):
        """PATCH method - Update một phần resource (Not necessarily Idempotent)"""
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        
        data = api.payload
        db.books[id].update(data)
        return db.books[id], 200
    
    @books_ns.doc('delete_book')
    @books_ns.response(204, 'Book deleted successfully')
    def delete(self, id):
        """DELETE method - Xóa resource (Idempotent)"""
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        
        del db.books[id]
        return '', 204  # HTTP 204 No Content (Chuẩn)

@authors_ns.route('/')
class AuthorList(Resource):
    @authors_ns.marshal_list_with(author_model)
    def get(self):
        """GET /api/v2/authors - Pattern nhất quán"""
        return list(db.authors.values()), 200
    
    @authors_ns.expect(author_model, validate=True)
    @authors_ns.marshal_with(author_model, code=201)
    def post(self):
        """POST /api/v2/authors - Pattern nhất quán"""
        data = api.payload
        author = {'id': db.author_counter, **data}
        db.authors[db.author_counter] = author
        db.author_counter += 1
        return author, 201

@authors_ns.route('/<int:id>')
@authors_ns.param('id', 'Author identifier')
class AuthorResource(Resource):
    @authors_ns.marshal_with(author_model)
    def get(self, id):
        """GET /api/v2/authors/{id} - Pattern nhất quán"""
        if id not in db.authors:
            api.abort(404, f"Author {id} not found")
        return db.authors[id], 200
    
    @authors_ns.expect(author_model)
    @authors_ns.marshal_with(author_model)
    def put(self, id):
        """PUT /api/v2/authors/{id} - Pattern nhất quán"""
        if id not in db.authors:
            api.abort(404, f"Author {id} not found")
        data = api.payload
        db.authors[id] = {'id': id, **data}
        return db.authors[id], 200
    
    @authors_ns.response(204, 'Author deleted')
    def delete(self, id):
        """DELETE /api/v2/authors/{id} - Pattern nhất quán"""
        if id not in db.authors:
            api.abort(404, f"Author {id} not found")
        del db.authors[id]
        return '', 204
