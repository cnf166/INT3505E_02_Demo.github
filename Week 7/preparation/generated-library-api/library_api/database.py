# library_api/database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

basedir = os.path.dirname(os.path.realpath(__file__))

def init_db(app):
    """Initialize database with app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../books.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

class Book(db.Model):
    __tablename__ = 'book'
    
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self):
        """Convert Book object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'date_joined': self.date_added.isoformat() if self.date_added else None
        }