"""
Version 3: Stateless
"""

from flask import Flask, request
from flask_restx import Api, Resource, fields
from functools import wraps
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# Models
login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

token_model = api.model('Token', {
    'token': fields.String(description='JWT access token'),
    'expires_at': fields.String(description='Token expiration time')
})

book_model = api.model('Book', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'author': fields.String(required=True),
    'isbn': fields.String(required=True),
    'borrowed_by': fields.String(description='User who borrowed the book')
})

borrow_model = api.model('Borrow', {
    'book_id': fields.Integer(required=True),
    'user': fields.String(required=True)
})

class StatelessDataStore:
    def __init__(self):
        # Users
        self.users = {
            'admin': generate_password_hash('admin123'),
            'user1': generate_password_hash('pass123'),
            'user2': generate_password_hash('pass456')
        }
        
        # Books - Resource data (OK to store)
        self.books = {
            1: {'id': 1, 'title': 'RESTful Web Services', 'author': 'Leonard Richardson', 
                'isbn': '978-0596529260', 'borrowed_by': None},
            2: {'id': 2, 'title': 'Building Microservices', 'author': 'Sam Newman',
                'isbn': '978-1491950357', 'borrowed_by': None},
            3: {'id': 3, 'title': 'Domain-Driven Design', 'author': 'Eric Evans',
                'isbn': '978-0321125217', 'borrowed_by': None}
        }
        self.book_counter = 4
        
        # Không có session storage, logged_in_users, etc.
        # Mọi thông tin authentication phải gửi kèm trong mỗi request

db = StatelessDataStore()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Token phải được gửi trong HEADER của MỖI request
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Format: "Bearer <token>"
            except IndexError:
                return {'message': 'Token format invalid. Use: Bearer <token>'}, 401
        
        if not token:
            return {'message': 'Token is missing! Each request must include authentication token.'}, 401
        
        try:
            # Verify token (stateless - không query session database)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired! Please login again.'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token is invalid!'}, 401
        
        # Pass user info to the route
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    @ns.marshal_with(token_model)
    def post(self):
        data = api.payload
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            api.abort(400, 'Username and password required')
        
        # Verify credentials
        if username not in db.users or not check_password_hash(db.users[username], password):
            api.abort(401, 'Invalid credentials')
        
        # Create JWT token (self-contained, no server-side session)
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({
            'username': username,
            'exp': expires_at
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return {
            'token': token,
            'expires_at': expires_at.isoformat()
        }, 200

@ns.route('/books')
class BookList(Resource):
    @ns.doc('list_books', security='Bearer')
    @ns.marshal_list_with(book_model)
    @token_required
    def get(self, current_user):
        return list(db.books.values()), 200
    
    @ns.doc('create_book', security='Bearer')
    @ns.expect(book_model)
    @ns.marshal_with(book_model, code=201)
    @token_required
    def post(self, current_user):
        data = api.payload
        book = {
            'id': db.book_counter,
            'title': data['title'],
            'author': data['author'],
            'isbn': data['isbn'],
            'borrowed_by': None
        }
        db.books[db.book_counter] = book
        db.book_counter += 1
        return book, 201

@ns.route('/books/<int:id>')
@ns.param('id', 'Book identifier')
class BookResource(Resource):
    @ns.doc('get_book', security='Bearer')
    @ns.marshal_with(book_model)
    @token_required
    def get(self, current_user, id):
        """Lấy thông tin sách (Stateless)"""
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        return db.books[id], 200
    
    @ns.doc('delete_book', security='Bearer')
    @token_required
    def delete(self, current_user, id):
        """Xóa sách (Stateless)"""
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        del db.books[id]
        return '', 204

@ns.route('/books/<int:id>/borrow')
@ns.param('id', 'Book identifier')
class BorrowBook(Resource):
    """
    Stateless: Thông tin user được lấy từ TOKEN, không từ session
    """
    @ns.doc('borrow_book', security='Bearer')
    @ns.marshal_with(book_model)
    @token_required
    def post(self, current_user, id):
        """
        Mượn sách (Stateless operation)
        - User info từ JWT token (trong header)
        - Không có session state
        - Mỗi request độc lập
        """
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        
        book = db.books[id]
        
        if book['borrowed_by']:
            api.abort(400, f"Book already borrowed by {book['borrowed_by']}")
        
        # User info từ token (stateless), không từ session
        book['borrowed_by'] = current_user
        return book, 200

@ns.route('/books/<int:id>/return')
@ns.param('id', 'Book identifier')
class ReturnBook(Resource):
    @ns.doc('return_book', security='Bearer')
    @ns.marshal_with(book_model)
    @token_required
    def post(self, current_user, id):
        """
        Trả sách (Stateless operation)
        """
        if id not in db.books:
            api.abort(404, f"Book {id} not found")
        
        book = db.books[id]
        
        if not book['borrowed_by']:
            api.abort(400, "Book is not borrowed")
        
        if book['borrowed_by'] != current_user:
            api.abort(403, "You didn't borrow this book")
        
        book['borrowed_by'] = None
        return book, 200