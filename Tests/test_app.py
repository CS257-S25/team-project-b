import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    """Tests for the Flask app routes in app.py."""

    def setUp(self):
        """Set up test client for the Flask app."""
        self.client = app.test_client()

    def test_homepage(self):
        """Test the homepage loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)  # Basic HTML check

    def test_stats_get(self):
        """Test GET request for the stats page."""
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_stats_post_valid(self):
        """Test POST request for the stats page with valid data."""
        response = self.client.post('/stats', data={
            'country': 'Afghanistan',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases', response.data)  # Or a phrase from your stats page

    def test_stats_post_invalid(self):
        """Test POST request for the stats page with invalid country."""
        response = self.client.post('/stats', data={
            'country': 'FakeCountry',
            'beginning_date': '2020-01-01',
            'ending_date': '2020-01-12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No data found', response.data)  # Or whatever your error message says

    def test_compare_get(self):
        """Test GET request for the compare page."""
        response = self.client.get('/compare')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_compare_post(self):
        """Test POST request for the compare page with valid data."""
        response = self.client.post('/compare', data={
            'countries': ['Afghanistan', 'Albania'],
            'week': '2020-01-01'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total cases', response.data)

    def test_help_page(self):
        """Test the /help page."""
        response = self.client.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_404_page(self):
        """Test the 404 page."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)

if __name__ == '__main__':
    unittest.main()
