"""uniit tests for the Flask application for COVID-19 stats comparison"""
import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    """Unit tests for the Flask application"""
    def setUp(self):
        self.app = app.test_client()
    """"Set up the test client for the Flask application"""
    def test_homepage(self):
        response = self.app.get('/')
        self.assertIn(b'Welcome to my ID2 Application!', response.data)
    """def test_compare_invalid_date(self):"""
    def test_compare_valid_data(self):
        response = self.app.get('/compare/2020-03-01/US,AF')
        self.assertIn(b'COVID-19 data for 2020-03-01:', response.data)

if __name__ == '__main__':
    unittest.main()
