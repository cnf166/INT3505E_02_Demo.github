from flask import Flask 

from .extensions import api, db
from .resources import ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='2.0', title='Library Management API',
          description='Version 2: Uniform Interface Demo')

    books_ns = api.namespace('books', description='Book operations', path='/api/v2/books')
    authors_ns = api.namespace('authors', description='Author operations', path='/api/v2/authors')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(books_ns)
    api.add_namespace(authors_ns)

    return app