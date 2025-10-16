"""
Version 4: Cacheable
"""

from flask import Flask, request, make_response
from flask_restx import Api, Resource, fields
import hashlib
import json
from datetime import datetime, timedelta
from functools import wraps


# Models
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'author': fields.String(required=True),
    'isbn': fields.String(required=True),
    'publish_year': fields.Integer(),
    'category': fields.String(),
    'updated_at': fields.DateTime(description='Last modified time')
})

stats_model = api.model('Statistics', {
    'total_books': fields.Integer(),
    'available_books': fields.Integer(),
    'borrowed_books': fields.Integer(),
    'categories': fields.Raw(),
    'generated_at': fields.DateTime()
})

class CacheableDataStore:
    def __init__(self):
        self.books = {
            1: {
                'id': 1, 'title': 'HTTP: The Definitive Guide', 
                'author': 'David Gourley', 'isbn': '978-1565925090',
                'publish_year': 2002, 'category': 'Networking',
                'updated_at': datetime.utcnow()
            },
            2: {
                'id': 2, 'title': 'RESTful Web APIs', 
                'author': 'Leonard Richardson', 'isbn': '978-1449358068',
                'publish_year': 2013, 'category': 'Web Development',
                'updated_at': datetime.utcnow()
            },
            3: {
                'id': 3, 'title': 'Computer Networks', 
                'author': 'Andrew Tanenbaum', 'isbn': '978-0132126953',
                'publish_year': 2010, 'category': 'Networking',
                'updated_at': datetime.utcnow()
            }
        }
        self.book_counter = 4
        self.last_modified = datetime.utcnow()
    
    def get_all_books(self):
        return list(self.books.values())
    
    def get_book(self, book_id):
        return self.books.get(book_id)
    
    def create_book(self, data):
        book = {
            'id': self.book_counter,
            **data,
            'updated_at': datetime.utcnow()
        }
        self.books[self.book_counter] = book
        self.book_counter += 1
        self.last_modified = datetime.utcnow()
        return book
    
    def update_book(self, book_id, data):
        if book_id in self.books:
            self.books[book_id].update(data)
            self.books[book_id]['updated_at'] = datetime.utcnow()
            self.last_modified = datetime.utcnow()
            return self.books[book_id]
        return None
    
    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
            self.last_modified = datetime.utcnow()
            return True
        return False
    
    def get_statistics(self):
        """Generate statistics - expensive operation, good for caching"""
        books = list(self.books.values())
        categories = {}
        for book in books:
            cat = book.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_books': len(books),
            'available_books': len(books),
            'borrowed_books': 0,
            'categories': categories,
            'generated_at': datetime.utcnow()
        }

db = CacheableDataStore()

@ns.route('/books/<int:id>')
@ns.param('id', 'Book identifier')
class BookResource(Resource):
    @ns.doc('get_book_cacheable')
    @ns.marshal_with(book_model)
    def get(self, id):
        """
        GET single book with caching
        Longer cache time for individual resources
        """
        book = db.get_book(id)
        if not book:
            api.abort(404, f"Book {id} not found")
        
        # Generate ETag
        etag = generate_etag(book)
        
        # Check cache
        is_cached, status_code = check_cache_validation(
            etag=etag,
            last_modified=book['updated_at']
        )
        
        if is_cached:
            response = make_response('', 304)
            response.headers['ETag'] = f'"{etag}"'
            response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes
            return response
        
        # Fresh data
        response = make_response(book, 200)
        response = add_cache_headers(
            response,
            max_age=300,  # Cache individual book for 5 minutes
            etag=etag,
            last_modified=book['updated_at']
        )
        return response
    
    @ns.doc('update_book_invalidate')
    @ns.expect(book_model)
    @ns.marshal_with(book_model)
    def put(self, id):
        """
        PUT: Update book (Invalidates cache)
        """
        data = api.payload
        book = db.update_book(id, data)
        if not book:
            api.abort(404, f"Book {id} not found")
        
        # No cache for modified resource
        response = make_response(book, 200)
        response.headers['Cache-Control'] = 'no-cache'
        return response
    
    @ns.doc('delete_book_invalidate')
    def delete(self, id):
        """
        DELETE: Remove book (Invalidates cache)
        """
        if not db.delete_book(id):
            api.abort(404, f"Book {id} not found")
        
        response = make_response('', 204)
        response.headers['Cache-Control'] = 'no-cache'
        return response

@ns.route('/statistics')
class Statistics(Resource):
    @ns.doc('get_statistics_cached')
    @ns.marshal_with(stats_model)
    def get(self):
        stats = db.get_statistics()
        
        # Generate ETag
        etag = generate_etag(stats)
        
        # Check cache
        is_cached, status_code = check_cache_validation(
            etag=etag,
            last_modified=db.last_modified
        )
        
        if is_cached:
            response = make_response('', 304)
            response.headers['ETag'] = f'"{etag}"'
            response.headers['Cache-Control'] = 'public, max-age=600'
            return response
        
        response = make_response(stats, 200)
        response = add_cache_headers(
            response,
            max_age=600,  # Cache 10 phut
            etag=etag,
            last_modified=db.last_modified
        )
        return response

