import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up the test client for the Flask application."""
        self.app = app.test_client()

    def test_homepage(self):
        """Test the homepage loads and contains title text."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to my ID2 Application!', response.data)

    def test_stats_page_loads(self):
        """Test that the stats page loads with GET request."""
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select a country and date range', response.data)

    def test_compare_page_loads(self):
        """Test that the compare page loads with GET request."""
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Compare COVID-19 Stats by Country', response.data)

    def test_404_page(self):
        """Test a non-existent route returns the custom 404 page."""
        response = self.app.get('/thispagedoesnotexist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)

if __name__ == '__main__':
    unittest.main()
