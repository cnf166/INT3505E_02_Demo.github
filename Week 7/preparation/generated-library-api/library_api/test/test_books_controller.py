import unittest

from flask import json

from library_api.models.book_create import BookCreate  # noqa: E501
from library_api.models.book_search_response import BookSearchResponse  # noqa: E501
from library_api.models.book_update import BookUpdate  # noqa: E501
from library_api.models.create_book201_response import CreateBook201Response  # noqa: E501
from library_api.models.delete_book200_response import DeleteBook200Response  # noqa: E501
from library_api.models.error import Error  # noqa: E501
from library_api.models.get_books200_response import GetBooks200Response  # noqa: E501
from library_api.test import BaseTestCase


class TestBooksController(BaseTestCase):
    """BooksController integration test stubs"""

    def test_create_book(self):
        """Test case for create_book

        Create a new book
        """
        book_create = {"author":"J.R.R. Tolkien","title":"The Hobbit"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_book(self):
        """Test case for delete_book

        Delete a book
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/book/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_book_by_id(self):
        """Test case for get_book_by_id

        Get a book by id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/book/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_books(self):
        """Test case for get_books

        Get all books
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_books(self):
        """Test case for search_books

        Search books by title or author with pagination
        """
        query_string = [('q', ''),
                        ('page', 1),
                        ('per_page', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/search',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_book(self):
        """Test case for update_book

        Update a book
        """
        book_update = {"author":"J.R.R. Tolkien","title":"The Hobbit - Updated"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/book/{id}'.format(id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(book_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
