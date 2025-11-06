import unittest
import json
import os
import tempfile
from app import app, db, Book


class LibraryAPITestCase(unittest.TestCase):

    def setUp(self):
        # Create a temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_ECHO'] = False
        
        self.app = app
        self.client = app.test_client()
        

        # Create database tables and seed test data
        with app.app_context():
            db.create_all()
            self._seed_test_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _seed_test_data(self):
        books = [
            Book(title="1984", author="George Orwell"),
            Book(title="Animal Farm", author="George Orwell"),
            Book(title="The Hobbit", author="J.R.R. Tolkien"),
        ]
        db.session.add_all(books)
        db.session.commit()

    def test_get_all_books(self):
        response = self.client.get('/books')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('books', data)
        self.assertEqual(len(data['books']), 3)

    def test_create_book(self):
        new_book = {'title': 'Test Book', 'author': 'Test Author'}
        
        response = self.client.post(
            '/books',
            data=json.dumps(new_book),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['book']['title'], 'Test Book')

    def test_get_book_by_id(self):
        response = self.client.get('/book/1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['book']['title'], "1984")

    def test_get_book_not_found(self):
        response = self.client.get('/book/9999')
        self.assertEqual(response.status_code, 404)

    def test_update_book(self):
        updated_data = {'title': 'Updated Title', 'author': 'Updated Author'}
        
        response = self.client.put(
            '/book/1',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['book']['title'], 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete('/book/1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('book_deleted', data)
        
        verify_response = self.client.get('/book/1')
        self.assertEqual(verify_response.status_code, 404)

    def test_search_books_by_title(self):
        response = self.client.get('/books/search?q=Hobbit')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 1)

    def test_search_books_by_author(self):
        response = self.client.get('/books/search?q=Orwell')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 2)

    def test_search_books_case_insensitive(self):
        response = self.client.get('/books/search?q=orwell')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 2)

    def test_search_no_results(self):
        response = self.client.get('/books/search?q=NonExistent')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 0)

    def test_pagination_first_page(self):
        response = self.client.get('/books/search?page=1&per_page=2')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 2)
        self.assertEqual(data['total'], 3)

    def test_pagination_with_search(self):
        response = self.client.get('/books/search?q=Orwell&page=1&per_page=1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['total'], 2)

    def test_full_crud_workflow(self):
        # Create a new book
        new_book = {'title': 'CRUD Test', 'author': 'CRUD Author'}
        
        create_response = self.client.post('/books', data=json.dumps(new_book), content_type='application/json')
        self.assertEqual(create_response.status_code, 201)
        book_id = json.loads(create_response.data)['book']['id']
        
        read_response = self.client.get(f'/book/{book_id}')
        self.assertEqual(read_response.status_code, 200)
        
        update_data = {'title': 'Updated', 'author': 'Updated'}
        update_response = self.client.put(f'/book/{book_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        
        delete_response = self.client.delete(f'/book/{book_id}')
        self.assertEqual(delete_response.status_code, 200)
        
        verify_response = self.client.get(f'/book/{book_id}')
        self.assertEqual(verify_response.status_code, 404)


if __name__ == '__main__':
    print("="*70)
    print("🧪 LIBRARY API TESTS")
    print("="*70)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(LibraryAPITestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\nALL TESTS PASSED!")
    else:
        print("\nSOME TESTS FAILED!")
    print("="*70)