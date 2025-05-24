import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test the home page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the COVID-19 Stats App', response.data)

    def test_stats_page(self):
        """Test the stats page"""
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stats Page', response.data)

    def test_compare_page(self):
        """Test the compare page"""
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Compare Page', response.data)
    

if __name__ == '__main__':
    unittest.main()
