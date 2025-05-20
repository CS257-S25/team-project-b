import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    """Unit tests for the Flask COVID-19 stats comparison application."""

    def setUp(self):
        """Set up the test client for the Flask application."""
        self.app = app.test_client()

    def test_homepage(self):
        """Test the homepage loads and contains the welcome message."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to my ID2 Application!', response.data)

    def test_compare_valid_data(self):
        """Test the compare route with valid date and country codes."""
        response = self.app.get('/compare/2020-03-01/US,AF')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'COVID-19 data for 2020-03-01:', response.data)

    def test_valid_stats(self):
        """Test if valid country stats load correctly."""
        response = self.app.get('/stats/US/2020-03-01/2021-03-10')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'COVID-19 stats for US', response.data)

    def test_compare_invalid_date(self):
        """Test the compare route with an invalid date format."""
        response = self.app.get('/compare/invalid-date/US,AF')
        self.assertNotEqual(response.status_code, 200)
        
    def test_compare_fun_facts(self):
        """Test the funfacts route."""
        response = self.app.get('/funfacts')
        self.assertNotEqual(response.status_code, 200)  
        self.assertIn(b"Fenan", response.data) 
    

if __name__ == '__main__':
    unittest.main()
