import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    """Unit tests for the Flask COVID-19 stats comparison application."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        """Test the homepage loads and contains title text."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Track Global COVID-19 Data', response.data)

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
