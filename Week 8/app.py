from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app, doc='/', title="Library Management API", description="DEMO")

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return self.title

book_model = api.model(
    'Book',
    {
        'id': fields.Integer(),
        'title': fields.String(),
        'author': fields.String(),
        'date_joined': fields.String(),
    }
)

@api.route('/books')
class Books(Resource):
    @api.marshal_list_with(book_model, code=200, envelope="books")
    def get(self):
        ''' Get all books '''
        books = Book.query.all()
        return books

    @api.marshal_with(book_model, code=201, envelope="book")
    def post(self):
        ''' Create a new book '''
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return new_book

@api.route('/book/<int:id>')
class BookResource(Resource):
    @api.marshal_with(book_model, code=200, envelope="book")
    def get(self, id):
        ''' Get a book by id '''
        book = Book.query.get_or_404(id)
        return book, 200

    @api.marshal_with(book_model, envelope="book", code=200)
    def put(self, id):
        ''' Update a book '''
        book_to_update = Book.query.get_or_404(id)
        data = request.get_json()
        book_to_update.title = data.get('title')
        book_to_update.author = data.get('author')
        db.session.commit()
        return book_to_update, 200

    @api.marshal_with(book_model, envelope="book_deleted", code=200)
    def delete(self, id):
        ''' Delete a book '''
        book_to_delete = Book.query.get_or_404(id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return book_to_delete, 200

@api.route('/books/search')
class BookSearch(Resource):
    @api.doc(params={
        'q': {
            'description': 'Title or author',
            'in': 'query',
            'type': 'string',
            'default': ''
        },
        'page': {
            'description': 'Page number',
            'in': 'query',
            'type': 'integer',
            'default': 1
        },
        'per_page': {
            'description': 'Number of items per page',
            'in': 'query',
            'type': 'integer',
            'default': 10
        }
    })
    
    @api.marshal_list_with(book_model, code=200, envelope="books")
    def get(self):
        ''' Search books by title or author with pagination '''
        search_query = request.args.get('q', '', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = Book.query
        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                db.or_(
                    Book.title.ilike(search_pattern),
                    Book.author.ilike(search_pattern)
                )
            )

        paginated_books = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'books': paginated_books.items,
            'total': paginated_books.total,
            'pages': paginated_books.pages,
            'current_page': paginated_books.page
        }

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Book': Book
    }

if __name__ == "__main__":
    app.run(debug=True)


