<<<<<<< HEAD
import unittest
from io import StringIO
import sys
import app

class TestCovidStats(unittest.TestCase):
    """Test file for our flask app"""
    def test_about_page(self):
        self.assertEqual(app.aboutpage(), "Hello, this is the about page.")
        
    def test_cl_main_not_enough_args(self):
        pass
=======
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
>>>>>>> 2dca5ef (test)
