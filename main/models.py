from .extensions import db 
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    # RBAC - admin/user cow bản
    role = db.Column(db.String(20), default='user') #default: user / option admin

    #1 user có thể mượn nhiều sách
    borrows = db.relationship("Borrow", back_populates="user")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(50))

    #1 sách có thể có nhiều bản sao
    copies = db.relationship("Copy", back_populates="book")

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("student.id"))
    book_id = db.Column(db.ForeignKey("book.id"))
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    #Quan hej
    user = db.relationships("User", back_populates="borrows")
    copy = db.relationships("Copy", back_populates="borrows")

class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    status = db.Column(db.String(20), default="available") #available/borrowed

    book = db.relationship("Book", back_populates="copies")
    borrows = db.relationship("Borrow", back_populates="copy")

