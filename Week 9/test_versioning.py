import unittest
from versioning import app

class TestAPIVersioning(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    # v1 Tests
    def test_v1_get_users(self):
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('users', data)
        self.assertEqual(len(data['users']), 2)
    
    def test_v1_get_single_user(self):
        response = self.app.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 1)
        self.assertNotIn('email', data)  # v1 doesn't have email
    
    # v2 Tests
    def test_v2_get_users(self):
        response = self.app.get('/api/v2/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('count', data)
        self.assertEqual(len(data['data']), 2)
    
    def test_v2_get_single_user(self):
        response = self.app.get('/api/v2/users/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('email', data['data'])  # v2 has email
        self.assertEqual(data['data']['id'], 1)

if __name__ == '__main__':
    unittest.main()
